# Parabola — Automation Guardrails

A focused repair guide for teams building pipelines with **Parabola**.
Goal is simple: stop silent data drift, schema breaks, pagination traps, and idempotency bugs without changing your infra. Use the steps and acceptance targets below to make the fix repeatable.

---

## What this page is

* A quick path to locate the failing layer in your Parabola flow: input → transform → join → export → webhook/API.
* Structural fixes that survive retries, partial failures, and schema changes.
* Exact links into the WFGY Problem Map where the permanent patch lives.

---

## When to use this page

* CSVs import but downstream counts are off.
* A join explodes row counts or drops keys.
* Pagination or rate limits make exports flaky.
* Webhook tasks replay and create duplicates.
* Column names change and flows keep “succeeding”.
* Schedules “succeed” yet the destination is stale.

---

## Open these first

* Data contracts and citations for rows and fields:
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* Live monitoring and run-debug checklists for pipelines:
  [Live Monitoring for RAG and Pipelines](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) ·
  [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

* Boot order and “first run” failures that look like Parabola bugs:
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) ·
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* Vectorstore and retrieval acceptance targets you may export into:
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Fix in 60 seconds

1. **Lock a data contract for every flow edge**

   * Define required columns, types, nullability, and primary key.
   * Put the contract in the flow description and in a sidecar `.json`.
   * Reject on contract break, do not “coerce”.

2. **Make writes idempotent**

   * Add an **idempotency key** from source primary key + run id.
   * Upsert on key. Soft-delete on tombstone streams.

3. **Tame pagination and rate limits**

   * Use explicit page cursors where available.
   * Backoff with jitter and a cap. Persist last good cursor.
   * Fail closed on partial pages, resume from cursor.

4. **Stabilize joins**

   * Pre-dedupe on join keys.
   * Count rows before and after. Warn if ratio not in \[0.9, 1.1] unless configured.
   * For one-to-many, aggregate first, then join.

5. **Quarantine bad rows**

   * Sink violations to a “dead-letter” sheet with reason code.
   * Never drop silently.

6. **Schedule with proof**

   * Record run hash = inputs’ checksums + step graph rev.
   * A run is “good” only if the same hash reproduces.

---

## Common failure modes → exact fixes

| Symptom                                    | Root cause                                      | Open this fix                                                                                               |
| ------------------------------------------ | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Row counts drift after CSV import          | Type coercion and null handling change silently | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)                 |
| Duplicates after webhook retries           | No idempotency key on destination               | [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)             |
| Join multiplies rows unexpectedly          | Non-unique keys or many-to-many join            | [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)       |
| Exports fail intermittently                | Pagination or rate-limit handling missing       | [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)             |
| First run looks “green” but index is empty | Boot order wrong, destination not ready         | [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)         |
| Scheduled run “succeeds” but target stale  | No acceptance gates or version checks           | [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)       |
| Downstream retrieval pulls wrong docs      | Snippet schema absent, traceability missing     | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |

---

## Minimal triage checklist

* Inputs: file counts and checksums logged.
* Contract: columns, types, PK declared and enforced.
* Dedupe: before join, after import.
* Idempotency: deterministic key on write path.
* Pagination: cursor persisted between attempts.
* Quarantine: every rejection is stored with reason.
* Acceptance: target store has post-write assertions.

---

## Copy-paste prompt to ask the AI

```txt
I uploaded TXT OS and Problem Map.

Context: Parabola pipeline failing.

- symptom: [brief]
- sources: [csv/api names]
- current guards: [contract? idempotency? pagination? join?]

Tell me:
1) which layer is failing and why,
2) which exact WFGY page to open,
3) the smallest patch to make writes idempotent and schema-locked,
4) how to verify with row counts and hashes.

Use BBMC/BBPF/BBCR/BBAM if relevant.
```

---

## Acceptance targets

* Contract violations are zero.
* Duplicate writes are zero across retries.
* Join ratio stays within configured band or the run blocks.
* Pagination resumes from last cursor with no missing pages.
* Destination post-write assertions pass on every schedule.
* Re-running with same inputs reproduces identical hash.

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
