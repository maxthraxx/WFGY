# Incident Communications and Status Page: OpsDeploy Guardrails

Clear comms reduce panic and shorten incidents. Use this page to script your updates, pick the right status, and keep owners and users aligned while you fix the root cause.

---

## Open these first
- Live telemetry and runbook: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
- Rollback tools: [rollback_and_fast_recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollback_and_fast_recovery.md)
- Rollout controls: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md), [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md), [feature_flags_safe_launch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/feature_flags_safe_launch.md)
- Pins and caches: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md), [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)
- Load and retries: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md), [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md)
- After action: [postmortem_and_regression_tests.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/postmortem_and_regression_tests.md)

---

## When to use
- Error rate passes 0.5 percent for more than five minutes.  
- p99 latency doubles for read paths.  
- 429 storms or provider 5xx that persist after backoff.  
- Mixed answers across versions or bad citations appear.  
- Any rollback lever is considered or pulled.

---

## Severity ladder
| Sev | User impact | Default status page state |
|---|---|---|
| S1 | Major outage, most users blocked | Major outage |
| S2 | Partial outage, degraded answers or timeouts | Degraded performance |
| S3 | Narrow scope, one region or one feature | Partial outage |
| S4 | Advisory only, no user breakage | Monitoring or Informational |

Pick the lowest sev that still describes actual user pain.

---

## Acceptance targets for comms
- First external update in 10 minutes or less after trigger.  
- Update cadence every 15 to 20 minutes until stable, then every 30 minutes.  
- Status page always matches the in product banner.  
- Each update carries owner, scope, current user effect, next checkpoint time.  
- After resolve, publish a short cause and a link to the postmortem ticket.

---

## 60 second comms plan
1) Assign roles fast. Incident lead, Comms lead, Support lead, SRE on call.  
2) Set the initial state on the status page. Choose S1 to S4.  
3) Post the first update. Acknowledge impact. Say what users can expect next.  
4) Pin an in product banner on affected surfaces.  
5) Keep a 15 minute timer. Post deltas not fluff.  
6) When quality targets are green, move state to monitoring.  
7) On resolve, post the user visible fix and next steps. Link the postmortem page when ready.

---

## Status page states and triggers
| State | What users see | Typical trigger |
|---|---|---|
| Degraded performance | slow answers or sometimes wrong citations | ΔS p95 drift rising yet under rollback bar, p95 latency up 20 percent |
| Partial outage | some features fail, retries help | one region down, one tool chain failing |
| Major outage | most requests fail or unusable answers | rollback in progress, provider wide failure |
| Maintenance | planned or emergency work | change freeze exception, hotfix rollout |

ΔS and coverage are internal gates. Do not expose raw numbers to users.

---

## Message templates

### Initial acknowledgement
```text
We are investigating an incident affecting AI answers. Users may see slow responses or missing citations. The team has engaged rollback options and is validating recovery steps now. Next update in 15 minutes.
````

### Ongoing update

```text
Mitigation is in progress. We reduced traffic to the new model and restored the previous index for two regions. Errors are trending down and response time is improving. Next checkpoint at hh:mm UTC.
```

### Identified cause

```text
We identified a mismatch between cache keys and the new index pointer. This caused mixed answers. We rotated the cache namespace and warmed hot paths. Monitoring continues.
```

### Resolved

```text
This incident is resolved. Answers and citations are stable. We will publish a brief write up and the prevention steps. Thank you for your patience.
```

### Postmortem scheduled

```text
A postmortem is scheduled. We will share the timeline, the root cause, and changes that prevent recurrence. Target publish within 48 hours.
```

---

## In product banner copy

Short. Actionable. Example:

```text
Some AI answers may be slow or incomplete right now. We are restoring normal service. No action needed by you.
```

Add a link to the status page entry.

---

## Internal notification matrix

| Audience      | Channel                           | What to include                               |
| ------------- | --------------------------------- | --------------------------------------------- |
| Exec on call  | paging plus chat room             | sev, scope, owner, ETA for next checkpoint    |
| Support       | help center macro and status link | what users experience, safe workaround if any |
| Sales and CSM | email bulletin or room            | who is affected, what to tell customers       |
| Eng org       | incident room topic               | technical progress and rollback lever status  |

Keep one source of truth. Everything else points to it.

---

## Evidence to log for comms

* Timestamps of each public update.
* Status page state changes and who changed them.
* Link to the exact pins in effect during each window.
* ΔS, coverage, λ snapshots that drove decisions.
* Rollback time, cache namespace, region scope.
* Final resolve time and the postmortem ticket id.

---

## Common pitfalls

* Silence while engineers work. Post small deltas on time.
* Status page says green while the banner says yellow. Keep them aligned.
* Promising exact ETAs. Promise the next checkpoint time instead.
* Over sharing internals. Users need effect and recovery, not raw metrics.
* Forgetting to remove the banner after resolve.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

