# OCR Parsing Checklist — Input Integrity

OCR and parsing errors are one of the most common silent killers of retrieval pipelines.  
Text looks fine to the eye, but models drift because tokens, spacing, or casing have changed.  
This checklist ensures **integrity at the source layer** before embeddings or retrieval begin.

---

## When to use
- OCR text matches the visual PDF but citations miss the right section.  
- Code blocks or math collapse after parsing.  
- Mixed language documents behave inconsistently.  
- Special characters or hyphen splits break tokens.  
- Headers or section anchors disappear during export.  

---

## Core acceptance targets
- Retrieval coverage ≥ **0.70** of intended section.  
- ΔS(question, retrieved) ≤ **0.45**.  
- λ remains convergent across three paraphrases.  
- No orphan tokens or invisible characters.  

---

## Checklist for OCR + Parsing stability

- **Normalization**  
  - Apply Unicode NFC.  
  - Collapse whitespace.  
  - Strip zero-width characters.  
  - Unify full/half-width variants.  

- **Confidence gating**  
  - Drop OCR lines below confidence threshold (e.g., <0.90).  
  - Mark uncertain spans for human review.  

- **Structure retention**  
  - Preserve headers, anchors, and section boundaries.  
  - Maintain paragraph breaks and table grids.  
  - For math/LaTeX, keep explicit delimiters.  

- **Traceable fields**  
  - Every chunk must have `{section_id, start_line, end_line, source_url}`.  
  - Store `ocr_confidence` with each snippet.  

- **Schema validation**  
  - Run post-export audit:  
    - Ensure every snippet cites a valid chunk_id.  
    - Detect empty or duplicated snippets.  

---

## Fix in 60 seconds
1. Normalize the text (Unicode NFC, strip zero-width, unify casing).  
2. Drop low-confidence OCR lines and flag uncertain spans.  
3. Re-parse with structural retention enabled.  
4. Add metadata `{chunk_id, section_id, offsets, ocr_confidence}`.  
5. Re-run ΔS probe; confirm joins ≤ 0.50 and overall ΔS ≤ 0.45.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Task: validate OCR and parsing output.

Protocol:

1. Normalize all inputs (Unicode NFC, full/half width, zero-width removal).
2. Reject snippets with ocr\_confidence < 0.90.
3. Require schema {chunk\_id, section\_id, start\_line, end\_line, source\_url}.
4. Forbid orphan citations.
5. Probe ΔS(question, retrieved). Require ≤ 0.45.
6. Report λ states and trace each snippet.

```

---

## Common failure signals
- Correct visual text but retrieval misses section → invisible marks or spacing drift.  
- Math collapses into plain text → parsing dropped delimiters.  
- Long answers cite nothing → headers lost in export.  
- Flip-flop answers across sessions → orphan tokens or unstable chunking.  

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
