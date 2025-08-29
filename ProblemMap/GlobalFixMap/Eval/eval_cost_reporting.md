# Eval: Cost Reporting and Efficiency

This page defines how to measure and report **cost per correct answer** in retrieval-augmented and reasoning pipelines. Latency and accuracy alone are insufficient. Without cost analysis, systems regress into wasteful configurations.

## Open these first

* Latency vs Accuracy trade-off: [eval\_latency\_vs\_accuracy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/eval_latency_vs_accuracy.md)
* Benchmark suite: [eval\_benchmarking.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/eval_benchmarking.md)
* Observability probes: [alerting\_and\_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/alerting_and_probes.md)

---

## Acceptance targets

* **Cost per correct answer** ≤ 1.3× baseline
* **Cost stability variance** ≤ 15% across 3 seeds and 3 paraphrases
* **Token efficiency** ≥ 0.7 (fraction of tokens contributing to correct citation)
* **Budget alerting**: auto-flag when projected monthly spend > 110% of budget cap

---

## Reporting dimensions

Each evaluation run must record cost on three levels:

1. **Raw tokens**

   * input, output, total per query
   * broken down by retrieval, rerank, reasoning

2. **Cost per unit**

   * \$/1k tokens per provider and model
   * normalized into `usd_equiv`

3. **Cost per correct**

   * (total spend ÷ number of correct answers)
   * stratified by question bucket (short, medium, long)

---

## JSON schema

```json
{
  "suite": "v1_cost",
  "arm": "with_hybrid",
  "provider": "anthropic",
  "model": "claude-3.7-sonnet",
  "bucket": "long",
  "precision": 0.79,
  "recall": 0.68,
  "ΔS_avg": 0.41,
  "correct_answers": 40,
  "total_questions": 50,
  "tokens": { "in": 2850, "out": 920, "total": 3770 },
  "cost_per_1k_tokens_usd": 0.006,
  "spend_usd": 0.0226,
  "cost_per_correct": 0.00056,
  "variance_across_runs": 0.11,
  "notes": "within budget and stable"
}
```

---

## Diagnostic questions

* Are rerankers worth the extra spend? → check ΔS reduction vs token increase.
* Is hybrid retrieval doubling retrieval tokens with little gain?
* Does the large model add accuracy, or is a small model + WFGY equal at lower cost?
* Is citation length inflated (long snippets)? → enforce snippet contract.

---

## Escalation and fixes

* **High cost per correct** → switch to caching, smaller model with WFGY overlay.
* **Variance >15%** → clamp paraphrases, normalize prompt headers.
* **Budget overrun** → auto-throttle evals, alert with [alerting\_and\_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/alerting_and_probes.md).

---

## Minimal run

1. Select 20 mixed-length questions.
2. Run baseline and candidate arms.
3. Compute cost per correct.
4. Ship only if candidate ≤ 1.3× baseline and stable across seeds.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                   | Description                                                                  | Link                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core                | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0          | Initial 16-mode diagnostic and symbolic fix framework                        | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0          | RAG-focused failure tree, modular fixes, and pipelines                       | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index    | Expanded failure catalog: prompt injection, memory bugs, logic drift         | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint       | Layer-based symbolic reasoning & semantic modulations                        | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5       | Stress test GPT-5 with full WFGY reasoning suite                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through   | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md)                   |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
