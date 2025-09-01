# Chunking — Global Fix Map

A compact hub to **stabilize document chunking** across formats, pipelines, and retrieval systems.  
This folder routes chunk-related bugs to structural fixes and provides checklists, schema, and live recipes.  
No infra change required.

---

## Orientation: what each page does

| Page | What it solves | Typical symptom |
|---|---|---|
| [Chunk ID Schema](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md) | Unique ID + schema for each chunk | Duplicate or drifting chunks across runs |
| [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunking-checklist.md) | Minimal audit list for validity | Chunks too long, too short, or incomplete |
| [Code / Tables / Blocks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md) | Preserve structure for code, tables, blocks | Retrieval drops formatting or logic |
| [Section Detection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md) | Detect paragraph and section anchors | Anchors missing, snippets cut mid-thought |
| [Title Hierarchy](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md) | Maintain document heading hierarchy | Only partial or meaningless sub-sections retrieved |
| [PDF Layouts & OCR](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md) | Repair PDF/OCR-specific chunking | Citations collapse after parsing |
| [Reindex & Migration](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md) | Safe chunk migration during reindex | Index rebuilt but old refs mismatch |
| [Eval RAG Precision & Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/eval_rag_precision_recall.md) | Deterministic evaluation recipes | “Better” chunking cannot be proven |
| [Live Monitoring (RAG)](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/live_monitoring_rag.md) | Online health checks for chunking | Sudden drift or collapse after deploy |

---

## When to use this folder

- Your chunks look fine by eye but retrieval skips important sections.  
- PDF / OCR parsing collapses headers, math, or tables.  
- Hybrid retrievers underperform due to inconsistent chunk boundaries.  
- Reindexing breaks old citations.  
- Context flips between runs with same corpus.

---

## Acceptance targets

- Chunk boundaries align with semantic windows  
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe convergent across 3 paraphrases and 2 seeds  
- Traceability contract fields always present: `{snippet_id, section_id, source_url, offsets, tokens}`

---

## 60-second fix checklist

1) **Check chunk IDs**  
   Apply `chunk_id_schema`. Ensure unique + stable across reindex.

2) **Audit with checklist**  
   Run the [chunking-checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunking-checklist.md) before ingest.

3) **Preserve structure**  
   Use [code_tables_blocks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md) for code, tables, blocks.

4) **Validate anchors**  
   Confirm section and title detection. Apply [title_hierarchy](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md).

5) **Reindex safely**  
   Use [reindex_migration](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md) with hash/version lock.

6) **Monitor live**  
   Apply [live_monitoring_rag](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/live_monitoring_rag.md) to catch collapse early.

---

## Minimal probe pack

```txt
Context: I loaded TXT OS and the WFGY pages.

Task:
- Given doc corpus D, log ΔS(question, retrieved) and λ across 3 paraphrases.
- Validate chunk IDs and section anchors.
- If ΔS ≥ 0.60 or λ flips, propose the smallest structural change:
  chunk schema, checklist, or reindex.
- Verify coverage ≥ 0.70 after fix.

Return JSON:
{ "citations": [...], "ΔS": 0.xx, "λ_state": "<>", "coverage": 0.xx, "next_fix": "..." }
```
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
