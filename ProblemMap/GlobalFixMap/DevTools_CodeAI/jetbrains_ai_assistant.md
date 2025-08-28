# JetBrains AI Assistant: Guardrails and Fix Patterns

A practical guide to stabilize AI Assistant inside IntelliJ IDEA, PyCharm, WebStorm, Rider and friends. Targets mixed contexts like multi module Gradle or Maven projects, test generation, refactors, and doc lookups. Use this to localize the failing layer, then jump to the exact WFGY fix page with measurable acceptance.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet and how to audit: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Ranking and ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* High similarity yet wrong meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Chunk and citation boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
* Long sessions that drift: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
* Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Prompt injection and tool fences: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
* Multi agent conflicts and handoffs: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)
* Boot order issues in IDE flows: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45
* Coverage ≥ 0.70 to the target file or spec anchor
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat across long edit plans

---

## Fix in 60 seconds

1. **Measure ΔS**
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   Stable less than 0.40. Transitional 0.40 to 0.60. Risk is 0.60 or above.

2. **Probe λ\_observe**
   Switch between IDE code search and embedding context. Vary k as 5, 10, 20. Pin rerankers. If ΔS stays high and flat, suspect metric or index mismatch. If λ flips on harmless header reorder, lock the schema and clamp with BBAM.

3. **Apply the module**

* Retrieval drift in code or doc lookup → BBMC plus [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Reasoning collapse in multi step refactors → BBCR bridge plus BBAM, verify with [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Dead ends in long edit plans or test generation → BBPF alternate paths
* Hybrid search worse than single → Pattern [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## Typical JetBrains breakpoints and the right fix

* **Multi module Gradle or Maven skew**
  Context pulls from sibling modules or stale targets. Lock anchors with `module_path`, `pom.xml` or `build.gradle` hash, and `sourceSet`. Warm the index after sync.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **Wrong symbol in a monorepo**
  Embeddings prefer near neighbors. Require cite then explain with exact spans.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Generated tests reference phantom helpers**
  Enforce file anchors and commit SHA before test generation.
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Long chat drift during refactors and inspections**
  Plan degrades after 25 to 40 steps. Split the plan and re join with a BBCR bridge.
  Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* **Index readiness and language server mismatch**
  First run fails or cites wrong files. Add warm up fences and verify analyzer versions.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **Unsafe shell or Gradle tasks suggested from README**
  Lock tool allow lists and apply SCU separation for untrusted text.
  Open: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md), Pattern: [SCU](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## IDE checklist for JetBrains AI Assistant

* Warm up the selected context source and confirm `INDEX_HASH`, `LANG_SERVER_VER`, and project model synced.
* Use one retrieval metric per run. Do not mix analyzers while fixing a single bug.
* Prompts carry anchors: `repo@commit`, `module_path`, `file_path`, `symbol`, `line_start`, `line_end`, `snippet_id`.
* Log per step: ΔS, λ state, coverage. Alert when ΔS ≥ 0.60 or λ diverges.
* Regression gate requires tests pass, coverage ≥ 0.70, ΔS ≤ 0.45, identical diff twice.

---

## Minimal schema you should capture

`{ repo, commit_sha, module_path, file_path, symbol, line_start, line_end, snippet_id, tokens, ΔS, λ_state }`
Require cite then explain. Forbid cross module reuse without a new citation.

---

## Deep diagnostics

* **Three paraphrase probe**
  Ask the same change three ways. If λ flips on harmless header reorder, clamp with BBAM and lock the schema.

* **Anchor triangulation**
  Compare ΔS for target vs a decoy module or sibling package. If close, re chunk and normalize embeddings.
  See: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Plan length audit**
  If entropy rises after 25 to 40 steps, split the plan and re join with a BBCR bridge.
  See: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* **Live instability**
  Add probes and backoff guards in Run Configurations or task runners.
  See: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Copy paste prompt for JetBrains AI chat

```txt
You have TXTOS and the WFGY Problem Map loaded.

My JetBrains AI issue:
- symptom: [one line]
- anchors: repo={name}, commit={sha}, module={path}, file={path}, lines={a..b}
- traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ across 3 paraphrases

Tell me:
1) the failing layer and why,
2) the exact WFGY page to open,
3) minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) a reproducible test to verify the fix.
Use BBMC, BBPF, BBCR, BBAM when relevant. Keep it auditable and short.
```

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
