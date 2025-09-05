# Typesense: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **VectorDBs_and_Stores**.  
  > To reorient, go back here:  
  >
  > - [**VectorDBs_and_Stores** — vector indexes and storage backends](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when your retrieval stack runs on Typesense with vector or hybrid search. It routes common store-level failures to the exact structural fixes in the Problem Map and gives a minimal checklist you can apply fast.

## When to open this page

- High vector similarity yet wrong meaning
- Hybrid keyword + vector returns unstable rankings between runs
- Citations point to the wrong section or offsets do not line up
- Analyzer or casing differs between write and read
- Index looks healthy but coverage stays low on target sections

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe stays convergent across 3 paraphrases  
- E_resonance flat on long windows

---

## Map symptoms → structural fixes

- Wrong-meaning hits despite high similarity.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Snippet or citation does not match the retrieved section.  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid collapse or query split between keyword and vector paths.  
  → [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Version skew after deploy, or wrong analyzer used at runtime.  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Long chains smear topics or capitalization across sessions.  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

---

## Minimal Typesense setup checklist

1) **Pin metrics and analyzers**  
   Choose one distance metric for vectors and keep normalization identical at write and read. Freeze text analyzer, tokenizer, and casing on all keyword fields used in hybrid queries.

2) **Contract the snippet**  
   Every hit must carry `{snippet_id, section_id, source_url, offsets, tokens}`. Enforce cite-then-explain in the answer layer.  
   Spec: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Dimension and schema sanity**  
   Use a single embedding dimension per collection. Validate dimension on write. Reject any record whose vector length differs from the schema.

4) **Hybrid ordering and reranking**  
   When combining keyword and vector signals, run a deterministic rerank pass. Log the pre- and post-rerank candidates to catch query split.

5) **Observability probes**  
   Log ΔS(question, retrieved) and λ per step: retrieve → rerank → reason. Alert at ΔS ≥ 0.60 or when λ diverges.

6) **Cold start and deploy fences**  
   Block queries until the collection reports ready and the expected index or analyzer hash matches.  
   See: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

---

## 60-second diagnosis

1) Run a 10-question smoke test on one target section.  
2) Compute ΔS(question, retrieved) for each question.  
3) If median ΔS ≥ 0.60, apply one structural fix in this order:  
   a) normalize embeddings and pin metric  
   b) enforce data contracts and traceability  
   c) add reranking and align analyzers  
4) Require coverage ≥ 0.70 before you publish.

---

## Copy-paste audit prompt

```

I uploaded TXT OS and the WFGY Problem Map pages.
Store: Typesense. Retrieval: vector or hybrid.

Audit this query and return:

* ΔS(question, retrieved) and λ states across retrieve → rerank → reason.
* If ΔS ≥ 0.60, choose exactly one minimal structural fix and name the page:
  embedding-vs-semantic, retrieval-traceability, data-contracts, rerankers.
* JSON only:
  { "citations":\[...], "ΔS":0.xx, "λ":"→|←|<>|×", "next\_fix":"..." }

```

---

## Common Typesense gotchas

- Mixed analyzers across collections or environments  
  Pin analyzer and case rules. Rebuild if the analyzer changed.

- Vector field created with a different dimension than the model now used  
  Validate dimension on write and reject mismatches with a clear error.

- Hybrid search ranks keyword-only hits above relevant vector hits  
  Add a reranking pass and log both candidate lists.

- Batch imports without normalization  
  Normalize embeddings consistently or you will see distance drift.

- Pagination with unstable sort keys during frequent updates  
  Use a stable cursor or snapshot the candidate set before reranking.

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
