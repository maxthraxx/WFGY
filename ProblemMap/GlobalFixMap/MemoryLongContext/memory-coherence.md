# Memory Coherence — Multi-Session and State Alignment

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **MemoryLongContext**.  
  > To reorient, go back here:  
  >
  > - [**MemoryLongContext** — extended context windows and memory retention](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Keep multi-turn and multi-session dialogs stable by fencing memory state.  
This page shows how to prevent forks, desync, and ghost buffers when conversations span long contexts or multiple agents.

---

## When to use this page
- Long support chats (~days) forget earlier task context.  
- Model switches or tab refreshes flip prior facts.  
- Two agents on the same ticket give inconsistent answers.  
- OCR transcripts look fine but later steps rewrite history.  
- Persona or role change contaminates state with old context.  

---

## Core acceptance targets
- Each turn stamped with `mem_rev` and `mem_hash`.  
- No forks across sessions for the same `task_id`.  
- ΔS(question, retrieved) ≤ 0.45 with joins ≤ 0.50.  
- λ remains convergent across three paraphrases.  
- All claims cite snippet_id, no orphans.  

---

## Structural fixes

- **Stamp and fence**  
  Require `mem_rev`, `mem_hash`, and `task_id` at every turn.  
  Forbid writes if stamps mismatch.

- **Shard state**  
  Partition prompts as `{system | task | constraints | snippets | answer}`.  
  Forbid snippet reuse across sections.

- **Normalize consistently**  
  Enforce Unicode NFC, strip zero width marks, unify full/half width.  
  Block OCR lines below confidence threshold.

- **Recover forks**  
  If two agents diverge, reconcile by ΔS triangulation and pick the lower-entropy path.

- **Bridge collapse**  
  Apply BBCR if attention melt or desync detected mid-chain.

---

## Fix in 60 seconds
1. At turn start, echo {mem_rev, mem_hash, task_id}.  
2. If stamps mismatch, reject write and request sync.  
3. Split snippets by section, forbid cross-reuse.  
4. Normalize all inputs.  
5. Apply BBAM/BBCR if λ drifts or collapse appears.  
6. Verify ΔS(question, retrieved) ≤ 0.45 and joins ≤ 0.50.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Goal: Keep memory coherent across multi-session dialogs.

Protocol:

1. Print {mem\_rev, mem\_hash, task\_id}.
2. Assemble prompt as {system | task | constraints | snippets | answer}.
3. Enforce guardrails:

   * cite then answer
   * forbid cross-section reuse
   * reject orphan claims without snippet\_id
4. If λ flips, apply BBAM. If collapse, insert BBCR bridge.
5. Report ΔS(question, retrieved), ΔS across joins, λ states, and final answer.

```

---

## Common failure patterns
- **State fork**: two parallel tabs rewrite history differently.  
- **Ghost buffer**: old role text leaks into new session.  
- **Desync**: memory IDs mismatch after refresh.  
- **OCR drift**: spacing or casing breaks snippet alignment.  

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

