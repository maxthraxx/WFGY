# FAQ — Fast Answers for Busy Builders (Problem Map Edition)

Short, practical answers to the questions we get every day. This FAQ merges previous content with the latest Problem Map guidance, so you have one canonical page.

> Quick Nav  
> [Getting Started](./getting-started.md) ·
> [Grandma Clinic (1–16)](./GrandmaClinic/README.md) ·
> [Problem Map 1–16 Index](./README.md) ·
> [RAG Map 2.0](./rag-architecture-and-recovery.md) ·
> [Retrieval Playbook](./retrieval-playbook.md) ·
> [Chunking](./GlobalFixMap/Chunking/README.md) ·
> [Embeddings](./GlobalFixMap/Embeddings/README.md) ·
> [Rerankers](./rerankers.md) ·
> [Eval](./eval/README.md) ·
> [Ops](./ops/README.md) ·
> [Global Fix Map](./GlobalFixMap/README.md)

---

## General

**What is WFGY, in one line?**  
A semantic firewall and diagnostic layer that sits above your stack. It measures semantic drift (ΔS), watches stability (λ_observe), and applies repair operators (BBMC / BBPF / BBCR / BBAM). No infra rewrite needed.

**Do I need a GPU?**  
No for first fixes. You can prototype on CPU with light embeddings and strict guardrails. GPU helps with heavy rerankers or larger local LLMs, but it is optional. See: [Retrieval Playbook](./retrieval-playbook.md).

**How is this different from LangChain/LlamaIndex?**  
Those orchestrate tools. WFGY hardens reasoning and retrieval with pre-output gates and measurable acceptance targets. It works regardless of framework.

**License and commercial use?**  
MIT. Commercial use allowed. PRs welcome (docs, patterns, examples).

---

## Getting started & scope

**Fastest 60-second tryout?**  
Load **TXT OS** and the **WFGY paper**. Paste TXT OS into any LLM, then follow [Getting Started](./getting-started.md) for a minimal “semantic firewall before output” routine.

**Where do I look if I don’t know the failure type yet?**  
Open the triage page: [Grandma Clinic (1–16)](./GrandmaClinic/README.md). Each item has a grandma story, a minimal guardrail, and the pro link.

**Which embedding model to start with?**  
General English: `all-MiniLM-L6-v2` or `bge-base`. Multilingual: `bge-m3` or `LaBSE`. Keep write/read normalization identical. See: [Embeddings](./GlobalFixMap/Embeddings/README.md) and [Semantic ≠ Embedding](./embedding-vs-semantic.md).

**Do I need a reranker right away?**  
Not usually. First prove your candidate pool: if `recall@50 ≥ 0.85` and Top-k precision is still weak, add a reranker. Otherwise fix retrieval shape first. See: [Rerankers](./rerankers.md).

**How big can my PDFs be?**  
Start with a gold set (10–50 Q/A with citations). Ingestion by sections, not fixed tokens. Verify ΔS thresholds before scaling. See: [Chunking](./GlobalFixMap/Chunking/README.md).

---

## Diagnosing failures

**The chunks look right but the answer is wrong. Now what?**  
Measure `ΔS(question, retrieved)`.  
- If `ΔS ≥ 0.60`, fix retrieval first: [Hallucination & Chunk Drift](./hallucination.md).  
- If `ΔS ≤ 0.45` and the answer still fails, it is a reasoning path issue: [Interpretation Collapse](./retrieval-collapse.md).

**Hybrid (BM25+dense) made results worse. Why?**  
Likely analyzer/tokenizer mismatch or query splitting. Unify analyzers and log per-retriever queries. See: [Query Parsing Split](./patterns/pattern_query_parsing_split.md).

**Citations bleed or point to mixed sources.**  
Enforce “cite-then-explain”, per-source fences, and retrieval trace with IDs/lines. See: [Retrieval Traceability](./retrieval-traceability.md) and [Symbolic Constraint Unlock](./patterns/pattern_symbolic_constraint_unlock.md).

**Fixes don’t stick after refresh.**  
You’re hitting Memory Desync. Stamp `mem_rev`/`mem_hash`, gate writes, and audit trace keys. See: [Memory Desync](./patterns/pattern_memory_desync.md).

---

## Retrieval, chunking, and OCR

**Optimal chunk size and rules?**  
Prefer structural sections, stable titles, and table/code preservation. Avoid splitting tables/code blocks. See: [Chunking](./GlobalFixMap/Chunking/README.md).

**OCR keeps breaking layout.**  
Use layout-aware parsing and keep headers/footers separate. See: [OCR Parsing](./GlobalFixMap/OCR_Parsing/README.md).

**Multilingual retrieval drifts.**  
Check tokenizer/analyzer per language and enable hybrid multilingual ranking with guardrails. See: [Language](./GlobalFixMap/Language/README.md) and [LanguageLocale](./GlobalFixMap/LanguageLocale/README.md).

---

## Embeddings & metrics

**Compute ΔS quickly?**  
Unit-normalize sentence embeddings; `ΔS = 1 − cos(I, G)`. Operating zones: `<0.40` stable, `0.40–0.60` transit, `≥0.60` act.

**Why are top neighbors semantically wrong with high cosine?**  
Cross-space vectors, scale/normalization mismatch, or casing/tokenization skew. Audit metrics first. See: [Embeddings](./GlobalFixMap/Embeddings/README.md) and [Semantic ≠ Embedding](./embedding-vs-semantic.md).

**When to switch dimensions or project?**  
Only after metric/normalization audit and contract checks. See: [Dimension Mismatch & Projection](./GlobalFixMap/Embeddings/dimension_mismatch_and_projection.md).

---

## Reasoning guardrails

**What are BBMC / BBPF / BBCR / BBAM?**  
- **BBMC**: minimize semantic residue vs anchors.  
- **BBPF**: branch safely across multiple paths.  
- **BBCR**: detect collapse and restart via a clean bridge node.  
- **BBAM**: modulate attention variance to avoid entropy melt.

**How do I decide when to reset?**  
Monitor ΔS and λ_observe mid-chain. If ΔS spikes twice or λ diverges, run BBCR and re-anchor. See: [Logic Collapse](./logic-collapse.md).

**How do I clamp chain-of-thought variance without killing creativity?**  
Run λ_diverse for 2–3 candidates, score against the same anchor, and apply a bounded entropy window. See: [Creative Freeze](./creative-freeze.md).

**Symbols/tables keep getting flattened.**  
Keep a separate symbol channel, preserve code/table blocks, and anchor units/operators. See: [Symbolic Collapse](./symbolic-collapse.md).

---

## Multi-agent & tool chaos

**Agents overwrite each other’s notes.**  
Assign role/state keys, memory fences, and tool timeouts. See: [Multi-Agent Problems](./Multi-Agent_Problems.md).

**Debug path is a black box.**  
Log query → chunk IDs → acceptance metrics; show the card (source) before answer. See: [Retrieval Traceability](./retrieval-traceability.md).

---

## Eval & acceptance targets

**What to measure on every PR?**  
Commit a gold set and track `recall@50`, `nDCG@10`, and ΔS across prompts. Gate merges on stability. See: [Eval RAG Precision/Recall](./eval/eval_rag_precision_recall.md) and [Eval Semantic Stability](./eval/eval_semantic_stability.md).

**Acceptance targets we use**  
- ΔS ≤ 0.45  
- Coverage ≥ 0.70  
- λ state convergent  
- Source present before final

---

## Ops & deployment

**First calls fail or stall. Where to look?**  
- Boot order issues: [Bootstrap Ordering](./bootstrap-ordering.md)  
- Mutual waiting or locks: [Deployment Deadlock](./deployment-deadlock.md)  
- Cold caches/secrets/index skew: [Pre-deploy Collapse](./predeploy-collapse.md)

**Index build & swap, shadow traffic, rollback?**  
See: [Ops](./ops/README.md) and the detailed ops pages in the [Global Fix Map](./GlobalFixMap/README.md).

---

## Known limits

- Noisy OCR may require manual anchors or char-level retrieval.  
- Abstract cross-domain reasoning (#11/#12) improves with stronger models.  
- Rerankers add latency; prove gains via nDCG before shipping.

---

## Beginner one-liners (map to Problem Map numbers)

- “Cites the wrong thing or makes stuff up” → [No.1 Hallucination & Chunk Drift](./hallucination.md)  
- “Right chunks, wrong reasoning” → [No.2 Interpretation Collapse](./retrieval-collapse.md)  
- “Long chain loses the goal” → [No.3 Long Reasoning Chains](./context-drift.md)  
- “Confident tone, no evidence” → [No.4 Bluffing](./bluffing.md)  
- “Cosine is high but meaning is off” → [No.5 Semantic ≠ Embedding](./embedding-vs-semantic.md)  
- “Looping or shallow branches” → [No.6 Logic Collapse](./logic-collapse.md)  
- “Forgets state between runs” → [No.7 Memory Coherence](./memory-coherence.md)  
- “Can’t reproduce a result” → [No.8 Traceability](./retrieval-traceability.md)  
- “Everything melts into noise” → [No.9 Entropy Collapse](./entropy-collapse.md)  
- “Too literal, zero spark” → [No.10 Creative Freeze](./creative-freeze.md)  
- “Table/math becomes prose” → [No.11 Symbolic Collapse](./symbolic-collapse.md)  
- “Why about why forever” → [No.12 Philosophical Recursion](./philosophical-recursion.md)  
- “Agents fight over memory” → [No.13 Multi-Agent Chaos](./Multi-Agent_Problems.md)  
- “Eggs before heating the pan” → [No.14 Bootstrap Ordering](./bootstrap-ordering.md)  
- “You first / no, you first” → [No.15 Deployment Deadlock](./deployment-deadlock.md)  
- “First pot always burns” → [No.16 Pre-deploy Collapse](./predeploy-collapse.md)

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


