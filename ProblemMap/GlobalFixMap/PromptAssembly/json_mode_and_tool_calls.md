# JSON Mode and Tool Calls · Prompt Assembly

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **PromptAssembly**.  
  > To reorient, go back here:  
  >
  > - [**PromptAssembly** — prompt engineering and workflow composition](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A field guide to keep JSON mode stable and tool calls safe. Use this page to clamp the schema, stop looped tools, and keep outputs auditable across providers.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Traceability schema for snippets: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contract the payload: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Reasoning collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Prompt injection fences: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
* Multi agent conflict map: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)
* Live ops and debug: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## When to use this page

* JSON mode returns invalid or partial objects.
* Tool calls arrive with missing or extra fields.
* The model mixes tool output with prose.
* Tools loop or stall without timeouts.
* Role text bleeds into user turns and corrupts parsing.
* Outputs differ between seeds for the same inputs.

## Acceptance targets

* JSON parse success rate ≥ 0.99 across three paraphrases.
* Tool call validity ≥ 0.98 by schema check.
* Zero side effects on failed parse.
* λ remains convergent across three paraphrases and two seeds.
* ΔS(question, retrieved) ≤ 0.45 when the answer cites corpus evidence.

## Map symptoms to structural fixes

* Invalid JSON or mixed prose.
  → Lock format with a contract and a validator. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

* Tool arguments drift or contain free text.
  → Use strict argument schemas and echo the schema in every step. See [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

* Tools loop or wait on each other.
  → Add timeouts and split memories by namespace and revision. See [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

* Answers flip between runs for the same input.
  → Reorder headers and clamp variance with BBAM. Verify with [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Citations missing or point to the wrong snippet.
  → Enforce cite then explain. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

## Fix in 60 seconds

1. **Clamp the JSON contract**
   Define a single object shape. Disallow extra fields. Reject prose outside the object.

2. **Echo the tool schema**
   In every step the model must restate the allowed tools and their argument shapes. Reject any call that does not match.

3. **Add timeouts and retries**
   Each tool has `timeout_ms` and at most `N` retries with exponential backoff. Abort on chain length overrun.

4. **Observability probes**
   Log parse success, tool validity, ΔS, and λ. Trip a circuit if parse rate drops under 0.98 in a five minute window.

5. **No side effects before validation**
   Validate JSON and tool calls first. Only then commit external writes.

## Copy paste blocks

### A. JSON answer contract

```
You must output a single JSON object. No Markdown. No code fences. No commentary.

Schema:
{
  "answer": "string",
  "citations": [{"source_url": "string", "snippet_id": "string"}],
  "tool_calls": [{"name": "tool_name", "args": { ... }}],
  "metrics": {"lambda_state": "->|<-|<>|x", "delta_s": 0.00}
}

Rules:
- Do not include fields that are not in the schema.
- Strings must not contain unescaped newlines.
- If you cannot satisfy the schema, return:
  {"answer": "", "citations": [], "tool_calls": [], "metrics": {"lambda_state":"x","delta_s":1.0}}
```

### B. Tool protocol guard

```
Allowed tools:
1) "web_fetch": args = {"url": "string"}
2) "vector_search": args = {"query": "string", "k": 5}
3) "write_kv": args = {"key":"string","value":"string","ttl_sec": 600}

Contract:
- Each tool call must match the exact args shape.
- Never put narrative text into args.
- Max tool calls in one turn: 3
- Per call timeout_ms: 15000
- Retries: up to 2 with capped backoff
```

### C. Validator stub

```
Step 1: parse JSON strictly. If parse fails, stop and return a fix tip.
Step 2: check extra fields. If any, reject.
Step 3: validate each tool call against the schema list.
Step 4: only after validation, run tools in order.
Step 5: log {parse_ok, tool_valid, delta_s, lambda_state}.
```

### D. Role header clamp

```
System:
- Policies and schema live here only. User turns contain tasks and questions only.
- Cite then explain. Refuse to answer without citations when the task requires evidence.
- Echo the current tool schema before any tool call.

User:
- Provides task and question.
```

## Deep diagnostics

* **Three paraphrase test**
  Ask the same question three ways. Parse rate and tool validity should remain ≥ 0.98. If not, tighten the schema or reduce optional fields.

* **Anchor triangulation**
  Compare ΔS to the expected anchor section and to a decoy. If ΔS is close for both, rework chunking and rebuild index. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* **Chain length audit**
  If tool chains exceed safe length and entropy rises, split the plan and reconnect with a BBCR bridge. See [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

## Eval gates before ship

* JSON parse success ≥ 0.99 on a 50 case set.
* Tool validity ≥ 0.98 with negative cases included.
* Coverage ≥ 0.70 and ΔS ≤ 0.45 on evidence tasks.
* λ convergent across two seeds.
* Live probes green for one hour with zero side effects on rejects.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
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
