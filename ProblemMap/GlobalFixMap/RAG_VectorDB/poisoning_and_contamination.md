# Poisoning and Contamination — Guardrails and Fix Pattern

Use this page when your **retriever starts surfacing adversarial or low-trust text** that did not exist in your canonical corpus, or when cache/index merges leak content across tenants or environments. We treat three classes: content poisoning, index contamination, and query-time prompt-in-context attacks.

---

## Open these first

- Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Traceability and snippet schema → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Metric and normalization sanity → [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/metric_mismatch.md) · [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/normalization_and_scaling.md)  
- Tokenizer pitfalls → [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/tokenization_and_casing.md)  
- Store health and splits → [vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md)  
- Hybrid fusion → [hybrid_retriever_weights.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/hybrid_retriever_weights.md)

---

## Core acceptance

- **Provenance coverage ≥ 0.95** of indexed snippets have a valid signed ingest manifest.  
- **Poison recall ≥ 0.90** on a seeded red-team set with near-zero false positives (≤ 0.02).  
- **Tenant isolation**: zero cross-namespace hits in 10k randomized queries.  
- **ΔS(question, retrieved) ≤ 0.45** after quarantine, across 3 paraphrases and 2 seeds.  
- **λ** remains convergent when adversarial candidates are present but quarantined.

---

## Quick triage

| Symptom | Likely cause | Open this |
|---|---|---|
| New, off-brand text appears in results after a site crawl | ingestion path accepts untrusted domains or query params | tighten allowlist via [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and add manifest checks below |
| Same doc shows mixed tenant banners or footers | index contamination or namespace leak | [vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md) |
| Adversarial strings like “ignore previous instructions” stored inside snippets | context-level prompt injection preserved into corpus | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and citation-first prompting |
| Abrupt shift in token stats, casing, or Unicode forms | poisoned batch with tokenizer skew | [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/tokenization_and_casing.md) |
| Good recall, but answers quote junk domains | provenance score missing in fusion | add authority/manifest weights in fusion and see [hybrid_retriever_weights.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/hybrid_retriever_weights.md) |

---

## Hardening plan in 7 concrete steps

1) **Provenance contract at ingest**  
   Require an **ingest manifest** per document: `{source_type, source_url, crawl_time, signer, content_hash, schema_rev}`. Reject if missing or signer not in allowlist. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

2) **Canonicalize and fingerprint**  
   Build `content_hash = xxh64(canonical_text)` and `simhash_64` on token 3-grams. Log `(doc_id, section_id, content_hash, simhash_64)` for every snippet.

3) **Authority and trust scoring**  
   Maintain `provenance_score ∈ [0,1]` from source allowlist, TLS, HSTS, domain reputation, and signer. Store with each snippet.

4) **Poison scoring and quarantine**  
   Compute `poison_score` from features: abrupt Δ in token distribution, repeated instruction phrases, suspicious URLs, CSS/JS remnants, high simhash match to known attack corpora. If `poison_score ≥ τ_p`, route to **quarantine_index** not the main index.

5) **Namespace fences**  
   Enforce `{tenant_id, product_id, env}` in the key. Deny cross-namespace reads by default. Verify in retrieval traces.

6) **Fusion with provenance**  
   During hybrid fusion, weight by provenance: `w_final = α·w_bm25 + β·w_dense + γ·provenance_score − δ·poison_score`. Do **dedupe** before and after fusion.

7) **Revocation and rebuild**  
   Keep a **revocation list** of `content_hash` and manifests. On revocation, remove from indexes, purge caches, and re-embed neighbors to avoid residual bias.

---

## Minimal reference recipe

```yaml
ingest:
  allowlist:
    domains: ["docs.company.com", "kb.company.com"]
    schemes:  ["https"]
    signer_keys: ["ed25519:..."]
  manifest_required: true

fingerprint:
  canonicalize: {nfkc: true, lowercase: true, collapse_spaces: true, strip_soft_hyphen: true}
  content_hash: "xxh64"
  simhash_bits: 64

scores:
  provenance:
    domain_reputation_weight: 0.4
    signer_weight: 0.4
    tls_policy_weight: 0.2
  poison:
    tokenshift_z_max: 0.25
    adversarial_phrase_boost: true
    url_entropy_threshold: 4.2

retrieval:
  namespace_keys: ["tenant_id", "product_id", "env"]
  fusion_weights: {bm25: 0.35, dense: 0.45, provenance: 0.25, poison: -0.40}
  quarantine_threshold: 0.60
  quarantine_index: "rag_quarantine"

ops:
  revocation_list: "kv:rag_revocations"
  cache_invalidate_on_revoke: true
````

---

## Query-time shields

* **Citation-first** and schema-locked prompting so the model must **quote before reasoning**. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).
* **Outlier alert** when a top candidate has `provenance_score < 0.3` or lives in `quarantine_index`.
* **Tenant assert** in every request: `{tenant_id, env}` must match the index namespace. Reject otherwise.

---

## Observability you must log

* Poison detection counts per batch and per source domain.
* Top phrases that triggered poison flags with sample hashes.
* Namespace violations blocked.
* Fusion weight contributions for the final top k.
* ΔS and λ at retrieve, fuse, quarantine, and answer.
* Revocation actions: which hashes, which indexes, time to full purge.

---

## Incident response and cleanup

1. Freeze writes to affected namespaces.
2. Export suspect snippets by `content_hash` and `manifest_id`.
3. Add to revocation list, purge index shards and caches.
4. Re-embed neighbor windows around removed spans to reduce drift.
5. Rebuild acceptance set: verify ΔS ≤ 0.45 and coverage ≥ 0.70 on gold Qs.
6. Postmortem and **new allowlist rule** to prevent recurrence.

---

## Verification

* Seed 200 adversarial docs mixed into 10k clean.

  * Poison recall ≥ 0.90 at τ selected by ROC on the seed.
  * False positive rate ≤ 0.02 on clean control.
  * Tenant isolation: 0 cross-namespace hits in 10k queries.
  * Final ΔS and λ targets met across paraphrases.

---

## Copy-paste prompt for the LLM step

```txt
You have TXTOS and WFGY Problem Map loaded.

Given the fused candidates with fields {provenance_score, poison_score, namespace, snippet_id, content_hash, citations}:

1) Discard any candidate where namespace != request.namespace.
2) If poison_score ≥ 0.60, quarantine and return a short fix note.
3) Rerank remaining by (model_score + 0.25*provenance_score - 0.40*poison_score).
4) Enforce cite-then-explain and return:
{
  "kept": [{"snippet_id": "...", "source_url": "..."}],
  "quarantined": [{"snippet_id": "...", "reason": "..."}],
  "ΔS": 0.xx,
  "λ_state": "...",
  "next_fix": "..."
}
```

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** — <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>

