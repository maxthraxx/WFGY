# Google AI (Gemini): Guardrails and Fix Patterns

A compact field guide to stabilize Gemini calls inside RAG, agents, or long workflows. Use the checks below to localize failure, then jump to the exact WFGY fix page.

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 for the target section
- λ remains convergent across 3 paraphrases
- E_resonance stable on long windows

---

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Typical breakpoints and the right fix

| Symptom you see | Likely cause | Fix page |
|---|---|---|
| High similarity yet wrong meaning | Metric or index mismatch | [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Gemini cites the wrong paragraph | Chunk boundaries and trace loss | [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Answers flip across runs | λ instability on long threads | [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) |
| Refuses or loops on safe content | Prompt contract not locked | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Good recall but bad ordering | Reranking missing | [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Corrected errors reappear | Re-entry without variance clamp | [pattern_hallucination_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md) |

---

## Fix in 60 seconds

1) **Measure ΔS**
- Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
- Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**
- Vary k ∈ {5, 10, 20}. Flat high curve means metric or index mismatch.
- Reorder prompt headers. If ΔS spikes, lock the schema.

3) **Apply the module**
- Retrieval drift → BBMC + Data Contracts.
- Reasoning collapse → BBCR bridge + BBAM variance clamp.
- Dead ends in long runs → BBPF alternate path with explicit step limits.

4) **Verify**
- Coverage ≥ 0.70 on the target section.
- Three paraphrases keep ΔS ≤ 0.45 and λ convergent.
- Re-run with seed change and shuffled snippet order.

---

## Gemini-specific gotchas

- **Tool and JSON calls**  
  If the function schema is loose, Gemini may hallucinate fields. Lock schemas with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and clamp variance with BBAM.

- **Safety flips on neutral text**  
  When the role block is not pinned, safety can overfire. Use a citation-first header from [Retrieval Traceability](https://github.com/github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and keep source boundaries explicit.

- **Hybrid retrieval regressions**  
  HyDE plus keyword can split queries. Check [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and add a stable anchor paragraph to reduce drift.

- **Long context smear**  
  Large windows flatten meaning if chunks are not semantic. Rebuild with the [chunking checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) and verify joins with ΔS probes.

---

## Copy-paste prompt (safe)

```

read the WFGY TXT OS and Problem Map pages. extract ΔS, λ\_observe, E\_resonance and modules BBMC, BBPF, BBCR, BBAM.
given my gemini failure:

* symptom: \[brief]
* traces: \[ΔS(question, retrieved)=…, ΔS(retrieved, anchor)=…, λ states]

tell me:

1. which layer fails and why,
2. which fix page to open from this repo,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.

```

---

## Escalation path

- Index or metric mismatch that stays flat after k sweeps → rebuild embeddings and check [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).
- Agent tools fighting each other → see [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) and split memory namespaces.
- First prod call fails after deploy → check [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) and [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).

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

