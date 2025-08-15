# 📑 Data Contracts — Stable Interfaces for RAG & Agents

Everything WFGY touches is JSON-first and versioned. These “contracts” make pipelines observable, reproducible, and easy to debug.

> **Quick Nav**  
> [Retrieval Playbook](./retrieval-playbook.md) ·
> [Traceability](./retrieval-traceability.md) ·
> [Eval](./eval/README.md) ·
> [Ops](./ops/README.md) ·
> Patterns: [SCU](./patterns/pattern_symbolic_constraint_unlock.md) ·
> [Memory Desync](./patterns/pattern_memory_desync.md)

---

## 0) Envelope (required for all records)

```json
{
  "schema_version": "1.0.0",
  "event": "ingest.write | retrieve.run | rerank.run | answer.decide",
  "ts": "2025-08-13T10:22:59Z",
  "trace_id": "uuid",
  "agent_id": "scout|medic|engineer|retriever|system",
  "mem_rev": "r42", 
  "mem_hash": "sha256:..."
}
````

* `mem_rev`/`mem_hash` prevent **memory overwrite** and **desync**.
* Use the same envelope for logs and datasets.

---

## 1) Chunk record

**Purpose:** atomic, traceable text unit for retrieval.

```json
{
  "$schema": "https://wfgy.dev/schemas/chunk-1.0.json",
  "chunk_id": "c_00123",
  "doc_id": "d_wfgy_paper",
  "section_id": "s_intro",
  "span": {"line_start": 120, "line_end": 154},
  "lang": "en",
  "text": "Delta-S measures semantic stress ...",
  "hash": "sha256:...",
  "embedding": {
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "dim": 384,
    "vector": [0.012, -0.044, ...],
    "normalized": true,
    "metric": "cosine"
  },
  "anchors": ["ΔS", "semantic stress"]
}
```

**Rules**

* Keep **original text** + **normalized text** (case/punctuation) if you apply normalization downstream.
* Always store `metric` and `normalized`.

---

## 2) Query record

```json
{
  "$schema": "https://wfgy.dev/schemas/query-1.0.json",
  "q_id": "q_2025_08_13_0001",
  "text": "How does ΔS detect retrieval failure?",
  "lang": "en",
  "hyde": "Generate a canonical query about ... (optional)",
  "tokens": {"count": 12, "analyzer": "icu"},
  "hints": {"doc_id": ["d_wfgy_paper"], "section_id": []}
}
```

---

## 3) Retrieval result (candidate)

```json
{
  "$schema": "https://wfgy.dev/schemas/retrieved-1.0.json",
  "q_id": "q_2025_08_13_0001",
  "ranker": "dense|bm25|hybrid",
  "k": 50,
  "items": [
    {
      "chunk_id": "c_00123",
      "doc_id": "d_wfgy_paper",
      "score": 0.812,           // retriever-native score
      "cosine": 0.91,           // optional explicit cosine
      "ΔS_q_ctx": 0.36,         // optional, if ground anchor available
      "source": "dense",
      "features": {"bm25": 8.3, "dense": 0.91}
    }
  ]
}
```

---

## 4) Rerank result

```json
{
  "$schema": "https://wfgy.dev/schemas/rerank-1.0.json",
  "q_id": "q_2025_08_13_0001",
  "model": "BAAI/bge-reranker-base",
  "k_in": 60,
  "k_out": 8,
  "items": [
    {
      "chunk_id": "c_00123",
      "pre_score": {"dense": 0.91, "bm25": 8.3},
      "post_score": {"ce": 0.82},
      "reason": "mentions ΔS definition and failure threshold",
      "selected": true
    }
  ]
}
```

---

## 5) Prompt frame (schema-locked)

```json
{
  "$schema": "https://wfgy.dev/schemas/prompt-frame-1.0.json",
  "system": "You are a grounded assistant. Cite before you explain.",
  "task": "Answer the user's question using ONLY the cited snippets.",
  "constraints": ["No cross-source merging", "Cite line spans"],
  "citations": [
    {"id": "c_00123", "doc_id": "d_wfgy_paper", "section_id": "s_intro", "span": [120,154]}
  ],
  "question": "How does ΔS detect retrieval failure?"
}
```

---

## 6) Answer + trace

```json
{
  "$schema": "https://wfgy.dev/schemas/answer-1.0.json",
  "q_id": "q_2025_08_13_0001",
  "answer_text": "ΔS measures the semantic gap ...",
  "cited_chunks": ["c_00123", "c_00987"],
  "λ_observe": "→",
  "metrics": {"ΔS_q_ctx": 0.38, "latency_ms": 922}
}
```

---

## 7) Metrics pack (for CI)

```json
{
  "$schema": "https://wfgy.dev/schemas/metrics-1.0.json",
  "dataset": "goldset_v1",
  "recall@50": 0.91,
  "nDCG@10": 0.62,
  "ΔS_mean": 0.41,
  "ΔS_p95": 0.58,
  "λ_convergent_rate": 0.82
}
```

---

## Acceptance checklist

* ✅ All records include **envelope** (schema\_version, event, ts, trace\_id, mem\_rev/hash).
* ✅ Chunks persist **metric** and **normalized** flags.
* ✅ Prompts are **schema-locked** (cite → explain).
* ✅ Answers store **cited chunk IDs** and **λ state**.
* ✅ Metrics committed per PR (goldset.jsonl).

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
