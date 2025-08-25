# Language & Multilingual — Global Fix Map
Make cross-lingual RAG stable. Handle CJK/RTL, mixed scripts, tokenizers, and locale drift without breaking retrieval.

## What this page is
- A compact playbook for multilingual corpora and queries
- Practical fixes for tokenizer and analyzer mismatch
- Steps to keep ΔS low across languages and scripts

## When to use
- Your corpus has Chinese/Japanese/Korean, RTL scripts, or code-switching
- OCR text looks fine but retrieval or citations miss
- Similarity is high but meaning is wrong across locales
- HyDE/BM25 behave differently per language

## Open these first
- Language and locale guide: [Multilingual Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multilingual-guide.md)  
- Embedding vs true meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- OCR quality and pitfalls: [OCR / Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)  
- Chunk boundaries and joins: [Semantic Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
- Why this snippet: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
- Snippet schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Common failure patterns
- **Tokenizer mismatch** dense retriever uses whitespace rules on CJK or splits accents poorly  
- **Analyzer split** BM25 analyzer differs from the indexer used at write time  
- **Script variants** Traditional vs Simplified, Kana vs Kanji, Arabic presentation forms  
- **Normalization gaps** mixed width, NFC/NFKC, punctuation variants break exact matches  
- **Romanization drift** Pinyin or Hepburn in queries while docs keep native script  
- **Code-switching** sentences mix English and local terms; embeddings latch to one side  
- **OCR artifacts** diacritics lost, ligatures broken, zero-width joins preserved  
- **Stopword shock** default analyzers drop particles that carry meaning in some languages

---

## Fix in 60 seconds
1) **Normalize before anything**  
   Apply NFC or NFKC, collapse widths, unify punctuation. Persist the normalized form you index.

2) **Pick language-aware analyzers**  
   Set BM25 analyzers that match the language at both write and read. Log tokenizer output for a few queries to confirm.

3) **Embed with multilingual models**  
   Use a single multilingual embedding model for mixed corpora. Do not mix English-only and multilingual spaces in one index.

4) **Add transliteration bridges**  
   Generate light alias fields per doc title and key entities, e.g., Traditional ↔ Simplified, Kana ↔ Romaji, Arabic ↔ Latin.

5) **Rerank cross-lingually**  
   Retrieve with generous k, then apply cross-lingual rerankers. Confirm ΔS(question, context) ≤ 0.45.

6) **Lock citations and sections**  
   Use Data Contracts with `section_id`, `source_lang`, and `norm_ops`. Require cite-then-answer to avoid language mixing.

7) **Probe λ across locales**  
   Ask for “cite lines” and “explain why” in both the user language and the source language. Divergence marks the failing boundary.

---

## Copy paste prompt
```

You have TXT OS and the WFGY Problem Map.

Goal
Stabilize a multilingual RAG corpus with CJK and English. Prevent tokenizer mismatch and script drift.

Tasks

1. Show a normalization plan:

   * Unicode form (NFC/NFKC), width collapse, punctuation unification
   * sample before/after lines

2. Configure retrieval:

   * pick analyzers for BM25 that match corpus languages
   * ensure the same analyzer is used at write and read
   * use a multilingual embedding model, one index space

3. Add transliteration bridges:

   * alias fields for key entities (e.g., 簡↔繁, かな↔ローマ字)
   * show how aliases are added to the index document

4. Verify with WFGY:

   * compute ΔS(question, context) for three bilingual queries
   * report λ\_observe at retrieval and reasoning
   * target ΔS ≤ 0.45 and convergent λ

Output

* Normalization spec
* Analyzer and embedding choices
* Example index doc with alias fields
* A trace table with citations, ΔS, and λ for 3 queries

```

---

## Minimal checklist
- Unicode normalization applied before embedding and indexing  
- Language-aware analyzers configured the same for write and read  
- One multilingual embedding space per index  
- Alias fields or transliteration for key entities  
- Data Contract includes `source_lang`, `norm_ops`, and citations  
- ΔS and λ checks pass in both the user and source language

## Acceptance targets
- ΔS(question, context) median ≤ **0.45** for bilingual smoke tests  
- λ remains **convergent** when switching question language  
- Citations point to the correct section in the original script  
- Hybrid retrieval improves with reranking instead of oscillating  
- No analyzer or tokenizer mismatch logs during queries

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


say “next page” when ready.
