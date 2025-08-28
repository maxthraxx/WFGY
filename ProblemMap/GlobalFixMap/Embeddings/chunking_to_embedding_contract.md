# Chunking → Embedding Contract

A hard interface that keeps your chunker and your embedding encoder in semantic lockstep. Use this page when the chunks look fine but retrieval quality wobbles, or when “high-similarity yet wrong meaning” shows up after an index rebuild.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Snippet schema details: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Chunking checklist: [Semantic Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* OCR quality gate: [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
* Hallucination repair: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
* Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Vector store health: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
* Query splits and ordering: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

## What this page fixes

* Chunks pass manual inspection while top-k is semantically off.
* Index rebuild changes results even with identical data.
* Non-English corpora degrade after “helpful” normalization.
* OCR sources drift due to hyphenation, headers, or artifacts.

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat on long windows

---

## Minimal contract schema

The producer (chunker) must write these fields. The consumer (embedder) must read and honor them. Store the object as JSON alongside the vector.

```json
{
  "chunk_id": "str, stable and unique",
  "parent_id": "str, stable id of page/section/file",
  "source_id": "str, canonical source key",
  "section_id": "str, logical section anchor if available",
  "text": "str, exactly what will be embedded",
  "offsets": { "start": 1234, "end": 1678 }, 
  "page_no": 12,
  "lang": "ISO 639-1 or -3 code, e.g. 'en', 'zh', 'de'",
  "chunk_method": "fixed|sentence|semantic|hybrid",
  "window": { "max_tokens": 512, "stride": 384, "overlap": 128 },
  "tokenizer": {
    "name": "cl100k_base|llama3|... exact label",
    "version": "semver or commit",
    "case": "preserve|lower",
    "unicode_norm": "none|NFC|NFKC",
    "strip_punct": false,
    "keep_newlines": true
  },
  "embedder": {
    "model": "exact model id",
    "revision": "weights or date tag",
    "pooling": "cls|mean|last|custom",
    "normalize_l2": true
  },
  "metadata": {
    "source_url": "optional canonical link",
    "title": "optional",
    "breadcrumbs": ["chapter", "section"]
  },
  "hashes": {
    "text_sha256": "sha256 of text pre-embedding",
    "contract_sha256": "sha256 of the whole object minus hashes"
  }
}
```

**Contract rule**
Whatever is in `text` is exactly what gets embedded. If any pre-processing differs between producer and consumer, you must rewrite `text` and refresh `text_sha256`.

---

## Producer rules (chunker)

1. Decide the unit first. Page, section, or sentence window. Do not mix units within the same index.
2. Emit `text` after final normalization. Never rely on the embedder to repeat normalization.
3. Preserve citations and code blocks if users will query by them. Remove navigation boilerplate.
4. For OCR, fix soft hyphens, line wraps, and column order before writing `text`.
5. Keep overlap explicit in `window`. Future rebuilds must not change it silently.
6. Record tokenizer identity and casing policy.
7. Compute `text_sha256` and a contract hash.
8. Assign stable `chunk_id` and `parent_id`.
9. Add `lang`. Use a detector only once during ingestion, then persist.
10. Store page and section anchors for traceability and UI jumps.

## Consumer rules (embedder)

1. Embed exactly `text`. No extra cleanup.
2. Use the `embedder.model` and `tokenizer` from the contract. If you change either, rebuild vectors.
3. Respect `normalize_l2`. Keep pooling the same across the whole index.
4. Refuse to embed when the contract hash or tokenizer name changed.
5. Refuse to embed beyond `window.max_tokens`. Truncate by tokenizer, not by characters.
6. Keep the vector dimensionality constant within a store. New dimension means new collection.
7. Persist a copy of the full contract next to the vector row for audits.

---

## Validation checklist before indexing

* Re-tokenize `text`, verify `token_count ≤ window.max_tokens`.
* Recompute `text_sha256` and compare. If mismatch, halt.
* Run ΔS(original\_page, reconstructed\_snippet) on a small gold set. Expect ≤ 0.45.
* Sample fifteen multilingual chunks. Verify casing and unicode flags match contract.
* Check near-duplicate collapse by `text_sha256` and by cosine on the vectors.
* Probe λ across three paraphrases and two seeds. No flip states after reranking.

---

## Common failure smells → exact fix

* Wrong-meaning hits with high similarity.
  → [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and confirm contract tokenizer aligns with the model.

* Rebuild changes results although data did not change.
  → Verify `tokenizer.version`, `embedder.revision`, and `window` are identical; if not, re-embed and re-index. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

* Non-English drift after “helpful” lowercasing or punctuation stripping.
  → Switch `tokenizer.case=preserve`, `unicode_norm=NFC`. Re-embed the affected language slice. See [Semantic Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md).

* OCR sources hallucinate cross-columns or broken words.
  → Repair with the OCR gate first, then rebuild. See [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md).

* High recall yet unstable top-k order.
  → Pin query parsing, then add a reranker. See [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

* Index feels “holey” near boundaries.
  → Increase overlap or switch to a sentence or semantic window, then verify coverage. See [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md).

---

## Minimal migration plan when the contract changes

1. Freeze writes.
2. Export the current contract set.
3. Compute diff of `tokenizer`, `embedder`, and `window`.
4. Re-embed in a new collection.
5. Dual-read and A/B for one week of traffic.
6. Cut over when ΔS and coverage targets pass on the live eval set.
7. Garbage collect the old collection.

---

## Copy-paste test harness

```python
# Pseudocode for CI
for chunk in sample_chunks:
    tok = load_tokenizer(chunk["tokenizer"]["name"], chunk["tokenizer"]["version"])
    ids = tok.encode(chunk["text"])
    assert len(ids) <= chunk["window"]["max_tokens"]
    assert sha256(chunk["text"]) == chunk["hashes"]["text_sha256"]

    vec = embed(chunk["text"], model=chunk["embedder"]["model"], rev=chunk["embedder"]["revision"])
    if chunk["embedder"]["normalize_l2"]:
        vec = l2norm(vec)
    assert len(vec) == expected_dim  # fixed per model
```

---

## Verify after the fix

* Retrieve on a ten-question gold set.
* Expect coverage ≥ 0.70 and ΔS ≤ 0.45.
* λ does not flip across two seeds.
* Repeat after seven days to ensure stability drift did not reappear.

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
