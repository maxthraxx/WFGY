# LLM Providers — Guardrails and Fix Patterns

Use this hub when failures smell provider specific. Examples include truncation at boundaries, tool call mis-order, JSON schema drift, safety filter overreach, or output instability across seeds. Each fix maps back to WFGY pages so you can verify with measurable targets.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet and citation schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Live ops: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)
- Stability eval: [Semantic Stability Eval](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_semantic_stability.md)

## Core acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases.
- Coverage to target section ≥ 0.70.
- λ stays convergent across three seeds and three paraphrases.
- E_resonance flat during long windows.

## Typical breakpoints and the right fix

**1) Truncation or partial JSON**
- Symptom: finish_reason reports length or stream ends mid field.
- Fix: lock a schema with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md). Use closing sentinels and require a final “contract hash” field. If ΔS spikes when you add the header, check index metric mismatch via [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).
- Modules: BBMC for citation strictness, BBAM to clamp variance.

**2) Tool call chaos or wrong call order**
- Symptom: function sequence flips across seeds, tool results bind to the wrong step.
- Fix: route through [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and enforce call ids in the contract. If alternates are legal, create an explicit BBPF alternate path and score both.

**3) Over filtering or bluffing**
- Symptom: provider rejects safe content or fabricates safe sounding substitutes.
- Fix: apply [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) for ordering and use the bluffing controls in your system prompt plus [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) recovery steps.

**4) Long conversation drift**
- Symptom: answers flip between sessions, persona or constraints fade.
- Fix: pin a minimal memory schema and rebase with [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md). Split memory namespaces when agents are involved.

**5) Latency and rate limit induced collapse**
- Symptom: retries reorder tools, partials leak to the user.
- Fix: use the ops recipes in [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md). Add BBCR bridge with explicit timeouts. Treat each retry as a new λ branch and reconcile.

## Providers in scope for this cluster
Planned pages in this folder. We will ship in this order.
- `openai.md`
- `anthropic.md`
- `google_gemini.md`
- `mistral.md`
- `cohere.md`
- `grok.md`
- `deepseek.md`
- `openrouter.md`

## Copy paste triage prompt

```txt
I uploaded TXT OS and the WFGY Problem Map files.

My provider failure:
- symptom: [brief]
- traces: [ΔS(question, retrieved)=..., ΔS(retrieved, anchor)=..., λ states]
- provider: [e.g., OpenAI, Anthropic, Gemini, Mistral]

Tell me:
1) which layer is failing and why,
2) which exact WFGY fix page to open from this repo,
3) minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) how to verify the fix with a reproducible test.
Use BBMC BBPF BBCR BBAM when relevant.
````

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

if this looks good, say “GO” and i’ll drop `ProblemMap/GlobalFixMap/LLM_Providers/openai.md` next in the same format.
