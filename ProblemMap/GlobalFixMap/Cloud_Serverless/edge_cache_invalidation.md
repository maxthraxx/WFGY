# Edge Cache Invalidation — Guardrails

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Cloud_Serverless**.  
  > To reorient, go back here:  
  >
  > - [**Cloud_Serverless** — scalable functions and event-driven pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A practical repair guide for CDN and edge caches when your app ships new prompts, models, or assets. Use this to keep caches consistent across regions and prevent old content from leaking back in after a deploy or rollback.

## When to use this page

* Users still receive old prompts or UI after a release.
* Rollbacks do not take effect everywhere at once.
* Canary works but global traffic serves mixed versions.
* Private pages or signed assets are accidentally cached.
* Your purge jobs complete but stale content keeps reappearing.

## Open these first

* Release safety and boot order: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
* Deadlocks during deploy or purge waves: [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)
* First call fails after rollout: [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Auditable payloads and version fields: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Live probes and rollback signals: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
* RAG wide view, for prompt and snippet assets: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

## Acceptance targets

* After release, 99.9 percent of requests serve the new version within 120 seconds across all edge regions.
* Purge jobs finish with measured `purge_latency_p95 ≤ 30 s`.
* Stale-hit rate ≤ 0.1 percent after the convergence window.
* No private responses stored at the edge. Zero cache-poison events in audit.

---

## Fix in 60 seconds

1. **Pick a single strategy for each asset class**

   * **Immutable by content hash** for static files and prompt bundles. Example: `/prompts/prompt.ABC123.txt` with `Cache-Control: public, max-age=31536000, immutable`.
   * **Purge by key** for dynamic render endpoints and JSON. Attach `Surrogate-Key: release:<id> route:/api/search`.

2. **Stamp every response with validators**

   * Set `ETag` from a stable hash of the payload and `Release-Id: RYYYYMMDD.N`.
   * Include `Vary` only where needed: `Vary: Authorization, Accept-Encoding`.

3. **Two step rollout**

   * **Step A** publish all immutable assets first.
   * **Step B** flip traffic and purge keys in parallel: `release:<id>`, plus any route keys. Keep a fixed order to avoid cache rewarming storms.

4. **Define a safe bypass**

   * Accept a header `X-Bypass-Cache: 1` that disables caching at origin and marks the response `Cache-Control: no-store`.
   * Use it in monitors and during hotfix windows only.

5. **Put a time box on stale**

   * For pages that tolerate brief staleness use `stale-while-revalidate=60, stale-if-error=300`.
   * For prompts, snippets, and policy text do not allow staleness.

---

## Typical breakpoints → exact fix

* **Users alternate between old and new UI**
  Mixed strategy or missing keys. Consolidate to content-hash for static and surrogate-keys for dynamic.
  Open: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **Purge completes but some regions keep serving stale**
  Purge API acknowledges enqueue, not completion. Add region probes and continue until `purge_latency_p95` clears.
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

* **Private pages cached at the edge**
  Missing auth vary or cache-control. Set `Cache-Control: private, no-store` for authenticated pages and add `Vary: Authorization`.
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Prompt or policy text cached long after rollback**
  Treat prompt bundles as immutable artifacts by hash. Switch references, never overwrite the old file path.
  Open: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

* **Cache poisoning through query strings or fragments**
  Normalize URLs, reject unknown parameters, and include a canonical key.
  Open: [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

---

## Minimal recipes you can copy

### A) Content addressed asset

```txt
# Build time
hash = sha256(file)
target = /assets/prompt.${hash}.txt
upload(target, file)

# Response headers at CDN
Cache-Control: public, max-age=31536000, immutable
ETag: "W/${hash}"
Release-Id: R2025.08.29.1
```

### B) Surrogate key taxonomy

```txt
Surrogate-Key: release:R2025.08.29 route:/api/search tenant:t123
Cache-Control: public, max-age=120, stale-while-revalidate=60
ETag: "payload-7f98"
```

Purge list for a rollout:

```txt
keys = [
  "release:R2025.08.29",
  "route:/app/home",
  "route:/api/search"
]
```

### C) Safe purge worker

```txt
for key in keys:
  job_id = cdn.purge_by_key(key)
  wait_until_complete(job_id, timeout=60)  # poll region status
```

### D) Do not cache private responses

```txt
if request.has_auth():
  set_header("Cache-Control", "private, no-store")
  set_header("Vary", "Authorization")
else:
  set_header("Cache-Control", "public, max-age=120")
```

### E) Rollback in place

```txt
# Switch the release pointer
set_kv("current_release", "R2025.08.28")
cdn.purge_by_key("release:R2025.08.29")
```

---

## Observability you must add

* `purge_latency_p50 p95`, `purge_errors`.
* `stale_hit_rate` by route, by region.
* `validator_mismatch` when `If-None-Match` disagrees with current `ETag`.
* `private_cache_incidents`.
* Synthetic probes for each region that fetch with and without `X-Bypass-Cache`.

## Verification

* Blue green check: both releases respond with different `ETag` and `Release-Id`.
* After purge, regional probes converge within the target window.
* Auth pages never show `Age` header.
* Prompt and policy files always referenced by hash, never by mutable name.

## When to escalate

* If purge never converges, split surrogate keys and shorten TTL temporarily.
* If traffic thrashes origin after purge, warm top routes with low QPS prefetch.
* If private leakage occurs, add explicit deny rules at CDN for `Authorization` present.

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
