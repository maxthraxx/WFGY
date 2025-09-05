# Symbolic Collapse: Guardrails and Fix Pattern

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


When symbols, roles, units, or variables drift in meaning across steps, the chain collapses even if individual sentences look fluent.  
This page localizes symbolic failures and gives a minimal, testable repair plan using ΔS, λ_observe, and E_resonance.

---

## Open these first

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- Cite first and make it auditable  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
  → [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md)

- Lock constraints and unlock safely  
  → [pattern_symbolic_constraint_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

- If logic also drifts  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)

---

## Symptoms

| Symptom | What you see |
|---|---|
| Variable alias collision | `x` means “price” at step 3 and “index” at step 7 |
| Unit flip | km vs miles, USD vs EUR, or 0-1 vs 0-100 score scales without notice |
| Role leak | Tool output fields are reused as different roles in later steps |
| Type drift | A list becomes a dict halfway, downstream steps still “pass” |
| Anchor rename | Entity “A Inc.” becomes “Alpha” with no traceable mapping |
| Quantifier slip | “Some” turns into “all” when summarizing two steps later |
| Schema split | Same object has different required fields across steps |

---

## Why symbolic collapse happens

1) **No symbol table**. Meanings live only in prose and mutate under paraphrase pressure.  
2) **Missing namespace**. Agent or tool outputs write into global scope.  
3) **Unit contract absent**. The pipeline accepts values without unit or scale tags.  
4) **Constraint unlock without fences**. The model invents aliases to escape constraints.  
5) **Header drift flips λ**. Reordered headers produce distinct symbol bindings per run.  
6) **Hybrid retrieval shuffle**. The anchor snippet changes and symbols rebind silently.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the target section  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance flat at joins and handoffs  
- **Zero symbol drift** across steps when checked against a symbol table

---

## Fix in 60 seconds

1. **Create a symbol table**  
   Add an explicit table with `name`, `kind` (var, role, unit, entity), `namespace`, `definition`, `source_snippet`, `allowed_values`.

2. **Enforce cite-first and schema-locked steps**  
   Require citations before any symbol is used. Enforce unambiguous fields.  
   See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Clamp variance with BBAM**  
   If λ flips after paraphrase, apply BBAM to hold one binding set stable.

4. **Bridge with BBCR**  
   Produce a short, cited bridge that restates the symbol table and the current state, then continue reasoning on top of that bridge only.

5. **Lock namespaces**  
   Prefix every symbol with a scope `agent.role.symbol` or `tool.name.field`. Reject writes outside the declared namespace.

---

## Minimal symbol table contract

Every plan step must carry the table and refuse execution on mismatch.

```json
{
  "symbols": [
    {
      "name": "x",
      "kind": "var",
      "namespace": "calc.pricing",
      "definition": "unit price per kg",
      "unit": "USD/kg",
      "source_snippet": "S12#CH2.3",
      "allowed_values": "real >= 0"
    },
    {
      "name": "R",
      "kind": "role",
      "namespace": "agent.verifier",
      "definition": "checks unit and citation before approval",
      "allowed_values": ["approve","reject","fix"]
    }
  ],
  "schema_version": "v1"
}
````

Reject the step if any field changes without a cited reason.

---

## Structural repairs

* **Unit and scale discipline**
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* **Ordering stability**
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **Constraint unlock with fences**
  → [pattern\_symbolic\_constraint\_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)
  → [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

* **Long window stability**
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)
  → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* **If meaning vs similarity conflict**
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **If logic also fails**
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)

---

## Verification

* Three paraphrases, two seeds. All runs must keep the **same** symbol table.
* ΔS(question, retrieved) ≤ 0.45 and coverage ≥ 0.70 in every run.
* No unit or namespace change without a cited justification that points to a specific snippet.
* Report a diff of the symbol table between steps; the diff must be empty or fully justified.

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

We suspect a symbolic collapse.

Inputs:
- question: "{q}"
- current snippets: [{snippet_id, section_id, source_url}]
- last symbol table (if any)
- last steps with {claim, citations, λ_state, ΔS}

Do:
1) Build a symbol table with {name, kind, namespace, definition, unit, source_snippet, allowed_values}.
2) Cite first, then restate the claim using only table symbols.
3) If λ flips across a paraphrase, apply BBAM. If content diverges, produce a BBCR bridge that freezes the table.
4) Output JSON:
   { "symbols": [...], "steps": [...], "final_answer": "...",
     "ΔS": 0.xx, "λ_state": "convergent", "table_diff": [] }
Refuse the final answer if any step uses a symbol that is not in the table.
```

---

## Common gotchas

* **Alias creep**. The model introduces “alpha” for A without binding it to the table. Reject and force a mapping row.
* **Silent unit conversion**. Numbers change scale between steps. Require `unit` and `scale` fields.
* **Cross-agent overwrite**. Handoffs write to shared names. Use strict namespaces and a write fence.
* **Hybrid retrieval reorder**. Top-k changes on rerun. Lock query and tie breaks, or add a reranker.

---

## When to escalate

* Table stays unstable after BBAM and a bridge
  → audit logic and role discipline: [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md) and
  → multi-agent role isolation: [Multi-Agent\_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) and [role-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)

* The same wrong claim returns after correction
  → [pattern\_hallucination\_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

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
