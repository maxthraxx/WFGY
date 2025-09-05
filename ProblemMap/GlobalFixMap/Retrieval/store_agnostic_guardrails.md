# Store-Agnostic Guardrails for Retrieval

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


Use this page to harden retrieval quality without changing your vector store. The checks localize failure causes and route you to the exact structural fix so you can verify with measurable targets.

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance stays flat on long windows

---

## 15-minute triage checklist

1) **Lock metrics and analyzers**  
   One analyzer for write and read. Verify distance metric and normalization.  
   Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

2) **Enforce the snippet contract**  
   Required fields: `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Trace why this snippet**  
   Add cite-then-explain and store the trace.  
   Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

4) **Probe ΔS and λ**  
   Three paraphrases and two seeds. If ΔS ≥ 0.60 or λ flips, clamp variance.  
   Open: [deltaS_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)

5) **k sweep and rerankers**  
   k in {5, 10, 20}. Try a deterministic reranker when order matters.  
   Open: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) ·
   [hybrid_reranker_recipe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/hybrid_reranker_recipe.md)

6) **Check chunk boundaries and anchors**  
   If facts exist but never surface, realign chunking and anchors.  
   Open: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) ·
   [chunk_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)

7) **Detect fragmentation**  
   If coverage is low while index looks healthy, suspect store fragmentation.  
   Open: [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

8) **Hybrid failure**  
   If hybrid underperforms a single retriever, split parsing and rebalance.  
   Open: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

9) **Embedding vs meaning**  
   High similarity yet wrong answer means metric or family mismatch.  
   Open: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Minimal instrumentation you can paste

```python
# Pseudocode: keep these checkpoints store agnostic
def retrieve(q, k=10):
    # unified analyzer and explicit metric
    return retriever.invoke(q, k=k)

def trace_schema(snippet):
    assert {"snippet_id","section_id","source_url","offsets","tokens"} <= set(snippet.keys())

def observe(q, snippets, answer):
    # compute ΔS and λ, record probes
    log = probes.compute(q, snippets, answer)
    if log["ΔS"] >= 0.60 or log["λ_flip"]:
        raise Exception("High ΔS or λ flip. Apply variance clamp and rerankers.")
    return log

def pipeline(q):
    s = retrieve(q, k=10)
    for x in s: trace_schema(x)
    msg = prompt.cite_then_explain(q, s)
    ans = llm.invoke(msg)
    return observe(q, s, ans)
````

---

## Copy-paste LLM prompt

```txt
You have TXT OS and the WFGY pages loaded.

Task:
1) Enforce cite-then-explain with fields {snippet_id, section_id, source_url, offsets, tokens}.
2) Log ΔS(question, retrieved) and λ across 3 paraphrases and 2 seeds.
3) If ΔS ≥ 0.60 or λ flips, propose the smallest structural change referencing:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers, query-parsing-split.
4) Return JSON:
{ "citations": [...], "answer": "...", "ΔS": 0.xx, "λ_state": "<>", "coverage": 0.xx, "next_fix": "..." }
```

---

## Symptoms → exact structural fix

| Symptom                            | Likely cause                                  | Open this                                                                                                                                                                                                                                                |
| ---------------------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| High similarity yet wrong meaning  | metric or embedding family mismatch           | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)                                                                                                                                             |
| Facts exist but never retrieved    | chunk drift or store fragmentation            | [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) · [pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) |
| Hybrid worse than single retriever | query parsing split, mis-weighted rerank      | [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)                              |
| Citations missing or unstable      | schema not enforced, formatter renamed fields | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)                                          |
| Answers flip between runs          | prompt header reordering or variance          | [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)                                                                      |

---

## Rebuild order when numbers stay bad

Follow the store-agnostic sequence and re-measure after each step.
Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

1. Lock analyzer and distance metric
2. Re-chunk with anchor checklist
3. Re-embed with a single family and normalization
4. Add deterministic reranker and stabilize order
5. Tighten data contracts and traceability
6. Evaluate with the gold set and ΔS probes
   Open: [retrieval\_eval\_recipes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md)

---

## Ops monitors to keep on

* Index readiness fence and version hash
  Open: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* Live ΔS and λ alerts on long windows
  Open: [ops live monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

* Regression gate for coverage and ΔS
  Open: [eval precision and recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

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

