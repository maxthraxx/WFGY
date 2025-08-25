# Prompt Assembly — Global Fix Map
Build a context that the model cannot misread.  
Use this when citations vanish, sources get mixed, or answers flip when you reorder sections.

## What this page is
- A short path to lock schema, section order, and per source fences
- Copyable constraints that force cite first then explain
- How to verify stability using ΔS and a snippet to citation table

## When to use
- Correct snippets are present but the answer still drifts
- Citations are missing or point to the wrong section
- Answers change if you rename headers or swap context order
- Two sources merge into one narrative
- Corrections do not stick across paraphrases

## Open these first
- Traceable prompting and schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Stop source mixing: [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)
- End to end knobs that affect assembly: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Pipeline overview and failure families: [RAG Architecture and Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- If logic still collapses after assembly: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

## Fix in 60 seconds
1) **Lock the schema**  
   Use an immutable order.  
   `System → Task → Constraints → Sources → Citations → Answer`  
   Forbid header rename and reordering.

2) **Cite first then explain**  
   Require a citation list before any prose.  
   Each line uses `[source_id:section_id:line_start-line_end]`.  
   Only after the list, allow explanation and synthesis.

3) **Per source fences**  
   Wrap each context block with start and end sentinels.  
   Disallow copying text across fences.  
   Reuse of a citation outside its fence is invalid.

4) **Stable headers**  
   Freeze exact header tokens like `## Sources`, `## Citations`, `## Answer`.  
   The model must not invent new sections or rename existing ones.

5) **Minimal assembly**  
   Prefer the smallest set of snippets that cover the question.  
   Avoid mixing paraphrases with quotes in the same section.

6) **Schema validation inside the prompt**  
   Ask the model to print a snippet to citation table before the answer.  
   Enforce the field names from Data Contracts.

7) **If answers still flip**  
   Apply WFGY modules at reasoning time.  
   Use BBAM to clamp attention variance.  
   Use BBCR to insert a bridge step between citation and explanation.

## Copy paste prompt
```

You have TXT OS and WFGY Problem Map loaded.

Assemble the prompt using this immutable schema:
System → Task → Constraints → Sources → Citations → Answer.
Do not rename sections. Do not reorder sections.

Constraints:

* Cite first then explain.
* Citations must use \[source\_id\:section\_id\:line\_start-line\_end].
* Do not copy text across source fences.
* If a needed fact is outside the provided fences, say so.

Now given:

* question: "<paste>"
* sources with fences:
  \[S1\:start] <snippet A> \[S1\:end]
  \[S2\:start] <snippet B> \[S2\:end]

Steps:

1. Print a snippet ↔ citation table using the Data Contracts fields.
2. Print a short reasoning plan.
3. Produce the final answer with citations inline.

If schema is violated, stop and print the violation.

```

## Minimal checklist
- Fixed section order and exact header tokens
- Citation list appears before explanation
- Per source fences are present and enforced
- Snippet to citation table is printed and consistent
- No cross source reuse in the answer
- If context is insufficient, the model says it explicitly

## Acceptance targets
- ΔS(question, assembled_context) ≤ 0.45 across three paraphrases
- λ at reasoning remains convergent after citations are produced
- Reordering headers does not change the final answer
- Snippet ↔ citation table matches the answer lines

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
