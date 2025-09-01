# Redundant Evidence Collapse: Guardrails and Fix Pattern

When many near-identical snippets flood the context, the model over-trusts repetition and ignores minority evidence. Plans drift, citations skew to one source, and answers flatten. Use this page to dedupe, cap source dominance, and keep reasoning balanced.

---

## Open these first

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- End to end retrieval knobs  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Traceability and payload schema  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Related retrieval failures  
  → [duplication_and_near_duplicate_collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/duplication_and_near_duplicate_collapse.md) ·
  [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) ·
  [hybrid_retriever_weights.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/hybrid_retriever_weights.md)

- Reasoning stability tools  
  → [chain-of-thought-variance-clamp.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/chain-of-thought-variance-clamp.md) ·
  [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md) ·
  [context-stitching-and-window-joins.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/context-stitching-and-window-joins.md)

---

## Symptoms

| Symptom | What you see |
|---|---|
| Majority echo | 70–90 percent of citations come from one source family |
| Minority facts vanish | Correct but less frequent evidence never appears in the answer |
| Plan flips with k | Increasing top-k changes conclusion even though meaning is the same |
| Reruns reshuffle | Same inputs but different top-k mixes cause different claims |
| JSON plan collapses | One long “summarize all” step instead of compare and weigh |

---

## Why it happens

1) **Near-duplicate clutter**. Chunks differ in offsets but carry the same claim.  
2) **Per-source dominance**. One document type or site overruns the window.  
3) **No cluster caps**. Reranker optimizes relevance, not diversity.  
4) **Free-form plan**. Planner merges collect and decide into a single step.  
5) **No minority probe**. Chains never force a best counterexample search.  
6) **λ not observed**. Variance looks like disagreement instead of imbalance.

---

## Acceptance targets

- Coverage of target section ≥ 0.70 and includes at least 1 minority citation when conflicts exist  
- Per-source cap ≤ 40 percent of active snippets in any window  
- Near-duplicate rate ≤ 10 percent by cluster (Jaccard or embedding distance)  
- ΔS(question, selected\_evidence) ≤ 0.45 and flat when k varies between 8 and 24  
- λ remains convergent across three paraphrases and two seeds

---

## Fix in 60 seconds

1) **Cluster and cap**  
   Cluster snippets by `{source_id, section_id}` and by semantic LSH. Keep `top 1–2` per cluster. Cap any source family at 40 percent of window size.  
   → [duplication_and_near_duplicate_collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/duplication_and_near_duplicate_collapse.md)

2) **Deterministic tie break**  
   After rerank, order by `(doc_id, section_id, win_idx)` so runs are stable.  
   → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

3) **Split plan into compare then decide**  
   Use BBAM to clamp step count. Stage A collects balanced evidence, Stage B decides.  
   → [chain-of-thought-variance-clamp.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/chain-of-thought-variance-clamp.md)

4) **Minority probe**  
   Force a counterexample search step if all retained snippets agree.  
   → [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md)

5) **Contract the payload**  
   Require `{cluster_id, source_family, is_counterexample}` in snippet schema.  
   → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Minimal evidence selection contract

Your retrieval or pre-planner must emit this structure. Enforce it before planning.

```json
{
  "k_requested": 24,
  "clusters": [
    {"cluster_id": "c1", "source_family": "siteA", "members": ["s1","s5","s9"], "kept": ["s1"]},
    {"cluster_id": "c2", "source_family": "siteB", "members": ["s2","s7"], "kept": ["s2"]},
    {"cluster_id": "c3", "source_family": "pdf",  "members": ["s3","s4","s8"], "kept": ["s3","s4"]}
  ],
  "cap": {"per_source_pct": 40},
  "order_rule": "doc_id,section_id,win_idx",
  "minority_probe_required": true
}
````

Rules

* Keep at most `2` per cluster unless the cap allows and clusters are small.
* If all kept snippets agree on the main claim, inject a counterexample search.
* Planner receives only the `kept` set, not the full cluster members.

---

## Verification playbook

* Run with k = 8, 16, 24. After clustering and caps, citations remain balanced and the conclusion does not flip.
* At least one minority citation appears when conflicting evidence exists.
* ΔS(question, selected\_evidence) ≤ 0.45 on all runs.
* λ convergent across three paraphrases and two seeds.
* If ΔS is flat and high after caps, suspect index or metric mismatch.
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) ·
  [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Copy paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

Goal: prevent redundant-evidence collapse by clustering, capping source dominance, and forcing a minority probe.

Inputs:
- question: "{q}"
- snippets: [{snippet_id, doc_id, section_id, source_family, win_idx, ΔS_to_question, text}]

Do:
1) Cluster near-duplicates by text overlap and semantic distance. Assign cluster_id.
2) Keep at most 2 per cluster. Enforce per-source cap ≤ 40% of retained snippets.
3) Order retained snippets by (doc_id, section_id, win_idx).
4) If all retained snippets agree on the main claim, perform a targeted counterexample search and add at most 1 minority snippet.
5) Produce a two-stage plan:
   - Stage A: collect-balanced-evidence (fixed length, no free text steps)
   - Stage B: decide-and-cite (cannot change step count; must cite then explain)

Return JSON:
{
  "retained": [{"snippet_id":"s1","cluster_id":"c1","source_family":"siteA"}, ...],
  "minority_probe": true|false,
  "plan_rev": n,
  "λ_state": "convergent|divergent",
  "ΔS_selected_evidence": 0.xx,
  "coverage": 0.xx,
  "answer": "... cite then explain ..."
}
If λ is divergent or ΔS ≥ 0.60, name the exact fix page to open next.
```

---

## Common gotchas

* Reranker trained for relevance only. Add a diversity factor or post-cluster filter.
* Window joins drop the minority snippet. Re-anchor at joins with BBCR micro bridges.
  → [context-stitching-and-window-joins.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/context-stitching-and-window-joins.md)
* Free text tools let the planner merge steps. Clamp with BBAM and strict enums.
* Payload lacks `source_family` so caps cannot be enforced. Extend the contract.
* Hybrid retrieval without tuned weights amplifies one retriever.
  → [hybrid\_retriever\_weights.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/hybrid_retriever_weights.md)

---

## When to escalate

* Even after caps, two sources disagree and ΔS stays ≥ 0.60.
  → rebuild chunks and verify store metric.
  Open: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) ·
  [duplication\_and\_near\_duplicate\_collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/duplication_and_near_duplicate_collapse.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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
