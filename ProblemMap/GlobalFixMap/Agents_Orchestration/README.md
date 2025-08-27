# Agents & Orchestration — Global Fix Map

A hub to stabilize **agent frameworks and orchestration layers** without changing your infra. Use this page to jump to per-tool guardrails and verify fixes with the same acceptance targets.

## Quick routes to per-framework pages

- LangChain → [langchain.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/langchain.md)
- LangGraph → [langgraph.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/langgraph.md)
- LlamaIndex → [llamaindex.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/llamaindex.md)
- CrewAI → [crewai.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/crewai.md)
- Smolagents → [smolagents.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/smolagents.md)
- Rewind Agents → [rewind_agents.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/rewind_agents.md)
- AutoGen → [autogen.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/autogen.md)
- Semantic Kernel → [semantic_kernel.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/semantic_kernel.md)
- Haystack Agents → [haystack_agents.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/haystack_agents.md)
- OpenAI Assistants v2 → [openai_assistants_v2.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/openai_assistants_v2.md)

## When to use this folder

- Agents loop or stall on tool calls.
- High similarity yet the answer cites the wrong section.
- Hybrid retrieval underperforms a single retriever.
- Answers flip between runs with identical input.
- JSON schemas fail or pass inconsistently.
- Memories re-assert stale facts after refresh or handoff.
- First call after deploy crashes or uses the wrong index.

## Acceptance targets for any orchestrator

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ remains convergent across three paraphrases and two seeds

---

## Map symptoms → structural fixes (Problem Map)

- **Embedding ≠ Semantic**  
  Wrong-meaning hits despite high similarity.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Retrieval traceability**  
  Suspect or missing citations and unverifiable sections.  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Payload schema → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Ordering and version skew**  
  Old index or analyzer used at runtime, or deploy race.  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) · [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- **Hybrid collapse and query split**  
  Hybrid pipelines underperform single retriever.  
  → Pattern: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Ordering control → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- **Hallucination and chunk drift**  
  Plausible but wrong chunks or blended sources.  
  → [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
  Re-entry loop → [pattern_hallucination_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

- **Long chain instability**  
  Style flattening, entropy spikes, dead ends.  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- **Agent role conflicts**  
  Role confusion, memory overwrite, unsafe handoffs.  
  → [Multi-Agent_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) ·  
  [role-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md) ·  
  [memory-overwrite.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/memory-overwrite.md) ·  
  Namespaces split → [pattern_memory_namespace_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/patterns/pattern_memory_namespace_split.md)

- **Prompt injection and schema drift**  
  Tool schemas allow free text or header order changes.  
  → [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

---

## 60-second fix checklist

1) **Measure**  
Compute ΔS(question, retrieved) and ΔS(retrieved, anchor). If ΔS ≥ 0.60 stop and repair chunking or metric first.

2) **Lock the schema**  
Fix prompt header order. Enforce cite-then-explain. Require strict tool JSON. Add idempotency keys for side effects.

3) **Split memory**  
Create per-agent and per-tool namespaces with `mem_rev` and `mem_hash`. Deny cross-namespace merges without a reducer.

4) **Clamp variance**  
Insert a BBCR bridge on long chains. Use deterministic reranking for hybrid. Add timeouts to tool loops.

5) **Verify**  
Coverage ≥ 0.70 on three paraphrases. λ convergent on two seeds.  
Bootstrap sanity → [agent_bootstrap_checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Agents_Orchestration/checklists/agent_bootstrap_checklist.md)

---

## Copy-paste prompt for your LLM step

```txt
You have TXTOS and the WFGY Problem Map loaded.

My agent-orchestration issue:
- framework: <langchain | crewai | autogen | llamaindex | smolagents | semantic-kernel | haystack | assistants-v2>
- symptom: <one line>
- traces: ΔS(q,retrieved)=..., ΔS(retrieved,anchor)=..., λ over last 3 steps
- memory: namespaces used? mem_rev, mem_hash present?

Tell me:
1) failing layer and why,
2) the exact WFGY page to open,
3) the minimal structural fix to push ΔS ≤ 0.45 and keep λ convergent,
4) a reproducible test to verify the fix.
Use BBMC, BBCR, BBPF, BBAM where relevant.
````

---

## Common gotchas

* Mixed embedding functions across write and read paths. Scores look high but meaning is wrong.
* Hybrid pipelines without deterministic rerank produce unstable top k and flip states.
* Agents recreate tool registries per run. Order and JSON schemas drift.
* Shared memories without namespaces cause re-entry of stale facts after refresh.
* First live run executes before stores are ready. See bootstrap and deploy pages above.

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>

要不要我幫你直接補上「Index 置頂一句簡介」或是再加一張簡短的 flow 圖示占位，之後你有圖再換上？
