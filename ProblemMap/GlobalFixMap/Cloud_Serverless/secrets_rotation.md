# Secrets Rotation and Key Fencing for Zero Downtime

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


A practical runbook to rotate API keys, signing secrets, and JWKS without breaking RAG pipelines or agent flows. Implements dual-accept windows, kid tagging, cache fences, and rollback so rotations are invisible to users and stable under load.

## When to use this page

* Incoming 401/403 spikes during deploys or scale-out.
* Webhook verification fails after a provider rotates its signing secret.
* Mixed keys across regions or functions after a partial rollout.
* Long-lived workers holding stale secrets in memory.
* SOC or policy requires periodic rotation with audit.

## Open these first

* Boot ordering and safe deploy windows: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
* Avoid state loops during changeover: [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)
* First-call crashes after release: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Lock tool schemas and reduce header bloat: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
* Trace and prove what snippet was used: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · Contract payloads: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Live probes and rollback drills: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Acceptance targets

* Zero user-visible errors during the rotation window. No p95 increase.
* 0 auth failures in synthetic probes across all regions and paths.
* Old secret fully revoked within the planned TTL and verified by logs.
* For RAG: no citation loss and ΔS(question, retrieved) ≤ 0.45 on the probe set after rotation.

---

## The two-keys-live pattern

Always rotate with two keys in play: the current key used for signing and a next key accepted for verification. Tag every credential with a key id so validation does not guess.

**Key rules**

1. Always include a stable kid on every token or signature.
2. Verify against `active_kids = {current, next}`. Sign with `current` only.
3. Flip in one step by promoting `next → current` when error rate is flat.
4. Revoke the old key after caches drain and long jobs finish.

**Minimal KV schema**

```json
{
  "secrets_epoch": "2025-08-27T12:00:00Z",
  "active": { "kid": "k_2025_08a", "secret_ref": "sm://wfgyp/prod/k_2025_08a" },
  "next":   { "kid": "k_2025_09a", "secret_ref": "sm://wfgyp/prod/k_2025_09a" },
  "accept_kids": ["k_2025_08a", "k_2025_09a"],
  "revoke_after_s": 259200, 
  "notes": "roll weekly; accept_kids must be length 2 max"
}
```

**HTTP header examples**

```
Authorization: Bearer <access_token_with_kid>
X-Key-Id: k_2025_08a
```

For JOSE tokens, put `kid` in the header. For HMAC signatures, include `X-Key-Id`.

---

## Zero-downtime rotation timeline

**T-24h**

* Create `next` in your secret manager.
* Update `accept_kids = {current, next}`.
* Push config to all regions and functions. Do not sign with next yet.

**T-0**

* Start signing with `current`. Keep accepting both.
* Warm all regions. Run probes for 10 minutes.
* Flip signer to `next` when probes are flat.

**T+1h to T+72h**

* Keep accepting both while streams drain and long jobs finish.
* Watch auth errors by `kid`.
* After TTL, remove `current` from `accept_kids` and revoke it in the secret manager.

**Rollback**

* If errors rise after the flip, restore signer to the previous `current`. Leave accept set unchanged.

---

## Long-lived workers and caches

* Serverless functions may cache secrets in memory. Read secrets on each invocation or attach an `If-Modified-Since` check with a short TTL.
* Edge and CDN caches can pin config. Add `secrets_epoch` to cache keys or use a config version header.
* For JWKS, publish both public keys and set short cache-control. Clients must refresh on `kid` miss.

Open: [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md)

---

## Webhook secret rotation

* Accept two signatures. Verify first with `kid` if provided. If not, attempt both only inside the rotation window.
* Return a 2xx with a deprecation header to prompt senders to upgrade keys.
* Log the `kid` used for every valid request and alert when legacy `kid` drops below a threshold.

---

## Third-party provider keys

* Inject provider API keys from a secret manager at request time. Never bake into build artifacts.
* Keep a per-provider `accept_kids` and test with small traffic shadow before promoting.
* If a provider rotates without `kid`, schedule a short freeze window and fall back to a secondary provider if available.

Related ops: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

## Observability you must add

* Counters of 401/403 by `route`, `region`, and `kid`.
* Ratio of requests verified by current vs next.
* Time to first successful verification with `next` in each region.
* Number of long-lived executions running past the flip time.
* JWKS cache hit and miss per `kid`.

---

## CI policy to prevent unsafe rotations

Fail the build when any of the following is true:

1. `accept_kids` does not contain exactly two values.
2. `next.secret_ref` is missing or unreadable.
3. `revoke_after_s` is not set or exceeds the policy maximum.
4. Routes that verify webhooks are not wired to read `X-Key-Id` or JOSE `kid`.

---

## Copy-paste verifier for serverless functions

```txt
On cold start:
1. Fetch LIMITS.json and SECRETS.json.
2. Pin {accept_kids, active.kid} to memory with TTL = 60s.
3. Expose verify(req):
   - extract kid from header or token header.
   - if kid in accept_kids → choose secret by kid and verify.
   - else refresh secrets and retry once, then fail.

On each request:
- If now - secrets_cache_ts > 60s → refresh in the background.
- Emit metric: {route, region, kid_used, verified=true|false}.
```

---

## Typical failure patterns → exact fix

* **Only one key accepted during rollout**
  Old workers keep signing while new verifiers reject. Add dual-accept and reduce cache TTL.
  Open: [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

* **Webhook fails because sender changed secret before receivers**
  Allow two secrets, prefer `kid` when present. Add retry with jitter and short backoff.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **Large headers during rotation**
  Multiple auth headers overflow 8–16 KB. Collapse to one `X-Key-Id` and one signature.
  Open: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

* **Silent partial revocation**
  Some regions still accept old key due to pinned caches. Force refresh and invalidate edge caches by `secrets_epoch`.
  Open: [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md)

---

## Verification checklist

* Blue-green probe calls succeed with both keys before the flip.
* After flip, 95 percent of traffic verifies with `next` within 10 minutes.
* After revoke, zero successful verifications with old `kid`.
* RAG probe answers remain unchanged and pass ΔS ≤ 0.45.

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


**Next page to write**: `ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md`
