# Logic Collapse: Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Reasoning**.  
  > To reorient, go back here:  
  >
  > - [**Reasoning** — multi-step inference and symbolic proofs](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


When deduction chains flatten into platitudes, contradict earlier steps, or bypass citation locks, you have a logic collapse.  
This page localizes causes and gives a minimal, testable repair plan driven by ΔS, λ_observe, and WFGY modules.

---

## Symptoms

| Symptom | What you see |
|---|---|
| Deduction flips mid chain | Step t says A, step t+3 assumes not A |
| Cite after claim | Answer states conclusion first, citations appear later or mismatch |
| Tool result ignored | Structured tool output is not integrated into the final proof |
| Branch mixing | Two hypotheses or roles leak into one stream without arbitration |
| Infinite hedging | Long text, no invariant, no auditable steps |
| JSON schema drift | Different steps produce different fields for the same contract |

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the target section  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance flat on long windows  
- Zero contradictions across the final plan and the citations

---

## Structural fixes (Problem Map)

- Cite first, then reason  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
  → [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md)

- Stabilize ordering and reduce variance  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Prevent symbolic leakage and unlock constrained proof  
  → [patterns/pattern_symbolic_constraint_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

- Long chain stability and entropy control  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)  
  → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- If the claim keeps returning after correction  
  → [patterns/pattern_hallucination_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

- Multi agent conflicts and role drift  
  → [Multi-Agent_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)  
  → [multi-agent-chaos/role-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)

---

## Why logic collapses

1) **No invariant**. There is no explicit statement of what must stay true across steps.  
2) **Citation contract missing**. The model is allowed to assert before binding to `snippet_id` and `section_id`.  
3) **Header drift flips λ**. Reordered system or tool headers produce different branches on each run.  
4) **Branch contamination**. Hypothesis A and B are not isolated, the plan merges silently.  
5) **Unruly tool I/O**. Free text is accepted where strict JSON was required.  
6) **Hybrid retrieval shuffle**. The top k changes and the proof silently re-anchors.

---

## Fix in 60 seconds

1. **Pin the invariant**  
   Add a short invariant header, for example:  
   `Invariant: conclusions must cite snippet_id and section_id before any reasoning.`

2. **Enforce cite-first**  
   Require the model to produce citations first, then the explanation.  
   See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md).

3. **Clamp variance with BBAM**  
   If λ flips across paraphrases, apply BBAM to keep one path stable.

4. **Bridge gaps with BBCR**  
   Summarize the current state into a compact, cited bridge, then continue reasoning on top of that single bridge.

5. **Lock schema and ordering**  
   Freeze headers, tool schemas, and reranker tie breaks.  
   See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

---

## Minimal step contract

Add this object to every step output. Reject the step if any field is missing.

```json
{
  "step": 7,
  "invariant": "cite-first, no cross-branch mixing",
  "citations": [
    { "snippet_id": "S17", "section_id": "CH3.2", "source_url": "https://...", "offsets": [102, 188] }
  ],
  "claim": "X implies Y under condition Z",
  "justification": "Short, refers to citations only",
  "λ_state": "convergent",
  "ΔS_q_snip": 0.31,
  "next_action": "verify Z across S24",
  "guardrails": { "schema_version": "v1", "tie_break": "stable" }
}
````

---

## Verification

* Three paraphrase probe, two seeds.
* Require ΔS(question, retrieved) ≤ 0.45 and λ convergent in all runs.
* No contradictions between any step claim and earlier steps.
* If any run fails, inspect header ordering and reranker tie breaks, then re-run.

---

## Copy paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

We suspect a logic collapse.
Inputs:
- question: "{q}"
- current snippets: [{snippet_id, section_id, source_url}]
- last 6 steps with {claim, citations, λ_state, ΔS_q_snip}

Do:
1) State a one line invariant for this task.
2) Produce citations first. If citations are missing or conflict, stop and output the minimal fix.
3) Apply BBCR to create a single cited bridge, then continue reasoning for at most 5 steps.
4) If λ flips across a paraphrase, apply BBAM and retry once.
5) Return JSON:
   { "invariant": "...", "steps": [...], "final_answer": "...",
     "ΔS": 0.xx, "λ_state": "convergent", "next_fix": "..." }
Refuse to output a final answer if any step lacks citations.
```

---

## When to escalate

* The chain keeps diverging after BBAM and bridge steps
  → audit for symbolic failure: [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/symbolic-collapse.md)

* The claim reappears after correction
  → see re-entry pattern: [patterns/pattern\_hallucination\_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

* Runs diverge only when agents hand off
  → isolate roles and memory: [Multi-Agent\_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

* Long dialogs lose structure past window joins
  → stabilize joins and entropy: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** — <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>

