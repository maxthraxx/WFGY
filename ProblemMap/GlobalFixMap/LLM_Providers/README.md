# LLM Providers: Guardrails and Fix Patterns

A compact hub to stabilize provider-specific failures without changing your infra. Use this when symptoms look “model problem” but root cause is actually schema, retrieval, or orchestration.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Live ops: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
- Boot order issues: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 for the target section
- λ remains convergent across three paraphrases and two seeds
- E_resonance stays flat through long windows

## Typical provider symptoms → exact fix

| Symptom | Likely cause | Open this |
|---|---|---|
| JSON mode breaks, invalid objects | schema too loose or nested tool calls | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) |
| Tool calls loop or stall | agent role drift, missing timeouts | [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md), [role-drift deep dive](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md) |
| High similarity yet wrong snippet | metric mismatch or fragmented store | [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) |
| Answers flip between runs | prompt headers reorder and λ flips | [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Hybrid retrievers worse than single | query parsing split, mis-weighted rerank | [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Jailbreaks or bluffing | overconfidence and missing fences | [Bluffing Controls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe λ_observe**  
   Vary k and prompt headers. If λ flips, lock the schema and apply a BBAM variance clamp.

3) **Apply the module**  
- Retrieval drift → BBMC + Data Contracts  
- Reasoning collapse → BBCR bridge + BBAM  
- Dead ends in long runs → BBPF alternate paths

4) **Verify**  
Coverage ≥ 0.70 on three paraphrases. λ convergent on two seeds.

## Provider-level gotchas checklist
- **Truncation**. Confirm token accounting for system + tools + hidden preambles. If truncated, compress citations through [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).  
- **Streaming chunk boundaries**. Do not parse partial JSON while λ is unstable. Buffer until BBAM settles.  
- **Temperature and top-p**. If ΔS is already high, reduce entropy. If retrieval is sparse, raise recall through rerankers instead of temperature.  
- **Multi-model routing**. Keep traceability stable when swapping GPT, Claude, Gemini, Mistral. Use the same snippet schema and citation header across providers.  
- **Rate limits and retries**. Backoff with idempotent ops. Never rebuild indexes inside retry loops.  
- **Eval parity**. Run the same acceptance on all providers to avoid overfitting a single model.

## Quick routes to per-provider pages
- OpenAI: [openai.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/openai.md)  
- Anthropic: [anthropic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/anthropic.md)  
- Google Gemini: [google_gemini.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/google_gemini.md)  
- Mistral: [mistral.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/mistral.md)  
- Groq: [groq.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/groq.md)  
- Cohere: [cohere.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/cohere.md)  
- DeepSeek: [deepseek.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/deepseek.md)  
- AWS Bedrock: [bedrock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/bedrock.md)  
- Azure OpenAI: [azure_openai.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/azure_openai.md)

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

say “GO” and I’ll do the first provider page. I suggest `ProblemMap/GlobalFixMap/LLM_Providers/openai.md` next.
