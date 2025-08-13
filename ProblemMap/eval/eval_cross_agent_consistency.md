# Eval — Cross-Agent Consistency (Scholar ↔ Auditor, Cohen’s κ, Conflict Policy)

**Goal**  
Measure and enforce agreement between two independent validators: a **Scholar** (claims/citations checker) and an **Auditor** (policy/provenance/constraints gate). Produce (1) quantitative agreement (Percent Agreement & Cohen’s κ) and (2) a deterministic **conflict-resolution policy** for ship/no-ship.

**What you get**
- A small **label space** and file formats
- A ≤120-line **reference scorer** (Python stdlib-only)
- **CI gates** and a transparent arbitration rule

---

## 1) Label Space (tri-state + abstain)

Every agent emits exactly one label per QID:

- `VALID` — grounded & policy-compliant answer (citations scoped to retrieved ids, passes guards)
- `NOT_IN_CONTEXT` — correct refusal (exact token `not in context`)
- `REJECT` — answer present but violates grounding/provenance/constraints/template
- `ABSTAIN` — (optional) agent can’t decide; counted separately

> Tip: Treat `VALID` and `NOT_IN_CONTEXT` as **both acceptable** outcomes; `REJECT` is a hard fail.

---

## 2) Data Contracts

### 2.1 Pairwise judgments (`eval/consistency_pairs.jsonl`)
One JSON per line, merged per `qid`:

```json
{
  "qid": "A0001",
  "scholar": {"label": "VALID", "reason": "claim contained; cites p1#2"},
  "auditor": {"label": "VALID", "reason": "provenance ok; constraints echoed"},
  "answer_json": {"claim": "X rejects null keys.", "citations": ["p1#2"], "constraints_echo": ["X rejects null keys."]},
  "retrieved_ids": ["p1#1","p1#2","p2#1"],
  "flags": {"provenance_violation": false, "constraints_mismatch": false}
}
````

You may also keep separate files:

* `eval/scholar.jsonl` with `{ "qid": "...", "label": "...", "reason": "..." }`
* `eval/auditor.jsonl` same schema

The scorer accepts either merged pairs or two files (it will join by `qid`).

---

## 3) Metrics

Let **N** be the number of items where both agents labeled (excluding missing pairs).
Let **L** be the set `{VALID, NOT_IN_CONTEXT, REJECT, ABSTAIN}` (ABSTAIN is optional).

* **Percent Agreement (PA)**:

  $$
  \text{PA} = \frac{1}{N}\sum_{i=1}^{N} \mathbf{1}[y^\text{sch}_i = y^\text{aud}_i]
  $$
* **Cohen’s κ (kappa)** on **nominal** labels (include `ABSTAIN` if present):

  $$
  \kappa = \frac{P_o - P_e}{1 - P_e}
  $$

  where $P_o$ is observed agreement (diagonal / N) and
  $P_e = \sum_{\ell \in L} p^\text{sch}_\ell \cdot p^\text{aud}_\ell$ (product of label marginals).

> Rule of thumb (not law): κ ≥ 0.75 = substantial agreement.

**Default CI gates (suggested)**

* Percent Agreement ≥ **0.90**
* Cohen’s κ ≥ **0.75**
* `ABSTAIN` rate ≤ **0.02**
* Disagreements with red flags (`provenance_violation` or `constraints_mismatch`) must be **auto-REJECT** in the final arbitration

---

## 4) Deterministic Conflict Policy (Arbitration)

Given a pair `(label_s, label_a)`:

1. If any **hard red flag** is true (`provenance_violation`, `constraints_mismatch`, citations ⊄ `retrieved_ids`) → **FINAL = REJECT**.
2. Else if `label_a ≠ VALID` → **FINAL = REJECT** (Auditor wins on policy).
3. Else if `label_a = VALID` and `label_s ∈ {VALID, NOT_IN_CONTEXT}` → **FINAL = label\_a**.
4. Else → **FINAL = REJECT**.

> Rationale: shipping requires **policy/provenance** green. Scholar validates content; Auditor vetoes unsafe ships.

The scorer will produce a TSV of disagreements with the computed **FINAL** so you can eyeball deltas.

---

## 5) Reference Scorer (stdlib-only, ≤120 lines)

Save as `ProblemMap/eval/cross_agent_consistency.py`:

```python
#!/usr/bin/env python3
import json, argparse, math, sys

LABELS = ["VALID","NOT_IN_CONTEXT","REJECT","ABSTAIN"]

def load_jsonl(path):
    with open(path, encoding="utf8") as f:
        for line in f:
            line=line.strip()
            if line: yield json.loads(line)

def join_pairs(pairs_path=None, scholar_path=None, auditor_path=None):
    if pairs_path:
        for r in load_jsonl(pairs_path): yield r
        return
    S={r["qid"]:r for r in load_jsonl(scholar_path)}
    A={r["qid"]:r for r in load_jsonl(auditor_path)}
    Q=set(S.keys()) & set(A.keys())
    for qid in sorted(Q):
        yield {
            "qid": qid,
            "scholar": {"label": S[qid]["label"], "reason": S[qid].get("reason","")},
            "auditor": {"label": A[qid]["label"], "reason": A[qid].get("reason","")},
        }

def confusion_and_kappa(rows):
    # build confusion on the 4 labels
    idx={l:i for i,l in enumerate(LABELS)}
    K=len(LABELS)
    M=[[0]*K for _ in range(K)]
    n=0
    for r in rows:
        ls=r["scholar"]["label"]; la=r["auditor"]["label"]
        if ls not in idx or la not in idx: continue
        M[idx[ls]][idx[la]]+=1; n+=1
    if n==0: return M, 0.0, 0.0, 0, {}
    po=sum(M[i][i] for i in range(K))/n
    rs=[sum(M[i]) for i in range(K)]
    cs=[sum(M[i][j] for i in range(K)) for j in range(K)]
    pe=sum((rs[i]/n)*(cs[i]/n) for i in range(K))
    kappa=(po - pe)/(1 - pe) if (1-pe)>1e-12 else 0.0
    abstain_rate=(rs[idx["ABSTAIN"]]/n) if "ABSTAIN" in idx else 0.0
    return M, po, kappa, n, {"abstain_rate":abstain_rate}

def final_arbitration(r):
    # hard flags (optional)
    flags=r.get("flags",{})
    if flags.get("provenance_violation") or flags.get("constraints_mismatch"):
        return "REJECT","hard_flag"
    # citations ⊆ retrieved_ids if present
    aj=(r.get("answer_json") or {})
    cits=set(aj.get("citations") or [])
    retrieved=set(r.get("retrieved_ids") or [])
    if cits and not cits.issubset(retrieved):
        return "REJECT","citation_out_of_scope"
    # auditor decides policy
    la=r["auditor"]["label"]; ls=r["scholar"]["label"]
    if la!="VALID":
        return "REJECT","auditor_veto"
    if ls in ("VALID","NOT_IN_CONTEXT"):
        return "VALID","auditor_ok"
    return "REJECT","incoherent_pair"

def summarize_disagreements(rows, out_path="runs/consistency_disagreements.tsv"):
    out=[]
    for r in rows:
        if r["scholar"]["label"] != r["auditor"]["label"]:
            final, why = final_arbitration(r)
            out.append((r["qid"], r["scholar"]["label"], r["auditor"]["label"], final, why))
    if out:
        with open(out_path,"w",encoding="utf8") as f:
            f.write("qid\tscholar\tauditor\tfinal\twhy\n")
            for row in out: f.write("\t".join(row)+"\n")
    return len(out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pairs", default=None)
    ap.add_argument("--scholar", default=None)
    ap.add_argument("--auditor", default=None)
    ap.add_argument("--pa_gate", type=float, default=0.90)
    ap.add_argument("--kappa_gate", type=float, default=0.75)
    ap.add_argument("--abstain_gate", type=float, default=0.02)
    args=ap.parse_args()
    rows=list(join_pairs(args.pairs, args.scholar, args.auditor))
    M, pa, kappa, n, extra = confusion_and_kappa(rows)
    n_dis = summarize_disagreements(rows)
    report = {
        "n": n,
        "percent_agreement": round(pa,4),
        "kappa": round(kappa,4),
        "abstain_rate": round(extra.get("abstain_rate",0.0),4),
        "disagreements": n_dis,
        "gates": {
            "pa": args.pa_gate, "kappa": args.kappa_gate, "abstain": args.abstain_gate
        },
        "pass": (pa>=args.pa_gate and kappa>=args.kappa_gate and extra.get("abstain_rate",0.0)<=args.abstain_gate)
    }
    print(json.dumps(report, indent=2))

if __name__=="__main__":
    main()
```

Run (pairs file):

```bash
python ProblemMap/eval/cross_agent_consistency.py \
  --pairs ProblemMap/eval/consistency_pairs.jsonl \
  --pa_gate 0.90 --kappa_gate 0.75 --abstain_gate 0.02 > eval/consistency.json
```

Run (separate files):

```bash
python ProblemMap/eval/cross_agent_consistency.py \
  --scholar ProblemMap/eval/scholar.jsonl \
  --auditor ProblemMap/eval/auditor.jsonl \
  > eval/consistency.json
```

This writes a human-readable TSV of disagreements at `runs/consistency_disagreements.tsv` with a **FINAL** arbitration recommendation per item.

---

## 6) CI Gates (copy-paste)

```bash
python ProblemMap/eval/cross_agent_consistency.py --pairs ProblemMap/eval/consistency_pairs.jsonl \
| tee eval/consistency.json

jq -e '.percent_agreement >= 0.90 and .kappa >= 0.75 and .abstain_rate <= 0.02 and .pass==true' eval/consistency.json
```

> If the job fails, attach `runs/consistency_disagreements.tsv` to the PR and prioritize fixes:
>
> 1. **Hard flags** first (provenance/constraints), 2) template/schema drift, 3) retriever recall.

---

## 7) Hygiene & Design Notes

* **Blind independence**: do not let Scholar see Auditor’s label (and vice versa).
* **Same evidence**: both agents must evaluate the identical `retrieved_ids` & `answer_json`.
* **Fixed refusal token**: `not in context` only. No synonyms.
* **Stable seeds**: if any agent is an LLM, fix temperature/seed (or run multi-vote with a deterministic reducer).
* **Audit trail**: keep `reason` fields minimal, actionable, and free of PII.

---

### 🧭 Explore More

| Module                | Description                                                          | Link                                                                                               |
| --------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core             | Standalone semantic reasoning engine for any LLM                     | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework                | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines               | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite                     | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ **[Star WFGY on GitHub](https://github.com/onestardao/WFGY)**

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>

想接著把 **`eval/eval_semantic_stability.md`**（seed/prompt 抖動下的輸出穩定性，Levenshtein/I-AA、claim/citation invariance gates）也補上嗎？
