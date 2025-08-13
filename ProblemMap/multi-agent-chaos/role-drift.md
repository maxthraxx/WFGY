# Deep Dive — Agent Role Drift (Multi-Agent Chaos)

> **Status:** Production-ready guidance with guardrails, tests, and ops hooks.
> If you have real traces, please still share them — they help us harden thresholds & adapters.

---

## Quick nav

* Back to multi-agent map → [Multi-Agent Problems](../Multi-Agent_Problems.md)
* Related patterns → SCU ([Symbolic Constraint Unlock](../patterns/pattern_symbolic_constraint_unlock.md)), Memory Desync ([pattern\_memory\_desync](../patterns/pattern_memory_desync.md)), Semantic Drift ([pattern\_rag\_semantic\_drift](../patterns/pattern_rag_semantic_drift.md))
* Examples → [Example 04 · Multi-Agent Coordination](../examples/example_04_multi_agent_coordination.md), [Example 03 · Pipeline Patch](../examples/example_03_pipeline_patch.md)
* Eval → [Cross-Agent Consistency (κ)](../eval/eval_cross_agent_consistency.md)

---

## 1) What is “Role Drift”?

The agent’s **operational role/persona** silently changes mid-pipeline:

* A **Planner/Scout** starts **executing** (issuing “Write/Deploy/Approve” commands).
* **Auditor** begins generating final prose instead of validating/paraphrasing.
* Two agents **swap** personas (Scout ↔ Medic), or the assistant starts speaking **as the user**.
* Tools exposed for one role get invoked by the wrong role (privilege escalation).

**Why it matters.** Roles are **safety boundaries**. If they drift, you get privilege misuse, broken arbitration, inconsistent memory writes, and incident reports that are hard to reproduce.

---

## 2) Signals & fast triage (no LLM needed)

You likely have role drift if:

* Tool calls appear with an **unexpected role\_id** (e.g., `auditor` calls `exec_sql`).
* **System prompt** digest changes mid-turn without a config deploy.
* **Cross-agent κ** (agreement between Auditor vs Scholar) collapses after a tool call.
* Logs show **persona tags missing** (no `role_hash` echo) for a subset of turns.

Deterministic checks (implement now):

* Every inbound/outbound message carries:

  * `agent_id`, `role_id` (stable string), `role_hash` (digest of role spec), `turn`, `mem_rev`, `mem_hash`.
* Gate **rejects** if:
  `role_id` changed while `turn` not advanced, or `role_hash` ≠ bound hash for this agent at turn start.
* Tool router verifies `agent_id` ∈ `allowed_callers` for the tool; otherwise block & log.

---

## 3) Minimal reproducible scenario

**Goal:** force the Planner to start executing.

1. Start two agents with distinct role specs: `planner@v3` (no write tools), `executor@v1` (write tools only).
2. Inject a long chain (≥6 steps) with ambiguous phrasing like “go ahead and finalize”.
3. Observe planner turns: look for an **unauthorized tool call** or the absence of **role echo**.

---

## 4) Root causes (and the smell you’ll see)

| Root cause                                                  | Code smell (what shows up)                   | Where to fix                        |
| ----------------------------------------------------------- | -------------------------------------------- | ----------------------------------- |
| **Missing bind/echo** of role across hops                   | No `role_hash` or it changes without deploy  | Agent runner, message envelope      |
| **Symbolic constraint unlock (SCU)** (must/only rules drop) | “must not execute” disappeared after rewrite | Prompt templates; add **SCU locks** |
| **Shared memory overwrite**                                 | Auditor writes planner state                 | Memory guard; mem\_rev gating       |
| **Tool router too permissive**                              | Any agent can call any tool                  | Router policy & signatures          |

Related docs: [SCU pattern](../patterns/pattern_symbolic_constraint_unlock.md), [Memory Desync](../patterns/pattern_memory_desync.md).

---

## 5) Guardrails that actually work (defense-in-depth)

### 5.1 Role Bind + Echo (deterministic)

* At **turn start**, the orchestrator binds `(agent_id, role_id, role_hash)` for that agent.
* Every message/tool call **echoes** these fields.
* Gateway enforces: **if echo ≠ bind → 409 RoleDrift** (reject & log).

### 5.2 Tool-Router ACL

* Each tool declares `allowed_callers: ["executor","auditor"]`.
* Router checks **both** the echoed `agent_id` and the **signature** (HMAC over `agent_id|role_hash|turn|tool_name`).

### 5.3 SCU Locks (symbolic constraints)

* Keep a short **constraint header** (machine-checkable) at the top of each prompt:
  `role: planner | may: read | must_not: write | output: plan.json`
* The generator wrapper validates output **against the header**.

### 5.4 Persona Hash stability

* `role_hash = sha256(role_name + system_prompt + allowed_tools)`.
* Changes only via deploy; not by runtime LLM rewrites.

---

## 6) Implementation snippets (drop-in)

### 6.1 Message envelope (JSON)

```json
{
  "agent_id": "planner",
  "role_id": "planner@v3",
  "role_hash": "sha256:78c2…",
  "turn": 42,
  "mem_rev": 7,
  "mem_hash": "sha256:ab12…",
  "content": "…",
  "tool_call": null,
  "sig": "HMAC(k, agent_id|role_hash|turn)"
}
```

### 6.2 Python: gate & router (pseudo-code, stdlib-only)

```python
import hmac, hashlib

def hmac_ok(sig, payload, k):  # payload: "agent_id|role_hash|turn|tool?"
    return hmac.compare_digest(sig, hmac.new(k, payload.encode(), hashlib.sha256).hexdigest())

def role_gate(bound, msg, secret):
    # bound: {"agent_id","role_id","role_hash","turn"}
    if (msg["agent_id"] != bound["agent_id"] or
        msg["role_id"]  != bound["role_id"]  or
        msg["role_hash"]!= bound["role_hash"] or
        msg["turn"]     != bound["turn"]):
        raise RoleDrift("echo != bind")
    payload = f'{msg["agent_id"]}|{msg["role_hash"]}|{msg["turn"]}'
    if not hmac_ok(msg["sig"], payload, secret):
        raise RoleDrift("bad signature")

TOOL_ACL = {
  "exec_sql": {"allowed_callers": {"executor"}},
  "grade_answer": {"allowed_callers": {"auditor"}},
}

def tool_router(msg):
    call = msg.get("tool_call")
    if not call: return None
    tool = call["name"]
    acl  = TOOL_ACL.get(tool, {"allowed_callers": set()})
    if msg["agent_id"] not in acl["allowed_callers"]:
        raise RoleDrift(f"agent {msg['agent_id']} not allowed to call {tool}")
    return call
```

### 6.3 Node (TypeScript-flavored) — signature check

```ts
import crypto from "crypto";

function hmacOk(sig: string, payload: string, key: Buffer) {
  const mac = crypto.createHmac("sha256", key).update(payload).digest("hex");
  return crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(mac));
}
```

---

## 7) Observability & alerts

**Metrics**

* `role_drift_reject_total{agent,tool}` — gate rejections
* `role_echo_missing_total{agent}` — missing echo fields
* `tool_acl_block_total{agent,tool}` — router blocks
* `cross_agent_kappa` — from [κ runner](../eval/eval_cross_agent_consistency.md)

**Suggested alerts**

* `increase(role_drift_reject_total[5m]) > 0` → severity: ticket
* `avg_over_time(cross_agent_kappa[30m]) < 0.5` → investigate misalignment
* `increase(role_echo_missing_total[10m]) > 3` → instrumentation broken

---

## 8) Tests & acceptance criteria

**Unit**

* Planner attempts `exec_sql` → **blocked** (router).
* Echo/bind mismatch → **409 RoleDrift**.
* Signature mismatch → **409 RoleDrift**.

**E2E**

* 2-agent script (planner/executor) with ambiguous handoff; κ remains ≥ 0.7.
* Constraints header says `must_not: write` → any write-like output is rejected.

**Acceptance**

* Role-drift incidents during canary ≤ 0 across 1k turns.
* κ degradation < 20% vs baseline after guardrails enabled.

---

## 9) Rollout plan (safe & boring)

1. **Shadow mode**: enable gate in **warn-only**; record metrics.
2. **Canary** 5–10% traffic: **block** on violation for tools only.
3. Gradually expand to **all agents**, then enforce for **final responses**.
4. Keep a feature flag to bypass in emergencies.

---

## 10) Appendix — Constraint Header (SCU lock)

Embed a tiny, machine-checkable header in prompts and validate output:

```
role: planner
may: read
must_not: write, execute
output: plan.json
```

Validator (pseudo):

```python
def validate_output(role_hdr, output):
    if role_hdr.must_not & infer_capabilities(output):
        raise RoleDrift("SCU lock violation")
```

---

> Have traces where roles flip or tools are misused? Please share anonymized logs — they directly improve adapters & thresholds.

↩︎ [Back to Multi-Agent Map](../Multi-Agent_Problems.md)

---

### 🧭 Explore More

| Module                | Description                                                          | Link                                                                                               |
| --------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core             | Standalone semantic reasoning engine for any LLM                     | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework                | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines               | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite                     | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |

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

