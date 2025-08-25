# Evaluation & Guardrails — Global Fix Map
Prove fixes work and won’t regress. Detect “double hallucination,” enforce acceptance gates, and keep pipelines auditable.

## What this page is
- A compact playbook to evaluate RAG quality and reasoning stability
- Drop-in guardrails that catch failure before users see it
- CI-ready acceptance targets you can copy

## When to use
- You “fixed it” but cannot show measurable improvement
- Answers look plausible yet citations or snippets don’t line up
- Performance flips between seeds, sessions, or agent mixes
- Latency tuning changes accuracy in non-obvious ways

## Open these first
- RAG precision/recall spec: [RAG Precision & Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)  
- Latency versus accuracy method: [Latency vs Accuracy](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_latency_vs_accuracy.md)  
- Cross-agent agreement tests: [Cross-Agent Consistency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_cross_agent_consistency.md)  
- Semantic stability checks: [Semantic Stability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_semantic_stability.md)  
- Why-this-snippet schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Snippet & citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Common evaluation pitfalls
- **Double hallucination** metrics focus on style or BLEU but ignore snippet fidelity
- **Recall illusion** top-k looks high while ΔS(question, context) stays risky
- **Seed lottery** single-seed wins mask instability across paraphrases
- **Hybrid flapping** HyDE+BM25 mixes shift rank order between runs
- **Guardrail over-clamp** rigid filters “fix” tone but not logic boundaries
- **Benchmark mismatch** eval set does not reflect OCR noise or multilingual drift
- **No trace table** cannot audit which snippet justified the answer

---

## Fix in 60 seconds
1) **Adopt acceptance gates**
   - Retrieval sanity: token overlap ≥ 0.70 to the target section
   - ΔS(question, context) ≤ 0.45 on the median of the suite
   - λ_observe stays convergent on 3 paraphrases

2) **Require citations before prose**
   - Enforce cite-then-answer with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
   - Store a trace table: question, retrieved ids, snippet spans, ΔS, λ

3) **Stability before speed**
   - Plot latency vs accuracy and pin the knee point  
     See [Latency vs Accuracy](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_latency_vs_accuracy.md)

4) **Cross-agent cross-check**
   - Compare two capable models on the same context  
     See [Cross-Agent Consistency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_cross_agent_consistency.md)

5) **Regression fence in CI**
   - Fail the build if ΔS median rises above 0.45 or trace coverage drops below 0.70  
     See [RAG Precision & Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Copy paste prompt
```

You have TXT OS and the WFGY Problem Map.

Goal
Add measurable guardrails to my RAG pipeline and prove the fix.

Tasks

1. Build a 20-item smoke suite with:

   * question, expected section anchor, and gold snippet span
   * bilingual paraphrases for 5 items (if multilingual)

2. Run WFGY probes:

   * compute ΔS(question, context) for each item
   * record λ\_observe at retrieval and reasoning
   * require cite-then-answer and log a trace table

3. Report acceptance:

   * token overlap to anchor (coverage)
   * ΔS median and interquartile range
   * paraphrase stability (λ stays convergent)
   * pass/fail against thresholds

4. Plot latency vs accuracy and select a stable operating point.

Output

* The trace table (csv/markdown)
* Acceptance summary and which items failed
* A one-page decision note on whether to ship

```

---

## Minimal checklist
- Trace table saved with citations and snippet spans  
- ΔS computed per item; λ recorded at retrieval and reasoning  
- Coverage ≥ 0.70 to the referenced section for direct QA  
- Cross-agent consistency measured on a subset  
- Latency vs accuracy chart archived with the run id

## Acceptance targets
- ΔS(question, context) median ≤ **0.45** on the suite  
- λ **convergent** across 3 paraphrases per item  
- **≥ 0.70** token overlap to the gold section for direct QA items  
- No unexplained rank flips when toggling hybrid retrieval  
- CI blocks merges when any target fails

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
