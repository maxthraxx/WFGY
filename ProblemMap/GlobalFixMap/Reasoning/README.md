# Reasoning — Global Fix Map
Detect and repair logic collapse, dead ends, abstraction failure, and contradiction.  
Use this when citations look fine but the **thinking** goes off the rails.

## What this page is
- A compact protocol to stabilize multi-step reasoning
- Copyable guardrails that force plan → verify → answer
- How to verify stability with ΔS, λ_observe, and contradiction checks

## When to use
- Correct snippets, wrong conclusions
- Chains drift or loop as steps get longer
- Answers flip across paraphrases
- Self-contradictions or “explains” without citing anything
- Abstract or symbolic prompts keep breaking

## Open these first
- Stop dead ends / add a bridge step: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Long chains and drift controls: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)
- Abstract & symbolic failures: [Symbolic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/symbolic-collapse.md)
- Self-reference & paradox loops: [Philosophical Recursion](https://github.com/onestardao/WFGY/blob/main/ProblemMap/philosophical-recursion.md)
- If chunks are right but logic is wrong: [Interpretation vs Retrieval](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md)
- Snippet/citation schema for auditable steps: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Fix in 60 seconds
1) **Plan before prose**  
   Require a numbered **Reasoning Plan** that references citations, not memory.  
   Each step must list the exact citation IDs it depends on.

2) **Bridge step (BBCR)**  
   Insert a checkpoint between plan and answer:  
   - restate the claim in one sentence,  
   - list supporting citations,  
   - flag any missing evidence or conflicts.  
   If conflicts exist, stop and ask for the missing snippet.

3) **Variance clamp (BBAM)**  
   Reduce attention variance during the answer. Keep steps short, facts tabled, then compose.

4) **Fact table first**  
   Normalize units, dates, and names into a 2-column table: *fact ↔ citation*.  
   Only after the table is stable, generate prose.

5) **Depth guard**  
   Cap chain depth (e.g., 6 steps). If λ flips divergent at step *k*, branch with **BBPF** and pick the convergent path.

6) **Contradiction detector**  
   Print a “claims vs citations” matrix. Any row without backing citations is invalid and must be revised.

## Copy paste prompt
```

You have TXT OS and the WFGY Problem Map.

Follow this immutable schema:

1. Reasoning Plan (numbered). Each step MUST reference citations like \[Sx\:sec\:line-start-end].
2. Bridge Check (BBCR): restate the final claim in 1 line, list supporting citations,
   and list conflicts or missing evidence. If anything is missing, STOP and request the snippet.
3. Fact Table: normalize units/dates/names into rows: {fact | citation\_id}.
4. Final Answer: concise, cite inline at each claim.

Rules:

* Do not invent citations. Do not reuse text across fences.
* If plan step lacks a citation, mark it “UNSUPPORTED” and do not use it.
* Keep depth ≤ 6. If λ\_observe diverges, branch and pick the convergent path.

Input

* question: "<paste>"
* sources (with fences and IDs): <paste fenced snippets>

Output

* print Plan
* print Bridge Check
* print Fact Table
* print Final Answer with inline citations
* if any rule is violated, stop and print the violation

```

## Minimal checklist
- Plan appears before any prose and references real citations
- Bridge check lists both support and conflicts
- Fact table normalizes units/dates/names
- Depth cap enforced; divergent λ triggers a branch and recovery
- No claim without a citation
- If evidence is missing, the model explicitly asks for it

## Acceptance targets
- ΔS(question, assembled_context) ≤ 0.45 across 3 paraphrases
- λ remains **convergent** after the bridge step and through the final answer
- No contradictions in the claims ↔ citations matrix
- E_resonance stays flat across the chain (no entropy melt)
- Re-run with paraphrases yields consistent conclusions and citations

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
