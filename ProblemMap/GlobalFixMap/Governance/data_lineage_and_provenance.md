# Data Lineage and Provenance — Guardrails and Fix Patterns

A governance fix page for when **data origin, transformation, and lineage** are unclear or unverifiable.  
Use this page when retrieval results cannot be traced back to their dataset source, or when provenance breaks across documents, chunks, embeddings, and answers.

---

## When to use this page
- Retrieval output has no clear link back to its document or section.  
- Embedding and chunk pipelines overwrite or drop provenance fields.  
- Audit trail is incomplete across ingestion, index, and RAG responses.  
- Approvals or waivers exist but cannot be joined to data versions.  
- Multi-hop pipelines lose lineage across systems (ETL, embedding, vectorstore, orchestration).  

---

## Acceptance targets
- Every retrieved snippet includes `{doc_id, section_id, source_url, offsets, revision}`.  
- Lineage fields survive across **document → chunk → embedding → retriever → LLM**.  
- Audit joins can reconstruct provenance end-to-end with ≥ 0.95 coverage.  
- ΔS(question, retrieved) ≤ 0.45 for governed outputs.  
- Waivers and overrides include expiry and accountable owner.  

---

## Typical breakpoints and WFGY fix

- **Lost provenance in chunking**  
  → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
  Ensure chunk metadata carries `doc_id`, `section_id`, and token offsets.

- **Vector store overwrites or strips lineage fields**  
  → [vectorstore-fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-fragmentation.md)  
  Enforce schema contracts on ingestion and retrieval layers.

- **Answers cannot be tied back to original snippet**  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Require cite-then-explain and enforce snippet ID propagation.

- **Ambiguous approval or version skew**  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md),  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)  

- **Multi-system lineage gaps (ETL, embedding, RAG orchestration)**  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
  Contract schema ensures interoperability across steps.  

---

## Minimal governance checklist
1. **Ingest contracts** — Every ETL pipeline attaches `doc_id`, `revision`, and `source_url`.  
2. **Chunk schema** — Ensure token offsets and section boundaries are immutable.  
3. **Embedding schema** — Carry `embedding_id`, `doc_hash`, and `index_hash`.  
4. **Retriever response** — Must include `snippet_id` + lineage fields, not just text.  
5. **LLM prompt contracts** — Require cite-then-explain, forbid unlinked spans.  
6. **Audit trail** — Every approval and waiver linked to specific dataset version.  

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

