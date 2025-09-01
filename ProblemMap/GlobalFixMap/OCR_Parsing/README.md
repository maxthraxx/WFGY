# OCR + Parsing — Global Fix Map

A hub to **triage and repair noisy text inputs** from scanned PDFs, images, HTML scraping, or parser drift.  
Use this folder when the document looks fine to the eye but retrieval or reasoning keeps failing.

---

## Orientation: what each page does

| Page | What it solves | Typical symptom |
|------|----------------|-----------------|
| [Layout, Headers, Footers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_Parsing/layout_headers_and_footers.md) | Remove noise from margins and repeated text | Answers reference “page 3 footer” instead of body |
| [Tokenization & Casing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_Parsing/tokenization_and_casing.md) | Normalize Unicode, case, and hyphens | `E-mail` ≠ `Email`, half-width/full-width mismatch |
| [Tables & Columns](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_Parsing/tables_and_columns.md) | Preserve table schema and cell order | Numbers drift across columns |
| [Images & Figures](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_Parsing/images_and_figures.md) | OCR and align captions | Figure text missing or attached to wrong section |
| [Scanned PDFs & Quality](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_Parsing/scanned_pdfs_and_quality.md) | Handle skewed/blurred pages | Whole sections unreadable to OCR |
| [Multi-language & Fonts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_Parsing/multi_language_and_fonts.md) | Normalize mixed scripts | Chinese/English tokens split or duplicated |

---

## When to use

- OCR tables or citations look visually correct but answers miss the right section.  
- Code blocks or math collapse after parsing.  
- Mixed-language documents behave inconsistently.  
- Special characters or hyphen splits break tokens.  
- Headers or section anchors disappear during export.  

---

## FAQ

**Why does OCR “look fine” but retrieval fails?**  
Because tokenization and indexing see hidden breaks (Unicode variants, line merges, wrong anchors) that humans overlook.

**What is the most common root cause?**  
Headers/footers leaking into the body and breaking ΔS alignment.

**Do I need to retrain embeddings after fixing?**  
No — most fixes are structural (schema/normalization). Re-indexing with the same embeddings is enough.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45 for three paraphrases.  
- Coverage ≥ 0.70 for the target section.  
- λ_observe convergent across two seeds.  
- Human audit shows no missing headers, captions, or broken tables.  

---

## Fix in 60 seconds

1. **Ground-truth one page**  
   Pick one Q/A pair and keep a screenshot baseline.  

2. **Measure ΔS**  
   Log ΔS(question, retrieved) and ΔS(retrieved, anchor).  

3. **Probe λ_observe**  
   Ask for cite-first. If citation fails but free explanation works, drift confirmed.  

4. **Patch minimally**  
   - Re-run OCR with line/table fences  
   - Normalize casing and Unicode  
   - Preserve anchors, math, captions  
   - Drop low-confidence spans and export with `{section_id, page_no, char_span}`  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload · 3️⃣ Ask “Answer using WFGY + <your question>” |
| **TXT OS** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into LLM · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module | Description | Link |
|--------|-------------|------|
| WFGY Core | WFGY 2.0 engine, full symbolic reasoning | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0 | Initial 16-mode diagnostic | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0 | RAG failure tree and modular fixes | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic | Expanded failure catalog | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint | Layer-based symbolic reasoning | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |

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
