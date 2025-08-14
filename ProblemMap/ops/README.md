# Ops — Deploy & Runbook (Problem Map)

**Purpose:** this folder contains operational runbooks, checklists and playbooks for deploying, observing, debugging and failing-over RAG pipelines and their surrounding infra.  
Target audience: SREs and engineers responsible for production RAG services. Newbie friendly — each section has a checklist and exact commands.

---

## Quick nav
- **Deployment checklist** → [deployment_checklist.md](./deployment_checklist.md)  
- **Live monitoring & alerts (RAG)** → [live_monitoring_rag.md](./live_monitoring_rag.md)  
- **Debug playbook (step-by-step)** → [debug_playbook.md](./debug_playbook.md)  
- **Failover & recovery** → [failover_and_recovery.md](./failover_and_recovery.md)

---

## Scope & assumptions
- Production topology: API gateway → RAG service (retriever + generator + guard) → Vector DB + Source storage.  
- Infra: Kubernetes (Helm) or docker-compose for small envs. Prometheus + Grafana for metrics; centralized logs (ELK/Fluentd/Vector).  
- Safety-first: ops steps favor **read-only** diagnostic commands until root cause is clear.

---

## How to use these runbooks
1. Read the **deployment checklist** before you deploy.  
2. Use **live monitoring** to ensure SLOs after deploy.  
3. If incident happens, follow **debug_playbook** (triage → isolate → mitigate → fix).  
4. If controller/broker or core services fail, follow **failover_and_recovery**.

---

## Quick operator checks (first 60s)
- Is service responding? `curl -fsS http://$SERVICE/healthz || true`  
- Are pods healthy? `kubectl get pods -n $NS`  
- Any obvious error spikes in logs (last 1 minute): `kubectl logs -n $NS -l app=$APP --since=1m | tail -n 200`  
- Check key metrics in Prometheus (latency/p95, error rate, retriever QPS).

---

## Where patterns & examples map here
- If retrieval bad → see `ProblemMap/retrieval-collapse.md` and [examples for vector-store repair](../examples/example_05_vectorstore_repair.md).  
- If bootstrap ordering failures on start → see `ProblemMap/bootstrap-ordering.md` & [pattern_bootstrap_deadlock.md](../patterns/pattern_bootstrap_deadlock.md).  
- For memory/state issues → `ProblemMap/patterns/pattern_memory_desync.md`.

---

> If you want me to also generate ready-to-apply Kubernetes manifests or Prometheus alerts for your environment (Helm values), I can produce them next — tell me cluster flavor (k8s / k3s / kind / docker-compose) and I’ll adapt.

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



