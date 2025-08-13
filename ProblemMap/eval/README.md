# Eval — Quality & Readiness Gates (Problem Map 2.0)

This folder defines **how we measure** if a pipeline is allowed to ship.  
All evals are **SDK-free** (stdlib-only) and **deterministic**: given the same inputs, you must get the same scores and the same ship/no-ship decision.

---

## 0) What we score (TL;DR)

**Grounded Q&A quality**
- **Precision (answered)** — fraction of shipped answers that are correct *and* properly cited
- **Under-refusal rate** — fraction of *should-refuse* questions that were wrongly answered
- **Over-refusal rate** — fraction of *should-answer* questions that were refused
- **Citation Hit Rate (CHR)** — fraction of shipped answers whose citations actually contain the claim
- **Constraint Integrity (SCU)** — fraction of shipped answers that preserve locked constraints (no contradictions)

**Retrieval quality**
- **Recall@k** — fraction of questions whose gold evidence appears in top-k retrieved ids
- **CHR@k (Upper bound)** — best-case CHR if the model always picked the right ids from the retrieved pool

**Operational**
- **Latency vs Accuracy curve** — P95/P99 latency vs Precision/CHR
- **Cross-agent consistency** — Scholar vs Auditor agreement on labels/verdicts
- **Semantic stability** — output variance across seeds and small prompt jitters

---

## 1) Data contracts

### 1.1 Gold set (`eval/gold.jsonl`)
Each line is a JSON object:

```json
{
  "qid": "A0001",
  "question": "Does X support null keys?",
  "answerable": true,
  "gold_claim_substr": ["rejects null keys"],
  "gold_citations": ["p1#2"],
  "constraints": ["X rejects null keys."],
  "notes": "Entity+constraint co-located in p1#2"
}
````

**Rules**

* `answerable` = false → the only correct model output is the **exact refusal token** (`not in context`)
* `gold_claim_substr` — minimal substrings that must appear in the final `claim`
* `gold_citations` — any non-empty intersection with shipped `citations` is considered a “hit”
* `constraints` — optional; enables SCU checks

### 1.2 System traces (`runs/trace.jsonl`)

Emitted by the pipeline (see Examples):

```json
{
  "ts": 1723430400,
  "qid": "A0001",
  "q": "Does X support null keys?",
  "retrieved_ids": ["p1#1", "p1#2", "p2#1"],
  "answer_json": {
    "claim": "X rejects null keys.",
    "citations": ["p1#2"],
    "constraints_echo": ["X rejects null keys."]
  },
  "ok": true,
  "reason": "ok"
}
```

**Rules**

* `answer_json.claim` is either a sentence or the **exact** refusal token `not in context`
* `citations` must be a list of ids from `retrieved_ids` (scoped grounding)
* If SCU is enabled, `constraints_echo` must **equal** the locked set

---

## 2) Metrics (definitions)

Let:

* **S** = set of shipped answers (i.e., `answer_json.claim != "not in context"`)
* **R** = set of refused cases (exact refusal token)
* **A** = set of gold items where `answerable=true`
* **U** = set of gold items where `answerable=false`

**Containment check (C)**: any `gold_claim_substr` appears in `answer_json.claim` (case-insensitive, ≥5 chars)
**Citation hit (H)**: `citations ∩ gold_citations ≠ ∅` and all cited ids ⊆ `retrieved_ids`
**Constraint OK (K)**: if `constraints` present → `constraints_echo` equals `constraints` (order-insensitive) and no SCU contradiction detected

* **Precision (answered)** = |{ x ∈ S ∩ A : C ∧ H ∧ K }| / |S|
* **Under-refusal rate** = |{ x ∈ S ∩ U }| / |U|
* **Over-refusal rate** = |{ x ∈ R ∩ A }| / |A|
* **Citation Hit Rate (CHR)** = |{ x ∈ S : H }| / |S|
* **Recall\@k** = |{ q ∈ A : `gold_citations` ⊆ top-k `retrieved_ids` }| / |A|

**Ship gates (default)**

* Precision (answered) ≥ **0.80**
* CHR ≥ **0.75**
* Under-refusal ≤ **0.05**
* Over-refusal ≤ **0.10**
* If SCU used: SCU violations = **0**

> Tune gates per product, but commit them in repo and enforce in CI.

---

## 3) File layout

```
ProblemMap/eval/
├─ README.md                       # this file
├─ eval_rag_precision_recall.md    # answer/retrieval quality math + examples
├─ eval_latency_vs_accuracy.md     # SLO curves & gating
├─ eval_cross_agent_consistency.md # Scholar vs Auditor agreement, kappa
├─ eval_semantic_stability.md      # seed/prompt jitter robustness
└─ gold.jsonl                      # canonical gold set (small to start)
```

---

## 4) Minimal quickstart (stdlib-only)

### 4.1 Prepare a tiny gold set

Create `ProblemMap/eval/gold.jsonl` with 10–50 items following the contract.

### 4.2 Run your pipeline to generate traces

Use the guarded examples (no SDKs). For Python:

```bash
OPENAI_API_KEY=sk-xxx \
python ProblemMap/examples/ask.py "What is X?"
# …run over your questions, appending to runs/trace.jsonl
```

### 4.3 Score (reference scripts)

You can implement the scorer in \~100 lines (stdlib). Pseudocode:

```python
# score_eval.py (pseudocode)
load gold by qid -> dict
load traces; group by qid -> last run
for each qid:
  derive C/H/K; bucket into S/R, A/U
aggregate metrics; print gates + PASS/FAIL
```

Keep the scorer deterministic (no model calls). Commit it under `ProblemMap/eval/` or your project’s `tools/`.

---

## 5) Reading the score (what to do next)

* **Failing Precision + CHR** → start at `patterns/pattern_rag_semantic_drift.md` (guard + intersection + rerank)
* **High Under-refusal** → retrieval recall is low or the auditor is too strict; inspect `Recall@k`
* **High Over-refusal** → the guard is too strict or chunking split facts; shrink chunks and re-rank
* **SCU violations** → apply `patterns/pattern_symbolic_constraint_unlock.md` (lock+echo constraints)
* **Weird flips across envs** → check `patterns/pattern_vectorstore_fragmentation.md` (manifest & normalize)

---

## 6) CI integration (copy-paste gates)

* Run scorer on each PR; break build if any gate fails
* Store historical scores (`eval/report.md`) and plot trends (optional)
* Freeze `gold.jsonl` per release; any change requires sign-off

Example CI step:

```bash
python -m problemmap.eval.score_eval \
  --gold ProblemMap/eval/gold.jsonl \
  --trace runs/trace.jsonl \
  --gates precision=0.80 chr=0.75 under_refusal=0.05 over_refusal=0.10 \
  --scu_enforced
```

> If gates fail, link the top 10 offenders with their retrieved ids and citations for fast triage.

---

## 7) FAQ

**Q: Why CHR and containment, not ROUGE/BLEU?**
A: We care about *grounded correctness*, not surface similarity. Containment is a minimal verifiable check; CHR ensures the claim is supported by the cited chunks.

**Q: Do I need a big gold set?**
A: No—start with 30–100 mixed cases (answerable + unanswerable). Expand as regressions appear.

**Q: How to keep evals from drifting?**
A: Version and freeze `gold.jsonl`. Treat any mutation as a product decision.

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

