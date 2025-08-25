# Language & Locale — Global Fix Map
Stabilize multilingual RAG and reasoning across CJK/RTL/Latin scripts.  
Fix tokenizer mismatch, Unicode normalization, mixed encodings, and cross-lingual retrieval drift.

## What this page is
- A compact, language-aware checklist for retrieval + reasoning
- Copyable prompts and guards for CJK/RTL, transliteration, and code-mixed text
- How to measure and prove stability with ΔS and λ_observe

## When to use
- Corpus is non-English or mixed (EN + ZH/JP/KR/AR/Hebrew)
- Same question works in English but fails in the target language
- High vector similarity yet wrong meaning after translation
- OCR text “looks correct” but citations drift or split tokens oddly
- Names/terms oscillate between Latin and native script

## Open these first
- End-to-end language guide: [Multilingual Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multilingual-guide.md)
- Embedding ≠ true meaning symptoms: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- OCR quality & normalizations: [OCR / Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
- Chunk boundaries & sectioning: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
- Snippet/citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Why-this-snippet trace: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Common failure patterns (quick diagnosis)
- **Tokenizer split**: CJK runs without spaces; BM25/analyzers mismatch; ΔS flat-high vs k → index/analyzer misaligned.
- **Unicode ghosts**: full-width vs half-width, NFD vs NFC, zero-width joiners; citations miss by a few characters.
- **Translation shadow**: English paraphrase passes, native-lang fails → cross-lingual embeddings or analyzer drift.
- **Script flip**: terms appear both transliterated and native; recall differs by script.
- **OCR noise**: identical glyphs (l/1/I, O/0), mixed directionality (RTL punctuation).

---

## Fix in 60 seconds
1) **Normalize text at ingest**
   - Apply Unicode **NFC**, trim zero-width, unify full/half-width.
   - Lowercase where appropriate; preserve casing for code and proper nouns.

2) **Choose analyzers per language**
   - CJK: use language-aware tokenizers (jieba, kuromoji, mecab) or character-ngrams.
   - RTL: ensure analyzer respects directionality; avoid stripping diacritics unless required.

3) **Dual-path embeddings**
   - Index in native language **and** in English via *machine translation shadow* for recall robustness.
   - Store `lang`, `script`, and `translit` flags per chunk in metadata.

4) **Anchor the schema**
   - Enforce snippet headers `{section_id, lang, script}`; forbid cross-section reuse.
   - Require **cite-then-answer**; block free-form merges across languages.

5) **Probe ΔS & λ by language**
   - Measure ΔS(question, retrieved) per language; aim ≤ 0.45.
   - If ΔS flat-high across k, rebuild with correct analyzer/metric.

6) **Name/term fences**
   - Maintain a term map `{native ↔ translit ↔ English}`; pin consistent variants in the prompt preamble.

---

## Copy-paste prompt
```

You have TXT OS and the WFGY Problem Map.

Task: stabilize multilingual retrieval and reasoning.

Follow this immutable protocol:

1. Detect language/script of the question. Print {lang, script}.
2. Retrieve with a dual-path strategy:

   * native-lang retriever
   * english-shadow retriever (machine-translated question)
3. Build a Snippet Table with columns:
   {section\_id | lang | script | translit\_variant? | citation}
4. Bridge Check (BBCR):

   * restate the claim in ONE line
   * list supporting snippet\_ids
   * list conflicts or missing evidence; if missing, STOP and ask for the exact snippet
5. Final Answer:

   * answer in the user's language
   * inline-cite each claim
   * keep terminology consistent with the Term Map

Rules:

* Normalize Unicode (NFC), strip zero-width chars, unify full/half-width before retrieval.
* If ΔS(question, retrieved) > 0.60 in native but ≤ 0.45 in english-shadow, report "translation shadow" and keep both citations.
* Do not merge sources across languages without explicit citation per claim.

Input

* question (user language): "<paste>"
* term\_map: {native ↔ translit ↔ english}
* snippets (with ids, language, script): <paste>

Output

* {lang, script}
* Snippet Table
* Bridge Check
* Final Answer (with inline citations)
* ΔS(native), ΔS(english-shadow), λ\_observe states

```

---

## Minimal checklist
- Unicode normalized; zero-width and width variants removed
- Language-aware analyzers or char-ngrams applied at index & query
- Dual-path embeddings or bilingual index available
- Snippet Table includes `{lang, script, translit?}`
- Cite-then-answer schema enforced; no cross-language merges without citations
- ΔS per-language measured; flat-high ΔS triggers index/metric audit

## Acceptance targets
- ΔS(question, retrieved) ≤ **0.45** in the user’s language
- λ remains **convergent** across paraphrases in both native and english-shadow paths
- Coverage ≥ **0.70** token overlap to the target section in native language
- Consistent terminology across scripts per Term Map; no orphan claims without citations

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

