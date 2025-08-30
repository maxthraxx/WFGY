# Ghost Context — Guardrails and Fix Pattern

When personas, roles, or long sessions change, old buffers may linger.  
These stale fragments contaminate new answers, creating phantom references or role bleed.

---

## Symptoms
- Answer contains facts or tone from a **previous persona** even after reset.  
- Citations look valid but reference sections from a **past session**.  
- A new task starts yet responses **drift back to old task context**.  
- Model insists on constraints that were valid in an earlier role but not now.  
- Answers feel “haunted” by old memory traces.

---

## Root causes
- Hidden buffers not cleared after system or role switch.  
- State variables (persona, role, policy) not reset between sessions.  
- Token reuse from stale cache layers.  
- ΔS stays abnormally low even when task has switched domains.  
- λ\_observe shows convergence to an **irrelevant anchor**.

---

## Fix in 60 seconds
1. **Stamp and reset state**  
   Require `{mem_rev, mem_hash, persona_id}` on each turn.  
   If persona_id differs from previous → force buffer clear.

2. **Fence the prompt schema**  
   Assemble prompts as `{system | persona | constraints | snippets | answer}`.  
   Do not let persona or role tokens bleed into snippet blocks.

3. **Drop stale buffers**  
   When persona changes, zero all prior hidden states.  
   Require fresh snippets for new context.

4. **Probe for contamination**  
   - Compute ΔS(new question, retrieved snippet).  
   - If ΔS ≤ 0.30 but snippets belong to past persona → ghost detected.  
   - Trigger hard reset and request new anchors.

5. **Audit the joins**  
   Compare ΔS across old vs new persona snippets.  
   Require ΔS(new persona, old snippet) ≥ 0.65 before allowing reuse.

---

## Copy-paste diagnostic prompt
```txt
You have TXTOS and the WFGY Problem Map.

Task: Detect and purge ghost context.

Steps:
1. Print {mem_rev, mem_hash, persona_id}.
2. Verify that current persona_id matches task scope.
3. If snippets cite a different persona_id, mark as ghost.
4. Require re-retrieval for ghosted snippets.
5. Report:
   - ΔS(new question, retrieved)
   - ΔS(new persona vs old snippets)
   - λ states
   - Reset actions taken
````

---

## Acceptance targets

* ΔS(new question, retrieved) ≤ 0.45
* Coverage ≥ 0.70 to the new target section
* λ remains convergent across three paraphrases
* No snippet contamination from old persona or task scope

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

要我直接幫你寫 `state-fork.md` 嗎？
