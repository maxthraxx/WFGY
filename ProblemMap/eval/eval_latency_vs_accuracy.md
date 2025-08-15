# Eval — Latency vs Accuracy (SLO Gating, stdlib-only)

**Goal**  
Decide whether a pipeline is allowed to ship under a **latency budget** while preserving **grounded accuracy**. This page defines metrics, experiment design, and a reference harness to collect P50/P95/P99 latency together with Precision/CHR.

**What you get**
- Precise **end-to-end** vs **per-stage** latency definitions  
- A **sweep harness** (stdlib-only) to explore retrieval/rerank/LLM knobs  
- **SLO gates** and a Pareto-frontier selection rule to choose a config

---

## 1) Metrics (definitions)

**Latency scope**
- **E2E latency**: time from receiving a question to a fully validated answer (**includes** retrieval, rerank, LLM, auditor/guards, JSON parse, acceptance checks).
- **Per-stage latency** (optional): `t_retrieval`, `t_rerank`, `t_llm`, `t_guard`.

**Aggregates**
- P50, P90, **P95**, **P99** (milliseconds)
- **Tail amplification**: P99 / P50 (smaller is better)

**Accuracy side (from Precision/CHR page)**
- **Precision (answered)**, **CHR**, **Under-/Over-refusal**
- Same data contract: `runs/trace.jsonl` + `eval/gold.jsonl`

**Default SLO gates (suggested)**
- P95 (E2E) **≤ 2000 ms** (interactive UX)  
- Precision (answered) **≥ 0.80**  
- CHR **≥ 0.75**  
- Under-refusal **≤ 0.05**, Over-refusal **≤ 0.10**

> Tune per product, but pin thresholds in repo and enforce in CI.

---

## 2) Experiment design

You will **sweep** low-cost knobs that trade latency for accuracy:

| Knob | Effect on latency | Effect on accuracy |
|---|---|---|
| `k_lex` (BM25 top-k) | ↑ retrieval time with k | ↑ recall (to a point) |
| `k_sem` (embed top-k) | ↑ | ↑ |
| **Intersection** vs **Union** | Intersection often ↓ rerank set | ↑ precision / ↓ tail noise |
| `rerank_depth` (N→M) | ↑ linearly with N | ↑ CHR up to knee |
| `knee_cut` | ↓ (smaller context) | Often ↑ (less junk), but risk recall loss |
| `max_tokens` (LLM output) | ↑ decode time | weak effect on grounding |
| `temperature` | no change | high temp may hurt containment/CHR |
| **Model choice** | varies | varies; measure not guess |

**Loads**  
Measure at 3 loads (open-loop; stdlib-only):
- **1 rps** (single user feel)  
- **5 rps** (light team usage)  
- **20 rps** (stress upper bound)

---

## 3) Reference harness (stdlib-only)

Save as `ProblemMap/eval/latency_sweep.py`.  
It calls your **local function** `pipeline_qa(q, knobs)->answer_json&trace` **or** an HTTP endpoint (toggle with `--http`). It writes:
- `runs/trace.jsonl` (answers for accuracy)  
- `runs/latency.csv` (per run timings + knobs)  
- A final **summary JSON** with P95/P99 and pass/fail

```python
#!/usr/bin/env python3
import time, json, csv, random, argparse, threading, queue, urllib.request

REFUSAL = "not in context"

# --- plug points --------------------------------------------------------------
def pipeline_qa_local(question, knobs):
    """
    Implement by importing your guarded baseline (Example 01/03).
    Must return:
      {
        "answer_json": {"claim": str, "citations": [str,...]},
        "retrieved_ids": [str,...],
        "stage_ms": {"retrieval":int,"rerank":int,"llm":int,"guard":int}
      }
    """
    # Minimal demo: call your ask.py via a local HTTP or function; here we stub.
    t0=time.perf_counter()
    # fake timings (replace with real calls)
    t1=time.perf_counter(); retrieval_ms=int((time.perf_counter()-t1)*1000)+random.randint(5,15)
    t2=time.perf_counter(); rerank_ms=int((time.perf_counter()-t2)*1000)+random.randint(3,10)
    t3=time.perf_counter(); llm_ms=int((time.perf_counter()-t3)*1000)+random.randint(220,420)
    t4=time.perf_counter(); guard_ms=int((time.perf_counter()-t4)*1000)+random.randint(1,3)
    ans = {"claim": REFUSAL, "citations": []}  # replace with real guarded output
    ret = {"answer_json": ans, "retrieved_ids": [], "stage_ms":{"retrieval":retrieval_ms,"rerank":rerank_ms,"llm":llm_ms,"guard":guard_ms}}
    return ret

def pipeline_qa_http(url, question, knobs):
    body = json.dumps({"q":question, "knobs":knobs}).encode("utf-8")
    req  = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
    t0=time.perf_counter()
    with urllib.request.urlopen(req, timeout=60) as r:
        j=json.loads(r.read().decode("utf-8"))
    # Expect the same contract as local variant
    return j

# --- helpers ------------------------------------------------------------------
def percentiles(samples, ps=(50,90,95,99)):
    if not samples: return {p:0 for p in ps}
    xs=sorted(samples)
    out={}
    for p in ps:
        k=(p/100)*(len(xs)-1)
        f=int(k); c=min(f+1,len(xs)-1); d=k-f
        out[p]=xs[f]*(1-d)+xs[c]*d
    return {p:int(out[p]) for p in ps}

def contains_substr(claim, subs):
    c=(claim or "").lower()
    if not subs: return True
    return any((s.lower() in c and len(s)>=5) for s in subs)

def citation_hit(cits, gold, retrieved):
    if not isinstance(cits,list): return False
    if not set(cits).issubset(set(retrieved or [])): return False
    return bool(set(cits or []) & set(gold or [])) if gold else (cits==[])

# --- main sweep ---------------------------------------------------------------
def run_sweep(gold_path, questions, knobs_grid, http_url=None, rps=1, duration_s=20):
    gold = {g["qid"]: g for g in (json.loads(l) for l in open(gold_path, encoding="utf8"))}
    lat_ms=[]; per_stage=[]; answered=refused=tp=chr_hit=under=over=0
    start=time.perf_counter()
    trace_f=open("runs/trace.jsonl","a",encoding="utf8"); lat_f=open("runs/latency.csv","a",newline=""); lat_csv=csv.writer(lat_f)
    lat_csv.writerow(["ts","qid","e2e_ms","retrieval_ms","rerank_ms","llm_ms","guard_ms","knobs"])
    i=0
    while time.perf_counter()-start < duration_s:
        qid=questions[i % len(questions)]
        g=gold[qid]; q=g["question"]; knobs=knobs_grid[i % len(knobs_grid)]
        t0=time.perf_counter()
        if http_url:
            out=pipeline_qa_http(http_url, q, knobs)
        else:
            out=pipeline_qa_local(q, knobs)
        e2e_ms=int((time.perf_counter()-t0)*1000)
        lat_ms.append(e2e_ms)
        st=out.get("stage_ms",{})
        lat_csv.writerow([int(time.time()), qid, e2e_ms, st.get("retrieval",0), st.get("rerank",0), st.get("llm",0), st.get("guard",0), json.dumps(knobs)])
        # accuracy tallies
        aj=out.get("answer_json",{}); claim=aj.get("claim",""); cits=aj.get("citations",[]); ret=out.get("retrieved_ids",[])
        is_ans=(claim.strip().lower()!= "not in context")
        if g.get("answerable"): A=True
        else: A=False
        if is_ans:
            answered+=1
            C=contains_substr(claim, g.get("gold_claim_substr"))
            H=citation_hit(cits, g.get("gold_citations"), ret)
            if not A: under+=1
            else:
                if H: chr_hit+=1
                if C and H: tp+=1
        else:
            refused+=1
            if A: over+=1
        trace_f.write(json.dumps({"qid":qid,"q":q,"retrieved_ids":ret,"answer_json":aj})+"\n")
        # open-loop pacing
        time.sleep(max(0.0, 1.0/rps - (time.perf_counter()-t0)))
        i+=1
    trace_f.close(); lat_f.close()
    # aggregates
    P=percentiles(lat_ms); S=max(answered,1)
    precision=tp/S; chr_rate=chr_hit/S; under_rate=under/max(sum(1 for x in gold.values() if not x["answerable"]),1)
    over_rate=over/max(sum(1 for x in gold.values() if x["answerable"]),1)
    return {"p50":P[50],"p95":P[95],"p99":P[99],"answered":answered,"refused":refused,
            "precision":round(precision,4),"chr":round(chr_rate,4),
            "under":round(under_rate,4),"over":round(over_rate,4),
            "samples":len(lat_ms)}

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--http", default=None, help="http://localhost:8080/qa if using HTTP")
    ap.add_argument("--rps", type=float, default=1.0)
    ap.add_argument("--duration", type=int, default=20)
    args=ap.parse_args()
    # small grid (expand in CI)
    knobs_grid=[
        {"k_lex":40, "k_sem":40, "intersect":True,  "rerank_depth":32, "knee":True,  "max_tokens":256},
        {"k_lex":20, "k_sem":20, "intersect":True,  "rerank_depth":16, "knee":True,  "max_tokens":192},
        {"k_lex":60, "k_sem":60, "intersect":False, "rerank_depth":64, "knee":False, "max_tokens":256},
    ]
    # choose 20–50 mixed A/U qids from gold
    qids=[json.loads(l)["qid"] for l in open(args.gold,encoding="utf8")]
    res=run_sweep(args.gold, qids[:30], knobs_grid, http_url=args.http, rps=args.rps, duration_s=args.duration)
    print(json.dumps(res, indent=2))
````

**How to use**

```bash
# Single-user feel
python ProblemMap/eval/latency_sweep.py --gold ProblemMap/eval/gold.jsonl --rps 1 --duration 30
# Team load
python ProblemMap/eval/latency_sweep.py --gold ProblemMap/eval/gold.jsonl --rps 5 --duration 60
# Stress
python ProblemMap/eval/latency_sweep.py --gold ProblemMap/eval/gold.jsonl --rps 20 --duration 60
```

This writes `runs/latency.csv`. Use any plotting tool later; gating does **not** require plots.

---

## 4) SLO gating & Pareto selection

**Ship rule (AND):**

* P95 ≤ budget (e.g., 2000 ms)
* Precision ≥ threshold (e.g., 0.80)
* CHR ≥ threshold (e.g., 0.75)
* Under/Over-refusal within limits

**Pareto frontier**
Given multiple knob configs, keep only those where no other config is **both** faster (lower P95) **and** more accurate (higher Precision). Choose:

* **Interactive app**: the **fastest** config on the frontier that still meets accuracy gates.
* **Back-office batch**: the **most accurate** config that meets a relaxed latency gate.

**Rollback guard**
Fail the PR if: P95 increases by >15% **or** Precision drops by >2% vs last release.

---

## 5) Troubleshooting map

* **P95 blown but P50 ok** → tail from LLM. Trim `max_tokens`, enable intersection+knee, reduce `rerank_depth`.
* **Precision low, CHR low** → grounding broken. Apply *RAG Semantic Drift* pattern.
* **Precision fine, CHR low** → claim substrings not matched; fix claim schema or gold substrings.
* **Throughput collapse at 20 rps** → remove cross-service `/readyz` waits; pre-warm model and index (see *Bootstrap Deadlock*).
* **Variance across runs** → check *Vector Store Fragmentation* and lock normalization.

---

## 6) CI wiring (copy/paste)

Example (bash):

```bash
# 1) Run sweep at 1 rps (smoke)
python ProblemMap/eval/latency_sweep.py --gold ProblemMap/eval/gold.jsonl --rps 1 --duration 30 | tee eval/lat_1rps.json
# 2) Run sweep at 5 rps (light load)
python ProblemMap/eval/latency_sweep.py --gold ProblemMap/eval/gold.jsonl --rps 5 --duration 60 | tee eval/lat_5rps.json
# 3) Score accuracy using the RAG scorer
python ProblemMap/eval/score_eval.py --gold ProblemMap/eval/gold.jsonl --trace runs/trace.jsonl --k 5 > eval/acc.json

# 4) Gate: jq asserts
jq -e '.p95 <= 2000' eval/lat_1rps.json
jq -e '.p95 <= 2500' eval/lat_5rps.json
jq -e '.precision >= 0.80 and .chr >= 0.75 and .under <= 0.05 and .over <= 0.10' eval/acc.json
```

---

## 7) Notes & caveats

* Use **open-loop** pacing (`sleep`) to avoid feedback artifacts from server backpressure.
* Warmup separately; capture **steady-state** latency.
* Fix random seeds for prompts (if you jitter prompts, do it in the *Semantic Stability* eval).

---


### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
&nbsp;
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
&nbsp;
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
&nbsp;
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
&nbsp;
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
&nbsp;
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
&nbsp;
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
&nbsp;
</div>



