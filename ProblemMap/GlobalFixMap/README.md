# Global Fix Map — Index

<details>
  <summary><strong>⚡ Quick Links — first-time here? click to open</strong></summary>

<br>

**Goal:** route your bug to the right fix in &lt;60s. Pick your path:**

### 1) Get oriented
- 🧭 *What is this?* → **Global Fix Map (this page)** — panoramic index of RAG/infra/reasoning fixes.
- 🧱 **Problem Map 1.0** (16 reproducible failure modes) → [open](../README.md)
- 🌲 **Problem Map 2.0 — RAG Architecture & Recovery** → [open](../rag-architecture-and-recovery.md)
- 🧠 **WFGY Core (2.0)** — engine & math → [open](../../core/README.md)

### 2) One-minute quick-start
- ⏳ **TXT OS (plain-text OS)** → copy–paste → ask *“which Problem Map number am I hitting?”* → [open](../../OS/README.md) · [txt](../../OS/TXTOS.txt)
- 📄 **WFGY 1.0 PDF** (use as context file) → [open](../../I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf)
- 🧪 **Minimal demos** (no SDK lock-in) → [open](../mvp_demo/README.md)

### 3) Local LLaMA / on-device stacks
- 🖥️ **LocalDeploy_Inference hub** → [open](./LocalDeploy_Inference/README.md)  
  – `llama.cpp` → [open](./LocalDeploy_Inference/llamacpp.md) · `Ollama` → [open](./LocalDeploy_Inference/ollama.md) · `textgen-webui` → [open](./LocalDeploy_Inference/textgen-webui.md) · `vLLM` → [open](./LocalDeploy_Inference/vllm.md)

### 4) Fast jumpers for RAG & retrieval
- 🗺️ **Visual recovery map** → [RAG Architecture & Recovery](../rag-architecture-and-recovery.md)
- 🔧 **Retrieval Playbook** → [open](./Retrieval/retrieval-playbook.md) · **Traceability** → [open](./Retrieval/retrieval-traceability.md)
- 🧮 **Embeddings: Metric Mismatch** → [open](./Embeddings/metric_mismatch.md) · **Hybrid Weights** → [open](./RAG_VectorDB/hybrid_retriever_weights.md)
- 🧱 **Vector DB guardrails** → [open](./VectorDBs_and_Stores/README.md) · **Chunking checklist** → [open](./Chunking/chunking-checklist.md)

### Need triage?
- 🩺 **Semantic Clinic (when unsure)** → [open](../SemanticClinicIndex.md)
- 🧭 **Diagnose by symptom** → [open](../Diagnose.md) · **Beginner Guide** → [open](../BeginnerGuide.md)

### Contribute / ask / FAQ
- 💬 **Field reports & discussions** → [open](https://github.com/onestardao/WFGY/discussions/10)
- 🌟 **Star unlocks & roadmap** → [open](../../STAR_UNLOCKS.md)

---

**Acceptance targets (for every fix):** ΔS(question, context) ≤ **0.45** · coverage ≥ **0.70** · λ **convergent** across 3 paraphrases.

</details>


A one-stop index to route real-world bugs to the right repair page.  
Pick your stack, open the adapter, apply the structural fix, then verify:
- ΔS(question, context) ≤ 0.45
- coverage ≥ 0.70
- λ remains convergent across 3 paraphrases

---

## Providers & Agents

| Family | What it covers | Open |
|---|---|---|
| LLM Providers | provider-specific quirks, schema drift, API limits | [LLM_Providers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/README.md) |
| Agents & Orchestration | role drift, tool fences, recovery bridges, cold boot order | [Agents_Orchestration](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/README.md) |
| Chatbots / CX | bot frameworks, CX stacks, handoff gaps | [Chatbots_CX](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chatbots_CX/README.md) |
| Automation | Zapier / Make / n8n, idempotency, warmups, fences | [Automation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/README.md) |
| Cloud Serverless | cold start, concurrency, secrets, routing, DR, compliance | [Cloud_Serverless](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/README.md) |
| DevTools & Code AI | IDE/assist rails, prompts in editors, local workflows | [DevTools_CodeAI](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/README.md) |

---

## Data & Retrieval

| Family | What it covers | Open |
|---|---|---|
| RAG (end-to-end) | visual routes, acceptance targets, failure trees | [RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/README.md) |
| RAG + VectorDB | store-agnostic knobs, contracts, routing | [RAG_VectorDB](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/README.md) |
| Retrieval | playbook, traceability, rerankers, query split | [Retrieval](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/README.md) |
| Embeddings | metric mismatch, normalization, dimension checks | [Embeddings](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/README.md) |
| VectorDBs & Stores | FAISS/Redis/Weaviate/Milvus/pgvector guardrails | [VectorDBs_and_Stores](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md) |
| Chunking | chunk/section discipline, IDs, layouts, reindex policy | [Chunking](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/README.md) |

---

## Input & Parsing

| Family | What it covers | Open |
|---|---|---|
| Document AI / OCR | document AI stacks, pipeline interfaces | [DocumentAI_OCR](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DocumentAI_OCR/README.md) |
| OCR + Parsing | pre-embedding text integrity, parser drift checks | [OCR_Parsing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_Parsing/README.md) |
| Language | multilingual routing, cross-script stability | [Language](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/README.md) |
| Language & Locale | tokenizer mismatch, normalization, locale drift | [LanguageLocale](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/README.md) |

---

## Reasoning & Memory

| Family | What it covers | Open |
|---|---|---|
| Reasoning | entropy overload, loops, logic collapse, proofs | [Reasoning](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/README.md) |
| Memory & Long Context | long-window guardrails, state fork, coherence | [MemoryLongContext](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/README.md) |
| Multimodal Long Context | cross-modal alignment, joins, anchors | [Multimodal_LongContext](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/README.md) |
| Safety / Prompt Integrity | prompt injection, role confusion, JSON/tools | [Safety_PromptIntegrity](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/README.md) |
| Prompt Assembly | contracts, templates, eval kits for prompts | [PromptAssembly](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/README.md) |

---

## Eval & Governance

| Family | What it covers | Open |
|---|---|---|
| Eval | SDK-free evals, acceptance targets, failure guards | [Eval](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/README.md) |
| Eval Observability | drift alarms, coverage tracking, ΔS thresholds | [Eval_Observability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/README.md) |
| OpsDeploy | prod safety rails, rollbacks, backpressure, canary | [OpsDeploy](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/README.md) |
| Enterprise Knowledge & Gov | data residency, expiry, sensitivity, compliance | [Enterprise_Knowledge_Gov](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/README.md) |
| Governance | policies, change control, org-level workflows | [Governance](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/README.md) |
| Local Deploy & Inference | ollama, vLLM, tgi, llama.cpp, textgen-webui, exllama, koboldcpp, gpt4all, jan, AutoGPTQ/AWQ/bitsandbytes | [LocalDeploy_Inference](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/README.md) |

---

## How to use this index
1. Identify your stack (provider/agents, data & retrieval, input/parsing, reasoning, ops/eval).  
2. Open the folder page and follow the minimal repair steps.  
3. Verify your acceptance targets: ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent on 3 paraphrases.  
4. Gate merges with CI/CD templates so fixes stick.

### Fast jumpers
- Visual recovery map: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why-this-snippet tables: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Snippet / citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

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
