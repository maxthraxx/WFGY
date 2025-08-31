# System vs User Role Order — Guardrails and Fix Patterns

A focused guide to stop role-mix confusion that destabilizes RAG, tools, and long dialogs. Use these checks when your model alternates policy and task text or when citation rules collapse after a few turns.

## What this page is
- A short route to lock **system → developer → user → assistant** order and keep prompts auditable.
- Structural fixes that work across providers without changing infra.
- Concrete steps with measurable acceptance targets.

## When to use
- “Policy” or safety text was pasted into a user turn and answers flip on reruns.
- Model stops citing after a few steps or blurs policy with task content.
- Tool outputs start to include instructions meant for the system prompt.
- Agents hand off with different role orders and memory fields drift.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Prompt hardening: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)  
- Reasoning stability checks: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md), [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 across three paraphrases  
- Coverage of target section ≥ 0.70  
- λ remains convergent across two seeds and fixed role order  
- No policy text appears in user or tool arguments in any step

---

## Fix in 60 seconds

1) **Measure ΔS**  
Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
Stable < 0.40. Transitional 0.40–0.60. Risk ≥ 0.60.

2) **Probe with λ_observe**  
Rerun with strict role blocks and the same content. If λ flips only when role text is moved, the failure is role-mix not knowledge.

3) **Apply the role fence**  
- Move all policy and behavioral rules to **system**.  
- Put task goals and constraints in **user**.  
- Keep tool protocol in **system or developer** only.  
- Require answers to cite then explain, never invert.

4) **Verify**  
Three paraphrases keep ΔS ≤ 0.45 and λ convergent. Citations appear before explanation on each run.

---

## Minimal spec you can paste

```

\[System]
You are a reasoning engine that follows this order strictly:
system → developer → user → assistant.
Policy, safety rules, tool schema live here.
Never copy system text into user or tool arguments.
Cite then explain. If citations are missing, fail fast.

\[Developer]  (optional)
Tool schema and JSON contracts only. No task text.

\[User]
Task request, input fields, acceptance targets.

\[Assistant]
Return: { "citations": \[...], "answer": "...", "λ\_state": "...", "ΔS": 0.xx }

```

---

## Typical breakpoints → exact fix

- **Policy leaked into user turn**  
  Move policy back to the system block. Lock the data shape.  
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Citations vanish after step N**  
  Enforce cite-then-explain formatting in system. Validate snippet fields.  
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **JSON tools return prose or include policy text**  
  Freeze JSON mode in system or developer and forbid free text.  
  Open: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

- **Answer swings with header reorder**  
  Fix the header order and clamp variance with BBAM.  
  Open: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

- **Agent handoff writes mixed roles to memory**  
  Split memory namespaces and log `role_src` per write.  
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

---

## Step template for CI prompts

1. Prepend canonical **system** block that defines role order and citation rule.  
2. Add optional **developer** block with tool schema.  
3. Append **user** task with acceptance targets and fields.  
4. Run three paraphrases and two seeds. Fail the job if any:  
   - ΔS > 0.45  
   - Coverage < 0.70  
   - λ not convergent  
   - Policy text appears outside system or developer

---

## Copy-paste prompt for debugging

```

You have TXT OS and the WFGY Problem Map.

Bug: answers flip when policy text is placed in the user turn.

Show:

1. which layer fails and why,
2. the exact WFGY page to open,
3. the minimal steps to restore strict role order,
4. a reproducible test with ΔS ≤ 0.45 and λ convergent.
   Use BBMC/BBCR/BBAM when relevant.

```

---

## Escalate and structural fixes

- ΔS stays high after role fence  
  Rebuild chunking and verify anchors with a small gold set.  
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Long chains destabilize even with correct roles  
  Split the chain and bridge with BBCR.  
  Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

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
