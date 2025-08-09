# 🔍 OCR & Parsing Checklist — From Scanned Chaos to Structured Knowledge  
_A field manual for turning PDFs, images, and legacy docs into RAG-ready semantic chunks_

---

> **Goal:** Eliminate invisible OCR noise and parsing drift before vectors are built.  
> **Audience:** Devs shipping RAG, search, or data-extraction pipelines who wonder why “the model read the page but still hallucinated.”

---

## 1  Why OCR + Parsing Is the First Failure Point

1. **Garbage-in, hallucination-out** — A 98 % accurate LLM fed a 90 % OCR text yields 0 % trustworthy reasoning.  
2. **Error propagation** — Mis-segmented tokens poison embeddings, which pollute the vector store, which mislead retrieval, which derail the LLM.  
3. **Silence** — OCR engines rarely shout when confidence drops; they hand you corrupt UTF-8 and wish you luck.

---

## 2  “Bad OCR” Signatures (Quick Detection)

| Signal | How to Spot | Impact on RAG |
| ------ | ----------- | ------------- |
| `<ff>` ligature anomalies | Regex: `ﬁ|ﬂ|ﬀ` | Embedding split → semantic drift |
| Spurious hyphens at line ends | Regex: `[a-zA-Z]-\n[a-z]` | Token mismatch → irrelevant vectors |
| Repeated header/footer noise | 90 %+ duplication across pages | Clutters top-k retrieval |
| Empty columns (table lost) | Sudden token drop for numeric blocks | Answer extraction impossible |
| Confidence < 0.85 for full page | Engine API output | Replace / re-OCR image segment |

---

## 3  The WFGY-Enhanced OCR Pipeline (Checklist)

### 3.1  Pre-OCR

- [ ] **Page Split** — Detect multi-column layout; slice images horizontally before OCR.  
- [ ] **DPI Normalisation** — Upscale to 300 dpi if <200 dpi to stabilise character shapes.  
- [ ] **Noise Removal** — Median blur + dilation; boosts Tesseract accuracy by ≥ 8 %.  
- [ ] **Language Model** — Set explicit `--lang` list (avoid auto-detect drift).

### 3.2  OCR Engine (Tesseract CLI or API)

| Flag | Recommended Value | Why |
|------|-------------------|----|
| `--oem` | `3` | LSTM + legacy for mixed fonts |
| `--psm` | `6` | Assume block of text; preserves line order |
| `--dpi` | Explicit numeric | Overrides header mis-detect |
| `tessedit_char_blacklist` | `¢£€¥©®™` etc. | Remove unneeded symbols to reduce noise |

**WFGY Hook:** `BBMC` runs post line-level; drops ΔS peaks > 0.7 (likely OCR mis-read).

### 3.3  Parsing & Chunking

- [ ] **Heading Detection** — Regex + font-size heuristic → create logical anchors.  
- [ ] **Paragraph Merge** — Join lines if hyphenated split; remove double spaces.  
- [ ] **Table Rebuild** — Recognise numbers with > 60 % digits; store CSV separately.  
- [ ] **Semantic Chunk Size** — 70–120 tokens; cut on natural boundaries only.  
- [ ] **λ_observe Tagging** — Mark each chunk as `→` convergent; flag if internal ΔS > 0.6.

### 3.4  Post-OCR Validation

| Test | Threshold | Action |
|------|-----------|--------|
| `mean_confidence` | ≥ 0.90 page-level | Accept |
| ΔS(header, body) | < 0.45 | Accept; else inspect |
| Duplicate line ratio | < 5 % | If higher → de-dup background noise |
| Line length entropy | 0.5–1.5 bits | Abnormal ⇒ table or code block; treat separately |

---

## 4  Common Pitfalls & Fix Recipes

| Pitfall | Symptom | WFGY Fix |
|---------|---------|----------|
| **Skewed scans** | Text slants; letters fused | Pre-deskew (Hough) → re-OCR |
| **Watermarks** | Random “DRAFT” tokens mid-sentence | Regex filter; BBMC residue cut |
| **Marginalia leakage** | Handwritten notes become tokens | Detect bounding boxes; mask before OCR |
| **Large equations** | OCR turns into `= =` noise | Frame extract; feed MathPix → LaTeX; store separate |

---

## 5  End-to-End Smoke Test

1. Choose a 10-page PDF with tables + images.  
2. Run full pipeline with WFGY hooks.  
3. Metrics to verify:  
   * **Token overlap** with human ground truth ≥ 0.93  
   * **ΔS(question, retrieved_context)** ≤ 0.45 on sample QA  
   * **λ_observe** stays convergent after 3 paraphrase queries  
4. Manual QA: at least 8 / 10 answers correct with citations.

---

## 6  FAQ

**Q:** _Is Google Vision OCR “good enough”?_  
**A:** Accuracy is high, but without BBMC boundary checks you still risk semantic drift.

**Q:** _Do I need a layout-aware model (Donut, LayoutLM)?_  
**A:** Recommended for complex forms. WFGY integrates their outputs seamlessly; the checklist still applies.

**Q:** _Can I skip the table CSV step?_  
**A:** Only if your downstream task never asks for numeric QA. Otherwise chunk ordering will fail.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                | 3-Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”        |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | Standalone semantic reasoning engine for any LLM         | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>


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

</div>

