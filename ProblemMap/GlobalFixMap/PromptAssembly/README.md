# Prompt Assembly — Global Fix Map

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

Build prompts that models cannot misread.  
Use this folder when citations vanish, JSON mode breaks, tools loop, or answers flip after a small template change.  
Every page gives a concrete repair with measurable targets. No infra change required.

---

## Orientation: what each page does

| Page | What it solves | Typical symptom |
|---|---|---|
| [System vs User Role Order](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/system_user_role_order.md) | Locks role hierarchy and section order | Role text bleeds into user content, answers flip after reorder |
| [JSON Mode and Tool Calls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/json_mode_and_tool_calls.md) | Validates schemas and fences tool outputs | Free text in tool responses, invalid JSON, missing fields |
| [Citation First](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md) | Enforces cite then explain with required fields | Citations missing or point to the wrong snippet |
| [Anti Prompt Injection Recipes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/anti_prompt_injection_recipes.md) | Ready to paste defenses for common exploits | Hidden instructions override system prompt |
| [Memory Fences and State Keys](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md) | Prevents cross turn or cross agent overwrite | Agents rewrite each other’s memory, history leaks |
| [Tool Selection and Timeouts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/tool_selection_and_timeouts.md) | Picks tool deterministically, adds timeouts | Loops, stalls, or wrong tool chosen |
| [Template Library (minimal)](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/template_library_min.md) | Small set of reusable prompt blocks | Inconsistent phrasing across agents or runs |
| [Eval Prompts and Checks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/eval_prompts_and_checks.md) | Deterministic acceptance gates | “Looks better” but no stable way to prove it |

---

## When to use

- Citations point to the wrong snippet or disappear after retries.  
- JSON mode produces invalid objects or tool calls stall in loops.  
- Role text bleeds into user content after a small template change.  
- Long chains smear topics when you reorder headers.  
- Agents overwrite each other’s memory without fences.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe convergent across three paraphrases and two seeds  
- E_resonance flat on long windows

---

## Map symptoms to structural fixes

| Symptom | Likely cause | Open this |
|---|---|---|
| Wrong meaning despite high similarity | Metric or analyzer mismatch | [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Citations inconsistent or missing after retries | No traceability schema enforced | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| JSON breaks or tool responses contain free text | Tool schema not fenced, logic collapsed | [JSON Mode and Tool Calls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/json_mode_and_tool_calls.md) · [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/prompt_injection.md) |
| Answers flip when you reorder headers | Header order changes λ state | [System vs User Role Order](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/system_user_role_order.md) · [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) |
| Long chains drift or stall | Entropy overload in long windows | [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) |
| Hybrid retrieval worse than single retriever | Reranker or query split issue | [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Hallucination re entry after correction | Snippet contract missing, weak anchors | [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) |

---

## Fix in 60 seconds

1) **Measure ΔS**  
Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe λ_observe**  
Vary k and the order of prompt headers. If λ flips, lock the schema and clamp variance with BBAM.

3) **Apply the right module**  
- Missing or wrong citations → **Citation First** + **Retrieval Traceability**  
- JSON tool drift or invalid outputs → **JSON Mode and Tool Calls**  
- Role bleed or policy mixing → **System vs User Role Order**  
- Multi agent loops or overwrites → **Memory Fences and State Keys**  
- Tool indecision or hangs → **Tool Selection and Timeouts**

4) **Verify**  
Run **Eval Prompts and Checks** on three paraphrases and two seeds.  
Ship only if ΔS ≤ 0.45 and coverage ≥ 0.70.

---

## Copy paste diagnostic prompt

```txt
You have TXT OS and the WFGY Problem Map loaded.

My prompt assembly issue:
- symptom: [one line]
- traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ on 3 paraphrases

Report:
1) failing layer and why,
2) which exact page to open from Prompt Assembly,
3) minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) a reproducible check to verify the fix.
Use BBMC, BBPF, BBCR, BBAM when relevant.
````

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
