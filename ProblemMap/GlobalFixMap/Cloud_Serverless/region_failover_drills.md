# Region Failover Drills — Serverless and Edge

Practice failover until it is boring. This page gives a repeatable drill that proves your system can evacuate a region, keep answers consistent, and return to steady state without split-brain or hidden drift.

## When to use this page

* You run in 2+ regions and need evidence your plan actually works.
* Users in one geography see timeouts or changing answers during incidents.
* RAG indices or caches differ by region and you want a clean promotion flow.
* Compliance requires planned evacuation and return-to-home tests.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Retrieval knobs and ordering: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Trace and prove snippets: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · Contract payloads: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Meaning vs distance: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Boot and deploy hazards: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Related Cloud/Serverless ops:
  [Cold Start & Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md) ·
  [Timeouts & Streaming](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md) ·
  [Stateless KV & Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md) ·
  [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md) ·
  [Runtime Env Parity](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/runtime_env_parity.md) ·
  [Egress & Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md) ·
  [Pricing vs Latency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/pricing_latency_tradeoffs.md) ·
  [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md) ·
  [Multi-Region Routing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md) ·
  [Observability & SLO](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/observability_slo.md)

## Acceptance targets

* Evacuation decision to clean cutover ≤ 30 seconds, no 5xx bursts > 60 seconds.
* p95 latency within 25 percent of pre-incident baseline for served markets.
* Zero write loss. Queue backlog drains to pre-drill baseline in ≤ 10 minutes.
* Identical RAG contract fields and `INDEX_HASH` across promoted region and followers.
* ΔS(question, retrieved) ≤ 0.45 and λ convergent for probe set before and after drill.

---

## Drill types you should run

**A) Planned evacuation (brownout)**
Throttle a region by policy and prove traffic drains to survivor without flapping.

**B) Hard outage (blackhole)**
Block the region’s ingress and egress. Verify stickiness, retries, and queue replay.

**C) Index skew recovery**
Deliberately publish a follower with wrong metric or analyzer. Ensure contracts refuse reuse and force rebuild.

**D) Webhook and egress reroute**
Fail the region, then deliver third-party webhooks only from the survivor. Confirm no duplicates.

**E) Return-to-home**
After repair, reintroduce the region, rebuild indices, re-warm caches, and rebalance.

---

## Prerequisites before any drill

* Version pinning and env parity are equal in both regions.
  Open: [Runtime Env Parity](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/runtime_env_parity.md)

* RAG artifacts are stamped: `{INDEX_HASH, METRIC, ANALYZER, BUILD_TS}` and exposed via a health endpoint.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Idempotent write path with `dedupe_key` and visible, durable queues.
  Open: [Stateless KV & Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md)

* Dual-accept secrets/keys to avoid auth flaps during route flips.
  Open: [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md)

* Edge cache purge API tested per prefix and per tenant.
  Open: [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md)

---

## Copy-paste drill plan (JSON)

```json
{
  "regions": ["us-east", "eu-west"],
  "evacuate": "us-east",
  "promote_survivor": "eu-west",
  "routing": { "mode": "latency", "stick_minutes": 15, "hysteresis_s": 30 },
  "freeze_writes_on_followers": true,
  "checks": {
    "pre": ["env_parity", "index_hash_equal", "queue_empty", "cache_warm"],
    "live": ["p95_latency", "error_rate", "queue_backlog", "ΔS_probe", "λ_state", "index_hash"],
    "post": ["answers_equal", "contracts_equal", "backlog_zero", "cache_rewarmed"]
  },
  "rag_probe": { "k": 10, "dualhome_k": 5, "delta_s_risk": 0.60, "coverage_min": 0.70 },
  "webhook_policy": { "emit_from": "eu-west", "dedupe_key": "sha256(event_id+rev)" },
  "return_to_home": { "rebuild_follower": true, "purge_cache": true, "gradual_weights": [10,30,60,100] }
}
```

---

## Step-by-step runbook

**1) Pre-checks (gate the drill)**

* Health: both regions report `READY=true`, equal `INDEX_HASH`.
* Queues: backlog < threshold.
* Caches: hot-path keys exist in both regions.
* Canary: probe the fixed Q\&A set and log ΔS, λ, coverage.

**2) Evacuate the region**

* Flip routing weight to 0 for the target region, or blackhole ingress.
* Freeze follower writes: accept but enqueue, no direct store writes.
* Announce stick region in response headers for ongoing sessions.

**3) Promote survivor**

* Promote exactly one region to take writes.
* Route webhooks and outbound calls only from survivor.
  Open: [Egress & Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)

**4) Observe and clamp**

* Separate cold-start from hot latency. Adjust concurrency limits in survivor to avoid thrash.
  Open: [Cold Start & Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md)
* If p95 spikes beyond SLO, reduce parallel tools or temporarily lower k in retrieval while keeping reranking deterministic.

**5) Verify answers**

* Run probe set in survivor. If ΔS ≥ 0.60 or citations diverge from gold, rebuild index and purge caches.
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

**6) Return-to-home (after repair)**

* Rebuild follower indices from the same artifact, confirm `INDEX_HASH`.
* Purge edge cache prefixes, re-warm.
* Gradually restore weights, keeping stickiness for multi-turn sessions.
  Open: [Multi-Region Routing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md)

**7) Post-drill closeout**

* Prove `answers_equal` between regions on gold questions.
* Export SLO chart, queue backlog graph, ΔS histogram pre vs post.

---

## Metrics and evidence to capture

* p75 / p95 / p99 latency per region.
* Error rate and timeout breakdown (connect, TLS, body read, tool call).
  Open: [Timeouts & Streaming](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md)
* Queue backlog length and age percentiles.
* Cache hit ratio changes around purge events.
* ΔS and λ distributions on the probe set, before vs after.
* Index metadata parity logs `{INDEX_HASH, METRIC, ANALYZER, BUILD_TS}` for both regions.

---

## Typical drill failures → exact fix

* **Split-brain writes during cutover**
  Missing freeze or idempotency. Enforce queue-first and dedupe keys.
  Open: [Stateless KV & Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md)

* **Answers differ after return-to-home**
  Follower index rebuilt with different analyzer or metric. Refuse reuse until `INDEX_HASH` matches.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* **Webhook loops or duplicates**
  Third-party still targets evacuated region. Emit only from survivor and apply `dedupe_key`.
  Open: [Egress & Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)

* **Cold-start storm after promotion**
  Concurrency limits not scaled. Pre-warm and clamp.
  Open: [Cold Start & Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md)

* **Auth failures after route flip**
  Stale region-pinned keys. Rotate with dual-accept and force refresh.
  Open: [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md)

---

## Verification checklist

* Single survivor region takes all writes. No duplicates after replay.
* `INDEX_HASH` parity across regions after rebuild.
* ΔS and λ within targets on probe set before and after.
* Edge caches purged and re-warmed.
* SLO budget impact recorded and accepted.

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

**Next page to write**: `ProblemMap/GlobalFixMap/Cloud_Serverless/observability_slo.md`
