# Vespa: Guardrails and Fix Patterns

Use this page when your retrieval stack runs on Vespa with vector or hybrid ranking. It routes common store-level failures to the right structural fixes in the Problem Map and gives a minimal checklist you can apply fast.

## When to open this page

- High vector similarity yet wrong meaning  
- Hybrid keyword + vector flips order between runs  
- Citations land on the wrong section or offsets do not match  
- Tensor dimensions or distance functions differ across write and read  
- Coverage stays low on the intended section even though recall looks fine

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe remains convergent across 3 paraphrases  
- E_resonance flat on long windows

---

## Map symptoms → structural fixes

- Wrong-meaning hits despite high similarity.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Snippet or citation does not match the retrieved section.  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid collapse or query split between BM25 and vector.  
  → [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Version skew after deploy or wrong rank profile in use.  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Long chains smear topics or capitalization across sessions.  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

---

## Minimal Vespa setup checklist

1) **Pin tensor schema and metric**  
   Use one embedding model per vector field. Keep a single tensor dimension and a single distance function for the rank profile. Reject documents that do not match the expected dimension.

2) **Contract the snippet**  
   Every hit must carry `{snippet_id, section_id, source_url, offsets, tokens}`. Enforce cite-then-explain in the answer layer.  
   Spec: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Hybrid ordering and reranking**  
   Combine keyword recall with `nearestNeighbor` recall, then run a deterministic rerank pass. Log both candidate lists to detect query split.  
   Guide: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

4) **Analyzer and casing parity**  
   Freeze tokenization, stemming, and casing rules for all text fields used in BM25 or filters. Keep the same rules at write and read.

5) **Observability probes**  
   Log ΔS(question, retrieved) and λ per step: retrieve → rerank → reason. Alert when ΔS ≥ 0.60 or λ diverges.

6) **Cold start and deploy fences**  
   Block traffic until the new application package, schema hash, and rank profile version are active.  
   See: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

---

## 60-second diagnosis

1) Run a 10-question smoke set on one target section.  
2) Compute ΔS(question, retrieved) for each question.  
3) If median ΔS ≥ 0.60, apply one structural fix in this order:  
   a) normalize embeddings and pin one distance function  
   b) enforce data contracts and traceability  
   c) add deterministic reranking and align analyzers  
4) Require coverage ≥ 0.70 before you publish.

---

## Copy-paste audit prompt

```

I uploaded TXT OS and the WFGY Problem Map pages.
Store: Vespa. Retrieval: BM25 + nearestNeighbor with rerank.

Audit this query and return:

* ΔS(question, retrieved) and λ across retrieve → rerank → reason.
* If ΔS ≥ 0.60, choose exactly one minimal structural fix and name the page:
  embedding-vs-semantic, retrieval-traceability, data-contracts, rerankers.
* JSON only:
  { "citations":\[...], "ΔS":0.xx, "λ":"→|←|<>|×", "next\_fix":"..." }

```

---

## Common Vespa gotchas

- Mixed embedding dimensions or distance functions across rank profiles  
  Standardize on one and validate on write.

- Summary fields do not include offsets or token spans  
  Add fields to the summary and verify the contract.

- Match-phase or targetHits tuned too low for the collection size  
  Recall collapses and rerank cannot recover. Increase recall or shard-level limits.

- Filter mismatches due to analyzer differences  
  Keep analyzer and casing identical across environments.

- Application package deployed but old profile still served  
  Fence the cutover and verify the active profile hash before enabling traffic.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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
