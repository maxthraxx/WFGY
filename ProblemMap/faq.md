# ❓ FAQ — Fast Answers for Busy Builders

Short, practical answers to the questions we get every day.

> **Quick Nav**  
> [Getting Started](./getting-started.md) ·
> [RAG Map 2.0](./rag-architecture-and-recovery.md) ·
> [Retrieval Playbook](./retrieval-playbook.md) ·
> [Rerankers](./rerankers.md) ·
> [Patterns](./patterns/README.md) ·
> [Eval](./eval/README.md) ·
> [Ops](./ops/README.md)

---

## General

**What is WFGY?**  
A symbolic reasoning layer + diagnostic toolkit that sits *above* your stack. It measures semantic stress (ΔS), shows which layer drifted (λ_observe), and applies repair operators (BBMC/BBPF/BBCR/BBAM). You don’t need to change your infra.

**Do I need a GPU?**  
No. You can prototype on CPU with small embedding models. Rerankers and local LLMs benefit from GPU but are optional. See: [Retrieval Playbook](./retrieval-playbook.md).

**License? Can I use it at work?**  
MIT. Commercial use allowed. If you ship improvements, we welcome PRs (docs or code).

**How is this different from LangChain/LlamaIndex?**  
Those are orchestration layers. **WFGY is a reasoning firewall and diagnostic map**—it detects/repairs *semantic* failure regardless of framework.

---

## Setup & scope

**What’s the fastest way to try it?**  
Grab **TXT OS** and **WFGY 1.0 PDF**, paste TXT into any model, and follow the prompts in [Getting Started](./getting-started.md).

**Which embedding model should I start with?**  
General docs: `all-MiniLM-L6-v2` (light) or `bge-base`. Multilingual: `bge-m3` / `LaBSE`. Keep **write/read normalization identical**. See: [Embedding vs Semantic](./embedding-vs-semantic.md).

**Do I need a reranker?**  
Only if first-stage **recall@50 ≥ 0.85** but Top-k precision is weak. Otherwise fix candidate generation. See: [Rerankers](./rerankers.md).

**How big can my PDFs be?**  
Start with a **gold set** (10–50 Q/A with citations). For ingestion, chunk by semantic sections (not fixed tokens). Verify ΔS thresholds before scaling.

---

## Diagnosing failures

**The chunks look right but the answer is wrong—now what?**  
Measure **ΔS(question, retrieved)**. If ≥ 0.60, fix retrieval first; if ≤ 0.45 and reasoning still fails, open **Interpretation Collapse**.  
Links: [hallucination.md](./hallucination.md) · [retrieval-collapse.md](./retrieval-collapse.md)

**Hybrid (BM25 + dense) got worse—why?**  
Likely **Query Parsing Split** (tokenizer/analyzer drift). Unify analyzers and log per-retriever queries.  
Link: [pattern_query_parsing_split.md](./patterns/pattern_query_parsing_split.md)

**Citations bleed across sources.**  
Enforce **per-source fences** + “cite-then-explain” schema; this is **SCU**.  
Links: [retrieval-traceability.md](./retrieval-traceability.md) · [pattern_symbolic_constraint_unlock.md](./patterns/pattern_symbolic_constraint_unlock.md)

**Fixes don’t stick after refresh.**  
You’re seeing **Memory Desync**. Stamp `mem_rev`/`mem_hash`, gate writes, and audit traces.  
Link: [pattern_memory_desync.md](./patterns/pattern_memory_desync.md)

---

## Implementation details

**How do I compute ΔS quickly?**  
Use cosine on unit-normalized sentence embeddings: `ΔS = 1 − cos(I, G)`.  
Thresholds: `<0.40` stable · `0.40–0.60` transitional · `≥0.60` act.  
Ground anchor `G` can be a section title/snippet you expect.

**What are BBMC/BBPF/BBCR/BBAM in one line?**  
- **BBMC** — minimize semantic residue vs anchors.  
- **BBPF** — branch safely across multiple paths.  
- **BBCR** — detect collapse; insert a bridge node and restart cleanly.  
- **BBAM** — modulate attention variance to avoid entropy melt.

**Where are the data shapes?**  
See: [Data Contracts](./data-contracts.md). They’re JSON-first, easy to log, and versioned.

---

## Teams & Ops

**How do we avoid regressions?**  
Commit `goldset.jsonl`, measure **recall@50**, **nDCG@10**, and ΔS across PRs.  
Links: [eval_rag_precision_recall.md](./eval/eval_rag_precision_recall.md) · [eval_semantic_stability.md](./eval/eval_semantic_stability.md)

**Any privacy guidance?**  
Yes—PII redaction, retention, access control, and provider governance patterns are here: [Privacy & Governance](./privacy-and-governance.md).

---

## Known limits

- Extremely noisy OCR may require **manual anchors** or **char-level retrieval**.  
- Cross-domain abstract reasoning (#11/#12) needs stronger models.  
- Rerankers improve precision but add latency—**prove gains** via nDCG.

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

---

