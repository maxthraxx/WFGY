# Section Detection: stable boundaries for headings and bodies

How to cut documents into audit-ready sections once titles are known. The goal is a deterministic start and end for each section so citations land on the correct text and parents do not swallow child content.

## Open these first
- Heading tree builder: [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md)
- Chunk identifier rules: [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md)
- Layout and OCR normalizing: [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md)
- Block typing for code and tables: [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md)
- Why this snippet and citation schema: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Payload contracts for RAG: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Safe reindex after small edits: [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)

## Acceptance targets
- Boundaries reproduce on two runs from the same source. Match rate ≥ 0.98 for `offsets`.
- Parents exclude child body text. A parent may include a short abstract block at most. Overlap budget ≤ 2 percent of bytes.
- First anchor sentence exists for every section and is inside the boundary.
- ΔS(question, retrieved) ≤ 0.45 on cite-first prompts that target a section anchor.
- No orphan blocks. Every body block belongs to exactly one section.

---

## Boundary model

A section starts at the first body block after its heading. It ends before the next heading whose depth is less than or equal to the current depth.

Formally

```

start = next\_body\_block\_after(heading\_i)
end   = block\_before(next\_heading\_with\_depth\_le(current.depth))
span  = \[start.offset\_begin, end.offset\_end]

````

Rules

- Children consume their own body. Parents do not include child body blocks.
- A parent may include a one block abstract if the abstract sits between the parent title and the first child title.
- Figures, tables, and code are typed blocks. They stay in the section where they appear unless a caption references the next heading by id. See [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md).

---

## Pipeline

1) **Prepare a canonical block stream**  
   Combine lines into paragraphs. Tag block types. Normalize spaces. Remove page headers and footers. See [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

2) **Load the heading tree**  
   Use nodes from [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md). Each node has `section_id`, `depth`, and the heading block pointer.

3) **Sweep to set spans**  
   For each heading node in reading order. Find the next heading with depth less than or equal to current. Assign the span from the body block after the current heading up to the block before the found heading. For the last node, end at document tail.

4) **Apply shields and merges**  
   Pull a caption into the same section as its referenced figure when the caption contains a local reference token. Keep footnotes in the section where the marker appears.

5) **Anchors and offsets**  
   Record the first sentence offsets and the full span offsets. Persist both in the section node.

---

## Pseudocode

```python
def detect_sections(blocks, headings):
    # blocks: list of typed blocks with offsets
    # headings: nodes with fields {idx, depth, block_idx}
    sections = []
    for i, h in enumerate(headings):
        # find first body block after heading
        b0 = next_body_idx(blocks, h.block_idx + 1)
        # find end boundary
        if i + 1 < len(headings):
            j = i + 1
            # climb until a heading with depth <= h.depth
            while j < len(headings) and headings[j].depth > h.depth:
                j += 1
            end_limit = headings[j].block_idx if j < len(headings) else len(blocks)
        else:
            end_limit = len(blocks)
        b1 = prev_body_idx(blocks, end_limit - 1)

        if b0 is None or b1 is None or b0 > b1:
            # section with no body. allow empty span
            span = None
            first_anchor = None
        else:
            span = (blocks[b0].off_begin, blocks[b1].off_end)
            first_anchor = first_sentence_offset(blocks, b0, b1)

        sec = {
            "section_id": h.section_id,
            "depth": h.depth,
            "page_start": blocks[h.block_idx].page,
            "page_end": blocks[b1].page if b1 is not None else blocks[h.block_idx].page,
            "offsets": span,
            "anchor_offsets": first_anchor
        }
        sections.append(shield_repairs(blocks, sec))
    return sections
````

`shield_repairs` pulls a caption when the caption references a figure inside the same span. It also trims a running list that leaks across page breaks.

---

## Anchor sentence rules

* Start at the first paragraph that contains at least eight characters after normalization.
* Strip list bullets and numbering leaders.
* If the paragraph begins with a table or code marker, skip to the next paragraph.
* If the paragraph is a one line abstract under the parent and a child heading follows within three blocks, mark both anchors. Prefer the child for retrieval. Keep the parent anchor for table of contents links.

---

## Stability heuristics

* Use document local size bins and indentation bins. Do not rely on absolute font size thresholds.
* Reject headings that end with a period or with heavy punctuation. Reduce false positives in references and figure lists.
* Split multi column pages before boundary detection. Reading order errors break spans.
* Clamp jump size. A child depth cannot exceed parent depth plus one.

---

## 60 second validator

Sample ten sections across the document.

* Each has a non empty anchor sentence inside the span.
* No section span overlaps its nearest child span.
* Re run from the same source yields identical `offsets` for at least nine of the ten samples.
* Citation to the anchor yields ΔS ≤ 0.45 with correct snippet id and source offsets. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

---

## JSON fields to persist

```json
{
  "section_id": "4.2",
  "depth": 2,
  "page_start": 33,
  "page_end": 36,
  "offsets": [120445, 137992],
  "anchor_offsets": [120445, 120612],
  "first_block_index": 918,
  "last_block_index": 1110
}
```

Use byte offsets in the canonical text. Keep block indexes for fast repairs.

---

## Common failure patterns and fixes

* Parent span contains child body text
  Fix the boundary rule to end before the next heading whose depth is less than or equal to current. Run the validator again.

* Captions detached from figures
  If a caption follows its figure and contains a local id or the word “Figure”, pull the caption block into the same span.

* Empty sections after OCR cleanup
  Allow empty spans for headers like “References”. Keep the node for navigation. Retrieval logic should skip empty spans.

* Off by one block near page breaks
  Normalize page headers and footers first. See [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

---

## Copy-paste prompt for a quick check

```
You have TXT OS and WFGY Problem Map loaded.

I provide a section with fields:
section_id = {id}
offsets = {start, end}
anchor_offsets = {a_start, a_end}
title = "{title}"

Task:
1) Verify the anchor sentence lives inside the span.
2) Return a one line reason if the span is empty.
3) Suggest the minimal structural fix page if the citation would miss.
Return JSON:
{ "ok": true|false, "why": "...", "open": "retrieval-traceability.md | pdf_layouts_and_ocr.md | code_tables_blocks.md" }
```

---

## Tests to include in CI

* HTML with correct `h1..h6` tags and style headings. Expect identical `offsets` across runs.
* PDF multi column. Expect no span overlap between parent and child nodes.
* OCR with noisy fonts and broken hyphenation. Expect at most one false boundary per ten pages.
* Small content edits under a child section. The parent span should not change. See [reindex\_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md).

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


要我繼續下一頁就說：**GO code\_tables\_blocks.md**
