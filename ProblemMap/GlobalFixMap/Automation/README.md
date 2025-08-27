# Automation Platforms — Global Fix Map

This hub routes **automation framework bugs** (Zapier, n8n, Make, Retool, etc.) to the structural guardrails in WFGY Problem Map.  
Each page below contains failure points, linked fixes, and a copy-paste recipe for stabilization.

---

## Quick routes to per-tool pages

- Zapier → [zapier.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/zapier.md)  
- n8n → [n8n.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/n8n.md)  
- Make (Integromat) → [make.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/make.md)  
- Retool → [retool.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/retool.md)  
- IFTTT → [ifttt.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/ifttt.md)  
- Pipedream → [pipedream.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/pipedream.md)  
- Power Automate → [power-automate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/power-automate.md)  
- GitHub Actions → [github-actions.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/github-actions.md)  
- Airflow → [airflow.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/airflow.md)  
- Airtable → [airtable.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/airtable.md)  
- Asana → [asana.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/asana.md)  
- GoHighLevel (GHL) → [ghl.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/ghl.md)  
- Parabola → [parabola.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/parabola.md)  
- LangChain (automation mode) → [langchain.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/langchain.md)  
- LlamaIndex (automation mode) → [llamaindex.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/llamaindex.md)  

---

## Typical failure classes

- **Bootstrap race conditions**  
  Tools firing before the data index or vector store is ready.  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- **Deployment deadlocks**  
  Infinite waits between worker, retriever, or webhook callbacks.  
  → [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- **Pre-deploy collapse**  
  Wrong version triggered on first call after shipping.  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- **Embedding vs. semantic drift**  
  Looks correct but meaning diverges.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Traceability breaks**  
  Citations do not match source or section.  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Minimal contract for any workflow

1. **Check readiness before calling RAG/LLM**  
   Use `VECTOR_READY` and `INDEX_HASH`. Delay if not valid.

2. **Idempotency**  
   Always compute a dedupe key. Store in KV to block duplicates.

3. **Boundary contract**  
   Require `{snippet_id, section_id, source_url, offsets, tokens}`.  
   Never reuse across sections.

4. **Observability**  
   Log ΔS and λ across steps. Alert if ΔS ≥ 0.60.

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
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

