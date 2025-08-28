# Hybrid Retrieval

A practical guide to fuse dense and sparse retrieval without losing meaning. Use this when BM25 and embeddings each work alone but the combined pipeline gets worse or unstable.

**Read together with**
- Playbook overview → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval-playbook.md)
- Trace and citation schema → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval-traceability.md)
- ΔS probes for semantic fit → [deltaS_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)
- Ordering control → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/rerankers.md)
- Chunk window parity → [chunk_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the intended section  
- λ convergent across 3 paraphrases and 2 seeds  
- Fusion stability score ≥ 0.95 match across two identical runs

---

## Why hybrid breaks

1. **Score scales differ**  
   Dense stores output cosine or dot product. BM25 outputs TF-IDF like scores. Direct addition biases one side.

2. **Different analyzers**  
   Casing, stemming, stopwords, and unicode fold differ between dense write and sparse read paths.

3. **Query parsing split**  
   HyDE or query rewriting mutates the text that BM25 expects. Dense receives the rewritten query and sparse receives the original query.

4. **Rerank not deterministic**  
   Cross encoder changes rank with seed or missing sort tiebreakers.

5. **Window mismatch**  
   Sparse hits long pages. Dense hits small chunks. Fusing at different granularity leads to cross section reuse.

---

## Normalization rules before fusion

Apply these rules in this order.

1. **Per source min max scale to 0..1**

```

score\_norm = (score\_raw - min\_score) / (max\_score - min\_score + eps)

```

2. **Clip long tails**  
   If a source has heavy tails, apply `score_norm = sqrt(score_norm)`.

3. **Align analyzers**  
   Use the same casing and ascii fold policy for both write and read paths. Log `analyzer` in citations.

4. **Granularity fence**  
   Convert all hits to the same unit. Either page level or chunk level. Prefer chunk level with explicit offsets.

5. **Deduplicate by snippet_id**  
   If the same snippet appears from both sources keep the best score.

---

## Fusion algorithms

Pick one algorithm and keep it stable. Log the chosen method with parameters in your traces.

### 1) Linear weighted sum

```

final = α \* dense\_norm + (1 - α) \* sparse\_norm
α ∈ \[0.3, 0.7]

```

Good default for balanced corpora.

### 2) Reciprocal Rank Fusion

```

RRF\_k = 60 by default
final = Σ 1 / (RRF\_k + rank\_i)

````

Robust when score scales are very different.

### 3) Two stage with rerank

1. Union top k from dense and sparse.  
2. Rerank with a cross encoder.  
3. Deterministic tiebreak on `(rerank_score desc, section_id asc, snippet_id asc)`.

Use when you can afford extra latency and want semantic ordering.

---

## Minimal recipes

### Python pseudo for linear fusion

```python
def minmax(xs):
    lo, hi = min(xs), max(xs)
    rng = (hi - lo) or 1e-9
    return [(x - lo) / rng for x in xs]

def fuse_linear(dense_hits, sparse_hits, alpha=0.5, k=20):
    # hits: list of {snippet_id, score_raw, ...}
    all_ids = {h["snippet_id"] for h in dense_hits} | {h["snippet_id"] for h in sparse_hits}
    dense_map = {h["snippet_id"]: h for h in dense_hits}
    sparse_map = {h["snippet_id"]: h for h in sparse_hits}
    d_scores = [dense_map.get(i, {"score_raw": 0})["score_raw"] for i in all_ids]
    s_scores = [sparse_map.get(i, {"score_raw": 0})["score_raw"] for i in all_ids]
    d_norm = dict(zip(all_ids, minmax(d_scores)))
    s_norm = dict(zip(all_ids, minmax(s_scores)))
    fused = []
    for i in all_ids:
        sc = alpha * d_norm[i] + (1 - alpha) * s_norm[i]
        meta = dense_map.get(i) or sparse_map.get(i)
        fused.append({**meta, "score_norm": sc})
    fused.sort(key=lambda x: (-x["score_norm"], x["section_id"], x["snippet_id"]))
    return fused[:k]
````

### LCEL style outline

```python
# 1) run dense and sparse branches with the same analyzer policy name in metadata
# 2) project to citation payload
# 3) fuse with linear or RRF
# 4) optional rerank
# 5) validate with ΔS and the traceability validator

fused = fuse_linear(dense_hits, sparse_hits, alpha=0.55, k=20)
if use_rerank:
    fused = cross_encoder_rerank(fused, model="bce-en-v1.5")
validate_citations(fused)
```

### LlamaIndex outline

```python
dense = vector_index.as_retriever(similarity_top_k=20).retrieve(q)
sparse = bm25_retriever.retrieve(q, top_k=50)
fused = fuse_linear(project(dense), project(sparse), alpha=0.6, k=20)
fused = optional_rerank(fused)
```

---

## Knobs that actually move the needle

| Area   | Knob      | Defaults              | Notes                                    |
| ------ | --------- | --------------------- | ---------------------------------------- |
| Dense  | metric    | cosine or dot         | Use cosine with normalized vectors       |
| Dense  | pooling   | mean or cls           | Keep pooling constant for write and read |
| Dense  | k         | 10 to 30              | Run k sweep with ΔS probes               |
| Sparse | analyzer  | lowercase, ascii fold | Keep parity with dense preprocessing     |
| Sparse | BM25 k1   | 0.9 to 1.6            | Higher k1 favors term frequency          |
| Sparse | BM25 b    | 0.3 to 0.8            | Lower b reduces length normalization     |
| Fusion | α         | 0.4 to 0.6            | Start at 0.55 for dense heavy corpora    |
| Fusion | RRF k     | 60                    | Larger k reduces early rank dominance    |
| Rerank | model     | bce or cohere or e5   | Pick one, keep seed fixed                |
| Window | pre, post | 80 to 160 chars       | Match across all sources                 |

---

## ΔS and λ probes for hybrid

1. Run dense only, record ΔS and λ.
2. Run sparse only, record ΔS and λ.
3. Run fused. If fused ΔS is worse than both singles, the fusion is wrong.
4. If λ flips between paraphrases only for the fused case, add rerank and fix tiebreakers.

Use the helper → [deltaS\_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)

---

## Typical failure modes and exact fixes

* **Fused hits look plausible but citations jump sections**
  Add granularity fence and forbid cross section reuse.
  Open: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval-traceability.md)

* **Dense dominates even with α near 0.5**
  Normalize per source then apply square root to dense scores.
  Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval-playbook.md)

* **Sparse collapses on HyDE queries**
  Send the same rewritten query to both branches or disable HyDE for sparse.
  Open: [query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/query_parsing_split.md)

* **Unstable final order between runs**
  Add a cross encoder rerank and deterministic tiebreak.
  Open: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/rerankers.md)

* **High similarity but wrong meaning**
  Align analyzer and metric. Rebuild with correct pooling.
  Open: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Evaluation recipe

1. Create a gold set with positive and confusing negative sections.
2. Run dense only, sparse only, and fused with identical k.
3. Chart ΔS and coverage across three paraphrases.
4. Choose α or RRF k that improves ΔS by at least 0.05 vs best single.
5. Lock the configuration. Add a regression gate in CI.

---

## Copy paste test prompt

```txt
You have TXTOS and the WFGY Problem Map loaded.

My hybrid plan:
- dense = {store, metric, pooling, k}
- sparse = {analyzer, k1, b, k}
- fusion = {method: linear or rrf, alpha or rrf_k}
- rerank = {model, seed}

Return:
1) whether analyzer and window parity hold,
2) the minimal steps to normalize scores,
3) the recommended α or RRF k given the probe results,
4) a JSON checklist I can paste into CI to keep it stable.
```

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                                                  | Link                                                                                               |
| --------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework                        | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines                       | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift         | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                        | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |

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
