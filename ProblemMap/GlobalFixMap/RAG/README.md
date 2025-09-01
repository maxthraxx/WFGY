# RAG — Global Fix Map

A focused hub for **Retrieval-Augmented Generation failures**.  
Use this folder when answers exist in the corpus but retrieval or evaluation drifts. Each page gives precise guardrails, measurable acceptance targets, and direct links to structural fixes.

---

## When to use this folder
- Correct facts exist in the corpus but never appear in answers.  
- Citations break, hallucinations creep in, or snippets drift.  
- Hybrid retrievers perform worse than single retrievers.  
- Index looks healthy but coverage remains low.  
- Evaluation metrics vary wildly across identical runs.  

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ remains convergent across 3 paraphrases and 2 seeds  
- Eval variance ≤ 0.05 across 5 replays  

---

## Quick routes to per-page guides

- Retrieval drift → [retrieval_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/retrieval_drift.md)  
- Hallucination in RAG → [hallucination_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/hallucination_rag.md)  
- Citation breaks → [citation_break.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/citation_break.md)  
- Hybrid retriever failure → [hybrid_failure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/hybrid_failure.md)  
- Index skew → [index_skew.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/index_skew.md)  
- Context drift → [context_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/context_drift.md)  
- Entropy collapse → [entropy_collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/entropy_collapse.md)  
- Eval drift → [eval_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/eval_drift.md)  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)**  
> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐  

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

</div>
