# Retrieval Evaluation Recipes

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Retrieval**.  
  > To reorient, go back here:  
  >
  > - [**Retrieval** — information access and knowledge lookup](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A practical kit to score retrieval quality with small but reliable datasets. Use these recipes to detect metric mismatch, ordering variance, hybrid regressions, and chunk misalignment before they leak into answers.

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage to the intended section ≥ 0.70  
- λ remains convergent across 3 paraphrases and 2 seeds  
- Citation precision ≥ 0.85 and recall ≥ 0.75 on the gold set

References:  
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Build a small but hard gold set

Create 40 to 120 items. Each item has:

- **question** and **three paraphrases**  
- **target\_section** and **one decoy\_section**  
- **anchor\_snippet** that represents the minimal evidence  
- **answers\_not\_allowed** for near misses  
- **expected\_citations** as `{snippet_id, offsets}` list

Chunking guidance:  
[Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

Data schema example:

```json
{
  "qid": "Q037",
  "question": "How do I rotate API keys safely?",
  "paraphrases": [
    "Best practice for API key rotation?",
    "Rotate credentials without downtime, how?",
    "Safe credential rotation steps?"
  ],
  "target_section": "security/keys/rotation",
  "decoy_section": "security/keys/storage",
  "anchor_snippet": "Rotate old->new with overlap window and staged revocation...",
  "expected_citations": [
    {"snippet_id": "S-114", "offsets": [320, 480]}
  ],
  "answers_not_allowed": [
    "store keys in env only", "rotate monthly without overlap"
  ]
}
````

---

## Core metrics and how to compute them

* **ΔS(question, retrieved)** and **ΔS(retrieved, anchor)**
  Normalized semantic distance in \[0,1]. Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.
  See: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* **Coverage**
  Tokens from cited spans that overlap the ground anchor divided by tokens in the anchor.

* **Citation precision and recall**
  Precision = correct cited spans over all cited spans.
  Recall = correct cited spans over all ground spans.

* **λ\_convergence**
  Observe λ states across paraphrases and seeds. Divergence flags prompt variance or ordering drift.
  See: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

---

## Recipe 1: Single store baseline

Goal: verify metric and index health before any hybrid tricks.

Steps

1. Fix one embedding family and one metric.
2. Run k in {5, 10, 20}.
3. Log ΔS, coverage, precision, recall, λ for each run.
4. If ΔS stays high and flat while coverage is low, suspect metric or index mismatch.

Open next:
[Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Recipe 2: Reranker impact

Goal: separate recall from ordering stability.

Steps

1. Freeze retriever and analyzer.
2. Add a deterministic reranker and compare top-k order.
3. Measure flip rate of citations and λ under two seeds.

Open next:
[Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## Recipe 3: Hybrid vs single

Goal: prove hybrid helps or remove it.

Steps

1. Evaluate sparse only, dense only, and hybrid.
2. Compare ΔS and coverage per item.
3. If hybrid is worse, split query parsing and rebalance weights.

Open next:
[pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

---

## Recipe 4: Chunk alignment test

Goal: ensure anchors match boundaries.

Steps

1. For each gold item, compute ΔS to the anchor and to the decoy.
2. If both are close, re-chunk with anchor alignment and rebuild.

Open next:
[Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) ·
[chunk\_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)

---

## Recipe 5: Fragmentation probe

Goal: detect namespace skew and partial ingestion.

Steps

1. Run the same question across two namespaces or stores that should be equivalent.
2. Compare recall of the anchor snippet.
3. If recall is high only in one place, fix ingestion and dedupe.

Open next:
[pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Minimal harness you can adapt

```python
# Pseudocode only
def eval_item(store, reranker, item, k, seed):
    q = item["question"]
    ctx = store.retrieve(q, k=k, seed=seed)
    ordered = reranker.rank(q, ctx) if reranker else ctx
    cites = extract_citations(ordered)
    d_qr = deltaS(q, join_text(ordered))
    d_ra = deltaS(join_text(ordered), item["anchor_snippet"])
    cov, prec, rec = score_citations(cites, item["expected_citations"], item["anchor_snippet"])
    lam = observe_lambda(q, ordered, seed=seed)
    return {
        "qid": item["qid"], "k": k, "seed": seed,
        "ΔS_qr": d_qr, "ΔS_ra": d_ra, "coverage": cov,
        "precision": prec, "recall": rec, "λ_state": lam
    }

def run_suite(items, stores, rerankers, ks, seeds):
    results = []
    for it in items:
        for s in stores:
            for r in rerankers:
                for k in ks:
                    for seed in seeds:
                        results.append(eval_item(s, r, it, k, seed))
    return results
```

Log schema

```json
{
  "qid": "Q037",
  "system": "dense_only",
  "reranker": "none",
  "k": 10,
  "seed": 23,
  "ΔS_qr": 0.38,
  "ΔS_ra": 0.22,
  "coverage": 0.78,
  "precision": 0.92,
  "recall": 0.81,
  "λ_state": "convergent",
  "retrieval_order": ["S-114","S-012","S-077"],
  "analyzer": "lowercase",
  "metric": "cosine",
  "prompt_hash": "P-9c1f",
  "index_hash": "I-fc21"
}
```

Traceability contracts for fields:
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Regression gate before shipping

* ΔS ≤ 0.45 and coverage ≥ 0.70 on three paraphrases per item
* Citation precision ≥ 0.85 and recall ≥ 0.75
* λ convergent on two seeds
* No unresolved items with high ΔS and low coverage

Evaluation math and templates:
[eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Common failure patterns and where to fix them

* High similarity yet wrong meaning
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Snippet selected does not match citation
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* Hybrid worse than single retriever
  → [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* Coverage good offline but collapses online
  → [pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

* Eval flakiness after deploy
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) and [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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
