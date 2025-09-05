# Tokenization & Casing — OCR Parsing Guardrails

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **OCR_Parsing**.  
  > To reorient, go back here:  
  >
  > - [**OCR_Parsing** — text recognition and document structure parsing](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A focused fix page for post-OCR text where casing, spaces, or token boundaries are corrupted. Use this to normalize the stream **before** chunking/embedding, and verify with measurable targets. Works across Tesseract, Google DocAI, Azure OCR, ABBYY, PaddleOCR, and custom engines.

## When to use this page
- Words are split or glued (e.g., `re tri eval`, `metadataindex`).
- Case flaps mid-sentence (`tHE DocUment`), acronyms collapse (`R a G`).
- Invisible characters or double spaces change token counts.
- Chunkers behave inconsistently between runs with the same image/PDF.
- Embedding recall looks fine locally but retrieval ΔS stays high.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Chunking checklist: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
- Retrieval traceability (cite-then-explain schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload schema fences: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Embedding vs meaning (when token noise leaks into vectors): [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 after normalization.
- Coverage to target section ≥ 0.70 on three paraphrases.
- λ remains convergent across two seeds.
- Token count variance for the same page ≤ 1 percent after normalization.

---

## Symptoms → exact fix

- **Mid-token splits or merges** (`infor mation`, `vectorstoreindex`)  
  Fix No.1: **Rejoin by dictionary and layout anchors.**  
  Use wordlist + n-gram agree check, prefer joins that reduce ΔS on a small gold set.  
  See: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

- **Casing drift** (random upper/lower), acronym scatter (`r.a.g.`)  
  Fix No.2: **Casing normalization with protected spans.**  
  Protect enums, acronyms, chemical names, LaTeX blocks, code fonts.

- **Whitespace noise** (NBSP, thin space, double space)  
  Fix No.3: **Unicode normalization + space collapse**, keep offsets table.  
  Record before/after offset map to preserve citation alignment.  
  See: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Punctuation misreads** (`l` vs `1`, `O` vs `0`, `,` vs `.`)  
  Fix No.4: **Confusable set pass + local language model vote.**  
  Only apply inside numeric or acronym contexts, keep audit log.

- **Tokenizer mismatch across components**  
  Fix No.5: **Single tokenizer contract for parse → chunk → embed.**  
  Declare `tokenizer_name`, `lowercase`, `strip_accents` in payload.  
  See: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## 60-second fix checklist

1) **Normalize**  
   - Unicode NFC, strip BOM, collapse spaces except inside code/math blocks.  
   - Replace NBSP and thin spaces with ASCII space.  
   - Build `offset_map` old→new for citations.

2) **Protect**  
   - Detect protected spans: URLs, emails, hex, code, LaTeX, table headers, known acronyms.  
   - Freeze casing and punctuation inside protected spans.

3) **Rejoin / Split**  
   - Rejoin candidates by dictionary + bigram score.  
   - Split stuck words when edit distance to dictionary is lower after split.

4) **Contract**  
   - Emit `tokenizer_contract.json`:  
     `{ "tokenizer": "bert-base-uncased", "lowercase": true, "strip_accents": true }`  
     Attach to every downstream step.  
     See: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

5) **Verify**  
   - Recompute ΔS on a 20-question gold set.  
   - If ΔS stays ≥ 0.60, open [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and rebuild index with the same tokenizer contract.

---

## Minimal pipeline patch (pseudo)

```python
text = ocr_text

text = unicode_normalize_nfc(text)
text, offset_map = collapse_spaces_with_offsets(text)
spans = detect_protected_spans(text)  # urls, code, latex, acronyms
text = normalize_casing(text, protect=spans)

cands = find_split_merge_candidates(text, protect=spans)
text = apply_split_merge(text, cands, scorer="bigram+dict")

emit_payload(
  content=text,
  offset_map=offset_map,
  tokenizer_contract={
    "tokenizer": "bert-base-uncased",
    "lowercase": True,
    "strip_accents": True
  }
)
````

Keep the offset map, or citations will drift.
Tracing and schema rules come from: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Eval recipe

* Build a tiny page-level gold: 10–20 questions with expected anchor sections.
* Measure before/after: ΔS(question, retrieved), coverage, λ states.
* Acceptance to sign off: ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent on both seeds.
* Log token count and confusable corrections per page for audit.

---

## When to escalate

* ΔS remains high after normalization and re-chunking
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Citations drift after formatting changes
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Layout destroys sentence flow or table cells
  Open: **OCR\_Parsing/table\_parsing.md** once added, and the general [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

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
