# Safety & Prompt Integrity — Global Fix Map

A hub to stabilize **prompt-level safety and schema integrity** across providers, agents, and eval flows.  
Use this folder when failures look like jailbreaks, role confusion, or malformed tool calls.  
Each page maps **symptoms → root cause → structural fixes** with measurable acceptance targets.

---

## What this page is
- A **practical checklist** for anyone shipping LLM apps with tools, roles, or multi-agent setups.  
- Each failure pattern links to its own guide with copy-paste guardrails.  
- Works without infra changes — schema and prompt fixes only.  
- Acceptance targets (ΔS, λ, coverage) are reproducible.

---

## When to use
- Jailbreak attempts slip past normal filters.  
- Prompts collapse schema or inject rogue tools.  
- Tool calls drift into free text or JSON breaks.  
- Role instructions misalign (system vs user vs assistant).  
- Citations disappear or retrieval bypasses snippet contracts.  
- Eval pipelines show high ΔS drift even when retrieval is correct.  

---

## Common failure patterns

| Failure mode | What happens | Open this |
|--------------|--------------|-----------|
| **Prompt Injection** | Hidden instructions override your system prompt | [prompt_injection.md](./prompt_injection.md) |
| **Jailbreaks / Overrides** | User tricks model into ignoring rules | [jailbreaks_and_overrides.md](./jailbreaks_and_overrides.md) |
| **Role Confusion** | System / user / assistant boundaries collapse | [role_confusion.md](./role_confusion.md) |
| **Memory Fence Missing** | State leaks across runs, no stable key | [memory_fences_and_state_keys.md](./memory_fences_and_state_keys.md) |
| **JSON Drift** | Tool calls malformed, fields missing | [json_mode_and_tool_calls.md](./json_mode_and_tool_calls.md) |
| **Citation Lost** | Answers skip snippet or no “cite-then-explain” | [citation_first.md](./citation_first.md) |
| **Injection Defense Recipes** | Ready-to-paste guardrails against common exploits | [anti_prompt_injection_recipes.md](./anti_prompt_injection_recipes.md) |
| **Tool Timeouts** | Tool calls hang or return late | [tool_selection_and_timeouts.md](./tool_selection_and_timeouts.md) |
| **Role Ordering** | Wrong order breaks downstream eval | [system_user_role_order.md](./system_user_role_order.md) |
| **Template Gaps** | Prompts inconsistent across agents | [template_library_min.md](./template_library_min.md) |
| **Eval Drift** | No stable way to test safety fixes | [eval_prompts_and_checks.md](./eval_prompts_and_checks.md) |

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of cited section ≥ 0.70  
- λ convergent across three paraphrases and two seeds  
- No uncontrolled free-text execution in JSON or tool modes  
- Citation-first enforced in ≥ 95% of eval runs  

---

## 60-second fix checklist

1. Lock **system / user / assistant** role order.  
2. Enforce **citation-first** and snippet schema.  
3. Apply **JSON fences** + argument validation.  
4. Add **memory fences** keyed by `mem_rev` and `state_key`.  
5. Run **eval prompts + probes** before shipping.  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
| **TXT OS** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module | Description | Link |
|--------|-------------|------|
| WFGY Core | WFGY 2.0 engine: full symbolic reasoning & math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0 | Initial 16-mode diagnostic framework | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0 | RAG failure tree and modular fixes | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic | Expanded catalog: injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint | Layer-based symbolic reasoning & semantic mods | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5 | Stress test GPT-5 with WFGY reasoning suite | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Wizard will guide you | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)**  
> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. Star the repo to unlock more.  

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)  
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)  
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)  
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)  
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)  
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)  
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)  

</div>
