# Eval — Quality & Readiness Gates 

This folder defines **how we measure** if a pipeline is allowed to ship.  
All evals are **SDK-free** (stdlib-only) and **deterministic**: given the same inputs, you must get the same scores and the same ship/no-ship decision.

---

## Quick Links (run these first)

- **RAG Precision / Refusals / CHR / Recall@k →** `eval_rag_precision_recall.md`
- **Latency vs Accuracy (SLO & Pareto) →** `eval_latency_vs_accuracy.md`
- **Cross-Agent Consistency (Scholar ↔ Auditor, κ) →** `eval_cross_agent_consistency.md`
- **Semantic Stability (Seeds & Prompt Jitter) →** `eval_semantic_stability.md`

> Start with precision/CHR, then latency SLO, then agent agreement, then stability. Fail fast on each gate.

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
- **CHR@k (upper bound)** — best-case CHR if the model always picked the right ids from the retrieved pool

**Operational**
- **Latency vs Accuracy** — P50/P95/P99 vs Precision/CHR under knob sweeps and load  
- **Cross-agent consistency** — Scholar vs Auditor agreement (Percent Agreement, Cohen’s κ)  
- **Semantic stability** — invariance to seeds and benign prompt jitters (ACR/CGHC/CSS/NED)

---

## 1) Data contracts

### 1.1 Gold set (`eval/gold.jsonl`)
Each line:

```json
{
  "qid": "A0001",
  "question": "Does X support null keys?",
  "answerable": true,
  "gold_claim_substr": ["rejects null keys"],
  "gold_citations": ["p1#2"],
  "constraints": ["X rejects null keys."]
}
````

Rules

* `answerable=false` ⇒ the only correct model output is the **exact** refusal token: `not in context`
* `gold_claim_substr`: minimal substrings that must appear in the shipped `claim`
* `gold_citations`: any overlap with shipped `citations` counts as a hit
* `constraints` optional; enables SCU checks

### 1.2 System traces (`runs/trace.jsonl`)

Emitted by your guarded pipeline:

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

---

## 2) Default ship gates

* Precision (answered) ≥ **0.80**
* CHR ≥ **0.75**
* Under-refusal ≤ **0.05**
* Over-refusal ≤ **0.10**
* If SCU used: **0** constraint violations
* Latency SLO: P95 (E2E) ≤ **2000 ms** (interactive)
* Cross-agent: Percent Agreement ≥ **0.90**, κ ≥ **0.75**, ABSTAIN ≤ **0.02**
* Stability: ACR ≥ **0.95**, CGHC ≥ **0.95**, CSS ≥ **0.70**, NED₅₀ ≤ **0.20**, RCR ≥ **0.98**

> Tune per product, pin thresholds in repo, and enforce in CI.

---

## 3) File layout

```
ProblemMap/eval/
├─ README.md                       # this file (entrypoint)
├─ eval_rag_precision_recall.md    # answer/retrieval metrics + sample JSONL + scorer
├─ eval_latency_vs_accuracy.md     # SLO curves; sweep harness; Pareto selection
├─ eval_cross_agent_consistency.md # Scholar vs Auditor, κ, arbitration policy
├─ eval_semantic_stability.md      # seeds/jitters invariance, ACR/CGHC/CSS/NED
│
├─ score_eval.py                   # reference scorer for precision/CHR/refusals/recall@k
├─ latency_sweep.py                # sweep harness → runs/latency.csv + summary
├─ cross_agent_consistency.py      # PA/κ + disagreements TSV + arbitration
├─ semantic_stability.py           # runner+scorer for seeds/jitters
└─ gold.jsonl                      # canonical gold set (freeze per release)
```

---

## 4) Minimal quickstart (stdlib-only)

1. Create `eval/gold.jsonl` (10–50 items to start).
2. Run your guarded pipeline to append `runs/trace.jsonl`.
3. Score core metrics:

```bash
python ProblemMap/eval/score_eval.py \
  --gold ProblemMap/eval/gold.jsonl \
  --trace runs/trace.jsonl \
  --k 5 \
  --gates precision=0.80,chr=0.75,under=0.05,over=0.10
```

---

## 5) Run the full eval suite (CI recipe, copy/paste)

```bash
# A) Latency sweeps (1 rps & 5 rps)
python ProblemMap/eval/latency_sweep.py --gold ProblemMap/eval/gold.jsonl --rps 1 --duration 30 | tee eval/lat_1rps.json
python ProblemMap/eval/latency_sweep.py --gold ProblemMap/eval/gold.jsonl --rps 5 --duration 60 | tee eval/lat_5rps.json

# B) Core accuracy
python ProblemMap/eval/score_eval.py --gold ProblemMap/eval/gold.jsonl --trace runs/trace.jsonl --k 5 > eval/acc.json

# C) Cross-agent consistency
python ProblemMap/eval/cross_agent_consistency.py --pairs ProblemMap/eval/consistency_pairs.jsonl > eval/consistency.json

# D) Semantic stability (small daily sweep)
python ProblemMap/eval/semantic_stability.py --mode run   --gold ProblemMap/eval/gold.jsonl --http http://localhost:8080/qa --seeds 0,1,2 --jitters none,ws,syn
python ProblemMap/eval/semantic_stability.py --mode score --gold ProblemMap/eval/gold.jsonl --stability runs/stability.jsonl > eval/stability.json

# E) Gates
jq -e '.p95 <= 2000' eval/lat_1rps.json
jq -e '.p95 <= 2500' eval/lat_5rps.json
jq -e '.precision >= 0.80 and .chr >= 0.75 and .under_refusal <= 0.05 and .over_refusal <= 0.10' eval/acc.json
jq -e '.percent_agreement >= 0.90 and .kappa >= 0.75 and .abstain_rate <= 0.02 and .pass==true' eval/consistency.json
jq -e '.pass == true' eval/stability.json
```

---

## 6) Troubleshooting map

* **Precision low, CHR low** → Start at *RAG Precision & CHR* page; apply **Semantic Drift** pattern (guard + intersection + knee).
* **Over-refusal high** → Recall\@k too low or chunks split facts; shrink chunks and re-rank.
* **Latency P95 blown** → Trim `max_tokens`, enable intersection+knee, reduce `rerank_depth` (see *Latency vs Accuracy*).
* **Agent κ low** → Templates drift or inconsistent guards; fix schema and audit rules (*Cross-Agent Consistency*).
* **Stability fails** → Retrieval pool unstable; apply **Vector Store Fragmentation** and **SCU** patterns.

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

如果你想「只補差異」也可以，我再給你精準 patch；但這份是**一鍵覆蓋版**，最不容易再走鐘。接下來要不要我衝 `ops/README.md`（一頁式救火流程 + readiness/sentinel 模式），還是回到 `examples/` 把 `example_02_self_reflection.md` 補上？
