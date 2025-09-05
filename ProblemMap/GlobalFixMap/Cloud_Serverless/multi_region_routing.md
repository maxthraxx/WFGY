# Multi-Region and Failover Routing Guardrails

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


Keep latency low, fail over safely, and avoid split-brain state while your RAG, queues, and streams operate across regions. This page gives a compact playbook that you can paste into any load balancer or edge router policy.

## When to use this page

* Users in different geos see different answers or stale citations.
* Region outage triggers duplicate tool calls or replayed webhooks.
* Vector writes happen in one region while reads route to another.
* Canary in a single region is green yet the global cutover fails.
* DNS or anycast flips cut long-running streams.

## Open these first

* Boot order and deploy sequencing: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
* Cross-service waits during rollout: [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)
* First call failure after a new region comes online: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Retrieval correctness under routing changes: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) · [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Contract the payload and lock schemas: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Reindex rules after topology change: [Reindex and Migration](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)
* Live probes and rollback: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Acceptance targets

* p95 latency improves for local users or stays within ten percent of single-region baseline.
* No increase in 5xx at failover or failback.
* Idempotency dedupe rate ≥ 99.9 percent on all write paths during failover windows.
* For RAG: ΔS(question, retrieved) drift ≤ 0.03 across regions, λ remains convergent on two seeds.
* Vector index hash identical per region before routing users. `INDEX_HASH` matches on probes.

---

## Fix in 60 seconds

1. **Pin by header, not only DNS**
   Add `X-Region-Pin: {region}` and `X-Release: {rev}`. Edge selects nearest healthy region unless a pin is present. Synthetic probes always include the pin.

2. **Fence writes with idempotency keys**
   Compute `sha256(source_id + revision + index_hash + partition)` and drop duplicates in the KV. Keep the fence for failover\_window plus 24 hours.

3. **Replicate index and blobs before traffic**
   Block user routing until `INDEX_HASH` equals across regions and blob manifests match.

4. **Graceful streams**
   Sticky route long-lived connections. Drain the old region for N seconds. Do not cut an active stream at the router.

5. **Health with contract checks**
   Health is green only if `schema_rev`, `model_tag`, `index_hash` and secret versions match. Pure 200 is not sufficient.

---

## Routing patterns that work

* **Active-active with sticky reads**
  Reads route to nearest healthy region and stay sticky for the session. Writes go to the region that owns the partition. Use a queue to replicate to others.

* **Active-passive for stateful writers**
  All writes go to primary. Secondary serves read-only. Promote only after index and blob parity plus a clean queue tail.

* **Geo-partitioned stores**
  Partition by tenant or namespace. Keep retrieval within the same partition and region. Cross-partition requests require a join step with explicit contracts.

---

## Typical breakpoints → exact fix

* **Wrong snippet in far region despite high similarity**
  Index or metric differs. Compare `INDEX_HASH` and analyzer settings. Rebuild and verify a small gold set before routing traffic.
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Duplicate webhooks during regional flip**
  Retry plus DNS cutover replays the same event. Use the idempotency fence and a replay TTL beyond the failover window.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **Split-brain memory or tool cache**
  Agent memory writes with no version pins cross regions. Namespace by `tenant`, `mem_rev`, and `region`.
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

* **Streams cut at failover**
  Router does not support drain. Pin streams with a cookie or header, then change the default path only for new connections.
  Open: [Timeouts and Streaming Limits](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md)

* **Cost spikes after enabling global anycast**
  Cold starts increase in remote regions. Raise min instances or provisioned concurrency selectively on hot routes.
  Open: [Cold Start and Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md)

---

## Minimal recipes you can copy

### A) Region pinning contract

```txt
Request headers
- X-Region-Pin: us-east-1 | eu-west-1 | ap-southeast-1
- X-Release: r2025-08-27
- X-Index-Hash: a1b2c3
- X-Schema-Rev: sc-12
Router rule
- If pin present and region healthy → route pinned
- Else pick nearest healthy with matching {schema_rev, index_hash, model_tag}
- Sticky cookie for streaming connections
```

### B) Failover gate

```txt
Gate conditions before user traffic
- INDEX_HASH equal across regions
- Blob manifest parity
- Health probes return {schema_rev, model_tag, secrets_rev} exact match
- Synthetic RAG probes: ΔS drift ≤ 0.03 on k=10 questions
- Dedupe KV warm and reachable in both regions
```

### C) Vector replication note

```txt
Replication
- Prefer periodic rebuild from source texts per region
- If log shipping: checkpoint offsets, verify analyzer parity
- After topology change: run gold-set eval and lock reranker order
Refs: retrieval-playbook, reindex-migration
```

---

## Observability you must add

* Split metrics by `region`, `release_id`, and `revision`.
* Health includes `schema_rev`, `index_hash`, `model_tag`, `secrets_rev`.
* Dedupe hit rate, queue age, replay counts per region.
* ΔS and λ on a fixed probe set, per region.
* Stream drain success count at flips.

## Verification

* Probe set stable within acceptance targets.
* No duplicate side effects in the failover window.
* p95 improves for local users or remains flat.
* Queue age does not spike at promotion.

## When to escalate

* Persistent ΔS drift across regions after rebuild. Re-embed with the same analyzer and metric, then re-run the gold set.
* Dedupe misses during outage replay. Increase KV TTL and ensure consistent hashing across regions.
* Health green yet errors rise. Add contract checks to the probe and block routing when versions disagree.

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
