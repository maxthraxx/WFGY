# Layout, Headers, and Footers: OCR Parsing Guardrails

Strip or normalize page furniture before chunking or embedding. Stop headers, footers, page numbers, and watermarks from polluting semantic meaning and wrecking retrieval.

## Open these first
- OCR end to end checklist: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
- Snippet and citation schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Why this snippet: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Chunking checklist: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 after layout cleanup
- Coverage ≥ 0.70 for the target section
- λ stays convergent across three paraphrases and two seeds
- Zero header/footer strings inside content tokens of any chunk

---

## Typical failure signatures → exact fix
- **Running headers become part of every chunk**  
  Detect repeating lines at top bands per page. Move them to `page_furniture.header` metadata or drop by rule. See: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)

- **Footers and page numbers leak into answers**  
  Identify bottom band strings and numeric patterns. Attach to metadata `page_furniture.footer` and `page_furniture.page_num`, not the content body. See: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Watermarks mix with paragraphs**  
  Use low opacity or diagonal angle cues plus oversized bbox to flag watermark blocks. Remove from body, keep `watermark_text` only in metadata. See: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

- **Section title duplicated on every page**  
  Treat it as header when identical across ≥ 2 consecutive pages. Promote a single canonical section anchor. See: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Footnotes interleaved with paragraph flow**  
  Extract footnote blocks. Keep `footnote_id`, `anchor_offset`, and a separate citation lane. Never mix into paragraph tokens. See: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Fix in 60 seconds
1) **Detect bands**  
   For each page, split objects by vertical bands: `top ≤ 12%`, `bottom ≥ 88%`. Flag candidates for headers and footers.

2) **Find repeats**  
   Normalize text (case, whitespace, punctuation), then mark strings that repeat across pages. Anything stable goes to furniture.

3) **Rewrite content**  
   Remove furniture from body tokens. Store originals under `page_furniture`.

4) **Rechunk**  
   Chunk paragraphs without furniture. Carry `section_id`, `page`, and cleaned offsets.

5) **Probe**  
   Re-run three paraphrases. ΔS drops and λ stops flipping if furniture is out of the body.

---

## Minimal recipes by engine

- **Google Document AI**  
  Use `layout.boundingPoly` for band checks. Identify `paragraph` blocks within top/bottom polygons and mark as furniture. Keep `detectedLanguages`. Apply after-parse dedupe across pages.

- **AWS Textract**  
  From `Blocks` with `BlockType=LINE` or `WORD`, inspect `Geometry.BoundingBox.Top/Height`. Route repeated top-band lines to `page_furniture.header`, bottom band to `footer`. Keep `PAGE` relationships for page numbers.

- **Azure OCR**  
  Use `lines` with `boundingRegions`. Sort by `polygon` y positions, isolate bands, then repeat-check across pages. Store page number patterns `^\s*[ivxlcdm]+$|^\s*\d+\s*$` as `page_num`.

- **ABBYY**  
  Export XML, read `<block>` with coordinates. Apply band and repeat filters. Preserve watermarks as `watermark_text` if block has style or angle attributes.

- **PaddleOCR**  
  Use bbox outputs to filter by top/bottom thresholds. De-dup by normalized text across pages. Keep furniture in metadata only.

---

## Data contract additions for layout cleanup
Add these fields to your snippet schema:

```

{
"page": 7,
"section\_id": "2.3",
"bbox": \[x0,y0,x1,y1],
"text\_clean": "...",             // body without furniture
"text\_raw": "...",               // optional, original page text
"page\_furniture": {
"header": "Company Annual Report 2024",
"footer": "Confidential",
"page\_num": "xv",
"watermark\_text": "DRAFT"
},
"footnotes": \[
{"id":"fn12","text":"...","anchor\_offset":325}
],
"source\_url": "..."
}

```

Mandatory rule: model must read `text_clean` for reasoning. `page_furniture` is trace-only.

---

## Verification
- **Furniture leak test**: sample 20 chunks, assert no header/footer strings inside `text_clean`.
- **ΔS drop**: compare ΔS before and after cleaning on the same question. Target ≤ 0.45.
- **λ stability**: shuffle prompt headers, confirm λ stays convergent.
- **Footnote audit**: a question about a footnote must cite `footnotes[*].id`, not guess from body text.

If ΔS remains flat and high, reopen chunking and metric checks. See: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Copy-paste prompt for the LLM step
```

You have TXT OS and the WFGY Problem Map.

For each snippet I provide:

* use text\_clean for reasoning,
* treat page\_furniture as trace only,
* cite then explain.

Tasks:

1. If header/footer strings appear inside text\_clean, fail fast and return the minimal structural fix referencing:
   ocr-parsing-checklist, data-contracts, retrieval-traceability, chunking-checklist.
2. Return JSON:
   { "citations":\[...], "answer":"...", "λ\_state":"→|←|<>|×", "ΔS":0.xx, "next\_fix":"..." }
   Keep it auditable and short.

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
