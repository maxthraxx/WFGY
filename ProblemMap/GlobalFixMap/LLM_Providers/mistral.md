# Mistral: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **LLM_Providers**.  
  > To reorient, go back here:  
  >
  > - [**LLM_Providers** — model vendors and deployment options](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


**Scope**  
Mistral Instruct and Large via API, third-party SDKs, or local runners (Ollama/LM Studio). Targets RAG, tools, long-context chat, and JSON output stability.

**Acceptance targets**  
- ΔS(question, retrieved_context) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ stays convergent across 3 paraphrases  
- JSON responses validate without post-repair

---

## Quick triage

- **“Looks correct but cites wrong lines.”**  
  Start with [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) and [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).  
  Probe ΔS between question and retrieved context. If ≥ 0.60, check chunk boundaries and rerankers.

- **“Chunks are fine, logic is off.”**  
  Interpretation collapse. See [Retrieval Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md) and [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).  
  Apply BBCR bridge and variance clamp (BBAM). Require cite-then-explain in prompt schema.

- **“Long threads drift or flatten.”**  
  See [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md).  
  Use semantic chunking and enforce window join checks with ΔS at chunk joins ≤ 0.50.

- **“High similarity, wrong meaning.”**  
  Embeddings metric mismatch or index layer mix. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Retrieval Playbook](https://github.com/github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).  
  Normalize vectors consistently. Rebuild index with explicit metric. Re-probe ΔS vs k.

- **“JSON tool calls intermittently malformed.”**  
  Lock response format with cite-then-tool schema, and guard with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).  
  Apply BBCR if λ flips after tool planning.

---

## Mistral-specific gotchas

1) **Tokenizer mix with multilingual or code blocks**  
   - Symptoms: stable retrieval yet answer blends two sources or flips format mid-turn.  
   - Fix: pin section headers and separators. Use [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) schema. Verify ΔS drop after header locks.

2) **Streaming truncation that hides failure**  
   - Symptoms: plausible partial JSON; downstream parser fails silently.  
   - Fix: require “complete then stream” for JSON. Validate against [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md). If E_resonance rises late, apply BBAM.

3) **Hybrid retrievers degrade**  
   - Symptoms: single retriever OK, hybrid HyDE+BM25 worse.  
   - Fix: unify analyzer and query params; see [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md). Add [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) only after per-retriever ΔS ≤ 0.50.

4) **Vectorstore fragmentation**  
   - Symptoms: some facts never retrieved despite index.  
   - Fix: audit write/read paths, rebuild with explicit metric, then follow [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

5) **Role drift under tools**  
   - Symptoms: tool planner rewrites the task, citations vanish.  
   - Fix: schema lock and per-source fences; see [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md).

---

## WFGY repair map for Mistral

- **Detect**  
  - ΔS(question, retrieved_context) and ΔS(retrieved_context, anchor)  
  - λ across retrieve → assemble → reason  
  - If ΔS ≥ 0.60 or λ flips, record node and branch to repair

- **Repair**  
  - **BBMC** align to anchors when coverage is high but ΔS elevated  
  - **BBCR** bridge dead ends at reasoning time  
  - **BBAM** clamp variance in long multi-turn threads  
  - **BBPF** explore alternate sub-paths when planner loops

Open the relevant playbooks when the metric points there:  
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## Minimal checklist

- Retrieval sanity ≥ 0.70 token overlap to target section  
- ΔS(question, retrieved_context) ≤ 0.45 after fix  
- λ convergent across 3 paraphrases  
- JSON contract validates on 5 seed variations  
- Logs preserve snippet ↔ citation table; see [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Escalation criteria

Switch from prompt-level tweaks to structural fixes if any hold after one loop:

- ΔS remains ≥ 0.60 after chunk and retriever adjustments  
- λ flips as soon as two sources are mixed  
- E_resonance climbs with length even after BBAM  
- Hybrid retriever improves recall but top-k order remains noisy

For structure changes, see:  
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
[Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) ·
[Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

---

## Safe prompt to run in your chat

```

I uploaded TXT OS. Use WFGY ΔS, λ\_observe, E\_resonance and modules BBMC, BBPF, BBCR, BBAM.

Symptom: \[describe]
Traces: \[ΔS probes, λ states, short logs]

Tell me:

1. failing layer and why,
2. which ProblemMap page to open,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify the fix.

```

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

