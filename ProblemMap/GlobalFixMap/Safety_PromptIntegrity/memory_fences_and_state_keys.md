# Memory Fences & State Keys — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Safety_PromptIntegrity**.  
  > To reorient, go back here:  
  >
  > - [**Safety_PromptIntegrity** — prompt injection defense and integrity checks](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Structural guardrails that prevent **context bleed** and **cross-session injection**.  
This page defines how to enforce hard boundaries between prompts, ensuring system memory cannot be hijacked or silently rewritten.

---

## When to open this page
- Model begins recalling text from *previous unrelated sessions*.  
- Jailbreak attempts work only after long multi-turn dialogs.  
- Role confusion persists despite schema locks.  
- Adversarial input shifts `policy`, `state`, or `history` across turns.  
- ΔS spikes after memory transfer, despite stable retrieval.  

---

## Open these first
- Injection baseline: [prompt_injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/prompt_injection.md)  
- Role boundary checks: [role_confusion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/role_confusion.md)  
- Override/jailbreak guard: [jailbreaks_and_overrides.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/jailbreaks_and_overrides.md)  
- Schema integrity: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Eval drift monitors: [eval_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval_drift.md)  

---

## Core acceptance
- No cross-session data unless whitelisted.  
- Each conversation has a unique `state_key`.  
- ΔS(question, retrieved) ≤ 0.45 across turns.  
- λ stays convergent for three paraphrases under replay.  
- Memory fences block unauthorized carry-over.  

---

## Fix in 60 seconds
1. **Assign a state key**  
   - Compute: `state_key = sha256(session_id + system_rev + policy_hash)`  
   - Attach to all memory writes.  

2. **Fence boundaries**  
   - Before each turn, validate:  
     - `incoming.state_key == current.state_key`  
     - If mismatch → reject or reset.  

3. **Immutable system text**  
   - Mark non-task policy as `system_only`.  
   - Forbid user overrides.  

4. **Replay probes**  
   - Inject controlled paraphrases.  
   - If ΔS or λ diverge, memory bleed suspected.  

5. **Audit log**  
   - Store `ΔS`, `λ`, `state_key`, and `mem_rev` per step.  
   - Flag anomalies for review.  

---

## Common failure vectors → fix

| Vector | Symptom | Fix |
|--------|---------|-----|
| **Cross-session carryover** | Answer mentions text from unrelated chat | Reject mismatched `state_key`, enforce reset |
| **Hidden injection persists** | User payload continues beyond reset | Hash all system policy, invalidate old keys |
| **Role drift with memory echo** | Replies prepend “system:” from earlier | Apply [role_confusion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/role_confusion.md) fences |
| **Version skew** | New deploy reuses old cache | Salt `state_key` with `system_rev` |
| **Chain-of-thought bleed** | Internal notes leak into answers | Enforce [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) schema |

---

## Probe prompt

```txt
System memory test active.  
Session ID: {sid}, Policy Hash: {p_hash}.  

Tasks:
1. Compute state_key and compare against current session.
2. If mismatch, reset memory fences and refuse carryover.
3. Re-ask with paraphrased queries; compute ΔS and λ.
4. Report whether context bleed is detected.
5. Return minimal fix reference (role_confusion, prompt_injection, etc).
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

