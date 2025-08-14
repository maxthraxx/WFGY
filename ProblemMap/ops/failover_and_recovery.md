# Failover & recovery — deterministic recovery steps

**Purpose:** deterministic operator steps to failover or recover critical components (vectorstore, retriever, generator, indexer, controller). Aim to reduce data loss and return to safe state quickly.

---

## Basic principles
1. **Fail fast to a safe mode** — prefer read-only answers or cached responses over uncontrolled writes or risky LLM calls.  
2. **Preserve evidence** — do not truncate logs or delete index segments until investigation complete.  
3. **Prefer scoped recovery** — restart single pod/shard before cluster-wide actions.

---

## Scenario A: Vectorstore shard down / index corrupt

**Symptoms**
- Retriever returns empty sets or inconsistent scores for golden queries.  
- Vectorstore pod logs show IO / index errors.

**Steps**
1. Mark the shard unhealthy in the service registry (so retriever avoids it).  
2. If replica exists, route traffic to other replica.  
3. Attempt graceful re-open:
   ```bash
   kubectl -n $NS exec deploy/vectorstore -- /bin/sh -c "ctl index reopen shard-5"


4. If reopen fails, restore from latest snapshot (S3) to a new shard:

   * Create new PV and restore snapshot.
   * Start fresh pod pointed to restored PV.
5. Re-run small validation suite (10–50 golden qids) before reintroducing shard.

**Post recovery**

* Re-index missing docs if necessary; track reindex job progress.
* Add a postmortem entry and schedule a permanent fix.

---

## Scenario B: Generator (LLM) provider outage

**Symptoms**

* LLM errors (5xx), rate-limit responses, or auth failures.

**Steps**

1. Switch to backup LLM provider (if configured) via config flag:

   ```bash
   # toggle provider in config map or feature flag
   kubectl -n $NS set env deploy/rag-api PROVIDER=backup-provider
   ```
2. If no backup, enable local fallback:

   * Return cached answers for known qids.
   * Return safe refusal for unknown qids.
3. Throttle traffic and backlog long-running requests to a worker queue.
4. Once provider restored, slowly ramp traffic and compare CHR/precision to baseline.

---

## Scenario C: Bootstrap deadlock at startup

**Symptoms**

* Pods stuck in CrashLoopBackOff or `Ready` never true; logs show circular dependency or missing migration.

**Steps**

1. Inspect init containers & migration jobs:

   ```bash
   kubectl -n $NS get jobs
   kubectl -n $NS logs job/migrations
   ```
2. Run migrations manually in controlled pod:

   ```bash
   kubectl -n $NS run --rm -it migration-runner --image=myimage -- bash -c "python migrate.py"
   ```
3. Ensure controller component (if any) is up before starting retriever/generator. Use Helm hooks or manual `kubectl apply` ordering.
4. If necessary, scale down and start components one-by-one.

---

## Safety nets & best practices

* Keep automated snapshots of vectorstore daily; keep 7–14 days retention.
* Maintain a tested restore playbook and a “mini-cluster” restore test monthly.
* Automate warm-failover for LLMs: pre-warm API tokens for backup providers.

---

## Post-incident

* Triage root cause, assign fixes.
* Add automated test that would have caught this.
* Update runbooks and notify stakeholders.

---

### Links

* Deployment checklist → [deployment\_checklist.md](./deployment_checklist.md)
* Debug playbook → [debug\_playbook.md](./debug_playbook.md)
* Live monitoring → [live\_monitoring\_rag.md](./live_monitoring_rag.md)

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

