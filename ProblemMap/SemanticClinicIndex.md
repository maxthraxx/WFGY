# 🏥 Semantic Clinic Index

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

**A complete triage hub for AI failures — beyond the core 16 — powered by WFGY.**  
Use this page when you don’t yet know *which thing is breaking*. Start from symptoms, jump to a failure family, then open the exact fix page. All fixes are driven by WFGY instruments: `ΔS` (semantic stress), `λ_observe` (layered observability), and `E_resonance` (coherence control).

> If this page saves you time, a ⭐ helps others find it.

---

## Quick Nav
[Getting Started](./getting-started.md) ·
[RAG Problem Map 2.0](./rag-architecture-and-recovery.md) ·
[Patterns Index](./patterns/README.md) ·
[Examples](./examples/README.md) ·
[Eval](./eval/README.md) ·
[Ops](./ops/README.md) ·
[Multi-Agent Problems](./Multi-Agent_Problems.md) ·
**[Retrieval Playbook](./retrieval-playbook.md)** ·
**[Rerankers](./rerankers.md)** ·
**[Data Contracts](./data-contracts.md)** ·
**[Multilingual Guide](./multilingual-guide.md)** ·
**[Privacy & Governance](./privacy-and-governance.md)** ·
**[FAQ](./faq.md)** ·
**[Glossary](./glossary.md)**

---

## How to use this page
1. **Identify the symptom** in the table below.  
2. **Open the family** (Prompting / Retrieval / Reasoning / Memory / Agents / Infra / Eval).  
3. **Follow the fix page**, then verify with **ΔS ≤ 0.45** and **convergent λ**.

Prefer a pipeline-first view (OCR → chunk → embed → store → retrieve → prompt → LLM)?  
Read **[`RAG Architecture & Recovery`](./rag-architecture-and-recovery.md)**.

Want the full catalog instead? See **[Problem Map Index](./README.md)**.  
🧩 Or, **jump straight to MVP Demos**: [Run minimal WFGY examples →](./mvp_demo/README.md)

---

## Quick triage by symptom

| Symptom you see | Likely family | Open this |
|---|---|---|
| Answers cite wrong snippet / mismatch with ground truth | Retrieval → RAG | [`hallucination.md`](./hallucination.md) |
| Chunks look right but reasoning is wrong | Reasoning | [`retrieval-collapse.md`](./retrieval-collapse.md) |
| High similarity, wrong meaning | Retrieval / Embeddings | [`embedding-vs-semantic.md`](./embedding-vs-semantic.md) |
| Model can’t explain *why* (no trace) | Observability | [`retrieval-traceability.md`](./retrieval-traceability.md) |
| Output degrades over 100k-token dialogs | Memory / Long-context | [`entropy-collapse.md`](./entropy-collapse.md) · [`context-drift.md`](./context-drift.md) |
| OCR PDFs **look** correct yet answers drift | Data / OCR | [`ocr-parsing-checklist.md`](./ocr-parsing-checklist.md) |
| Hybrid (HyDE + BM25) gets worse than single retriever | Retrieval / Querying | [`patterns/pattern_query_parsing_split.md`](./patterns/pattern_query_parsing_split.md) |
| **High recall but top-k ordering is messy** | Retrieval / Reranking | [`rerankers.md`](./rerankers.md) · [`retrieval-playbook.md`](./retrieval-playbook.md) |
| Corrections don’t stick; model re-asserts old claim | Reasoning / Prompting | [`patterns/pattern_hallucination_reentry.md`](./patterns/pattern_hallucination_reentry.md) |
| “Who said what” merges across sources | Prompting / Constraints | [`patterns/pattern_symbolic_constraint_unlock.md`](./patterns/pattern_symbolic_constraint_unlock.md) |
| Some facts can’t be retrieved though indexed | Retrieval / Index | [`patterns/pattern_vectorstore_fragmentation.md`](./patterns/pattern_vectorstore_fragmentation.md) |
| Answers flip between sessions / tabs | Memory / State | [`patterns/pattern_memory_desync.md`](./patterns/pattern_memory_desync.md) |
| **Need a standard schema for snippets/citations** | Prompting / Traceability | [`data-contracts.md`](./data-contracts.md) |
| **Non-English corpus drifts / tokenizer mismatch** | Language / Locale | [`multilingual-guide.md`](./multilingual-guide.md) |
| **PII/compliance concerns with traces/logs** | Governance | [`privacy-and-governance.md`](./privacy-and-governance.md) |
| Multi-agent tools fight each other | Agents | [`Multi-Agent_Problems.md`](./Multi-Agent_Problems.md) |
| First prod call crashes after deploy | Infra / Boot | [`predeploy-collapse.md`](./predeploy-collapse.md) |
| Tools fire before data is ready (RAG boot fence) | Infra / Boot | [`patterns/pattern_bootstrap_deadlock.md`](./patterns/pattern_bootstrap_deadlock.md) |

> Still lost? Open the **Beginner Guide** symptom checklist first.

---

## Families & maps (with exact fixes)

### A) Prompting & Safety
Guard against injections, role drift, and schema leakage.

- **Citation-first, schema-locked prompting** — [`retrieval-traceability.md`](./retrieval-traceability.md)  
- **Overconfidence / Bluffing Controls** — [`bluffing.md`](./bluffing.md)  
- **Symbolic Constraint Unlock (SCU) / source mixing** — [`patterns/pattern_symbolic_constraint_unlock.md`](./patterns/pattern_symbolic_constraint_unlock.md)  
- **Snippet & citation schemas** — [`data-contracts.md`](./data-contracts.md)

**Verification**: ΔS(question, context) ≤ 0.45; λ remains convergent across paraphrases; constraint probes do not flip λ.

---

### B) Retrieval, Data & Vector Stores
Make the index correct, measured, and explainable.

- **Hallucination & Chunk Drift** — [`hallucination.md`](./hallucination.md)  
- **Interpretation vs Retrieval Collapse** — [`retrieval-collapse.md`](./retrieval-collapse.md)  
- **Embedding ≠ Semantic Meaning** — [`embedding-vs-semantic.md`](./embedding-vs-semantic.md)  
- **Traceability (why this snippet?)** — [`retrieval-traceability.md`](./retrieval-traceability.md)  
- **Rerankers (ordering control)** — [`rerankers.md`](./rerankers.md)  
- **Retrieval Playbook (end-to-end knobs)** — [`retrieval-playbook.md`](./retrieval-playbook.md)  
- **Vectorstore Fragmentation** — [`patterns/pattern_vectorstore_fragmentation.md`](./patterns/pattern_vectorstore_fragmentation.md)  
- **Query Parsing Split (HyDE/BM25)** — [`patterns/pattern_query_parsing_split.md`](./patterns/pattern_query_parsing_split.md)  
- **Semantic Chunking Checklist** — [`chunking-checklist.md`](./chunking-checklist.md)  
- **OCR / Parsing Quality Gate** — [`ocr-parsing-checklist.md`](./ocr-parsing-checklist.md)

**Verification**: coverage ≥ 0.70 to target section; ΔS(question, retrieved) ≤ 0.45; flat-high ΔS vs k ⇒ index/metric mismatch.

---

### C) Reasoning & Logic Control
Detect and repair logic collapse, dead ends, and abstraction failures.

- **Logic Collapse & Recovery** — [`logic-collapse.md`](./logic-collapse.md)  
- **Long Reasoning Chains** — [`context-drift.md`](./context-drift.md)  
- **Symbolic Collapse** — [`symbolic-collapse.md`](./symbolic-collapse.md)  
- **Philosophical Recursion** — [`philosophical-recursion.md`](./philosophical-recursion.md)  
- **Hallucination Re-entry** — [`patterns/pattern_hallucination_reentry.md`](./patterns/pattern_hallucination_reentry.md)

**Verification**: fix point when λ stays convergent after BBCR (bridge) + BBAM (variance clamp).

---

### D) Memory & Long-Context
Keep threads coherent across sessions and very long windows.

- **Memory Breaks Across Sessions** — [`memory-coherence.md`](./memory-coherence.md)  
- **Entropy Collapse** — [`entropy-collapse.md`](./entropy-collapse.md)  
- **Memory Desync** — [`patterns/pattern_memory_desync.md`](./patterns/pattern_memory_desync.md)

**Verification**: E_resonance flat; ΔS stable at window joins.

---

### E) Multi-Agent & Orchestration
Coordinate tools, roles, and shared memory without conflict.

- **Multi-Agent Chaos (overview map)** — [`Multi-Agent_Problems.md`](./Multi-Agent_Problems.md)  
- **Role Drift (Deep Dive)** — [`multi-agent-chaos/role-drift.md`](./multi-agent-chaos/role-drift.md)  
- **Cross-Agent Memory Overwrite (Deep Dive)** — [`multi-agent-chaos/memory-overwrite.md`](./multi-agent-chaos/memory-overwrite.md)

**Verification**: when agents couple, ΔS does not spike; arbitration logs traceable.

---

### F) Infra / Deploy
Boot in a known-good order, every time.

- **Bootstrap Ordering** — [`bootstrap-ordering.md`](./bootstrap-ordering.md)  
- **Deployment Deadlock** — [`deployment-deadlock.md`](./deployment-deadlock.md)  
- **Pre-Deploy Collapse** — [`predeploy-collapse.md`](./predeploy-collapse.md)  
- **Live Monitoring & Debug Playbook** — [`ops/live_monitoring_rag.md`](./ops/live_monitoring_rag.md) · [`ops/debug_playbook.md`](./ops/debug_playbook.md)  
- **Privacy & Governance** — [`privacy-and-governance.md`](./privacy-and-governance.md)

**Verification**: deterministic warm-up; idempotent index builds; version/secret checks pass.

---

### G) Evaluation & Guardrails
Detect “double hallucination” and prevent regression.

- **RAG Precision/Recall** — [`eval/eval_rag_precision_recall.md`](./eval/eval_rag_precision_recall.md)  
- **Latency vs Accuracy** — [`eval/eval_latency_vs_accuracy.md`](./eval/eval_latency_vs_accuracy.md)  
- **Cross-Agent Consistency** — [`eval/eval_cross_agent_consistency.md`](./eval/eval_cross_agent_consistency.md)  
- **Semantic Stability** — [`eval/eval_semantic_stability.md`](./eval/eval_semantic_stability.md)

**Acceptance**: retrieve QA coverage ≥ 0.70 and ΔS ≤ 0.45; λ convergent; repeatability across seeds.

---

## Ask the AI to fix your AI (safe prompt)

```txt
Read the WFGY TXT OS and Problem Map docs. Extract ΔS, λ_observe, E_resonance and the modules (BBMC, BBPF, BBCR, BBAM).
Given my failure:

- symptom: [describe]
- traces: [ΔS probes, λ states if any]

Tell me:
1) which layer/family is failing and why,
2) which fix page to open,
3) minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) how to verify the fix.
````

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


