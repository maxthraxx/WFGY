# Problem Map FAQ (full, beginner + practitioner)

This FAQ helps you pick the right fix fast. It is a field manual, not a brochure.  
If you are new, start with “Getting started,” then jump by category.

---

## Quick links by category

- [Getting started](#getting-started)
- [Semantic gates and acceptance targets](#semantic-gates-and-acceptance-targets)
- [RAG, retrieval, and chunking](#rag-retrieval-and-chunking)
- [Embeddings and vector stores](#embeddings-and-vector-stores)
- [Reasoning stability and lambda](#reasoning-stability-and-lambda)
- [Memory and long context](#memory-and-long-context)
- [Agents and orchestration](#agents-and-orchestration)
- [Safety and prompt integrity](#safety-and-prompt-integrity)
- [Deployment, infra, and ops](#deployment-infra-and-ops)
- [Evaluation and governance](#evaluation-and-governance)
- [Language, OCR, and PDFs](#language-ocr-and-pdfs)
- [Troubleshooting matrix](#troubleshooting-matrix)
- [Cost, performance, and vendor lock](#cost-performance-and-vendor-lock)
- [Contributing and proof](#contributing-and-proof)

### Direct map to the 16 problems

No.1 Hallucination & Chunk Drift → [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
No.2 Interpretation Collapse → [retrieval-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md)  
No.3 Long Reasoning Chains → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)  
No.4 Bluffing / Overconfidence → [bluffing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md)  
No.5 Semantic ≠ Embedding → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
No.6 Logic Collapse & Recovery → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
No.7 Memory Breaks Across Sessions → [memory-coherence.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)  
No.8 Debugging is a Black Box → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
No.9 Entropy Collapse → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
No.10 Creative Freeze → [creative-freeze.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/creative-freeze.md)  
No.11 Symbolic Collapse → [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/symbolic-collapse.md)  
No.12 Philosophical Recursion → [philosophical-recursion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/philosophical-recursion.md)  
No.13 Multi-Agent Chaos → [Multi-Agent_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)  
No.14 Bootstrap Ordering → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)  
No.15 Deployment Deadlock → [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)  
No.16 Pre-deploy Collapse → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

Related catalogs  
Problem Map home → [README.md](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)  
Semantic Clinic index → [SemanticClinicIndex.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)  
Global Fix Map overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="getting-started"></a>
## Getting started

**Q. Do I need an SDK or plugin?**  
No. The Problem Map is text-first. Apply minimal fixes directly in your current LLM chat.

**Q. I do not know my problem number. Where do I start?**  
Use the beginner guide and diagnose table:  
- Beginner guide → [BeginnerGuide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/BeginnerGuide.md)  
- Diagnose table → [Diagnose.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Diagnose.md)

**Q. Difference between Problem Map 1.0, Semantic Clinic, and Global Fix Map?**  
- Problem Map 1.0 is the 16-mode failure map with minimal fixes → [ProblemMap/README.md](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)  
- Semantic Clinic is the expanded catalog by topic → [SemanticClinicIndex.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)  
- Global Fix Map is end to end guardrails across stack → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

**Q. Do you have a 60-second quick start?**  
- One-line engine (PDF) → [WFGY 1.0 Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf)  
- Text OS scaffold → [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)

---

<a id="semantic-gates-and-acceptance-targets"></a>
## Semantic gates and acceptance targets

**Q. What is ΔS and why gate answers with it?**  
ΔS is a semantic distance between question, source, and candidate answer. Gate the output under a threshold so you do not accept drift. See overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

**Q. What defaults should I enforce on every answer?**  
- ΔS ≤ 0.45  
- Coverage ≥ 0.70  
- λ state convergent across 3 paraphrases  
- Source present before finalization

**Q. Where do I learn how to watch these in prod?**  
Start from the global overview and follow the observability section → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="rag-retrieval-and-chunking"></a>
## RAG, retrieval, and chunking

**Q. Model picks the wrong paragraph or mixes sources. Which number?**  
Usually No.1 or No.8.  
- No.1 Hallucination & Chunk Drift → [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- No.8 Debugging is a Black Box → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

**Q. What is the minimal guard for RAG answers?**  
Citation first, then write, with IDs and pages. See traceability → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

**Q. My chunking is brittle. Any contract to follow?**  
Start with the Global Fix Map overview and the Chunking section list → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

**Q. Retrieval is unstable after OCR PDFs.**  
Check OCR parsing and layout handling in the Global Fix Map overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="embeddings-and-vector-stores"></a>
## Embeddings and vector stores

**Q. High cosine, wrong meaning. What is that?**  
No.5 Semantic ≠ Embedding. Fix normalization and metric space issues. → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

**Q. Store-specific pitfalls to scan first?**  
Vector DB guardrails (per-tool)  
- FAISS → [faiss.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/faiss.md)  
- Chroma → [chroma.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/chroma.md)  
- Qdrant → [qdrant.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/qdrant.md)  
- Weaviate → [weaviate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/weaviate.md)  
- Milvus → [milvus.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/milvus.md)  
- pgvector → [pgvector.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/pgvector.md)

**Q. Hybrid got worse after I mixed retrievers.**  
Audit metrics first, then tune weights. Guidance in the Global Fix Map overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="reasoning-stability-and-lambda"></a>
## Reasoning stability and lambda

**Q. Coherent tone, wrong answer. Which numbers apply?**  
No.2 and No.6.  
- No.2 Interpretation Collapse → [retrieval-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md)  
- No.6 Logic Collapse & Recovery → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

**Q. What is λ observe and why checkpoints?**  
λ state tells you if the chain is converging. Add embedded checkpoints. Primer → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

**Q. How do I reset without losing everything?**  
Use controlled reset with anchors as in No.6 → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

---

<a id="memory-and-long-context"></a>
## Memory and long context

**Q. Sessions forget agreements between chats.**  
No.7 Memory Coherence. Use state keys and guarded read/write order → [memory-coherence.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)

**Q. Long context still drifts.**  
Check No.9 Entropy Collapse and add anchors → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

<a id="agents-and-orchestration"></a>
## Agents and orchestration

**Q. My agents overwrite each other’s memory.**  
No.13 Multi-Agent Chaos. Roles, state keys, fences → [Multi-Agent_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

**Q. Do these guards depend on a specific orchestrator?**  
No. They are provider-agnostic. See adapters in the Global Fix Map overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="safety-and-prompt-integrity"></a>
## Safety and prompt integrity

**Q. Prompt injection keeps leaking into the chain.**  
Use the Semantic Clinic entries and the safety section from the Global Fix Map overview → [SemanticClinicIndex.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)

**Q. Users jailbreak system instructions.**  
Set role order and timeouts; see Global Fix Map overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="deployment-infra-and-ops"></a>
## Deployment, infra, and ops

**Q. First production call fails though local tests passed.**  
No.16 Pre-deploy Collapse → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

**Q. Services block each other at rollout.**  
No.15 Deployment Deadlock → [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

**Q. Canonical boot order for AI stacks.**  
No.14 Bootstrap Ordering → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

---

<a id="evaluation-and-governance"></a>
## Evaluation and governance

**Q. How do I prove fixes work beyond toy cases?**  
Use ΔS, coverage, λ convergence, and traceability. Start here → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

**Q. Team needs audits and sign-off.**  
Governance patterns live in the Global Fix Map overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="language-ocr-and-pdfs"></a>
## Language, OCR, and PDFs

**Q. Multilingual RAG is flaky.**  
Check analyzers and ranking per language. Start from the Global Fix Map overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

**Q. CJK width and punctuation break retrieval.**  
See the language locale notes in the overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

**Q. OCR vendor choice and parsing details.**  
Use the Document AI and OCR entries from the overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="troubleshooting-matrix"></a>
## Troubleshooting matrix

**Q. Output sounds right but citations are missing.**  
No.4 Bluffing and No.8 Traceability.  
- Bluffing / Overconfidence → [bluffing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md)  
- Retrieval Traceability → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

**Q. Every retry is different in a bad way.**  
No.9 Entropy Collapse and missing anchors → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

**Q. Tables and equations flattened to prose.**  
No.11 Symbolic Collapse → [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/symbolic-collapse.md)

**Q. Hybrid retrieval got worse than single model.**  
Audit metrics and weights from the Global Fix Map overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="cost-performance-and-vendor-lock"></a>
## Cost, performance, and vendor lock

**Q. Will guards increase token bill or latency?**  
Minimal guards usually reduce retries and useless generations. Measure it with your eval harness. Overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

**Q. Does this force a specific vendor?**  
No. The guardrails are provider-agnostic. See adapters in the overview → [GlobalFixMap/README.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)

---

<a id="contributing-and-proof"></a>
## Contributing and proof

**Q. Where can I see real user threads or ask?**  
Hero Log discussions → [Discussions](https://github.com/onestardao/WFGY/discussions/10)

**Q. I want to contribute modules or demos.**  
Start here → [ProblemMap/README.md](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)

---

## Minimal fix checklist you can paste into any chat

- Card first. Show source IDs before writing the answer.  
- Pass the semantic gate. ΔS ≤ 0.45 against the chosen source.  
- Check coverage. ≥ 0.70 relative to the stated goal or query.  
- Keep λ convergent across 3 paraphrases. If not, reset with anchors.  
- Log the trace. Question, retrieval IDs, acceptance metrics, final answer.

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

