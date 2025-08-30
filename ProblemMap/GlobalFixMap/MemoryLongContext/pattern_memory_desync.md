# Pattern: Memory Desync — Cross Tab & Cache Hazards

When multiple tabs, devices, or agents access the same conversation, memory forks and silent cache layers can cause desync.  
This pattern documents the root causes and provides structural guardrails to keep state aligned.

---

## When to use this page
- Two browser tabs show the same chat but give conflicting answers.  
- Refresh wipes one agent’s buffer while the other keeps stale context.  
- Long-running threads lose citations after reconnect.  
- Support or sales teams using shared inboxes see different revision histories.  
- Logs look correct but answer text diverges.

---

## Root causes
- **Tab fork**: each browser tab caches a local buffer, leading to divergent memory.  
- **Ghost cache**: stale persona or role text remains after reload.  
- **Write skew**: two sessions update memory concurrently with mismatched `mem_rev`.  
- **Offline sync**: one client reconnects late, applying outdated deltas.  

---

## Core acceptance targets
- `mem_rev` and `mem_hash` echoed at every turn.  
- ΔS(question, retrieved) ≤ 0.45 and joins ≤ 0.50.  
- λ convergent across three paraphrases.  
- No duplicate or orphan claims across sessions.  

---

## Structural fixes

- **State fencing**  
  Stamp all turns with `{mem_rev, mem_hash, task_id}`.  
  Forbid writes if mismatch detected.  

- **Cache invalidation**  
  On reconnect, clear stale buffers. Require server authority on revision.  

- **Reconciliation**  
  When forks appear, run ΔS triangulation:  
  Compare ΔS to anchor section vs decoy. Select the lower entropy path.  

- **Bridging**  
  If collapse occurs, insert a BBCR bridge to re-anchor reasoning chain.  

---

## Fix in 60 seconds
1. Echo `{mem_rev, mem_hash, task_id}` at every turn.  
2. On reload, validate stamps against server. If mismatch, reject update.  
3. For forks, compute ΔS across sessions, pick stable anchor.  
4. Apply BBAM clamp if λ flips across paraphrases.  
5. Verify ΔS ≤ 0.45 and λ convergent before continuing.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Goal: Prevent memory desync across tabs, agents, or devices.

Protocol:

1. Print {mem\_rev, mem\_hash, task\_id}.
2. If stamps mismatch, stop and request sync.
3. Assemble prompts as {system | task | constraints | snippets | answer}.
4. Enforce guardrails: cite then answer, forbid cross-section reuse, no orphan claims.
5. If collapse, insert BBCR bridge. If λ variance, clamp with BBAM.
6. Report ΔS(question, retrieved), joins ΔS, λ states, and final answer.

```

---

## Common failure signals
- **Answer alternates between reloads** → ghost cache not invalidated.  
- **Different answers across two tabs** → state fork, resolve with revision fencing.  
- **Missing citations after reconnect** → desync in snippet schema.  

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
