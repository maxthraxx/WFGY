# OCR + Parsing — Global Fix Map
Triage and repair for scanned PDFs, images, HTML scraping, and parser noise.  
Use this page when the documents look fine to the eye but retrieval or reasoning keeps drifting.

## What this page is
- A fast route to validate text integrity before you touch embeddings or retrieval.
- Structural repairs that stop perception drift at the source layer.
- Concrete checks that give repeatable acceptance targets.

## When to use
- OCR tables or citations look visually correct but answers miss the right section.
- Code blocks or math collapse after parsing.
- Mixed language documents behave inconsistently.
- Special characters or hyphen splits break tokens.
- Headers or section anchors disappear during export.

## Open these first
- OCR and parsing checklist: [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
- Traceability and snippet schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Language and tokenizer guidance: [Multilingual Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multilingual-guide.md)
- Long context sanity and joins: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) · [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

## Fix in 60 seconds
1) **Ground-truth a page**
   - Pick one question and one expected section. Keep a human screenshot for reference.
2) **Measure ΔS**
   - Compute ΔS(question, retrieved) and ΔS(retrieved, anchor).  
   - Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.
3) **Add probes with λ_observe**
   - Ask for direct cite lines. If cite fails while free-form explain passes, perception drift is likely.
4) **Apply minimal patch**
   - Re-run OCR with line preservation and table fences.  
   - Keep headers, section ids, and page anchors.  
   - Remove text below an OCR confidence threshold and mark gaps.  
   - Normalize punctuation and hyphen join.  
   - Export a clean text bundle with `section_id`, `page_no`, `char_span`.

## Copy-paste prompt
```

I uploaded TXT OS and the WFGY ProblemMap files.

My OCR or parsing bug:

* symptom: \[brief]
* traces: \[examples or screenshots], \[ΔS(question,retrieved)], \[ΔS(retrieved,anchor)], \[λ states]

Tell me:

1. which perception step failed and why,
2. which exact fix page to open from this repo,
3. the smallest set of changes to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify the repair with a reproducible test.
   Return the snippet schema I should enforce in the index step.

```

## Minimal checklist
- Keep headings, captions, and table cells as separate blocks with ids.
- Preserve code fences and math blocks as non-wrapping segments.
- Normalize Unicode forms and spaces. Remove hard hyphen splits across lines.
- Store `source_id`, `section_id`, `page_no`, and `char_span` for each block.
- For images with text, keep the image link next to the extracted text for audits.

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 for three paraphrases.
- Cite-first passes on the same question.
- λ remains convergent after you swap paraphrases or reorder non-semantic headers.
- Token overlap to the target section ≥ 0.70.
- Human audit shows no missing headers or broken tables in the exported bundle.

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

