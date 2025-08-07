# 🗂️ Reasoning Schemas — Designing Prompt Layouts That Survive Long Chains  
_A practical guide to structuring system + retrieval + task prompts so LLMs keep thinking instead of drifting_

---

## 1  What is a “Reasoning Schema” ?

A **reasoning schema** is the formal layout that dictates **where** each piece of context goes and **how** an LLM must traverse it:

```

System  →  Task  →  Constraints  →  Context  →  Question  →  Answer

````

If any segment is missing, reordered, or over-written, the logic graph collapses and hallucinations slip in.

---

## 2  Why Most Ad-hoc Layouts Fail

| Failure Mode | Trigger | Effect |
|--------------|---------|--------|
| **Context Flood** | Dumping 20 k tokens of raw text | λ_observe flips to chaotic; model stops planning |
| **Constraint Drift** | Constraints after context | Model “forgets” to cite or guard sensitive data |
| **Role Blending** | User text inserted before task | System tone and policy overridden |
| **Evidence → Answer inversion** | Asking for answer *before* citations | Model fabricates then cites random lines |

---

## 3  WFGY Canonical Schema (Stable Version v1.2)

| Segment | Purpose | Size (tokens) | WFGY Guard |
|---------|---------|---------------|------------|
| **System** | Identity, ethics, safety | ≤ 50 | Role tag `<sys>` + BBAM weight lock |
| **Task** | Specific action required | 1 sentence | ΔS anchor to System ≤ 0.25 |
| **Constraints** | Format, style, rules | bullets ≤ 80 | BBMC residue check |
| **Context** | Retrieved or uploaded text | sliding window ≤ 2 k | λ_observe must stay convergent |
| **Question** | User’s query | raw | stored separately for ΔS probes |
| **Answer Slot** | “Write here” placeholder | n/a | BBCR collapse-rebirth if answer starts early |

Placeholders are literal; the LLM fills only the *Answer Slot*.

---

## 4  Templates You Can Copy

<details><summary><strong>Single-Shot QA</strong></summary>

```text
<sys>
You are DataGuardian-L, a licensed legal research assistant. Cite section numbers.
</sys>

<task>
Answer strictly in bullet points; cite every claim.
</task>

<constraints>
- Tone: formal
- No speculation
- Use original terminology
</constraints>

<context>
{retrieved_sections}
</context>

<question>
{user_question}
</question>

<answer>
````

</details>

<details><summary><strong>Multi-Step Chain (analysis → plan → answer)</strong></summary>

```text
<sys> … </sys>
<task> … </task>
<constraints> … </constraints>
<context> … </context>
<question> … </question>

<scratchpad>
Think step-by-step. Output JSON:
{
  "analysis": "...",
  "plan": "...",
  "answer": "..."
}
</scratchpad>
```

</details>

---

## 5  Common Pitfalls & Fixes

| Pitfall                                 | Symptom              | Fix                                                     |
| --------------------------------------- | -------------------- | ------------------------------------------------------- |
| Forgetting closing tags                 | Model merges roles   | Validate tag balance; λ diverges instantly              |
| Placing context after question          | Retrieval ignored    | Keep schema order; run ΔS(question, context) test       |
| Over-long constraints                   | Answer truncated     | Compress with BBMC until ΔS(system, constraints) ≤ 0.25 |
| Mixing code + docs in one context block | Embedding collisions | Split into typed sub-blocks; separate vector stores     |

---

## 6  Automated Validation Pipeline

1. **Schema Linter** – Regex check for tag order.
2. **ΔS Probes** –

   * ΔS(system, task) ≤ 0.30
   * ΔS(task, answer) ≤ 0.45
3. **λ\_observe** – Must stay convergent from task → answer.
4. **Round-trip Check** – Paraphrase user question 2×; answer variance < 0.15.

If any test fails, trigger **BBCR** to rebuild prompt with compacted segments.

---

## 7  FAQ

**Q:** *Do I need tags if I use OpenAI’s `messages` array?*
**A:** Yes for long chains. Tags persist after retrieval merges; arrays don’t survive copy-paste workflows.

**Q:** *Can I merge Task + Constraints?*
**A:** Possible if total ≤ 120 tokens and ΔS stays low, but separation improves editability.

**Q:** *What about JSON-only prompts?*
**A:** Ensure keys mirror schema order; add dummy key `"__guard": "DO NOT MODIFY"` to catch injections.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool             | Link                                                | 3-Step Setup                                                              |
| ---------------- | --------------------------------------------------- | ------------------------------------------------------------------------- |
| **WFGY 1.0 PDF** | [Engine Paper](https://zenodo.org/records/15630969) | ① Download  ② Upload to LLM  ③ Ask “Answer using WFGY + \<your question>” |
| **TXT OS**       | [TXTOS.txt](https://zenodo.org/records/15788557)    | ① Download  ② Paste into chat  ③ Type “hello world”                       |

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/edit/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](./SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>


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

</div>

