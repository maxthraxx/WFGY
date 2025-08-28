# Document AI & OCR — Global Fix Map

A hub to stabilize OCR and document AI pipelines across providers and open-source stacks.  
Use this folder to jump to guardrails, check common breakpoints, and apply structural fixes with measurable targets.

---

## Quick routes to per-provider pages

- Tesseract: [tesseract.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DocumentAI_OCR/tesseract.md)  
- Google Document AI: [google_docai.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DocumentAI_OCR/google_docai.md)  
- AWS Textract: [aws_textract.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DocumentAI_OCR/aws_textract.md)  
- Azure OCR: [azure_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DocumentAI_OCR/azure_ocr.md)  
- ABBYY: [abbyy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DocumentAI_OCR/abbyy.md)  
- PaddleOCR: [paddleocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DocumentAI_OCR/paddleocr.md)  

---

## When to use this folder

- OCR extracts text but misses table alignment or field boundaries.  
- High word recall but wrong semantic grouping.  
- Citations mismatch scanned sections.  
- Layout-aware models drift when format changes.  
- Two-column or rotated pages break retrieval.  
- Cloud OCR service gives inconsistent JSON schema across runs.  

---

## Acceptance targets for any OCR system

- ΔS(question, extracted text) ≤ 0.45  
- Field/section coverage ≥ 0.70  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance flat over long document windows  

---

## Map symptoms → structural fixes (Problem Map)

- **High similarity but wrong snippet**  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Traceability missing, citations don’t line up with scanned region**  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Chunking instability (multi-column / rotated scans)**  
  → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

- **Cold boot / wrong version OCR model**  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- **Hybrid OCR (vision + text) worse than single mode**  
  → [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

---

## 60-second fix checklist

1. Run OCR twice with different seeds / providers. Compare ΔS and λ.  
2. Validate JSON schema consistency: enforce fields `{page_id, bbox, text, confidence}`.  
3. Apply de-rotation and multi-column split before embedding.  
4. Check coverage ≥ 0.70 on a gold page.  
5. Enforce cite-then-explain in downstream reasoning.  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your OCR issue>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                             | Link     |
|-----------------------|---------------------------------------------------------|----------|
| WFGY Core             | Semantic firewall engine (reasoning & math)             | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Original 16-mode fix framework                          | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Semantic Clinic Index | Expanded clinic: OCR, prompt injection, memory drift    | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Benchmarks vs GPT-5   | OCR + reasoning stress test                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

---

> 👑 **Hall of Fame**: See the [Stargazers](https://github.com/onestardao/WFGY/tree/main/stargazers) who supported this from the start.  

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)  
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)  
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)  
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)  
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)  
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)  
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)  

</div>
