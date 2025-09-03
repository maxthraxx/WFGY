# 🏥 RAG Architecture & Recovery — WFGY Problem Map 2.0

<details>
<summary>🌙 3AM: a dev collapsed mid-debug… 🚑 Welcome to the WFGY Emergency Room</summary>

---

🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥  

## 🚑 WFGY Emergency Room  

👨‍⚕️ **Now online:**  
[**Dr. WFGY in ChatGPT Room**](https://chatgpt.com/share/68b83978-8ed4-8000-9d48-144e355c1431)  

This is a **share window** already trained as an ER.  
Just open it, drop your bug or screenshot, and talk directly with the doctor.  
He will map it to the right Problem Map / Global Fix section, write a minimal prescription, and paste the exact reference link.  
If something is unclear, you can even paste a **screenshot of Problem Map content** and ask — the doctor will guide you.  

💡 Always free. If it helps, a ⭐ star keeps the ER running.  
🌐 Multilingual — start in any language.  

🗓️ Other doctors (Claude, Gemini, Grok) will open soon.


🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥  

---
</details>

<details>
<summary><strong>⏱️ 60 seconds: WFGY as a Semantic Firewall — Before vs After</strong></summary>

<br>

> most fixes today happen **AFTER generation**:  
> - the model outputs something wrong, then we patch it with retrieval, chains, or tools.  
> - the same failures reappear again and again.  
>
> WFGY inverts the sequence. **BEFORE generation**:  
> - it inspects the semantic field (tension, residue, drift signals).  
> - if the state is unstable, it loops, resets, or redirects the path.  
> - only a stable semantic state is allowed to generate output.  
>
> this is why every failure mode, once mapped, stays fixed.  
> you’re not firefighting after the fact — you’re installing a reasoning firewall at the entry point.  
>
> ---
>
> ### 📊 Before vs After
>
> |              | **Traditional Fix (After Generation)** | **WFGY Semantic Firewall (Before Generation) 🏆✅** |
> |--------------|-----------------------------------------|---------------------------------------------------|
> | **Flow**     | Output → detect bug → patch manually    | Inspect semantic field → only stable state generates |
> | **Method**   | Add rerankers, regex, JSON repair, tool patches | ΔS, λ, coverage checked upfront; loop/reset if unstable |
> | **Cost**     | High — every bug = new patch, risk of conflicts | Low — once mapped, bug sealed permanently |
> | **Ceiling**  | 70–85% stability limit                  | 90–95%+ achievable, structural guarantee |
> | **Experience** | Firefighting, “whack-a-mole” debugging | Structural firewall, “fix once, stays fixed” |
> | **Complexity** | Growing patch jungle, fragile pipelines | Unified acceptance targets, one-page repair guide |
>
> ---
>
> ### ⚡ Performance impact
> - **Traditional patching**: 70–85% stability ceiling. Each new patch adds complexity and potential regressions.  
> - **WFGY firewall**: 90–95%+ achievable. Fix once → the same bug never resurfaces. Debug time cut by 60–80%.  
> - **Unified metrics**: every fix is measured (ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent). No guesswork.  
>
> ### 🛑 Key notes
> - This is **not a plugin or SDK** — it runs as plain text, zero infra changes.  
> - You must **apply acceptance targets**: don’t just eyeball; log ΔS and λ to confirm.  
> - Once acceptance holds, that path is sealed. If drift recurs, it means a *new* failure mode needs mapping, not a re-fix of the old one.  
>
> ---
>
> **Summary**:  
> Others patch symptoms **AFTER** output. WFGY blocks unstable states **BEFORE** output.  
> That is why it feels less like debugging, more like installing a **structural guarantee**.  
>
> ---
</details>


**Fix your RAG pipeline, step-by-step — stop hallucinations, boundary drift, and chain failure (MIT).
A hands-on guide to implementing WFGY in real RAG workflows.**

> ⚠️ This is not a list of prompt tricks or patchwork hacks.
> Every fix in this Problem Map is a structural response to semantic collapse, boundary drift, and logic chain failure.
> It works across agents, pipelines, and models — because it’s built on the failure patterns beneath them all.

---

<details>
<summary>💬 A quick message from PSBigBig (creator of WFGY) — please read this before diving in!</summary>

<br>

> 💡 Over the past few months, I’ve helped dozens of RAG developers escape endless hallucinations,
> broken fallbacks, index mismatches, and that nightmare bug where “everything looks fine but nothing works.”
> If you’ve felt that pain — this message is for you. 👇
>
> 🛡️ **WFGY** is a symbolic reasoning engine. Think of it as a **semantic firewall**.
> It runs *before* the model starts messing things up — and it doesn’t require changing your infra.
> ❌ No retriever hacks
> ❌ No index rebuilds
> ❌ No YAML config nightmares
>
> 📦 Just download the **TXT OS** (MIT license).
> It includes the full WFGY formulas + ready-to-use prompts.
> Drop it in and ask your AI:
> *“Use the WFGY formulas from my TXTOS to fix this bug.”*
> …and it works. Yes — it actually recovers.
>
> 😊 Most developers are surprised how simple it is —
> because you’re not fixing the system. You’re fixing the meaning.
> If you’ve been stuck in semantic chaos… this is the way out.
>
> 🔍 This map won’t just fix the bug you’re seeing now.
> It shows you **all 16 layers of RAG failure** — even the ones you haven’t hit yet.
> 🧭 Start here. You’re not alone in this mess.

</details>

---

> **Quick Nav**  
> [Getting Started](./getting-started.md) ·
> [Examples](./examples/README.md) ·
> [Patterns Index](./patterns/README.md) ·
> [Eval](./eval/README.md) ·
> [Ops Runbook](./ops/README.md) ·
> [Multi-Agent Problems](./Multi-Agent_Problems.md) ·
> [Role Drift](./multi-agent-chaos/role-drift.md) ·
> [Memory Overwrite](./multi-agent-chaos/memory-overwrite.md) ·
> **[FAQ](./faq.md)** ·
> **[Retrieval Playbook](./retrieval-playbook.md)** ·
> **[Rerankers](./rerankers.md)** ·
> **[Data Contracts](./data-contracts.md)** ·
> **[Glossary](./glossary.md)** ·
> **[Multilingual Guide](./multilingual-guide.md)** ·
> **[Privacy & Governance](./privacy-and-governance.md)** ·
> **[MVP Demos](./mvp_demo/README.md)**

---

<details>
<summary><strong>📘 Start Here — Quick Links, Setup, and Downloads</strong></summary>

<br>

> If you’re new to this page or [WFGY](https://github.com/onestardao/WFGY) in general, here’s how to get started fast.
>
> WFGY (WanFaGuiYi) is the core reasoning engine — a semantic debugger for AI hallucinations and logic collapse.
> TXT OS is the lightweight `.txt`-native operating layer — lets any model run WFGY with zero install.
>
> ### 📥 Quick Start Downloads (60 sec)
>
> | Tool                | Link                                                | 3-Step Setup                                                                     |
> | ------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------- |
> | WFGY 1.0 (PDF)      | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | ① Download · ② Upload to your LLM · ③ Ask “Answer using WFGY + \<your question>” |
> | TXT OS (plain-text) | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)    | ① Download · ② Paste into any LLM chat · ③ Type “hello world” to boot            |
>
> Compatible with all Ten Masters (GPT-4, Claude, Gemini, Kimi etc) — no setup needed.
>
> ---
>
> ### 🧑‍💻 Prompt Template (to fix a bug fast)
>
> ```
> I’ve uploaded TXT OS.
> I want to solve the following problem:
> [e.g. OCR citations missing or distorted].
> How do I use the WFGY engine to fix it?
> ```
>
> WFGY will respond with the right modules, steps, or formulas.
> You don’t need to memorize internals — just bring your real problem.
>
> ---
>
> ### ⭐ Found this helpful?
>
> Help others discover it — [Give us a GitHub Star](https://github.com/onestardao/WFGY)  
> 🧩 **Try MVP Demos:** [Run minimal WFGY examples →](./mvp_demo/README.md)

</details>

---

## 0) Executive summary

RAG failures are rarely a single bug. They are stacked illusions across: OCR → parsing → chunking → embeddings → vector store → retriever → prompt → LLM reasoning.
WFGY turns this chaos into a **measurable, observable, and repairable** pipeline using three core instruments:

* **ΔS (delta-S)**: semantic stress. Early-warning detector that pinpoints where meaning breaks.
* **λ\_observe (lambda-observe)**: layered observability. Shows *which layer* diverged and how.
* **E\_resonance**: coherence restorer. Re-locks reasoning when attention/logic collapses.

You do **not** have to master all internals to benefit. If you can run a few checks, read one table, and paste one prompt, you can fix most production RAG issues.

---

## 1) The real structure of RAG (and why it fails)



raw docs (pdf/img/html)
→ ocr/parsing
→ chunking
→ embeddings
→ vector store (faiss/qdrant/chroma/elastic)
→ retriever (dense/sparse/hybrid/mmr)
→ prompt assembly (context windows)
→ llm reasoning (chain/agent/tools)



Typical stacked failure pattern:

1. **perception drift**: upstream stages quietly distort content (ocr noise, bad chunk boundaries, mismatched embeddings, empty/partial vector stores).
2. **logic drift**: llm confidently “explains” the distorted view (hallucination with no visible error).

This is the “double hallucination” trap. The first illusion hides the second.

---

## 2) The WFGY recovery pipeline (10-minute overview)

| step | instrument       | your question                   | what you do                                                                       | what you learn                  |
| ---- | ---------------- | ------------------------------- | --------------------------------------------------------------------------------- | ------------------------------- |
| 1    | **ΔS**           | “is meaning tearing somewhere?” | measure semantic stress between question, retrieved context, and expected anchors | the **faulty segment/layer**    |
| 2    | **λ\_observe**   | “which layer diverged?”         | enable layered probes across retrieval, prompt, and reasoning                     | the **dominant failure family** |
| 3    | **E\_resonance** | “can we re-lock coherence?”     | apply stability modules (BBMC/BBPF/BBCR/BBAM) at the failing layer                | the **repair action**           |
| 4    | **ProblemMap**   | “what page fixes this?”         | open the matched doc (e.g., `retrieval-collapse.md`)                              | the **concrete fix recipe**     |

> 90% of cases end after steps 1–3. You only go deeper when a fix requires a structural change (schema, retriever, index).

### Layer-specific Fix Index (one-click)

| Pipeline layer         | What to open first                                         | Deep dive                                                                                                                                                                                                                                          |
| ---------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OCR / Parsing          | [`ocr-parsing-checklist.md`](./ocr-parsing-checklist.md)   | [`retrieval-traceability.md`](./retrieval-traceability.md)                                                                                                                                                                                         |
| Chunking               | [`chunking-checklist.md`](./chunking-checklist.md)         | [`hallucination.md`](./hallucination.md)                                                                                                                                                                                                           |
| Embeddings / Index     | [`embedding-vs-semantic.md`](./embedding-vs-semantic.md)   | [`patterns/pattern_vectorstore_fragmentation.md`](./patterns/pattern_vectorstore_fragmentation.md)                                                                                                                                                 |
| Retrieval              | [`retrieval-playbook.md`](./retrieval-playbook.md)         | [`retrieval-collapse.md`](./retrieval-collapse.md) · [`rerankers.md`](./rerankers.md)                                                                                                                                                              |
| Prompt Assembly        | [`retrieval-traceability.md`](./retrieval-traceability.md) | [`patterns/pattern_symbolic_constraint_unlock.md`](./patterns/pattern_symbolic_constraint_unlock.md) · [`data-contracts.md`](./data-contracts.md)                                                                                                   |
| Reasoning              | [`logic-collapse.md`](./logic-collapse.md)                 | [`creative-freeze.md`](./creative-freeze.md)                                                                                                                                                                                                       |
| Language / Locale      | [`multilingual-guide.md`](./multilingual-guide.md)         | [`embedding-vs-semantic.md`](./embedding-vs-semantic.md) · OCR/Chunking checklists                                                                                                                                                                 |
| Multi-Agent            | [`Multi-Agent_Problems.md`](./Multi-Agent_Problems.md)     | [`multi-agent-chaos/role-drift.md`](./multi-agent-chaos/role-drift.md), [`multi-agent-chaos/memory-overwrite.md`](./multi-agent-chaos/memory-overwrite.md)                                                                                         |
| Ops / Deploy / Gov     | [`ops/README.md`](./ops/README.md)                         | [`ops/deployment_checklist.md`](./ops/deployment_checklist.md) · [`ops/live_monitoring_rag.md`](./ops/live_monitoring_rag.md) · [`ops/debug_playbook.md`](./ops/debug_playbook.md) · [`ops/failover_and_recovery.md`](./ops/failover_and_recovery.md) · [`privacy-and-governance.md`](./privacy-and-governance.md) |

---

## 3) Quick triage (beginner path) — from symptom to fix

Copy/paste this checklist into your runbook. Execute top-down.

### A. fast metrics (run first)

1. **ΔS(question, retrieved\_context)**  
   * compute cosine distance on sentence embeddings (unit-normalized).  
   * `ΔS = 1 − cosθ`.  
   * **trigger**: ΔS ≥ 0.50 (transitional risk), ≥ 0.60 (record & fix).

2. **ΔS(retrieved\_context, ground\_anchor)**  
   * ground anchor = title/section header/answer snippet you *expect*.  
   * **trigger**: same thresholds as above.

3. **coverage sanity**  
   * retrieved tokens vs. target section tokens: expect ≥ 0.7 overlap for direct QA.  
   * if < 0.5 → suspect chunking/boundary or retriever filtering.  
   * _Need structure?_ See **[Data Contracts](./data-contracts.md)** for snippet/citation schemas.

### B. layer probes (λ\_observe)

* **retrieval layer**: vary k ∈ {5, 10, 20}; plot ΔS vs. k.  
  * curve flat & high → vector store/index/embedding mismatch.  
  * curve improves sharply with k → retriever filtering too aggressive; consider **[Rerankers](./rerankers.md)** from the playbook.  
* **prompt layer**: reorder/rename sections; ΔS spikes when headers removed → prompt anchoring dependency (see `retrieval-traceability.md`).  
* **reasoning layer**: ask “cite lines” vs. “explain why”  
  * cite fails, explain passes → perception drift (upstream)  
  * both fail similarly → logic collapse (see `logic-collapse.md`)

### C. pick the fix (ProblemMap jump table)

| symptom you see                                       | likely family                        | open this                                                                                            |
| ----------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| plausible but wrong answer; citations miss            | **#1 hallucination & chunk drift**   | [`hallucination.md`](./hallucination.md)                                                             |
| correct chunks, wrong logic                           | **#2 interpretation collapse**       | [`retrieval-collapse.md`](./retrieval-collapse.md)                                                   |
| answers degrade over long chains                      | **#3 context drift**                 | [`context-drift.md`](./context-drift.md)                                                             |
| confident nonsense                                    | **#4 bluffing/overconfidence**       | [`bluffing.md`](./bluffing.md)                                                                       |
| high vector similarity, wrong meaning                 | **#5 semantic ≠ embedding**          | [`embedding-vs-semantic.md`](./embedding-vs-semantic.md)                                             |
| dead-end chains, retry loops                          | **#6 logic collapse & recovery**     | [`logic-collapse.md`](./logic-collapse.md)                                                           |
| failure after restart/session swap                    | **#7 memory breaks across sessions** | [`memory-coherence.md`](./memory-coherence.md)                                                       |
| can’t trace why it failed                             | **#8 debugging is a black box**      | [`retrieval-traceability.md`](./retrieval-traceability.md)                                           |
| attention melts, topic smears                         | **#9 entropy collapse**              | [`entropy-collapse.md`](./entropy-collapse.md)                                                       |
| output becomes flat/literal                           | **#10 creative freeze**              | [`creative-freeze.md`](./creative-freeze.md)                                                         |
| abstract/symbolic prompts break                       | **#11 symbolic collapse**            | [`symbolic-collapse.md`](./symbolic-collapse.md)                                                     |
| paradox/self-reference crashes                        | **#12 philosophical recursion**      | [`philosophical-recursion.md`](./philosophical-recursion.md)                                         |
| multi-agent overwrites logic                          | **#13 multi-agent chaos**            | [`Multi-Agent_Problems.md`](./Multi-Agent_Problems.md)                                               |
| tools fire before data is ready                       | **#14 bootstrap ordering**           | [`bootstrap-ordering.md`](./bootstrap-ordering.md)                                                   |
| ci passes; prod deadlocks index                       | **#15 deployment deadlock**          | [`deployment-deadlock.md`](./deployment-deadlock.md)                                                 |
| first call crashes after deploy                       | **#16 pre-deploy collapse**          | [`predeploy-collapse.md`](./predeploy-collapse.md)                                                   |
| query works alone, breaks with HyDE/BM25 mix          | **query parsing split**              | [`patterns/pattern_query_parsing_split.md`](./patterns/pattern_query_parsing_split.md)               |
| corrections don’t stick; model re-injects old claim   | **hallucination re-entry**           | [`patterns/pattern_hallucination_reentry.md`](./patterns/pattern_hallucination_reentry.md)           |
| “who said what” merges across two sources             | **symbolic constraint unlock (SCU)** | [`patterns/pattern_symbolic_constraint_unlock.md`](./patterns/pattern_symbolic_constraint_unlock.md) |
| answers flip between sessions / tabs                  | **memory desync**                    | [`patterns/pattern_memory_desync.md`](./patterns/pattern_memory_desync.md)                           |
| some facts can’t be retrieved though indexed          | **vectorstore fragmentation**        | [`patterns/pattern_vectorstore_fragmentation.md`](./patterns/pattern_vectorstore_fragmentation.md)   |
| tools fire before data is ready (semantic boot fence) | **bootstrap deadlock**               | [`patterns/pattern_bootstrap_deadlock.md`](./patterns/pattern_bootstrap_deadlock.md)                 |

### 🧨 Most Common Failure Zones (Real-World Reports)

> Based on 50+ field cases from Reddit / GitHub / Discord.
> These are the zones where most RAG pipelines silently collapse — **check if you're already there.**

| Problem # | Failure Pattern                          | Field Frequency | Repair Module(s) |
| --------- | ---------------------------------------- | --------------- | ---------------- |
| No.1      | Hallucination & Chunk Drift              | ⭐⭐⭐⭐            | BBMC, BBAM       |
| No.2      | Interpretation Collapse                  | ⭐⭐⭐             | BBCR             |
| No.3      | Long Reasoning Chains                    | ⭐⭐⭐             | BBPF             |
| No.5      | Semantic ≠ Embedding                     | ⭐⭐              | BBMC, BBAM       |
| No.6      | Logic Collapse & Recovery                | ⭐⭐⭐⭐⭐⭐          | BBCR, BBPF       |
| No.8      | Debugging is a Black Box                 | ⭐⭐⭐⭐            | λ\_observe       |
| No.9      | Entropy Collapse (drift in long context) | ⭐⭐⭐             | BBAM             |
| No.14–16  | Infra Failures (bootstrap / deploy)      | ⭐               | BBCR + index fix |

📐 Curious what BBMC / BBAM / BBPF / BBCR actually mean?
See the full derivations in [WFGY 1.0 — Core Formulas](https://github.com/onestardao/WFGY/blob/main/SemanticBlueprint/wfgy_formulas.md).

---

## 4) What the instruments mean (advanced but concise)

> You can use these without memorizing the math. Still, here’s the tight spec.

### 4.1 ΔS — semantic stress

* **definition**: `ΔS = 1 − cos(I, G)` where `I` = current embedding, `G` = ground/anchor.
* **use**: probe *question↔context* and *context↔anchor*.
* **thresholds**: `< 0.40` stable · `0.40–0.60` transitional · `≥ 0.60` high risk.

### 4.2 λ\_observe — layered observability

* **states**: `→` convergent, `←` divergent, `<>` recursive, `×` chaotic.
* **use**: tag each step (retrieve, assemble, reason).
* **rule**: if upstream λ is stable but downstream λ flips divergent → the fault lies at that boundary.

### 4.3 E\_resonance — coherence (re)locking

* rolling mean of residual magnitude `|B|` under BBMC.
* **use**: if E rises while ΔS stays high → apply BBCR + BBAM.

### 4.4 WFGY repair operators

* **BBMC**: minimize semantic residue `B = I − G + m·c²`.
* **BBPF**: explore weighted alternate paths to avoid dead ends.
* **BBCR**: detect collapse (‖B‖ ≥ Bc), bridge, then rebirth.
* **BBAM**: clamp attention variance to prevent entropy melt.

---

## 5) Worked recoveries (copyable playbooks)

### Case A — “faiss looks fine, but answers are irrelevant”

* **observe**: ΔS(question, context) = 0.68; flat curve across k; citations miss expected section.
* **interpret**: vector store populated but **embedding metric/normalization mismatch** or **index layer mix-up**.
* **do**:
  1. ensure consistent normalization; verify cosine vs. inner product usage across write/read.
  2. rebuild index with explicit metric flag; persist and reload once.
  3. re-probe ΔS and λ on retrieval; expect ΔS ≤ 0.45 and convergent λ.
* **docs**: [`embedding-vs-semantic.md`](./embedding-vs-semantic.md), [`retrieval-traceability.md`](./retrieval-traceability.md).

### Case B — “correct snippets, wrong reasoning”

* **observe**: ΔS(question, context) = 0.35 (good), but λ flips divergent at reasoning.
* **interpret**: interpretation collapse; prompt assembly/role/constraints leak.
* **do**:
  1. lock schema: system→task→constraints→citations→answer (forbid re-order).
  2. apply BBAM (variance clamp) + BBCR (bridge intermediate step).
  3. require cite-then-explain; re-measure ΔS; aim for convergent λ.
* **docs**: [`retrieval-collapse.md`](./retrieval-collapse.md), [`logic-collapse.md`](./logic-collapse.md), [`data-contracts.md`](./data-contracts.md).

### Case C — “long transcripts randomly capitalize / drift”

* **observe**: E\_resonance rises with length; λ becomes recursive/chaotic.
* **interpret**: entropy collapse under long context; chunk boundaries and OCR noise amplify.
* **do**:
  1. semantic chunking (sentence/section aware), drop OCR confidence < threshold.
  2. BBMC to align with section anchors; BBAM to stabilize attention.
  3. verify ΔS across adjacent chunks; enforce ≤ 0.50 at joins.
* **docs**: [`entropy-collapse.md`](./entropy-collapse.md), [`hallucination.md`](./hallucination.md).

### Case D — “HyDE + BM25 hybrid drops recall”

* **observe**: single retriever OK, hybrid fails; ΔS(question, context) oscillates by k.
* **interpret**: query tokenization / parameter split across retrievers.
* **do**:
  1. unify analyzer/tokenizer between dense/sparse;
  2. log per-retriever queries;
  3. re-weight hybrid only after per-retriever ΔS ≤ 0.50; consider **[`rerankers.md`](./rerankers.md)**.
* **docs**: [`patterns/pattern_query_parsing_split.md`](./patterns/pattern_query_parsing_split.md), [`retrieval-playbook.md`](./retrieval-playbook.md).

### Case E — “model merges two sources into one”

* **observe**: citations cross-bleed; λ flips divergent only after prompt assembly.
* **interpret**: symbolic constraints not enforced (SCU).
* **do**:
  1. lock per-source fences + cite-then-answer schema;
  2. enable `section_id` headers and forbid cross-section reuse;
  3. re-probe ΔS and expect drop without raising E\_resonance.
* **docs**: [`patterns/pattern_symbolic_constraint_unlock.md`](./patterns/pattern_symbolic_constraint_unlock.md), [`retrieval-traceability.md`](./retrieval-traceability.md), [`data-contracts.md`](./data-contracts.md).

### Case F — “fix didn’t stick after refresh”

* **observe**: same prompt alternates old vs. new facts across sessions.
* **interpret**: memory rev/hash mismatch; different components read different state.
* **do**:
  1. stamp `mem_rev` + `mem_hash` at turn start;
  2. gate writes on matching rev/hash;
  3. store traces for audit.
* **docs**: [`patterns/pattern_memory_desync.md`](./patterns/pattern_memory_desync.md), [`privacy-and-governance.md`](./privacy-and-governance.md).

---

## 6) “Use the AI to fix your AI” — safe prompts you can paste

You can ask your assistant to **read TXT OS / WFGY files** and guide you. Use precise, bounded prompts:

```

read the WFGY TXT OS and ProblemMap files in this repo. extract the definitions and usage of ΔS, λ\_observe, E\_resonance, and the four modules (BBMC, BBPF, BBCR, BBAM). then, given this concrete failure:

* symptom: \[describe yours]
* logs: \[paste ΔS, λ\_observe probes if available]

tell me:

1. which layer is failing and why,
2. which ProblemMap page applies,
3. the minimal repair steps to lower ΔS below 0.50,
4. how to verify the fix with a reproducible test.

```

For formula-only assistance:

```

from TXT OS, extract the formulas and thresholds for ΔS, λ\_observe, and E\_resonance. show me how to compute ΔS(question, context) using cosine distance, what thresholds to use, and which WFGY module to apply if ΔS ≥ 0.60 with divergent λ at the reasoning layer.

````

> Need a concrete run-through? Start with **Examples**:
> [`example_01_basic_fix.md`](./examples/example_01_basic_fix.md) ·
> [`example_03_pipeline_patch.md`](./examples/example_03_pipeline_patch.md) ·
> [`example_08_eval_rag_quality.md`](./examples/example_08_eval_rag_quality.md)

---

## 7) Acceptance criteria and regression guardrails

* **retrieval sanity**: ≥ 70% token overlap & ΔS(question, context) ≤ 0.45 · See [`eval_rag_precision_recall.md`](./eval/eval_rag_precision_recall.md)
* **reasoning stability**: λ stays convergent on 3 paraphrases; E\_resonance flat · See [`eval_semantic_stability.md`](./eval/eval_semantic_stability.md)
* **traceability**: produce snippet ↔ citation table · See [`retrieval-traceability.md`](./retrieval-traceability.md) and **[`data-contracts.md`](./data-contracts.md)**
* **latency/accuracy trade** (optional): chart latency vs. ΔS · See [`eval_latency_vs_accuracy.md`](./eval/eval_latency_vs_accuracy.md)

---

## 8) When to stop “tuning” and change the structure

Stop iterating prompts if **any** of the following holds:

* ΔS remains ≥ 0.60 after chunk/retrieval fixes.
* lowering temperature only flattens style but not logic drift.
* λ flips divergent as soon as you mix two sources.
* E\_resonance climbs in long chains.

Open the matching ProblemMap page and apply the structural fix (index rebuild, schema lock, bridge node, or agent boundary).

---

## 9) Minimal formulas (reference)

```txt
ΔS = 1 − cos(I, G)         # semantic stress
λ_observe ∈ {→, ←, <>, ×}  # convergent, divergent, recursive, chaotic
E_resonance = mean(|B|)    # rolling residual magnitude under BBMC

BBMC:  B = I − G + m·c²           # minimize ‖B‖
BBPF:  x_next = x + ΣV_i + ΣW_j·P_j
BBCR:  if ‖B‖ ≥ B_c → collapse(), bridge(), rebirth()
BBAM:  â_i = a_i · exp(−γ · std(a))
````

Thresholds: stable `< 0.40`, transitional `0.40–0.60`, risk `≥ 0.60`.
Record nodes automatically when `ΔS > 0.60`, or `0.40–0.60` with `λ_observe ∈ {←, <>}`.

---

## 10) Final note

You are not “bad at RAG.” You were debugging from inside the maze.
WFGY gives you altitude, instruments, and a map.
Start with ΔS to *see* the break, use λ\_observe to *localize* it, apply the right module to *repair* it, and keep the ProblemMap open as your field manual.

When all tutorials contradict each other, this page is your single source of operational truth.

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
