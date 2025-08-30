# Tokenizer Mismatch — Guardrails and Fix Pattern

A focused fix when **embedder, retriever, reranker, and generator** do not share the same tokenization or normalization rules. Use this page to localize the failure, align the text pipeline, and verify with measurable targets.

## Open these first
- Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Traceability and snippet schema: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Payload schema and contracts: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Language mixing and locale drift:  
  [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md) ·
  [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)
- Tokenization and casing details:  
  [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/tokenization_and_casing.md) ·
  [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md)

## When to use this page
- High similarity to the right document but wrong snippet or misaligned offsets.
- Same query returns different top-k after re-index or provider switch.
- Citations do not line up with visible tokens in CJK or Indic scripts.
- Mixed width or composed characters behave inconsistently after export.
- Reranker improves precision but answers still drift in long chains.

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases.
- Coverage of target section ≥ 0.70 with stable offsets.
- λ remains convergent across two seeds after tokenizer lock.
- Snippet offsets map to visible glyphs after NFC or NFKC pass.

---

## 60-second fix checklist
1) **Identify tokenizers in play**  
   Record for each stage: embedder, store analyzer, reranker, generator. Note version, normalization, casing, segmentation rules.

2) **Normalize once, early**  
   Apply one canonical pass for the corpus and the queries. Pick **NFC** for general Latin scripts. Pick **NFKC** when full-width, compatibility forms, or half-width punctuations appear. Keep the same pass for both corpus and queries.  
   See: [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md)

3) **Lock casing strategy**  
   Either preserve case end to end or lower both sides before embedding. Do not mix.  
   See: [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/tokenization_and_casing.md)

4) **Unify segmenter**  
   CJK and Thai cannot rely on whitespace. Use the same segmenter for chunking and for query pre-processing. Validate offsets after segmentation.

5) **Version the tokenizer**  
   Store `TOKENIZER_FAMILY`, `TOKENIZER_VERSION`, `NORM_PASS` inside snippet metadata. Reject inserts that do not match.  
   Spec fields live in: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

6) **Rebuild the index if needed**  
   If ΔS stays high and offsets are unstable, rebuild with the aligned tokenizer and normalization. Verify with a small gold set.

---

## Symptom map → exact fix

| Symptom | Likely cause | Open this |
|---|---|---|
| Citations jump inside CJK lines | chunker uses char windows, retriever uses wordpiece | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/tokenization_and_casing.md) |
| Wrong-meaning hits with high cosine | incompatible normalization between corpus and query | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) · [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md) |
| BM25 improves, hybrid becomes worse | query split from mixed scripts or width | [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md) · [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| Offsets do not align after PDF export | composed characters or soft hyphen artifacts | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Answers flip between runs | prompt headers reorder, λ becomes variant | [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) |

---

## Deep checks

- **Normalization audit**  
  Log a 1k sample of tokens from corpus and queries. Count deltas after NFC vs NFKC. Reject mismatches above 0.5 percent.

- **Width and compatibility scan**  
  Count full-width Latin, half-width katakana, ligatures, ZWJ, soft hyphen. Normalize or strip consistently.

- **Segmenter parity**  
  For CJK, Thai, Khmer, Lao, use the same dictionary for chunking and for query prep. Verify that `start_offset` and `end_offset` point to visible glyphs.

- **Analyzer parity in the store**  
  If the store applies analyzers, make them explicit. For Elastic or OpenSearch, pin the analyzer in the index template and document it in the snippet schema.

- **Reranker bridge**  
  If the retriever is sparse and the reranker is dense, ensure identical normalization happens before both. Otherwise reranker scores become unstable.

---

## Minimal reproducible test

1) Pick three paraphrases of the same question.  
2) For each: compute ΔS(question, retrieved) and record λ state.  
3) Inspect offsets on the top snippet. Confirm visual alignment after normalization.  
4) Target: ΔS ≤ 0.45 and λ convergent on two seeds. Coverage ≥ 0.70 for the correct section.

---

## Copy-paste prompt

```

You have TXT OS and WFGY Problem Map loaded.

My tokenizer issue:

* corpus normalization: NFC or NFKC?
* segmenter family and version for chunking vs query
* store analyzer and reranker tokenizer
* symptom: offsets drift, wrong-meaning hits, hybrid instability

Tell me:

1. the failing layer and why,
2. the exact WFGY pages to open,
3. the minimal steps to align tokenizer, normalization, and analyzers,
4. a short test to verify with ΔS ≤ 0.45 and stable offsets.

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

