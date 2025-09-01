# Ops & Deploy — Global Fix Map

A compact hub to **ship safely and keep RAG/LLM systems stable after release**.  
Use this folder to pick the right guardrail, verify with measurable targets, and recover fast when things wobble. No infra change required.

---

## Open these first
- Visual recovery map → [RAG Architecture & Recovery](../../rag-architecture-and-recovery.md)  
- Retrieval knobs end-to-end → [Retrieval Playbook](../../retrieval-playbook.md)  
- Traceability and snippet schema → [Retrieval Traceability](../../retrieval-traceability.md) · [Data Contracts](../../data-contracts.md)  
- Boot order and deploy traps → [Bootstrap Ordering](../../bootstrap-ordering.md) · [Deployment Deadlock](../../deployment-deadlock.md) · [Pre-Deploy Collapse](../../predeploy-collapse.md)  
- Live ops tools → [Live Monitoring for RAG](../../ops/live_monitoring_rag.md) · [Debug Playbook](../../ops/debug_playbook.md)  

---

## When to use this folder
- First calls after deploy crash or return stale content.  
- ΔS and citations look fine yesterday but flip today.  
- Rate limits cascade, queues spike, latency climbs.  
- Canary looks good then full rollout breaks retrieval.  
- Index swap succeeds but answers cite old snippets.  
- Retries cause duplicate side effects or charges.  
- Feature flags bleed traffic into unfinished paths.  
- Maintenance windows corrupt embeddings or anchors.  

---

## Acceptance targets for a safe rollout
- **ΔS(question, retrieved) ≤ 0.45** across three paraphrases.  
- **Coverage ≥ 0.70** on the expected new section.  
- **λ remains convergent** on 2 seeds during rollout.  
- **Idempotency ≥ 99.9%** on retry storms.  
- **Zero silent index mismatches** (hash + counts match).  
- **P95 latency stays in budget** with backpressure active.  

---

## Quick routes — per-page guides

| Scenario | Fix Page |
|----------|----------|
| Rollout readiness | [rollout_readiness_gate.md](./rollout_readiness_gate.md) |
| Canary strategy | [staged_rollout_canary.md](./staged_rollout_canary.md) |
| Blue/green cutover | [blue_green_switchovers.md](./blue_green_switchovers.md) |
| Version pin & freeze | [version_pinning_and_model_lock.md](./version_pinning_and_model_lock.md) |
| Vector index swap | [vector_index_build_and_swap.md](./vector_index_build_and_swap.md) |
| Cache warmup | [cache_warmup_invalidation.md](./cache_warmup_invalidation.md) |
| Rate limits | [rate_limit_backpressure.md](./rate_limit_backpressure.md) |
| Feature flags | [feature_flags_safe_launch.md](./feature_flags_safe_launch.md) |
| Idempotency | [idempotency_dedupe.md](./idempotency_dedupe.md) |
| Retry logic | [retry_backoff.md](./retry_backoff.md) |
| Rollback plan | [rollback_and_fast_recovery.md](./rollback_and_fast_recovery.md) |
| Postmortems | [postmortem_and_regression_tests.md](./postmortem_and_regression_tests.md) |
| Change freeze | [release_calendar_and_change_freeze.md](./release_calendar_and_change_freeze.md) |
| Incident comms | [incident_comms_and_statuspage.md](./incident_comms_and_statuspage.md) |
| Shadow traffic | [shadow_traffic_mirroring.md](./shadow_traffic_mirroring.md) |
| Maintenance window | [read_only_mode_and_maintenance_window.md](./read_only_mode_and_maintenance_window.md) |
| DB migrations | [db_migration_guardrails.md](./db_migration_guardrails.md) |

---

## 60-second ship checklist

1. **Freeze the world** → Pin model IDs, prompt revs, index hashes.  
2. **Warm up safely** → Build index off-path, preload caches with canary.  
3. **Shadow then canary** → Mirror prod queries, step rollout 5% → 25% → 100%.  
4. **Guard the edge** → Enable backpressure, retries with jitter, idempotency keys.  
5. **Know your exit** → Keep rollback switch and comms draft ready.  

---

## Symptoms → exact fix

| What you see | Open this |
|--------------|-----------|
| Deploy points to old snippets | [vector_index_build_and_swap.md](./vector_index_build_and_swap.md) · [cache_warmup_invalidation.md](./cache_warmup_invalidation.md) |
| Canary fine, full rollout breaks | [staged_rollout_canary.md](./staged_rollout_canary.md) · [feature_flags_safe_launch.md](./feature_flags_safe_launch.md) |
| Wrong model after failover | [version_pinning_and_model_lock.md](./version_pinning_and_model_lock.md) |
| Retries duplicate charges | [idempotency_dedupe.md](./idempotency_dedupe.md) · [retry_backoff.md](./retry_backoff.md) |
| RL storms, timeouts | [rate_limit_backpressure.md](./rate_limit_backpressure.md) |
| Need rollback now | [rollback_and_fast_recovery.md](./rollback_and_fast_recovery.md) · [blue_green_switchovers.md](./blue_green_switchovers.md) |
| Maintenance corrupts anchors | [read_only_mode_and_maintenance_window.md](./read_only_mode_and_maintenance_window.md) · [db_migration_guardrails.md](./db_migration_guardrails.md) |
| Unsure if safe to ship | [rollout_readiness_gate.md](./rollout_readiness_gate.md) |

---

## FAQ

**Q: What does ΔS mean here?**  
A: ΔS is a stability score. It measures how much the retrieved content drifts from the expected anchor when you change the query slightly. Lower is better (≤ 0.45 is safe).  

**Q: What is λ convergence?**  
A: λ tracks whether retrieval order flips unpredictably. If λ is stable across seeds, your rollout is consistent.  

**Q: Why do I need idempotency keys?**  
A: Without them, retries can double-charge a user or run the same side-effect twice. Keys make every request “safe to retry.”  

**Q: How do I know if my index swap worked?**  
A: Check doc counts and hashes before cutover. If they mismatch, you’re pointing at an incomplete index.  

**Q: Canary looked fine but production broke — why?**  
A: Canary often hides tail-latency, cache misses, or load-based rate limits. Always test at increasing % of live traffic.  

**Q: Why do you mention rollback comms?**  
A: Technical rollback is only half. Users and stakeholders need fast updates, so pre-draft Statuspage or Slack messages are essential.  

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
