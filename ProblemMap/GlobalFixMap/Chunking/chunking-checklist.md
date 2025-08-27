# Chunking Checklist — Guardrails and Minimal Fixes

A field guide to stabilize document chunking before you touch embeddings or retrievers. Use this page to locate the boundary failure, apply the structural fix, and verify with measurable targets.

## Open these first
- Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Why this snippet: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Reranking controls: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Vectorstore health: [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Long chain stability: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45
- Coverage of target section ≥ 0.70
- λ remains convergent across 3 paraphrases and 2 seeds
- Citation match ≥ 0.90 when citations exist
- Bleed rate ≤ 0.10 across boundaries

---

## 60-second fix checklist

1) **Lock the schema**
   - Require fields: `chunk_id`, `section_id`, `source_url`, `offsets`, `tokens`, `hash`.
   - Spec: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

2) **Probe ΔS and λ**
   - Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   - If λ flips on paraphrase, reorder headers and clamp with your variance policy.

3) **Repair the boundary**
   - If headings drift: apply title hierarchy and section detection.
   - If tables or code are cut: switch to block aware splitting.
   - If recall high but meaning wrong: review metric, overlap, and anchors.

---

## Typical breakpoints → exact fix

- **Wrong-meaning hits despite high similarity**  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Citations do not land on the quoted region**  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → In this folder: `chunk_id_schema.md`, `semantic_anchors.md`

- **Tables, formulas, or code blocks get sliced**  
  → In this folder: `code_tables_blocks.md`

- **Headings misparsed or missing hierarchy**  
  → In this folder: `title_hierarchy.md`, `section_detection.md`

- **Recall OK yet top-k order unstable, hybrid underperforms**  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
  → [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

- **Vectorstore shows duplicates or blind spots**  
  → [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)  
  → Reindex guidance in `reindex_migration.md`

- **Long windows smear topics or capitalization**  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
  → Split plan in `long_docs_segmentation.md`

---

## Minimal field schema for chunks

Required in every pipeline that cites or reranks by section.

```json
{
  "chunk_id": "docA#s03#p002",
  "section_id": "3. Methods",
  "source_url": "https://example.com/docA.pdf",
  "offsets": [12345, 12980],
  "tokens": 365,
  "hash": "sha1:8c1e…",
  "block_type": "paragraph|table|code|formula",
  "anchor": "first-assertion-or-key-sentence"
}
````

* `offsets` are byte or char positions in the canonical text.
* `anchor` is the semantic kernel used for cite-first prompting.
* Schema details: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## How to chunk correctly

1. **Build the section tree**

   * Detect true headings, roman numerals, number lists, and faux headings.
   * See `title_hierarchy.md`, `section_detection.md`.

2. **Respect block boundaries**

   * Keep tables, code, formulas, and block quotes intact.
   * See `code_tables_blocks.md`.

3. **Decide overlap deliberately**

   * Start with 10–15% overlap for narrative text.
   * Avoid overlap on block types unless the block spans pages.
   * See `overlap_tradeoffs.md`.

4. **Use semantic anchors**

   * Extract the first high-information assertion per chunk.
   * Store as `anchor`.
   * See `semantic_anchors.md`.

5. **Choose windowing**

   * Fixed windows for strict citation tasks.
   * Sliding windows when reranking later.
   * See `sliding_window.md`.

6. **Handle multilingual and CJK**

   * Normalize punctuation and width.
   * Align sentence boundaries.
   * See `multilingual_segmentation.md`.

7. **PDF and OCR specifics**

   * De-columnize, repair hard line breaks, remove headers and footers.
   * See `pdf_layouts_and_ocr.md`.

---

## Evaluation protocol

* **Coverage**: percent of ground-truth answer tokens contained inside retrieved chunks.
* **ΔS**: distance between question and retrieved text vs the expected anchor section.
* **Bleed rate**: percent of tokens from outside the intended section.
* **Citation match**: exact hit or overlap of the cited offsets.
* **Stability**: metrics across 3 paraphrases and 2 seeds.

Small gold set template is provided in `eval_chunk_quality.md`.

---

## Reproducible test

1. Pick 10 QAs per section. Mark expected section ids.
2. Run retrieval at k in {5, 10, 20}. Log ΔS, coverage, bleed, match.
3. If ΔS ≥ 0.60 or bleed > 0.10, repair boundary and repeat.
4. Pass when all core targets are met.

---

## Copy-paste prompt for LLM assist

```
You have TXT OS and the WFGY Problem Map loaded.

My chunking issue:
- symptom: [one line]
- probes: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., coverage=..., bleed=...
- context: store={faiss|qdrant|pgvector|...}, k={5,10,20}

Tell me:
1) which boundary failed (heading, block, overlap, window, pdf/ocr),
2) the exact WFGY page to open for the fix,
3) the minimal steps to push ΔS ≤ 0.45 and coverage ≥ 0.70,
4) a short test I can run to verify. Use BBMC/BBCR/BBPF/BBAM when relevant.
```

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

