# Retrieval Traceability

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Retrieval**.  
  > To reorient, go back here:  
  >
  > - [**Retrieval** — information access and knowledge lookup](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A citation and audit schema that makes every answer explainable. Install this when answers look correct but citations are missing, misaligned, or not reproducible. The schema works across any store or framework.

**Use this page with**
- Contracts for payload shape → [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- ΔS probes for semantic fit → [deltaS_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)
- Chunk window parity → [chunk_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)
- Ordering control → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/rerankers.md)
- Store fences → [store_agnostic_guardrails.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/store_agnostic_guardrails.md)

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the intended section  
- λ convergent across 3 paraphrases and 2 seeds  
- Citation match rate ≥ 0.95 on the gold set

---

## Citation payload schema

Every retrieved unit must carry a portable citation payload. The payload is used in prompts, logs, and evals.

**Required fields**

| Field | Type | Meaning |
|---|---|---|
| `doc_id` | string | Stable document id across versions |
| `section_id` | string | Human legible section key or path |
| `snippet_id` | string | Unique id for this chunk or span |
| `source_url` | string | Canonical source link or URI |
| `offsets` | object | Character or token start and end |
| `tokens` | integer | Token count of the snippet |
| `index_hash` | string | Write time hash of the index |
| `embed_model` | string | Embedding model id and pooling |
| `analyzer` | string | Analyzer and casing policy |
| `rev` | string | Document revision or commit hash |

**Optional but recommended**

| Field | Type | Meaning |
|---|---|---|
| `window` | object | Pre and post context sizes |
| `page` | integer | Page number when applicable |
| `score_raw` | number | Raw similarity from the store |
| `score_norm` | number | Store independent score in 0 to 1 |
| `rerank_score` | number | Cross encoder score if used |
| `k_pos` | integer | Rank position before rerank |
| `k_final` | integer | Rank position after rerank |

**JSON shape**

```json
{
  "doc_id": "handbook_2024",
  "section_id": "policies/security/keys",
  "snippet_id": "hb24-sec-keys-0007",
  "source_url": "https://example.org/handbook#security-keys",
  "offsets": {"start": 2310, "end": 2688, "unit": "char"},
  "tokens": 188,
  "index_hash": "faiss:2f7d...9a",
  "embed_model": "bge-large-en-v1.5:mean",
  "analyzer": "lowercase+ascii_fold",
  "rev": "3b91f2a",
  "window": {"pre": 120, "post": 120},
  "page": 14,
  "score_raw": 0.8421,
  "score_norm": 0.78,
  "rerank_score": 0.67,
  "k_pos": 18,
  "k_final": 3
}
````

---

## Validation rules

1. **Cite first then explain**
   The model must emit citations before or together with the answer. Never after the answer only.

2. **Offsets are monotonic**
   `start < end`. Units are consistent within a run. Character and token units cannot be mixed in the same field.

3. **No cross section reuse by default**
   One answer segment can only use citations from the same `section_id`, unless a whitelist is provided.

4. **Analyzer parity**
   `analyzer` must match the read path. If the analyzer differs at read time, the run fails fast.

5. **Deterministic tiebreak**
   When scores tie, final order uses `(score_norm desc, section_id asc, snippet_id asc)`.

6. **Index identity**
   `index_hash` in citations must match the live index hash logged by the pipeline.

7. **Revision lock**
   `rev` must match the document revision that produced the chunk.

8. **Trace completeness**
   For each citation the log must include `score_raw` or `score_norm`, `k_pos`, and when present `k_final`.

---

## Prompt contract

Embed the citation schema directly in the prompt. Require validation behavior.

```txt
Contract:
- You must cite before you explain.
- Each citation item = {snippet_id, section_id, source_url, offsets, tokens}.
- All citations in one segment must share the same section_id unless I set allow_cross_section=true.
- If any field is missing or inconsistent, stop and return {error: "<field>", fix: "<page to open>"}.

Return JSON:
{
  "citations": [ ... ],
  "answer": "...",
  "ΔS": 0.xx,
  "λ": "<state>"
}
```

Pair this with the post step validator below.

---

## Minimal validators

**Python pseudo**

```python
def validate_citations(items, allow_cross=False):
    if not items:
        return "empty_citations"
    sect = items[0]["section_id"]
    for x in items:
        for f in ["snippet_id","section_id","source_url","offsets","tokens","index_hash","embed_model","analyzer","rev"]:
            if f not in x:
                return f"missing_{f}"
        if x["offsets"]["start"] >= x["offsets"]["end"]:
            return "bad_offsets"
        if not allow_cross and x["section_id"] != sect:
            return "cross_section_reuse"
        if "score_raw" not in x and "score_norm" not in x:
            return "missing_score"
    return "ok"
```

**Return codes**

| Code                  | Meaning                            | Next step                                 |
| --------------------- | ---------------------------------- | ----------------------------------------- |
| `empty_citations`     | Model skipped citation block       | Enforce cite first in prompt contract     |
| `missing_score`       | Store did not carry score metadata | Add score projection in the adapter       |
| `bad_offsets`         | Span math is broken                | Rebuild chunk offsets and verify unit     |
| `cross_section_reuse` | Mixed sources in one segment       | Forbid reuse or add an explicit whitelist |
| `mismatch_index_hash` | Read and write do not match        | Rebuild index or fix boot ordering        |
| `analyzer_mismatch`   | Analyzer differs at read time      | Align analyzer and normalization          |

---

## Log format

Log one line per question and per segment. Keep it grep friendly.

```
ts=2025-08-28 qid=Q001 seg=1
deltaS=0.37 lambda=convergent
k=10 store=faiss index_hash=2f7d...9a embed=bge-large-en-v1.5
citations=[hb24-sec-keys-0007,hb24-sec-keys-0008]
scores=[0.8421,0.8034] kpos=[18,7] kfinal=[3,1]
section_id=policies/security/keys rev=3b91f2a
```

You can mirror this to a table. Example DDL follows.

**SQL table**

```sql
CREATE TABLE rag_traces (
  ts TIMESTAMP NOT NULL,
  qid TEXT NOT NULL,
  seg INTEGER NOT NULL,
  deltaS REAL NOT NULL,
  lambda_state TEXT NOT NULL,
  store TEXT,
  index_hash TEXT,
  embed_model TEXT,
  analyzer TEXT,
  section_id TEXT,
  rev TEXT,
  citations JSONB,
  scores JSONB,
  kpos JSONB,
  kfinal JSONB
);
```

---

## Auditable answer format

Force the model to output a machine checkable block.

```json
{
  "citations": [
    {
      "snippet_id": "hb24-sec-keys-0007",
      "section_id": "policies/security/keys",
      "source_url": "https://example.org/handbook#security-keys",
      "offsets": {"start": 2310, "end": 2688, "unit": "char"},
      "tokens": 188
    }
  ],
  "answer": "Hardware keys are required for all admin roles. The policy defines rotation and recovery.",
  "ΔS": 0.37,
  "λ": "convergent"
}
```

---

## Typical failure modes and exact fixes

* **Citations look right but the text is from another section**
  Install the cross section fence and recheck analyzer parity.
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [chunk\_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)

* **Citation block is present but fields are missing**
  Add the adapter projection. Enforce required fields at the chain boundary.
  Open: [store\_agnostic\_guardrails.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/store_agnostic_guardrails.md)

* **Hybrid retrieval changes the final order every run**
  Add reranking with a fixed model and seed. Log `k_pos` and `k_final`.
  Open: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/rerankers.md)

* **High similarity but wrong meaning**
  Verify analyzer, pooling, and metric. Rebuild if mismatched.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Drop in adapters

**LangChain LCEL**

```python
def lc_project(doc):
    return {
        "doc_id": doc.metadata["doc_id"],
        "section_id": doc.metadata["section_id"],
        "snippet_id": doc.metadata["snippet_id"],
        "source_url": doc.metadata.get("source_url",""),
        "offsets": {"start": doc.metadata["start"], "end": doc.metadata["end"], "unit": "char"},
        "tokens": doc.metadata["tokens"],
        "index_hash": doc.metadata["index_hash"],
        "embed_model": doc.metadata["embed_model"],
        "analyzer": doc.metadata["analyzer"],
        "rev": doc.metadata["rev"],
        "score_raw": doc.metadata.get("score", None),
        "k_pos": doc.metadata.get("k", None)
    }
```

**LlamaIndex**

```python
proj = {
  "doc_id": node.ref_doc_id,
  "section_id": node.metadata.get("section_id",""),
  "snippet_id": node.node_id,
  "source_url": node.metadata.get("source_url",""),
  "offsets": {"start": node.start_char_idx, "end": node.end_char_idx, "unit": "char"},
  "tokens": node.metadata.get("tokens", 0),
  "index_hash": idx_hash,
  "embed_model": embed_id,
  "analyzer": analyzer_id,
  "rev": doc_rev,
  "score_raw": score
}
```

**Semantic Kernel**

```csharp
record Citation(string doc_id, string section_id, string snippet_id,
                string source_url, Offsets offsets, int tokens,
                string index_hash, string embed_model, string analyzer, string rev,
                double? score_raw = null, double? score_norm = null, int? k_pos = null, int? k_final = null);
```

---

## Evaluation recipe

1. Prepare a gold set with 3 to 5 questions per section.
2. Run 3 paraphrases and 2 seeds per question.
3. Check citation match rate and coverage.
4. If match rate falls below 0.95, inspect validator return codes first.
5. Only then tune retrieval and rerank knobs.

More detail → [retrieval\_eval\_recipes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md)

---

## Copy paste test

Use this to smoke test your chain.

```txt
You have TXTOS and the WFGY Problem Map loaded.

Task: validate the citations using the schema defined in my contract.
Input: {the model JSON}

If the payload is valid, reply "OK" and give ΔS and λ.
If invalid, return {error: "<code>", field: "<name>", tip: "<page to open>"}.
Use pages: retrieval-traceability, data-contracts, chunk-alignment, rerankers.
```

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                                                  | Link                                                                                               |
| --------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework                        | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines                       | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift         | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                        | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |

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
