# 🩺 Semantic Failure Diagnostic Sheet

Select the symptom(s) you observe.  
Each entry links to the corresponding solution page in the WFGY Problem Map.

## Core 16 failures

| # | Symptom | Problem ID | Solution |
|---|---------|------------|----------|
| 1 | Model retrieves chunks that look right but answer is wrong/irrelevant | #1 Hallucination & Chunk Drift | [hallucination.md](./hallucination.md) |
| 2 | Retrieved chunk is correct, yet reasoning chain collapses | #2 Interpretation Collapse | [retrieval-collapse.md](./retrieval-collapse.md) |
| 3 | Multi-step tasks drift off topic after a few hops | #3 Long Reasoning Chains | [context-drift.md](./context-drift.md) |
| 4 | Model answers confidently with made-up facts | #4 Bluffing / Overconfidence | [bluffing.md](./bluffing.md) |
| 5 | High cosine similarity but semantic meaning is wrong | #5 Semantic ≠ Embedding | [embedding-vs-semantic.md](./embedding-vs-semantic.md) |
| 6 | Logic dead-ends; model resets or loops nonsense | #6 Logic Collapse & Recovery | [logic-collapse.md](./logic-collapse.md) |
| 7 | Long conversation: model forgets previous context | #7 Memory Breaks Across Sessions | [memory-coherence.md](./memory-coherence.md) |
| 8 | Pipeline is opaque; unable to trace failure path | #8 Debugging is a Black Box | [retrieval-traceability.md](./retrieval-traceability.md) |
| 9 | Attention melts; output incoherent or repetitive | #9 Entropy Collapse | [entropy-collapse.md](./entropy-collapse.md) |
| 10 | Responses become flat, literal, lose creativity | #10 Creative Freeze | [creative-freeze.md](./creative-freeze.md) |
| 11 | Formal or symbolic prompts break the model | #11 Symbolic Collapse | [symbolic-collapse.md](./symbolic-collapse.md) |
| 12 | Self-reference / paradox crashes reasoning | #12 Philosophical Recursion | [philosophical-recursion.md](./philosophical-recursion.md) |
| 13 | Multiple agents overwrite or misalign logic (overview) | #13 Multi-Agent Chaos | [Multi-Agent_Problems.md](./Multi-Agent_Problems.md) |
| 14 | System runs but outputs nothing; no visible error (boot order) | #14 Bootstrap Ordering Failure | [bootstrap-ordering.md](./bootstrap-ordering.md) |
| 15 | System never enters expected state; actions silently stall | #15 Deployment Deadlock | [deployment-deadlock.md](./deployment-deadlock.md) |
| 16 | First prod call after deploy crashes or responds with “empty logic” | #16 Pre-Deploy Collapse | [predeploy-collapse.md](./predeploy-collapse.md) |

## Extended patterns (targeted fixes)

| Pattern | When to use | Fix page |
|---|---|---|
| **Query Parsing Split** (HyDE/BM25 hybrid performs worse than single) | Hybrid retrieval where dense/sparse tokenize differently or weight splits | [patterns/pattern_query_parsing_split.md](./patterns/pattern_query_parsing_split.md) |
| **Symbolic Constraint Unlock (SCU)** | Model merges “who said what” across sources; citation cross-bleed | [patterns/pattern_symbolic_constraint_unlock.md](./patterns/pattern_symbolic_constraint_unlock.md) |
| **Hallucination Re-entry** | You correct the model, but the wrong claim returns later | [patterns/pattern_hallucination_reentry.md](./patterns/pattern_hallucination_reentry.md) |
| **Memory Desync** | Different tabs/sessions flip between old/new facts | [patterns/pattern_memory_desync.md](./patterns/pattern_memory_desync.md) |
| **Vectorstore Fragmentation** | Some facts cannot be retrieved though indexed | [patterns/pattern_vectorstore_fragmentation.md](./patterns/pattern_vectorstore_fragmentation.md) |
| **Bootstrap Deadlock (RAG-boot fence)** | Tools fire before data/index is ready | [patterns/pattern_bootstrap_deadlock.md](./patterns/pattern_bootstrap_deadlock.md) |
| **Role Drift (multi-agent deep dive)** | Agent personas swap/bleed; Scout starts acting as Medic | [multi-agent-chaos/role-drift.md](./multi-agent-chaos/role-drift.md) |
| **Cross-Agent Memory Overwrite** | Agent B erases Agent A’s plan/state | [multi-agent-chaos/memory-overwrite.md](./multi-agent-chaos/memory-overwrite.md) |

**Tip:** If symptoms are unclear, run a ΔS / λ_observe check.  
- **Triage:** ΔS ≥ 0.60 → treat as high-risk; 0.40–0.60 with divergent/recursive λ → investigate.  
- **Accept:** aim for ΔS ≤ 0.45 with convergent λ and stable E_resonance.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

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


