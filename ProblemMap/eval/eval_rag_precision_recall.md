# Eval — RAG Precision, Refusals, CHR, and Recall@k (stdlib-only)

**Goal**  
Provide a deterministic, SDK-free way to score grounded Q&A quality and retrieval quality for RAG pipelines. This page defines metrics, data contracts, and a ≤100-line reference scorer.

**What you get**
- Clear **precision/CHR/refusal** definitions for grounded answers
- **Recall@k** for retrieval (upper bound on answerability)
- A tiny **reference scorer** (Python stdlib-only) + sample JSONL

---

## 1) Data Contracts

### 1.1 Gold set (`eval/gold.jsonl`)
One JSON object per line:

```json
{"qid":"A0001","question":"Does X support null keys?","answerable":true,"gold_claim_substr":["rejects null keys"],"gold_citations":["p1#2"],"constraints":["X rejects null keys."]}
{"qid":"A0002","question":"Explain Z.","answerable":false,"gold_claim_substr":[],"gold_citations":[]}
{"qid":"A0003","question":"What domain is allowed?","answerable":true,"gold_claim_substr":["only domain example.com"],"gold_citations":["pB#1"]}
````

Rules:

* `answerable=false` ⇒ the **only** correct output is the exact refusal token: `not in context`
* `gold_claim_substr`: minimal substrings that must appear in the shipped claim (case-insensitive, ≥5 chars)
* `gold_citations`: any overlap with shipped `citations` counts as a citation hit
* `constraints` (optional): used by SCU checks elsewhere; ignored in this page’s scorer unless you extend it

### 1.2 System traces (`runs/trace.jsonl`)

Emitted by your guarded pipeline:

```json
{"qid":"A0001","q":"Does X support null keys?","retrieved_ids":["p1#1","p1#2","p2#1"],"answer_json":{"claim":"X rejects null keys.","citations":["p1#2"]}}
{"qid":"A0002","q":"Explain Z.","retrieved_ids":["p1#1","p2#1"],"answer_json":{"claim":"not in context","citations":[]}}
{"qid":"A0003","q":"What domain is allowed?","retrieved_ids":["pB#1","p1#2"],"answer_json":{"claim":"Only domain example.com is allowed.","citations":["pB#1"]}}
```

Rules:

* `answer_json.claim` is either a sentence **or** the exact refusal token `not in context`
* `answer_json.citations` must be ids taken from `retrieved_ids` (scoped grounding)

---

## 2) Metrics (definitions)

Let

* **S** = set of shipped answers (claim ≠ `not in context`)
* **R** = set of refusals (claim == `not in context`)
* **A** = gold items with `answerable=true`
* **U** = gold items with `answerable=false`

Derived checks per qid:

* **Containment (C)**: any `gold_claim_substr` appears in the shipped `claim` (case-insensitive, min len ≥ 5)
* **Citation hit (H)**: `citations ∩ gold_citations ≠ ∅` and `citations ⊆ retrieved_ids`

Scores:

* **Precision (answered)** = |{ x ∈ S ∩ A : C ∧ H }| / |S|
  (Of what we shipped, how many are correct and properly cited?)
* **Under-refusal rate** = |{ x ∈ S ∩ U }| / |U|
  (Should have refused but answered anyway.)
* **Over-refusal rate** = |{ x ∈ R ∩ A }| / |A|
  (Should have answered but refused.)
* **Citation Hit Rate (CHR)** = |{ x ∈ S : H }| / |S|
* **Recall\@k** = |{ x ∈ A : `gold_citations` ⊆ top-k(`retrieved_ids`) }| / |A|

> Tip: track Precision and CHR together. High precision with low CHR usually means “answers look right but cite the wrong evidence.”

**Default ship gates (suggested)**

* Precision (answered) ≥ **0.80**
* CHR ≥ **0.75**
* Under-refusal ≤ **0.05**
* Over-refusal ≤ **0.10**

Commit gate thresholds to your repo and enforce them in CI.

---

## 3) Worked Mini-Example

Gold (3 items) + Traces above:

* A0001 → shipped, contains “rejects null keys”, cites `p1#2` (hit) → contributes to Precision and CHR
* A0002 → refusal, gold says unanswerable → correct refusal (neither hurts Precision nor Over-refusal)
* A0003 → shipped, contains “only domain example.com”, cites `pB#1` (hit)

With all three correct, you’ll see:

* Precision (answered) = 2/2 = 1.00
* CHR = 2/2 = 1.00
* Under-refusal = 0/1 = 0.00
* Over-refusal = 0/2 = 0.00
* Recall\@k depends on your chosen `k` and the retrieved ids (here, gold cites are present in tops)

---

## 4) Reference scorer (≤100 lines, Python stdlib-only)

Save as `ProblemMap/eval/score_eval.py`:

```python
#!/usr/bin/env python3
import json, sys, argparse

REFUSAL = "not in context"

def load_jsonl(path):
    with open(path, encoding="utf8") as f:
        for line in f:
            line=line.strip()
            if line: yield json.loads(line)

def contains_substr(claim, subs):
    c = (claim or "").lower()
    for s in subs or []:
        s = s.lower()
        if len(s) >= 5 and s in c:
            return True
    return subs == []  # if no gold substrings, treat containment as vacuously true

def citation_hit(citations, gold_cites, retrieved):
    if not isinstance(citations, list): return False
    if not set(citations).issubset(set(retrieved or [])): return False
    return bool(set(citations or []) & set(gold_cites or [])) if gold_cites else (citations == [])

def topk(ids, k): return (ids or [])[:k]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--trace", required=True)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--gates", default="precision=0.80,chr=0.75,under=0.05,over=0.10")
    args = ap.parse_args()

    gold = {g["qid"]: g for g in load_jsonl(args.gold)}
    traces = {}
    for t in load_jsonl(args.trace):
        qid = t.get("qid") or t.get("q_id")
        if qid: traces[qid] = t  # keep last

    S=R=A=U=0
    TP=CHR_hit=0
    UNDER=OVER=0
    RECALL=REC_DEN=0

    for qid,g in gold.items():
        ans = traces.get(qid, {})
        aj = (ans.get("answer_json") or {})
        claim = (aj.get("claim") or "").strip()
        cits  = aj.get("citations") or []
        ret   = ans.get("retrieved_ids") or []
        is_ans = claim.lower() != REFUSAL
        if g.get("answerable"): A+=1
        else: U+=1

        # sets
        if is_ans: S+=1
        else: R+=1

        # precision / chr
        if is_ans:
            C = contains_substr(claim, g.get("gold_claim_substr"))
            H = citation_hit(cits, g.get("gold_citations"), ret)
            if g.get("answerable")==False: UNDER += 1
            else:
                if H: CHR_hit += 1
                if C and H: TP += 1
        else:
            if g.get("answerable")==True: OVER += 1

        # recall@k
        if g.get("answerable")==True:
            REC_DEN += 1
            kset = set(topk(ret, args.k))
            if set(g.get("gold_citations") or []).issubset(kset):
                RECALL += 1

    precision = (TP / S) if S else 1.0
    chr_rate  = (CHR_hit / S) if S else 1.0
    under     = (UNDER / U) if U else 0.0
    over      = (OVER / A) if A else 0.0
    recallk   = (RECALL / REC_DEN) if REC_DEN else 0.0

    gates = dict(x.split("=") for x in args.gates.split(","))
    def ok(name, val, ge=True):
        thr = float(gates[name])
        return val >= thr if ge else val <= thr

    pass_all = (ok("precision", precision) and ok("chr", chr_rate) and
                ok("under", under, ge=False) and ok("over", over, ge=False))

    print(json.dumps({
        "answered": S, "refused": R, "answerable": A, "unanswerable": U,
        "precision": round(precision,4),
        "chr": round(chr_rate,4),
        "under_refusal": round(under,4),
        "over_refusal": round(over,4),
        "recall@k": round(recallk,4),
        "k": args.k,
        "gates": gates,
        "pass": pass_all
    }, indent=2))

if __name__ == "__main__":
    main()
```

Run:

```bash
python ProblemMap/eval/score_eval.py \
  --gold ProblemMap/eval/gold.jsonl \
  --trace runs/trace.jsonl \
  --k 5 \
  --gates precision=0.80,chr=0.75,under=0.05,over=0.10
```

Output (example):

```json
{
  "answered": 2,
  "refused": 1,
  "answerable": 2,
  "unanswerable": 1,
  "precision": 1.0,
  "chr": 1.0,
  "under_refusal": 0.0,
  "over_refusal": 0.0,
  "recall@k": 1.0,
  "k": 5,
  "gates": {"precision":"0.80","chr":"0.75","under":"0.05","over":"0.10"},
  "pass": true
}
```

---

## 5) CI wiring

* Add a job that runs the scorer on every PR and fails if `pass=false`.
* Store last report at `eval/report.md` (or JSON) to track regressions.
* Freeze `gold.jsonl` per release; changes require sign-off.

**Example CI step**

```bash
python ProblemMap/eval/score_eval.py \
  --gold ProblemMap/eval/gold.jsonl \
  --trace runs/trace.jsonl \
  --k 5 \
  --gates precision=0.80,chr=0.75,under=0.05,over=0.10 \
| tee eval/last_report.json

jq -e '.pass == true' eval/last_report.json
```

---

## 6) Troubleshooting

* **Precision low, CHR low** → Grounding broken. Apply Pattern: *RAG Semantic Drift*.
* **Precision low, CHR high** → Claim text misses `gold_claim_substr`. Tighten claim schema / substrings.
* **Under-refusal high** → Many unanswerables were answered; strengthen refusal behavior or retrieval constraints.
* **Over-refusal high** → You’re refusing real questions; improve recall\@k or shrink chunks.
* **Recall\@k low** → Index/manifest drift or retrieval logic. See *Vector Store Fragmentation* and Example 03.

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


