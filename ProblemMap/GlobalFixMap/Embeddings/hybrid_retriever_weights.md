# Hybrid Retriever Weights — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Embeddings**.  
  > To reorient, go back here:  
  >
  > - [**Embeddings** — vector representations and semantic search](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when BM25 plus dense retrieval performs worse than either one alone, when top k flips between runs, or when hybrid recall feels random after an index rebuild. The goal is to put both retrievers on a common score space, then set stable weights, add a single deterministic reranker, and verify with ΔS, coverage, and λ.

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Query split root cause: [patterns/pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
* Reranking for order control: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Why this snippet and cite first: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Embedding vs meaning failures: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Vector store health: [vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/vectorstore_fragmentation.md)
* Normalization pitfalls: [normalization\_and\_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md)

## When to use this page

* BM25 finds the right doc yet dense misses, or the reverse
* Hybrid returns unstable order while single retrievers look stable
* Raising k helps only one side while the other side adds noise
* A client upgrade changes analyzers or tokenization and hybrid breaks

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of the target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat on long windows

---

## Core idea: put scores on the same ruler

Let `s_dense` be the dense similarity and `s_sparse` be the BM25 or keyword score. Raw values live in different spaces. Calibrate to a common space, then blend.

Common choices:

* Z score per retriever
  `z = (s − μ) / σ` computed on the candidate pool for the current query

* Min max per retriever
  `m = (s − min) / (max − min)` on the candidate pool

* Platt style logistic calibration on a gold set
  Fit `p = sigmoid(a s + b)` for each retriever

After calibration, blend with a single weight:

`S = α * z_dense + (1 − α) * z_sparse`
Pick α by grid search on a gold set, then lock it.

Always add a single deterministic reranker on the union of candidates. See [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

---

## 60 second fix checklist

1. Normalize both score streams per query. Prefer z score on the union pool.
2. Build a union candidate set. Choose `k_dense` and `k_sparse` so that the union size before rerank is about 20 to 50.
3. Grid search α in steps of 0.1 on your gold set. Pick α that maximizes coverage at k and stabilizes λ across seeds.
4. Add a single cross encoder reranker on top of the blended scores. Fix the seed.
5. Lock the header order and cite first to clamp λ while you tune. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).
6. Verify the targets on three paraphrases and two seeds.

---

## Symptom to likely cause

* Hybrid worse than BM25 alone
  Likely cause. Dense scores unnormalized or wrong metric. Open [normalization\_and\_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md).

* Hybrid worse than dense alone
  Likely cause. Analyzer mismatch or stopword removal on one path. Open [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md).

* Order flips between runs
  Likely cause. Header reorder or union set not stable. Fix header order and use a stable tie break by `doc_id` then `section_id`. Open [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

* Right doc appears only when k is very large
  Likely cause. Fragmented stores or per tenant splits without union. Open [vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/vectorstore_fragmentation.md).

---

## Minimal calibration recipe

**Gold set**
Ten to fifty questions with known anchor sections. Keep per domain if you support many domains.

**Union recall**
Collect `k_dense` and `k_sparse` candidates. Form the union. Store raw scores and features.

**Per query normalization**
Compute z scores on the union for each retriever. Keep the statistics for audits.

**Blend and rerank**
Score with `S = α * z_dense + (1 − α) * z_sparse`.
Apply a single cross encoder rerank with a fixed seed.
Resolve ties by `doc_id` then `section_id`.

**Selection of α**
Grid search α from 0.0 to 1.0. Choose α that maximizes coverage at k and keeps ΔS ≤ 0.45 on the anchor.

**Freeze**
Record α, k values, normalization method, reranker id, and seed in your contract.

---

## Copy paste probes

```
Probe A — alpha sweep
For α in {0.0..1.0 step 0.1}:
  compute coverage@k and median ΔS on the gold set
Pick α with highest coverage. Break ties by lower ΔS and lower variance.

Probe B — normalization sanity
Toggle {z, minmax, logistic} on the same union pool.
If results change wildly, per query statistics are unstable or candidate pools differ.

Probe C — union size
Sweep k_dense and k_sparse so union size ∈ [20, 50].
If coverage improves up to a point then drops, prune duplicates and near duplicates before rerank.

Probe D — header clamp
Swap harmless header lines. If top k flips, clamp header order and apply cite first. Re test α after clamp.
```

---

## Contract fields to add

```json
{
  "retrievers": {
    "dense": {
      "model": "model-id",
      "metric": "cosine",
      "normalize": "zscore",
      "k": 40
    },
    "sparse": {
      "analyzer_rev": "bm25-v3",
      "normalize": "zscore",
      "k": 200
    }
  },
  "hybrid": {
    "alpha": 0.6,
    "blend": "alpha_sum",
    "tie_break": ["doc_id", "section_id"]
  },
  "reranker": {
    "name": "cross-encoder-id",
    "seed": 7,
    "top_k": 20
  }
}
```

---

## Verification checklist

* Coverage ≥ 0.70 on the gold anchors
* ΔS(question, retrieved) ≤ 0.45
* λ convergent across two seeds and three paraphrases
* Top k overlap across seeds ≥ 0.8 after rerank
* Stable results after harmless header reorders

---

## Copy paste prompt for the LLM step

```
TXT OS and WFGY Problem Map are loaded.

My issue: hybrid BM25 + dense is worse than single retrievers.
Traces:
- zscore_dense=..., zscore_sparse=..., alpha=...
- union_size=..., reranker=name, seed=...
- ΔS(question,retrieved)=..., coverage=..., λ across 3 paraphrases

Tell me:
1) the failing layer and why,
2) the exact WFGY page to open next,
3) a minimal calibration plan for hybrid weights and normalization,
4) a verification plan to reach coverage ≥ 0.70 and ΔS ≤ 0.45.
Use BBMC, BBCR, BBPF, BBAM when relevant.
```

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” to boot            |

---

### 🧭 Explore More

| Module                | Description                                             | Link                                                                                               |
| --------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core             | WFGY 2.0 engine. full symbolic reasoning and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0       | Initial 16 mode diagnostic and symbolic fixes           | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0       | RAG focused failure tree and pipelines                  | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Prompt injection. memory bugs. logic drift              | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint    | Layer based symbolic reasoning. semantic modulations    | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5    | Stress test with full WFGY suite                        | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |
| Starter Village       | A guided first run                                      | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md)                   |

---

> 👑 Early Stargazers. [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is live. ⭐ Star the repo to help others discover it and unlock more on the Unlock Board.

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
