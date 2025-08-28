# Scanned PDFs and Quality: OCR Parsing Guardrails

Stabilize OCR extraction on noisy scans, low-resolution images, and multi-generation photocopies. Ensure text is auditable, retrievable, and bound by schema despite quality issues.

## Open these first
- OCR parsing checklist: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)  
- Data contracts: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Hallucination control: [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- Chunking guide: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

## Acceptance targets
- OCR character error rate (CER) ≤ 2% after cleanup
- ΔS(question, retrieved) ≤ 0.45 even when scan quality < 300 dpi
- λ remains convergent across paraphrases
- All extracted text auditable against source image hash

---

## Typical failure signatures → fix
- **Broken characters and merged glyphs**  
  Apply normalization and Unicode repair before indexing. Validate against a whitelist of expected ranges.

- **Multi-generation photocopy blur**  
  Route through OCR engine supporting adaptive binarization. Anchor outputs with image hash to avoid ghost drift.

- **Double-encoded PDFs** (text + image overlay)  
  Deduplicate layers. Choose the higher-confidence text layer and tag source.

- **Skewed pages or rotated scans**  
  Run deskew filter before OCR. Capture skew angle metadata for audit.

- **Mixed-language or font variants**  
  Force language models per region. Split by script. Store per-block language code.

- **Noise artifacts** (staple marks, stamps, watermarks)  
  Strip bounding boxes below token threshold. Mark as `noise_block` instead of narrative text.

---

## Fix in 60 seconds
1) **Hash source image**  
   Store `scan_id` and `image_hash` for every page. Tie all extracted text back to this anchor.

2) **Normalize text**  
   Apply Unicode NFKC. Collapse broken ligatures and fix spacing errors.

3) **De-layer double PDFs**  
   Choose the OCR text layer with confidence ≥ 0.90. Drop shadow text.

4) **Audit with ΔS**  
   Probe scanned text with 3 paraphrases. If ΔS ≥ 0.60, run re-OCR with stricter binarization.

5) **Chunk and contract**  
   Split by page. Enforce data contract fields: `page_no`, `scan_id`, `text_clean`, `bbox`.

---

## Minimal recipes by engine

- **Google Document AI**  
  Use `qualityScores.confidence` field. Reject blocks with confidence < 0.7.

- **AWS Textract**  
  Hash `BlockType=PAGE`. Keep page-level confidence. Store as `scan_id`.

- **Azure OCR**  
  Normalize boundingRegions. Add `language` code explicitly if detected.

- **ABBYY**  
  Use `<charParams>` confidence. Flag low confidence segments for secondary OCR.

- **PaddleOCR**  
  Use angle classification for deskew. Split multilingual pages into per-line language tags.

---

## Data contract extension
```

{
"scan\_id": "p12\_imghash",
"page\_no": 12,
"image\_hash": "sha256:...",
"text\_clean": "...",
"language": "en",
"confidence": 0.92,
"noise\_blocks": \[...],
"source\_url": "..."
}

```

---

## Verification
- **Leak check**: ensure no shadow/duplicate text.  
- **Quality probe**: CER ≤ 2% on 1k sample chars.  
- **Stability probe**: ΔS stable across paraphrases.  
- **Auditability**: all text traceable to image hash.

---

## Copy-paste LLM prompt
```

You have TXTOS and WFGY Problem Map.

My scan:

* page\_no: {n}
* text\_clean: "..."
* confidence: 0.xx
* image\_hash: "..."

Tasks:

1. If text looks corrupted, fail fast and cite fix page.
2. Validate schema (ocr-parsing-checklist, data-contracts).
3. Return JSON: { "answer":"...", "citations":\[...], "ΔS":0.xx, "λ\_state":"..." }

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

要不要我直接幫你接續做下一個 `multi_language_and_fonts.md`？
