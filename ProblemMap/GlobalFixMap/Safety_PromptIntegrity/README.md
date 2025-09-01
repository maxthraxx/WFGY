# Safety & Prompt Integrity — Global Fix Map

A hub to stabilize **prompt-level safety and schema integrity** across providers, agents, and eval flows.  
Use this folder when failures look like jailbreaks, role confusion, or malformed tool calls. Each page maps symptoms → structural fixes with measurable acceptance targets.

---

## Quick routes to per-page guides

- Prompt injection patterns → [prompt_injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/prompt_injection.md)  
- Jailbreaks and override attempts → [jailbreaks_and_overrides.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/jailbreaks_and_overrides.md)  
- Role confusion between system / user / assistant → [role_confusion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/role_confusion.md)  
- Memory fences and state keys → [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/memory_fences_and_state_keys.md)  
- JSON mode and tool call guardrails → [json_mode_and_tool_calls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/json_mode_and_tool_calls.md)  
- Citation-first enforcement → [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/citation_first.md)  
- Anti-injection recipes (ready-to-paste) → [anti_prompt_injection_recipes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/anti_prompt_injection_recipes.md)  
- Tool selection and timeouts → [tool_selection_and_timeouts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/tool_selection_and_timeouts.md)  
- System vs user role ordering → [system_user_role_order.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/system_user_role_order.md)  
- Minimal template library → [template_library_min.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/template_library_min.md)  
- Eval prompts and integrity checks → [eval_prompts_and_checks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/eval_prompts_and_checks.md)

---

## When to use this folder

- Jailbreak attempts slip past standard filters.  
- Prompts collapse schema or inject rogue tools.  
- Tool calls drift into free text or JSON breaks.  
- Role instructions are misaligned (system vs user vs assistant).  
- Citations disappear, or retrieval steps bypass snippet contracts.  
- Eval pipelines show high ΔS drift even when retrieval is correct.  

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of cited section ≥ 0.70  
- λ remains convergent across three paraphrases and two seeds  
- No uncontrolled free-text execution in JSON or tool modes  
- Citation-first enforced in ≥ 95% of eval runs  

---

## 60-second fix checklist

- Lock system / user / assistant role order.  
- Enforce citation-first and snippet schema.  
- Apply JSON fences + argument validation.  
- Add memory fences keyed by `mem_rev` and `state_key`.  
- Run eval prompts + structural probes before ship.  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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

