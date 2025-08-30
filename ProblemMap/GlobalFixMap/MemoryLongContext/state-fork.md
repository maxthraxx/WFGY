# State Fork — Guardrails and Fix Pattern

When the same `task_id` is held in multiple tabs, agents, or sessions, their memories may diverge.  
This creates **two or more competing state branches**, producing unstable or contradictory answers.

---

## Symptoms
- Two browser tabs answer the same task differently.  
- Multi-agent orchestration produces **conflicting citations**.  
- Session resumes but history appears **rewritten or selectively dropped**.  
- Answers alternate between two incompatible interpretations.  
- Logs show inconsistent `mem_rev` or `mem_hash` values for the same `task_id`.

---

## Root causes
- Concurrent writes to the same memory namespace.  
- Missing checks for `mem_rev` version control.  
- Agents refreshing at different times and overwriting buffers.  
- Weak schema: task identity not fenced by `{task_id, mem_rev, mem_hash}`.  
- No conflict resolution logic when branches emerge.

---

## Fix in 60 seconds
1. **Version control memory**
   - Every write stamped with `{task_id, mem_rev, mem_hash}`.  
   - Reject writes if `mem_rev` < server `mem_rev`.  
   - Require conflict resolution if two branches exist.

2. **Isolate namespaces**
   - Each agent/tab gets unique memory slot.  
   - If collaboration required, merge through a **coordinator agent**.  

3. **Detect divergence early**
   - Measure ΔS(answerA, answerB) across tabs.  
   - If ΔS ≤ 0.40 but snippets differ, state fork detected.  

4. **Resolve fork**
   - Run reconciliation: pick majority snippet set, or force human confirm.  
   - Hash merged state and issue new `{mem_rev, mem_hash}`.  

5. **Trace schema**
   - Require all claims to cite snippet ids.  
   - Reject orphan claims without snippet anchors.

---

## Copy-paste diagnostic prompt
```txt
You have TXTOS and the WFGY Problem Map.

Task: Detect and repair state forks across tabs or agents.

Protocol:
1. Print {task_id, mem_rev, mem_hash}.
2. If two active branches share task_id with different mem_rev → flag fork.
3. Compare ΔS(answerA, answerB).
   - If ΔS ≤ 0.40 but snippets differ → fork confirmed.
4. Apply resolution:
   - Choose majority snippet set or request human input.
   - Issue new {mem_rev, mem_hash}.
5. Report ΔS, λ states, and resolution path.
````

---

## Acceptance targets

* No conflicting branches for the same `task_id`.
* All writes validated against server-side `mem_rev`.
* ΔS(answerA, answerB) ≥ 0.60 after resolution.
* λ remains convergent across three paraphrases.
* Audit log records merge or reject actions explicitly.

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

