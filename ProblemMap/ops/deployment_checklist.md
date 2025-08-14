# Deployment checklist — RAG pipeline (pre-deploy & post-deploy)

**Purpose:** a short, rigorous checklist to verify your environment and reduce bootstrap/dependency issues during deployment.

---

## Before you deploy (pre-flight)

### 1) Environment & prerequisites
- Kubernetes cluster accessible; `kubectl` points to correct context.  
  ```bash
  kubectl config current-context
  kubectl get nodes


* Ensure cluster resources: CPU / memory / ephemeral storage for vectorstore. Confirm quotas.
* Secrets: API keys (LLM), db credentials, vectorstore creds in k8s Secret or vault.
* Helm chart / manifests: reviewed and values set for production (replicas, resources, liveness/readiness).

### 2) Configuration sanity

* `values.yaml` contains:

  * `resources.requests` and `limits` for retriever/generator.
  * `replicaCount >= 2` for critical services (if expected load > small).
  * `readinessProbe` and `livenessProbe` configured.
* Vector store sizing: `index_shards`, disk IOPS, memory (embedding index memory).
* Network egress rules for model API (if external LLM).

### 3) Observability & alarms

* Prometheus scraping configured for app metrics endpoints (`/metrics`).
* Default dashboards in Grafana (latency, error-rate, retriever QPS, CHR).
* Alerts configured (see `live_monitoring_rag.md` for suggested alerts).

---

## Deploy steps

1. Create namespace & secrets:

   ```bash
   kubectl create ns rag-prod || true
   kubectl -n rag-prod apply -f k8s/secrets.yaml
   ```
2. Install/upgrade Helm chart:

   ```bash
   helm upgrade --install rag . -n rag-prod -f values.prod.yaml
   ```
3. Wait for pods to be ready (watch):

   ```bash
   kubectl -n rag-prod rollout status deploy/rag-api -w
   kubectl -n rag-prod get pods -o wide
   ```
4. Smoke tests (simple requests):

   ```bash
   curl -fsS http://<ingress>/healthz
   curl -fsS -X POST http://<ingress>/api/qa -d '{"qid":"smoke-1","q":"Who is the CEO of WFGY?" }' | jq
   ```

---

## Post-deploy checks (first 15 minutes)

* Confirm retriever returns docs for 10 sample queries:

  * Use your `retrieval` debug endpoint to inspect `retrieved_ids`.
* Confirm p95 E2E latency ≤ target (by env). Collect from Grafana or `kubectl logs`.
* Confirm CHR on 10 smoke items ≥ expected baseline (manually assert correctness).
* Check for error spikes in logs:

  ```bash
  kubectl -n rag-prod logs -l app=rag --since=10m | egrep "ERROR|WARN" | head -n 200
  ```

---

## Common config gotchas (double-check)

* Vectorstore read-only mode accidentally set? (affects writes)
* LLM rate-limiting / auth errors (wrong key or quota).
* Wrong index/namespace names between chunker and retriever (off-by-one).
* Probes misconfigured — containers get restarted continuously.

---

## Rollback criteria

Rollback if any of:

* P95 > target and sustained for 10m.
* Error rate > 3× baseline and not transient.
* Retrieval failures (empty pool) > 1% of requests.

Rollback command example:

```bash
helm rollback rag <previous_revision> -n rag-prod
```

---

### Quick checklist (copy/paste)

* [ ] Namespace created, secrets applied
* [ ] Helm values validated (resources, probes)
* [ ] Prometheus/Grafana dashboards in place
* [ ] Smoke tests passed (health & basic QA)
* [ ] Alerts deployed
* [ ] Canary traffic small → monitor 10–30 min

---

### Links

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



