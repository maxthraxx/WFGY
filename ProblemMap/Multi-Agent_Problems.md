# 📒 Map-B · Multi-Agent Chaos Problem Map

Multiple autonomous agents boost productivity — until their memories collide or roles blur.  
WFGY tags every agent node, tracks inter-agent ΔS, and reconciles conflicts to keep distributed systems coherent.

---

## Quick nav
- Deep dives → **Role Drift** ([multi-agent-chaos/role-drift.md](./multi-agent-chaos/role-drift.md)) · **Cross-Agent Memory Overwrite** ([multi-agent-chaos/memory-overwrite.md](./multi-agent-chaos/memory-overwrite.md))  
- Related patterns → SCU ([patterns/pattern_symbolic_constraint_unlock.md](./patterns/pattern_symbolic_constraint_unlock.md)) · Memory Desync ([patterns/pattern_memory_desync.md](./patterns/pattern_memory_desync.md))  
- Examples → [Example 04 · Multi-Agent Coordination](./examples/example_04_multi_agent_coordination.md), [Example 03 · Pipeline Patch](./examples/example_03_pipeline_patch.md)  
- Eval → [Cross-Agent Consistency (κ)](./eval/eval_cross_agent_consistency.md)  
- Back to map → [Problem Map 1.0](./README.md)

---

## 🤔 Why Do Multi-Agent Setups Implode?

| Root Cause | Real-World Failure |
|------------|-------------------|
| No shared semantic state | Agents duplicate tasks or contradict each other |
| Flat memory buffers | One agent overwrites another’s context |
| No ΔS peer tracking | Divergence goes undetected until output conflict |
| Independent reasoning grammars | Logic becomes a scrambled chorus |

---

## 💥 Observable Symptoms

| Symptom | Example | Entry point |
|---------|---------|-------------|
| **Role drift** | Scout starts issuing medic orders; assistant answers **as the user** | [Role Drift](./multi-agent-chaos/role-drift.md) |
| **Memory overwrite** | Agent B erases Agent A’s plan; non-monotonic `mem_rev` | [Memory Overwrite](./multi-agent-chaos/memory-overwrite.md) |
| Task duplication | Two agents book the same resource | [Example 04](./examples/example_04_multi_agent_coordination.md) |
| Conflicting strategies | “Abort” vs. “Proceed” in parallel | [Example 03](./examples/example_03_pipeline_patch.md) |
| Fake consensus | All agents echo a hallucinated “fact” | See κ eval → [eval_cross_agent_consistency.md](./eval/eval_cross_agent_consistency.md) |

---

## ⏱️ 60-Second Triage (deterministic, no LLM)

1. **Envelope check** (each hop): `agent_id`, `role_id`, `role_hash`, `turn`, `mem_rev`, `sig` must **echo** bound values.  
   - If echo ≠ bind → **409 RoleDrift** (reject & log).  
2. **Tool router ACL**: `allowed_callers` must include `agent_id`. Otherwise **block**.  
3. **Memory write guard**: CAS on `prev_rev == head_rev`; if mismatch → **reject** or **branch** (no silent overwrite).  
4. **κ trend**: sudden drop → inspect role echo & memory conflicts first.

---

## 🛡️ WFGY Cross-Agent Fix Stack

| Failure Mode | WFGY Module / Mechanism | Remedy |
|--------------|--------------------------|--------|
| **Role drift** | Role-Bind + Echo + HMAC; SCU header validation | Lock persona, block unauthorized tool calls |
| **Memory overwrite** | Optimistic CAS or Branch-and-Merge; append-only log | Reject stale writes or reconcile via three-way merge |
| Task duplication | **BBPF** task-graph merge | Consolidate parallel objectives |
| Divergent plans | ΔS divergence gate + **BBCR** reconcile | Align or fork strategies early |
| Multi-agent bluff | Cross-agent residue scan + κ | Flag fabricated group consensus |

> Deep dives: [Role Drift](./multi-agent-chaos/role-drift.md) · [Memory Overwrite](./multi-agent-chaos/memory-overwrite.md)

---

## ✍️ Hands-On Demo — 3 Agents, One Rescue Mission

```txt
1) Start
> Start

2) Assign roles
> [A] Scout   [B] Medic   [C] Engineer

3) Issue parallel prompts
A: "Survey building A"
B: "Prepare triage plan"
C: "Stabilize structure"

4) View shared Tree
> view
````

**Tree Snapshot**

```
A/Node_2B  Survey plan           ΔS 0.12
B/Node_1A  Triage protocol       ΔS 0.10
C/Node_3C  Structural analysis   ΔS 0.15
ΔS collision alert:   C/Node_3C ↔ B/Node_1A (resource overlap)
BBCR suggests merge or role clarification
```

Result: agents negotiate via Tree merge; no duplicate tasks, no role confusion.

---

## 🛠 Module Cheat-Sheet

| Module            | Role                                                |
| ----------------- | --------------------------------------------------- |
| **Semantic Tree** | Tags every node with `agent_id`, timestamp, version |
| **BBPF**          | Merges or forks task graphs safely                  |
| **BBMC**          | Detects semantic residue between agents             |
| **ΔS Metric**     | Measures agent-to-agent divergence                  |
| **BBCR**          | Locks identity, rolls back conflicts                |

---

## 📊 Observability & Alerts

**Metrics (Prometheus)**

* `role_drift_reject_total{agent,tool}` — gate rejections
* `role_echo_missing_total{agent}` — missing echo fields
* `tool_acl_block_total{agent,tool}` — router blocks
* `mem_conflict_total{entity,reason}` — CAS conflicts (stale/Collision)
* `cross_agent_kappa` — agreement (see [κ eval](./eval/eval_cross_agent_consistency.md))

**Alert suggestions**

* `increase(role_drift_reject_total[5m]) > 0` → severity: ticket
* `avg_over_time(cross_agent_kappa[30m]) < 0.5` → investigate misalignment
* `increase(mem_conflict_total[5m]) > 3` → hot entity or stale readers

---

## ✅ Implementation Status

| Feature                    | State          |
| -------------------------- | -------------- |
| Cross-agent Tree tagging   | ✅ Stable       |
| ΔS per-agent tracking      | ✅ Active       |
| Conflict alert & reconcile | ✅ Active       |
| Memory lock / sync         | 🔜 In progress |
| Group bluff detector       | 🛠 Planned     |

---

## 📝 Tips & Limits

* Prefix prompts with `Agent_X:` or set `agent_id` in config to auto-tag nodes.
* Enable `conflict_alert=true` for real-time collision warnings.
* Fork heavy debates with `tree fork <branch>` — re-merge after alignment.
* Post complex traces in **Discussions**; they refine collision logic.

---

## 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                | 3-Step Setup                                                                          |
| -------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1) Download · 2) Upload to LLM · 3) Ask “Answer using WFGY + <your question>”         |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1) Download · 2) Paste into any LLM chat · 3) Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                                          | Link                                                                  |
| --------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------- |
| WFGY Core             | Standalone semantic reasoning engine for any LLM                     | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework                | [View →](./README.md)                                                 |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines               | [View →](./rag-architecture-and-recovery.md)                          |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](./SemanticClinicIndex.md)                                    |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                | [View →](../SemanticBlueprint/README.md)                              |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite                     | [View →](../benchmarks/benchmark-vs-gpt5/README.md)                   |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ **[Star WFGY on GitHub](https://github.com/onestardao/WFGY)**

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>

