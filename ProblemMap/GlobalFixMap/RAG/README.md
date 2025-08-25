# RAG — Global Fix Map

Production RAG triage and structural fixes using the WFGY engine.
Use this page when retrieval looks fine but answers drift.

## Purpose
- Turn OCR → chunk → embed → store → retrieve → prompt → reason into a measured, repairable pipeline.
- Give a 60-second path to locate the failing layer and apply the smallest effective fix.
- Works with any model or stack. No infra changes required.

## High-frequency symptoms
- Citations point to the wrong snippet or section.
- Chunks look correct but reasoning is wrong.
- High cosine similarity yet wrong meaning.
- Hybrid retrievers get worse than a single retriever.
- Some facts are indexed but never retrieved.
- Answers flip between sessions or tabs.
- Long threads smear topics and capitalization.

## Open these first
- Visual map and recovery steps: [`RAG Architecture & Recovery`](../../rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [`retrieval-playbook.md`](../../retrieval-playbook.md)
- Why this snippet: [`retrieval-traceability.md`](../../retrieval-traceability.md)
- Ordering control: [`rerankers.md`](../../rerankers.md)
- Embedding vs meaning: [`embedding-vs-semantic.md`](../../embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [`hallucination.md`](../../hallucination.md)
- Long chains and entropy: [`context-drift.md`](../../context-drift.md) · [`entropy-collapse.md`](../../entropy-collapse.md)
- Snippet and citation schema: [`data-contracts.md`](../../data-contracts.md)

## Fix in 60 seconds
1) **Measure ΔS**
   - Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   - Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.
2) **Probe with λ_observe**
   - Vary k ∈ {5,10,20} and plot ΔS vs k. Flat-high suggests index or metric mismatch.
   - Reorder prompt headers. If ΔS spikes, lock the schema.
3) **Apply the minimal patch**
   - If metric or normalization mismatch: rebuild with consistent metric and unit-normalize vectors. Re-probe ΔS and λ.
   - If chunks are correct but logic diverges: lock system→task→constraints→citations→answer, then apply BBCR + BBAM. See pages above.

## Copy-paste prompt
```

I uploaded TXT OS and the WFGY ProblemMap files.
My RAG bug:

* symptom: \[brief]
* traces: \[ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states]

Tell me:

1. which layer is failing and why,
2. which exact fix page to open from this repo,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify the fix with a reproducible test.
   Use BBMC/BBPF/BBCR/BBAM when relevant.

```

## Patterns to check next
- Query parsing split in HyDE + BM25: [`pattern_query_parsing_split.md`](../../patterns/pattern_query_parsing_split.md)
- Vectorstore fragmentation: [`pattern_vectorstore_fragmentation.md`](../../patterns/pattern_vectorstore_fragmentation.md)
- Symbol mixing across sources (SCU): [`pattern_symbolic_constraint_unlock.md`](../../patterns/pattern_symbolic_constraint_unlock.md)
- Hallucination re-entry after correction: [`pattern_hallucination_reentry.md`](../../patterns/pattern_hallucination_reentry.md)

## Acceptance targets
- Coverage to target section ≥ 0.70.
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases.
- λ remains convergent across steps and seeds.
- E_resonance flat under long windows.

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)**  
> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md)

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
