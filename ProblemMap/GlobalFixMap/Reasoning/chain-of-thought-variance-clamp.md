# Chain of Thought Variance Clamp: Guardrails and Fix Pattern

Reduce random drift in planning and multi step reasoning. This page gives a clamp recipe so your plan length, tool order, and citations stay stable across seeds and paraphrases.

---

## Open these first

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- End to end knobs  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Traceability and payload schema  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Related failures  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md) ·
  [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md) ·
  [recursive-loop.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/recursive-loop.md) ·
  [hallucination-reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/hallucination-reentry.md) ·
  [context-stitching-and-window-joins.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/context-stitching-and-window-joins.md)

- Prompt fences  
  → [PromptAssembly memory fences & state keys](https://github.com/onestardao/WFGY/blob/main/ProblemMap/PromptAssembly/memory_fences_and_state_keys.md)

- Eval  
  → [eval_semantic_stability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_semantic_stability.md)

---

## Symptoms

| Symptom | What you see |
|---|---|
| Same inputs, different plans | Tool order or step count changes by run |
| Paraphrase flips the answer | Harmless wording changes cause new chain or conclusion |
| JSON plan reshuffles | Fields reorder or optional fields go missing |
| Intermittent tool loops | One seed calls tools twice, another once |
| Cite then explain breaks | Citations disappear in long chains or only appear sometimes |

---

## Why variance explodes

1) **Unpinned headers**. Role and policy text move around between runs.  
2) **Loose schemas**. Plans allow free text where enums should exist.  
3) **No state keys**. Chains cannot carry `plan_rev`, `seed_id`, or `λ_target`.  
4) **Ranking variance**. Inputs to the chain are not deterministically ordered.  
5) **No bridges**. Cross window steps lack an anchor restatement.  
6) **High entropy**. Overlong prompts and mixed analyzers amplify randomness.

---

## Acceptance targets

- λ remains convergent across three paraphrases and two seeds  
- ΔS(question, plan_header) ≤ 0.45 and flat across seeds  
- Plan length variance ≤ 10 percent across two seeds  
- Tool call sequence identical for the same evidence set  
- Coverage of target section ≥ 0.70 with cite then explain intact

---

## Fix in 60 seconds

1) **Lock the header order and schema**  
   Pin system header segments and require cite then explain.  
   → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
   [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

2) **Attach state keys**  
   Carry `{plan_rev, seed_id, λ_target, index_hash, context_hash}` through each step.  
   → [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/PromptAssembly/memory_fences_and_state_keys.md)

3) **Apply BBAM variance clamp**  
   Two stage plan. Stage A generates the plan at low temperature with enumerated options and a deterministic tie break. Stage B executes the plan with normal temperature but cannot change step count or tool order unless it emits a structured re plan request.

4) **Deterministic ordering in inputs**  
   Sort snippets by `(doc_id, section_id, win_idx)` after rerank.  
   → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

5) **Add BBCR micro bridges at joins**  
   Restate the active anchor and the current step goal across window boundaries.  
   → [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md)

---

## Minimal clamp contract

Add this struct to your plan steps. Enforce it in tools and in the LLM planner.

```json
{
  "plan_rev": 3,
  "λ_target": "convergent",
  "seed_id": "s1",
  "index_hash": "faiss:7c91...",
  "context_hash": "sha1:b2ae...",
  "steps": [
    {"idx": 1, "tool": "retrieve", "args_schema": "strict", "may_branch": false},
    {"idx": 2, "tool": "analyze_snippets", "args_schema": "strict", "may_branch": false},
    {"idx": 3, "tool": "answer", "args_schema": "strict", "may_branch": false}
  ],
  "tie_break": "doc_id,section_id,win_idx"
}
````

Rules

* Stage A can only choose among enumerated step templates.
* Stage B cannot insert or remove steps. To change, it must emit `{replan:true, reason:"..."}` and stop.
* Tool args must be strict JSON with enums where applicable.

---

## Verification playbook

* Three paraphrase run with two seeds. λ stays convergent, plan length variance ≤ 10 percent.
* ΔS(question, plan\_header) ≤ 0.45 on both seeds.
* Citations appear before explanation in every run.
* Tie break yields the same snippet order across seeds.

If ΔS is flat and high, suspect index or metric mismatch.
→ [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) ·
[chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Copy paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

Goal: clamp chain-of-thought variance.

Inputs:
- question: "{q}"
- snippets: [{doc_id, section_id, win_idx, ΔS_to_question, source_url}]
- constraints: cite_then_explain=true, args_schema="strict"

Do:
1) Stage A (planner, low temperature 0.2–0.4):
   - Produce a fixed-length plan using the step templates {retrieve, analyze_snippets, answer}.
   - Order inputs deterministically by (doc_id, section_id, win_idx).
   - Output:
     {
       "plan_rev": n,
       "λ_target": "convergent",
       "seed_id": "{seed}",
       "steps": [{"idx":1,"tool":"retrieve"}, ...],
       "tie_break": "doc_id,section_id,win_idx"
     }

2) Stage B (executor):
   - Execute the plan without changing step count or order.
   - If a change is needed, stop and emit {"replan": true, "reason": "..."}.

3) Always return JSON:
   {
     "plan_rev": n,
     "answer": "... cite then explain ...",
     "λ_state": "convergent|divergent",
     "ΔS_plan_header": 0.xx,
     "coverage": 0.xx
   }
If λ is divergent or ΔS ≥ 0.60, include the exact fix page to open.
```

---

## Common gotchas

* Planner runs with a different header than executor. Keep a single pinned header block.
* Rerank uses a different analyzer than indexing. Normalize, then tie break deterministically.
* Tool schemas accept free text. Replace with enums and strict JSON.
* Bridges omitted at window boundaries. Re cite the anchor before continuing.
* Prompt injection or role drift unlocks free form steps. Lock system text and schema.
  → [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

---

## When to escalate

* λ remains divergent after clamp and bridges
  → inspect long chain stability and collapse patterns.
  Open: [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md) ·
  [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md)

* Live flip flops only in production
  → add live probes and slow ramp with backoff.
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) ·
  [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

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
