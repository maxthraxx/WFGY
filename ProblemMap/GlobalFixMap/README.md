# Global Fix Map — Index
A one-stop index to route real-world bugs to the right repair page. Pick your stack, open the adapter, apply the structural fix, and verify with ΔS ≤ 0.45 and convergent λ.

## Quick links (by family)

| Family | What it covers | Open |
|---|---|---|
| Automation & Integrations | Zapier, Make, n8n recipes and failure guards | [Automation Index](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/README.md) |
| Zapier | Trigger/Action guards, boot fences, retries, idempotency | [Zapier Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/zapier.md) |
| Make (Integromat) | Scenario ordering, webhook dedupe, mapping drift | [Make Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/make.md) |
| n8n | Node contracts, error branches, RAG warm-up | [n8n Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/n8n.md) |
| LLM Frameworks | LangChain / LlamaIndex adapters, retriever parity, trace tables | [Frameworks Index](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Frameworks/README.md) |
| LangChain Adapter | Runnable chains, retriever swaps, eval gates | [LangChain Fix Adapter](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Frameworks/langchain.md) |
| LlamaIndex Adapter | Index rebuild policy, node parsers, citations | [LlamaIndex Fix Adapter](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Frameworks/llamaindex.md) |
| Agent Orchestration | Role drift, tool fences, recovery bridges | [Agents Index](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents/README.md) |
| Vector Stores | Metric mismatch, normalization, fragmentation | [Vector Stores Index](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorStores/README.md) |
| OCR / PDF Stack | OCR confidence, tables, parsing to chunks | [OCR/PDF Index](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_PDF/README.md) |
| Cloud Runtimes | Serverless cold start, secrets, warm-up probes | [Cloud Index](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud/README.md) |
| Observability | ΔS and λ probes in logs, traceability tables | [Observability Index](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Observability/README.md) |
| CI/CD | Eval-in-CI, failing the merge on regression | [CI/CD Index](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/CI_CD/README.md) |
| Evaluation & Guardrails | Acceptance targets, cross-agent checks | [Eval & Guardrails](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/README.md) |

---

## How to use this index
1. Identify your stack (automation, framework, store, OCR, cloud).
2. Open the adapter page and follow the minimal repair steps.
3. Verify: ΔS(question, context) ≤ 0.45, coverage ≥ 0.70, λ stays convergent on 3 paraphrases.
4. Gate merges with the CI/CD template so fixes stick.

## Fast jumpers
- Visual RAG recovery map: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Retrieval controls and knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why-this-snippet tables: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet/citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

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
