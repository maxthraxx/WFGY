# Deploy and Traffic Shaping — Guardrails

Control how new code reaches users so you avoid cold spikes, duplicate effects, and version-skew crashes. This page gives a fast, provider-agnostic playbook for serverless rollouts with RAG, streaming, queues, and webhooks in the loop.

## When to use this page

* “Zero-downtime” deploys still produce 5xx or p95 jumps.
* Webhooks or jobs fire twice during slot swaps or revision flips.
* Streaming responses cut mid-flight while traffic shifts.
* Vector writes or indexes receive mixed schema during rollout.
* Canary looks healthy, then collapses at 25–50 percent.

## Open these first

* Boot order safety: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
* Rollout deadlocks: [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)
* First call failure after deploy: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Live probes and rollback: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
* RAG wide view for downstream calls: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Contract the payloads you ship: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Acceptance targets

* No increase in 5xx rate at each traffic step.
* p95 latency delta between old and new ≤ 10 percent at equal load.
* Cold-start share ≤ 5 percent after warm-up gates.
* No duplicate side effects. Dedupe hit rate ≥ 99.9 percent for idempotent POST.
* For RAG: ΔS(question, retrieved) stays within ±0.03 between old and new. λ remains convergent on two seeds.

---

## Fix in 60 seconds

1. **Canary with gates**
   Route 1 → 5 → 25 → 50 → 100 percent only if gates pass: 5xx flat, p95 flat, ΔS stable, queue age flat.

2. **Pre-warm and pin**
   Set min instances or provisioned concurrency for the new revision. Pin a canary header `X-Release: new` for synthetic traffic before shifting users.

3. **Graceful draining**
   Enable connection draining. Keep old revision serving for N seconds while you stop sending new requests. Do not kill active streams.

4. **Idempotency fence**
   Add `Idempotency-Key` on all write paths and background jobs. Store in KV for at least release\_window + 24 h.

5. **Schema locks**
   Embed `INDEX_HASH`, `SCHEMA_REV`, and `MODEL_TAG` in every request. Reject if the backend is behind. Route user to the matching revision.

---

## Typical breakpoints → exact fix

* **Version skew between retriever and writer**
  New code writes updated fields but retriever uses old schema. Lock with `SCHEMA_REV` in requests and refuse cross-rev traffic.
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Webhook storms after deploy**
  Retries plus slot swap triggers double delivery. Use dedupe key = `sha256(source_id + event_rev + index_hash)`.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **Canary fine, 25 percent fails**
  New revision saturates cold CPU or NAT. Raise min instances or provisioned concurrency before the 25 percent step.
  Open: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Streaming cuts during shift**
  Traffic router closes long-lived connections. Enable draining and pin streams to a revision using a sticky cookie or header.

* **Queues drain twice**
  Two workers on different revisions read the same shard without a fence. Lock by `queue_partition + release_id`.

---

## Minimal recipes you can copy

### A) Weighted rollout with pinned canary

```txt
Headers:
- X-Release: canary
- X-Canary: true
Routing:
- 1% → 5% → 25% → 50% → 100%
Gates per step:
- 5xx delta ≤ 0.05%, p95 delta ≤ 10%
- ΔS drift ≤ 0.03 on canary questions (k=10)
- Queue age slope ≤ 0
Rollback:
- instant shift to previous revision if any gate fails
```

### B) Serverless config checklist

```txt
Warm-up
- min_instances or provisioned_concurrency ≥ expected p50 load
- warm path hits cache, model, secrets, vector client

Draining
- connection_drain_seconds: 60–120
- keep old revision for draining window after last route

Idempotency
- Idempotency-Key on POST, stored in KV ≥ 24h
- retry policy: 3 tries, jitter, total time < request timeout

Schema pins
- SCHEMA_REV, INDEX_HASH, MODEL_TAG in every call
```

### C) Background jobs and batch

```txt
During 1–25% steps:
- pause heavy batch, only allow user-facing flows
- cap queue concurrency per partition
- fence by (partition, release_id)
```

---

## Observability you must add

* Split all metrics by `release_id` and `revision`.
* 5xx, p95, cold-start rate per revision.
* Queue age, retries, dedupe\_hits.
* ΔS and λ on a fixed probe set, old vs new.
* Rollout timeline with traffic percent and gate decisions.

## Verification

* Probe set shows ΔS and λ unchanged within targets.
* No duplicate side effects in logs for the rollout window.
* p95 and error rate flat across each step.
* Draining proves streams finish on old revision.

## When to escalate

* Any gate fails twice at the same step → freeze traffic, roll back, keep warm, investigate NAT, DNS, or cold-start headroom.
* Schema incompatibility detected → hold rollout, bump `SCHEMA_REV`, re-index or add translation layer, re-run canary.
* Sticky routing not respected → switch to cookie pinning or per-request header pin.

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
