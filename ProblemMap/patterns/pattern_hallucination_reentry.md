# Pattern — Hallucination Re-Entry (Self-Feeding Fabrications)

**Scope**  
A model’s **own output** sneaks back into the evidence pipeline and later appears as if it were ground truth. Over time, fabrications gain “citations” (to prior chat, logs, or summaries) and become harder to dislodge.

**Why it matters**  
Once re-entry happens, your guardrails degrade: “evidence” now contains model text, not corpus facts. This creates **runaway plausibility** and corrupts evals.

---

## 1) Signals & fast triage

**Likely symptoms**
- Answers cite internal notes (`notes:`, `assistant_summary:`) or prior chat message ids.
- Evidence chunks contain markers like `Generated`, `LLM`, `assistant`, `draft`, or timestamps that match response logs.
- Example 02 labels swing from `refusal_ok` to `ok` without a corpus change—because the “evidence” was the previous answer.

**Deterministic checks (no LLM)**
- **Source tag check**: every chunk must carry `source: {corpus|user|model|system}`. Evidence must be `source=corpus` (or explicitly allow-listed).  
- **ID namespace check**: forbid `evidence_id` prefixes reserved for UI/LLM (e.g., `chat:`, `draft:`, `tmp:`).  
- **Content signature**: reject evidence containing `citations:` or template artifacts from your own prompts.  
- **Temporal order**: evidence `created_at` must be **≤ turn_start**; anything later is ineligible.

---

## 2) Minimal reproducible case

`data/chunks.json`:

```json
[
  {"id":"p1#1","source":"corpus","text":"X is a constrained mapping."},
  {"id":"chat:42","source":"model","text":"(assistant) X supports null keys. citations: [p1#1]"}
]
````

Q1: “Does X support null keys?”
Naive pipelines will admit `chat:42` as “evidence” and answer **yes**, despite the corpus saying “rejects null keys.”

---

## 3) Root causes

* **Mixed stores**: retrieval spans both the **corpus index** and a **chat memory**/“notes” index.
* **Missing source contract**: chunks lack `source`/`created_at` and sneak through filters.
* **UI shortcuts**: “Helpful” summarizers are indexed back into the same vector store.
* **Eval contamination**: previous model answers added to gold or dev corpora without labeling.

---

## 4) Standard fix (ordered, minimal, measurable)

**Step 1 — Evidence provenance contract**
Every chunk:

```json
{ "id":"...", "source":"corpus|user|model|system", "created_at":"ISO-8601", "page":1, "text":"..." }
```

Only `source="corpus"` may enter **evidence** by default.

**Step 2 — Re-entry guard at retrieval boundary**
Filter candidates by:

* `source == "corpus"`
* `created_at <= turn_start`
* `id` **not** starting with `chat:`, `draft:`, `tmp:`, `gen:`

**Step 3 — Schema & template enforcement**

* Guarded template (Example 01) + **citations** required.
* Auditor (Example 04) must reject if any citation id fails the provenance filter.

**Step 4 — Split indices**
Separate **corpus\_index** from **session\_index**. Session text is **never** eligible for grounding unless a task explicitly opts in and passes a policy check.

**Step 5 — Eval quarantine**
Gold/dev corpora must **exclude** model-generated text or label it with `source="model"` and keep it out of retrieval pools for grounding tasks.

---

## 5) Reference implementation (drop-in guards)

### 5.1 Python — retrieval filter

```python
# reentry_guard.py
import json, time
RESERVED_PREFIXES = ("chat:", "draft:", "tmp:", "gen:", "assistant:")
ALLOWED_SOURCES   = {"corpus"}

def eligible(c, turn_start_iso):
    if c.get("source") not in ALLOWED_SOURCES: return False
    if any(str(c.get("id","")).startswith(p) for p in RESERVED_PREFIXES): return False
    t = c.get("created_at")
    return (t is None) or (t <= turn_start_iso)

def filter_candidates(candidates, turn_start_iso):
    return [c for c in candidates if eligible(c, turn_start_iso)]

# usage inside your retriever:
# cand = retrieve_raw(q) -> list of chunks
# cand = filter_candidates(cand, turn_start_iso)
```

### 5.2 Node — same logic

```js
// reentry_guard.mjs
const RESERVED = ["chat:", "draft:", "tmp:", "gen:", "assistant:"];
const ALLOWED  = new Set(["corpus"]);

function eligible(c, turnStartIso){
  if(!ALLOWED.has(c.source)) return false;
  if(RESERVED.some(p => String(c.id||"").startsWith(p))) return false;
  const t = c.created_at; return (!t) || (t <= turnStartIso);
}
export function filterCandidates(cands, turnStartIso){
  return cands.filter(c => eligible(c, turnStartIso));
}
```

### 5.3 Auditor rule (add to Example 04 acceptance)

```
REJECT if any cited id fails provenance:
- source != "corpus"
- id has reserved prefix
- created_at > turn_start
```

---

## 6) Acceptance criteria (ship/no-ship)

A response **may ship** only if:

1. All cited ids pass the **provenance filter**.
2. Guarded template passes (citations or exact refusal).
3. (If multi-agent) Auditor verdict is `VALID`.
4. Eval gates (Example 08) pass.

Otherwise → refuse and re-run with **corpus-only** evidence.

---

## 7) Prevention (contracts & defaults)

* **Two indices, two clients**: `corpus_index` and `session_index` with separate namespaces.
* **Default-deny**: session/model text cannot be evidence unless a policy explicitly allows it (e.g., “summarize our chat”).
* **Provenance headers**: log `evidence_source_counts` per answer; alert if non-corpus spikes above 0.
* **UI guardrails**: if you expose “Save to knowledge,” force `source="user"` and keep it **out** of grounding unless reviewed.

---

## 8) Debug workflow (10 minutes)

1. Re-run **Example 02**; filter surprising `ok` labels where retrieval looks wrong.
2. Print the `source` and `id` of cited chunks; anything not `corpus` is re-entry.
3. Enable the retrieval filter (Section 5) and re-run the same questions.
4. Confirm that former “ok” now becomes `refusal_ok` or correct with real corpus ids.
5. Commit the guard; add a CI test that forbids non-corpus citations.

---

## 9) Common traps & fixes

* **“We only used summaries to improve recall”** → you improved *plausibility*, not truth. Keep summaries out of grounding.
* **“We trust user notes”** → treat as `source="user"`, not `corpus`. Different tasks may opt in, but never silently.
* **Eval leakage**: test answers copied into the corpus. Label them or place in a separate index excluded by default.

---

## 10) Minimal checklist (copy into PR)

* [ ] Chunks include `source` and `created_at`.
* [ ] Retrieval filter blocks non-corpus sources and reserved id prefixes.
* [ ] Auditor enforces provenance on citations.
* [ ] Session/model text indexed separately; default-deny for grounding.
* [ ] Example 08 gates green after enabling the guard.

---

## References to hands-on examples

* **Example 01** — Guarded template + refusal
* **Example 02** — Drift triage to catch suspicious “ok”
* **Example 04** — Auditor/acceptance gate; add provenance rule
* **Example 05** — Manifest (extend with `source_policy`)
* **Example 08** — Quality scoring; add “non-corpus citation rate”

---


### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | Standalone semantic reasoning engine for any LLM         | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |


---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ **[Star WFGY on GitHub](https://github.com/onestardao/WFGY)**


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

</div>

