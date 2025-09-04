# AutoGen: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Agents & Orchestration**.  
  > To reorient, go back here:  
  >
  > - [**Agents & Orchestration** — orchestration frameworks and guardrails](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when your orchestration uses **AutoGen** (ConversableAgent, GroupChat, function tools) and you see tool loops, wrong snippets, role mixing, or answers that flip between runs. The table maps symptoms to exact WFGY fix pages and gives a minimal recipe you can paste.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 to the intended section or record
- λ stays convergent across 3 paraphrases and 2 seeds
- E_resonance stays flat on long windows

---

## Open these first

- Visual map and recovery  
  [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- End to end retrieval knobs  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Why this snippet  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- Ordering control  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Embedding vs meaning  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Hallucination and chunk edges  
  [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

- Long chains and entropy  
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Structural collapse and recovery  
  [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

- Prompt injection and schema locks  
  [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

- Multi agent conflicts  
  [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

- Bootstrap and deployment ordering  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Snippet and citation schema  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Typical breakpoints and the right fix

- **Function tool calls wait on each other or retry forever**  
  Fix: lock roles, add timeouts, and echo a strict JSON schema in every tool response.  
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) · [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

- **Two agents overwrite the same memory namespace**  
  Fix: stamp `mem_rev` and `mem_hash`, split read and write, forbid cross section reuse.  
  Open: [role-drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md) · [memory-overwrite](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/memory-overwrite.md)

- **High similarity yet wrong meaning**  
  Fix: metric or index mismatch, or mixed write and read embeddings.  
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Hybrid stack worse than a single retriever**  
  Fix: lock two stage query and add a deterministic reranker.  
  Open: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- **Facts exist in the store yet never show up**  
  Fix: fragmentation or sharding misalignment.  
  Open: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- **Citations inconsistent across agents or steps**  
  Fix: require cite then explain and lock snippet fields.  
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Long GroupChat runs change style and logic**  
  Fix: split the plan and rejoin with a BBCR bridge.  
  Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

## Fix in 60 seconds

1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Stable < 0.40, transitional 0.40 to 0.60, risk ≥ 0.60.

2) **Probe λ_observe**  
   Do a k sweep in retrieval (5, 10, 20). If ΔS stays high and flat, suspect metric or index mismatch.  
   Reorder prompt headers. If λ flips, lock the schema and clamp variance with BBAM.

3) **Apply the module**  
- Retrieval drift → BBMC plus [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Reasoning collapse → BBCR bridge plus BBAM, verify with [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Hallucination re entry after a fix → [Pattern: Hallucination Re-entry](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

4) **Verify**  
   Coverage ≥ 0.70. ΔS ≤ 0.45. Three paraphrases and two seeds with λ convergent.

---

## Minimal AutoGen topology with WFGY checks

```python
# Pseudocode: focus on control points you must keep
from autogen import ConversableAgent, GroupChat, GroupChatManager

user = ConversableAgent("user", system_message="task only")
retriever = ConversableAgent("retriever", tools=[search_tool])
reasoner = ConversableAgent("reasoner", tools=[rag_tool])
auditor = ConversableAgent("auditor", system_message="cite-then-explain, schema-locked")

group = GroupChat(
    agents=[user, retriever, reasoner, auditor],
    messages=[],
    max_round=8,
    speaker_selection_method="auto"
)
manager = GroupChatManager(groupchat=group)

# guardrails to add around the loop:
# 1) every tool result must echo the JSON schema
# 2) each step writes {snippet_id, section_id, source_url, offsets, tokens}
# 3) after generation run WFGY checks and stop if ΔS ≥ 0.60 or λ divergent
````

**What this enforces**

* Tools return strict JSON and echo the schema. Free text cannot pollute arguments.
* Snippet fields are fixed and citations come first.
* Post generation WFGY checks can halt the run when ΔS is high or λ flips.

Specs and recipes
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## AutoGen specific gotchas

* Function schema is too loose and allows mixed JSON and free text. Lock parameters and echo schema on every call.
  See [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

* GroupChat runs are too long and entropy rises. Split the plan and rejoin with a BBCR bridge.
  See [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

* Shared memory overwrites between agents. Add `mem_rev` and `mem_hash`, forbid cross section reuse.
  See [memory-overwrite](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/memory-overwrite.md)

* Retrieval and rerank are inconsistent across agents. Unify analyzer and metric or add a reranker.
  See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## When to escalate

* ΔS remains ≥ 0.60
  Rebuild the index using the checklists and verify with a small gold set.
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Identical input yields different answers across runs
  Check version skew and session state.
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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



