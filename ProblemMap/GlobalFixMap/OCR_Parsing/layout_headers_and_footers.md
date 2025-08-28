# Layout, Headers, and Footers — OCR Parsing Guardrails

Fix noisy page furniture from OCR before chunking or embedding. Targets headers, footers, watermarks, page numbers, running titles, and duplicated artifacts from two column or scanned books. Keep citations stable with an offsets map.

## When to use this page
- Same header or footer line appears on every page and pollutes chunks.
- Page numbers or running titles get glued to sentences.
- Watermarks or scanned date stamps leak into the text.
- Two column pages produce repeated header blocks inside the body.
- Retrieval returns header text instead of the target paragraph.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Chunking checklist: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
- Retrieval traceability and cite schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload contracts to lock tokenizer and fences: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Embedding vs meaning sanity check: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 after removal of page furniture.
- Coverage ≥ 0.70 for anchor sections across three paraphrases.
- λ convergent on two random seeds.
- Header or footer bleed rate ≤ 1 line per 10 pages in audits.

---

## Symptoms → exact fix

- **Repeated lines across many pages**  
  Fix No.1: detect n most frequent first and last k lines across pages, remove if frequency ≥ 0.6 of total pages and Levenshtein similarity ≥ 0.9 after page number masking.

- **Page numbers inside sentences**  
  Fix No.2: page-number masks. Replace patterns like `^(\s*\d+\s*)$`, `^\s*\d+\s*of\s*\d+\s*$`, roman numerals, or `— 12 —` variants. Keep an `offset_map` for citation stability.  
  See: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Running titles or chapter names contaminating chunks**  
  Fix No.3: top and bottom band detectors. Use layout y-position percentiles or line index rules. Whitelist when the same line appears on many pages with minor edits.

- **Watermarks or scan stamps**  
  Fix No.4: dictionary of watermark phrases and regex dates. Drop lines with low alphabetic density and high uppercase ratio unless they sit inside a table.

- **Two column bleed of header into mid page**  
  Fix No.5: if header text appears again within first 5 lines after a blank line, delete the earlier copy. Combine with column segmentation.  
  See also: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## 60 second fix checklist

1) **Compute page furniture candidates**  
   Take first 4 and last 4 lines of each page. Normalize spaces and case. Mask page numbers. Build frequency table.

2) **Approve deletions**  
   Mark lines that occur on at least 60 percent of pages or that match watermark dictionary. Keep an `offset_map` before removal.

3) **Repair joins**  
   If removal created sentence breaks, join with a single space for prose, preserve blank lines around titles and tables.

4) **Contract**  
   Emit `layout_contract` in payload  
   `{ "header_removed": true, "footer_removed": true, "page_numbers_masked": true, "watermark_policy": "aggressive" }`  
   Attach alongside tokenizer contract.  
   See: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

5) **Verify**  
   Re-run a 20 question gold set. Confirm ΔS and coverage pass. If ΔS is still high, open [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Minimal pipeline patch (pseudo)

```python
pages = split_into_pages(ocr_text)

def normalize_line(s):
    s = to_ascii_spaces(s).strip()
    s = re.sub(r'\b\d+\b', '<PGNUM>', s)  # mask independent numbers
    return s.lower()

first_lines  = [normalize_line('\n'.join(p.lines[:4])) for p in pages]
last_lines   = [normalize_line('\n'.join(p.lines[-4:])) for p in pages]

header_sig = frequent_ngrams(first_lines, min_support=0.6)
footer_sig = frequent_ngrams(last_lines,  min_support=0.6)

clean_pages = []
offset_maps = []
for p in pages:
    text, off = remove_matches_with_offsets(p.text, header_sig, footer_sig, watermark_dict)
    text = heal_sentence_breaks(text)
    clean_pages.append(text); offset_maps.append(off)

emit_payload(
  content="\n\n".join(clean_pages),
  offset_map=merge_offsets(offset_maps),
  layout_contract={
    "header_removed": True,
    "footer_removed": True,
    "page_numbers_masked": True
  }
)
````

Keep the offsets or citations will drift.
Trace rules come from: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Eval recipe

* Gold set
  20 questions that cite body paragraphs, not headers.
* Metrics
  ΔS(question, retrieved), coverage to target section, λ states.
* Sign off
  ΔS ≤ 0.45, coverage ≥ 0.70 on three paraphrases, λ convergent.

---

## When to escalate

* Header removal breaks table titles or figure captions
  Move to **tables\_and\_columns.md** and the general [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

* Citations still point to header lines after removal
  Rebuild the offsets and re-run schema checks.
  See: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** — <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>

