# Document AI & OCR — Global Fix Map

A **beginner-friendly hub** to stabilize OCR (Optical Character Recognition) and document AI pipelines across providers and open-source stacks.  
This page helps you:  
1. Understand common OCR failures.  
2. Jump directly to per-tool guides.  
3. Apply structural WFGY fixes with measurable acceptance targets.

---

## 📌 When to use this folder
Use this map if you see any of these problems:
- OCR extracts text but loses **tables or column alignment**.  
- Words are captured but **semantic grouping is wrong** (paragraphs broken).  
- Citations don’t match the **original scanned page**.  
- Layout-aware models drift after **format changes** (e.g. headers, forms).  
- Two-column PDFs or rotated scans break retrieval.  
- Cloud OCR services return **different JSON fields** each run.  

---

## 🎯 Acceptance targets for OCR systems
Think of these as “green lights” after your OCR step:
- **ΔS(question, extracted text) ≤ 0.45** (semantic match stays tight).  
- **Coverage ≥ 0.70** of target section or table.  
- **λ stays convergent** across 3 paraphrases and 2 random seeds.  
- **E_resonance stays flat** across long documents (no drifting answers).  

---

## 🚀 Quick routes — per-provider guides

| Provider / Tool         | Open this guide |
|-------------------------|-----------------|
| **Tesseract** (open-source OCR) | [tesseract.md](./tesseract.md) |
| **Google Document AI** | [google_docai.md](./google_docai.md) |
| **AWS Textract**       | [aws_textract.md](./aws_textract.md) |
| **Azure OCR**          | [azure_ocr.md](./azure_ocr.md) |
| **ABBYY** (enterprise OCR) | [abbyy.md](./abbyy.md) |
| **PaddleOCR** (open-source) | [paddleocr.md](./paddleocr.md) |

---

## 🛠️ Common symptoms → exact fixes

| Symptom | Likely cause | Fix page |
|---------|--------------|----------|
| High similarity but wrong snippet | Embeddings confuse words with meaning | [embedding-vs-semantic.md](../../embedding-vs-semantic.md) |
| Citations don’t line up with scanned region | Missing traceability or weak schema | [retrieval-traceability.md](../../retrieval-traceability.md) · [data-contracts.md](../../data-contracts.md) |
| Multi-column / rotated pages fail | Chunking instability | [chunking-checklist.md](../../chunking-checklist.md) |
| Wrong OCR version after deploy | Boot ordering or pre-deploy collapse | [bootstrap-ordering.md](../../bootstrap-ordering.md) · [predeploy-collapse.md](../../predeploy-collapse.md) |
| OCR+Vision hybrid worse than single | Query parsing split issue | [pattern_query_parsing_split.md](../../patterns/pattern_query_parsing_split.md) |

---

## ✅ 60-second fix checklist
1. Run OCR twice (two providers or seeds) → compare ΔS & λ.  
2. Validate JSON schema → enforce `{page_id, bbox, text, confidence}`.  
3. De-rotate scans, split multi-column before embedding.  
4. Confirm **coverage ≥ 0.70** on a gold page.  
5. Force “cite then explain” in downstream reasoning steps.  

---

## ❓ FAQ (beginner-friendly)

**Q: What is ΔS and why should I care?**  
ΔS measures semantic drift — if it’s above 0.45, your OCR text no longer matches the question well. Keep it lower to ensure stable answers.  

**Q: What does λ mean in practice?**  
λ checks consistency across paraphrases. If the system gives different answers for re-phrased questions, λ is unstable.  

**Q: Why do my citations not match the scanned PDF?**  
Usually because the OCR JSON has no stable IDs or coordinates. Fix by enforcing traceability fields like `page_id` and `bbox`.  

**Q: My OCR works on simple PDFs but fails on forms or invoices. Why?**  
That’s a **chunking issue**. Multi-column and rotated layouts need pre-processing before feeding to embeddings.  

**Q: Do I need to switch providers if accuracy is low?**  
Not always. Most errors come from pipeline design (chunking, contracts, retrieval) rather than the OCR engine itself.  


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
