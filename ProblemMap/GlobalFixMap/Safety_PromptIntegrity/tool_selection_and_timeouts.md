# Tool Selection and Timeouts — Guardrails and Fix Patterns

A practical guide to choose the right tools, bound their behavior, and prevent loops or silent stalls.  
Use this page when the model calls the wrong tool, produces prose instead of JSON, or keeps retrying a dead endpoint.

---

## When to use this page
- Tool calls loop or never return useful output.  
- The wrong tool is picked even when inputs match another tool better.  
- JSON mode breaks and the model replies with natural language.  
- Latency spikes after deploy or under bursty traffic.  
- Multi-agent plans hang on a blocked tool or long queue.

---

## Open these first
- Threat model and defenses: [prompt_injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/prompt_injection.md)  
- Role hygiene and separation: [role_confusion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/role_confusion.md)  
- JSON mode and schema locks: [json_mode_and_tool_calls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/json_mode_and_tool_calls.md)  
- Memory isolation: [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/memory_fences_and_state_keys.md)  
- Cite then explain discipline: [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/citation_first.md)  
- RAG traceability and contracts: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Live ops and debugging: [ops/live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Core acceptance
- Tool selection accuracy ≥ 0.98 on a 50-case gold set.  
- P95 tool latency within budget for each class: HTTP, search, code-run, vector.  
- Zero unbounded calls. Every tool has a timeout, retry policy, and idempotency key.  
- Invalid JSON rate < 0.5 percent with strict schema validation.  
- ΔS(question, cited snippet) ≤ 0.45 after tool orchestration. λ remains convergent on two seeds.

---

## Fix in 60 seconds

1) **Lock the allowlist**  
   Only expose tools that are needed for the task. Everything else is unavailable.

2) **Set hard time budgets**  
   Per-tool timeout and total orchestration budget. Expose both to the model.

3) **Validate I/O**  
   Enforce JSON schema on inputs and outputs. Reject and re-ask on failure.

4) **Apply backoff and caps**  
   Retry with capped attempts and jitter. Never infinite retries.

5) **Observe ΔS and λ**  
   If ΔS stays high while tool usage changes, prefer rerankers or different retriever before trying new tools.

---

## Typical symptoms → exact fix

| Symptom | Likely cause | Open this |
|---|---|---|
| The model picks a browser tool for local facts | Tool palette too broad, weak routing | [json_mode_and_tool_calls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/json_mode_and_tool_calls.md), [role_confusion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/role_confusion.md) |
| Tool loops after a 429 | Missing backoff and idempotency | [ops/debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md) |
| RAG tool returns wrong snippet | Metric or index mismatch | [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| JSON mode breaks and prose appears | Schema not enforced | [json_mode_and_tool_calls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/json_mode_and_tool_calls.md) |
| Multi-agent stalls at a tool step | Memory overwrite or missing fence | [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/memory_fences_and_state_keys.md), [Multi-Agent_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) |

---

## Minimal policy you can paste

Use this inside your system prompt or orchestrator config.

```txt
Tool policy:
- Only use tools from this allowlist and only for their stated purpose.
- Every tool call must be a single JSON object that validates the schema shown with the tool.
- If a tool times out or returns an error, try at most 2 retries with exponential backoff (base 1.7) and jitter.
- Respect the total time budget: {total_budget_ms} for all tool usage in this request.
- Do not chain tools unless the previous tool returned a schema-valid result.
- If no tool is suitable, answer without a tool and say which tool would have been required.
````

---

## Orchestrator defaults

Set these once. Keep them consistent across environments.

* **Timeouts**
  HTTP: 8–12 s per call.
  Vector search: 2–4 s.
  Browser or scraping: 10–20 s with hard cap.
  Code-run or sandbox: 20–40 s.

* **Retries**
  429, 503, connection reset. Maximum 2 retries with jitter. No retries for 4xx other than 429.

* **Idempotency**
  `idempotency_key = sha256(tool_name + args_hash + mem_state_hash)` before any side effect.

* **Budgets**
  Per-tool budget and a global budget. When global budget remains < 15 percent, stop calling tools and return the best answer with citations.

* **Cancellation**
  Cancel slower duplicates. Keep the fastest successful call for a given tool class.

---

## Routing hints for model

Give the model a short rubric so it can choose tools correctly.

```txt
Routing rubric:
- Retrieval or citation needed → call retriever tool first. Then cite, then reason.
- Need ordering control for a long candidate list → use reranker instead of asking the LLM to sort.
- When the input already contains the answer text → do not search, answer with citations.
- Use browser only when the answer depends on a fresh webpage and the site is in the allowlist.
- If tool returns non-JSON or missing fields → request a retry with the same schema.
```

See also: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) · [citation\_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/citation_first.md)

---

## Red team probes

Run these with three paraphrases. Expect identical safe behavior.

* 429 storm on the primary retriever.
* Browser returns HTML with script tags and meta refresh.
* Vector store latency spikes to 6 s P95.
* Tool returns prose inside a JSON field.
* Agent handoff where the second agent tries to change the tool palette.

If any probe flips λ or breaks JSON, open:
[json\_mode\_and\_tool\_calls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/json_mode_and_tool_calls.md) ·
[role\_confusion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/role_confusion.md)

---

## Runbook snippet

Use this during incidents.

1. Check live metrics: error rate by tool, P95 latency, timeout count, retry count.
2. Triage the worst tool. Reduce k, switch to reranker, or skip non-critical tools.
3. Apply tighter timeout for the failing tool and raise backoff base.
4. Flip to a warm standby retriever or cache layer.
5. Re-run the gold probes. Ship only after acceptance targets pass.

Related ops pages: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

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

