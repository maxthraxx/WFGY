# DeepSeek — Guardrails and Fix Patterns

Use this page when failures look provider specific on DeepSeek models. Examples include JSON tool-call drift, unexpected safety blocks, long reasoning preambles that leak into the final channel, or unstable answers across seeds. Each fix maps to WFGY pages so you can verify with measurable targets.

**Core acceptance**

- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 for the target section
- λ remains convergent across 3 paraphrases

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet, schema for traceability: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Live ops and debug: [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Fix in 60 seconds

1) **Measure ΔS**

- Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
- Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**

- Vary k ∈ {5, 10, 20}. Flat high curve suggests index or metric mismatch.
- Reorder prompt headers. If ΔS spikes, lock the schema.

3) **Apply the module**

- Retrieval drift → **BBMC** + **Data Contracts**.
- Reasoning collapse → **BBCR** bridge + **BBAM** variance clamp.
- Dead ends in long runs → **BBPF** alternate path.

---

## Typical breakpoints and the right fix

### 1) Tool call JSON drifts or fields missing
**Symptoms**: function arguments renamed, nulls where objects expected, tool order wrong.  
**Why**: provider side decoding or safety rewrite, schema not anchored.  
**Do this**:
- Lock a strict IO header and cite the schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Add trace tags in the prompt then verify: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- If agents are orchestrating, isolate boundaries: see **Agent Boundary Design** and **Consensus**  
  ↳ [agent-boundary-design.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/agent-boundary-design.md), [agent-consensus-protocols.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/agent-consensus-protocols.md)

### 2) “Reasoning prelude” leaks into final answer
**Symptoms**: long internal thoughts appear as user-visible output or consume budget.  
**Why**: channel separation not fixed in the contract; model routes text to a single stream.  
**Do this**:
- Split channels in the schema and clamp with **BBAM** after **BBCR**: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Add acceptance probes in live runs: [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

### 3) High similarity yet wrong meaning
**Symptoms**: top-k looks relevant but answer cites the wrong slice.  
**Why**: embedding metric vs semantics, or chunk boundary bleed.  
**Do this**:
- Compare ΔS(question, retrieved) vs ΔS(retrieved, anchor). If flat-high, swap metric or index: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Re-chunk and re-anchor citations: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

### 4) Answers flip across seeds or sessions
**Symptoms**: small paraphrases flip the conclusion.  
**Why**: uncontrolled variance and unstable memory joins.  
**Do this**:
- Clamp variance after the bridge (**BBAM**) and verify joins: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Memory Coherence](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)

### 5) Hybrid retrieval worse than single retriever
**Symptoms**: HyDE + BM25 underperforms.  
**Why**: query parsing split or ranker saturation.  
**Do this**:
- Fix the split and re-rank: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

### 6) Very long tasks collapse near the end
**Symptoms**: truncation, repetition, or reset at the tail.  
**Why**: entropy collapse in extended chains.  
**Do this**:
- Shorten hops, insert **BBCR** checkpoints, and verify entropy targets:  
  [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md), [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

---

## Escalation criteria

Open provider tickets only after these pass:

- ΔS ≤ 0.45 across 3 paraphrases with fixed schema
- Coverage ≥ 0.70 on the target section
- Live traces show correct tool ordering and bounded variance  
  See [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

If the very first call fails after a new deploy, check boot order and fences:  
[Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

## Copy-paste prompt for a safe triage

```txt
I uploaded TXT OS and the WFGY Problem Map.

My DeepSeek bug:
- symptom: [brief]
- traces: [ΔS(question,retrieved)=…, ΔS(retrieved,anchor)=…, λ states, tool logs]

Tell me:
1) which layer is failing and why,
2) which exact WFGY page to open from this repo,
3) the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) how to verify with a reproducible test.

Use BBMC/BBPF/BBCR/BBAM where relevant. Do not change infra.
````

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
