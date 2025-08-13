# Pattern — Memory Desync (Context/State Mismatch)

**Scope**  
Conversation “memory” (user profile, preferences, prior facts) used by retrieval/generation **doesn’t match** the memory that should apply at this turn. Symptoms: references to **old names/IDs**, ignoring recent corrections, or oscillating answers between turns.

**Why it matters**  
When state diverges, your pipeline optimizes for the wrong goal. Models appear “random” or “stubborn,” but the real issue is **who read which memory, when**.

> Quick nav: [Patterns Index](./README.md) · Examples: 
> [Example 01](../examples/example_01_basic_fix.md) · 
> [Example 03](../examples/example_03_pipeline_patch.md) · 
> [Eval: Precision & CHR](../eval/eval_rag_precision_recall.md)


---

## 1) Signals & fast triage

**You likely have this if:**
- The answer cites profile details that were **updated moments ago** (and confirmed in UI) but still uses the **old value**.
- Logs show **different memory snapshots** between retrieval and generation for the **same turn**.
- Re-running the **same question** right after a correction flips results back and forth (oscillation).
- Agents disagree: Scholar uses memory rev=7; Auditor validates against rev=8 (Example 04), producing brittle verdicts.

**Deterministic checks (no LLM needed):**
- Every request includes **`mem_rev`** (monotonic integer) and **`mem_hash`** (stable digest).  
- Gate rejects the turn if any stage observes **different** `mem_rev/hash` than the one bound at turn start.

---

## 2) Minimal reproducible case

**Memory file** `data/memory.json`:

```json
{ "rev": 7, "user_name": "Alex", "timezone": "UTC", "preferences": { "style": "concise" } }
````

**Turn T:** User says “Call me **Alyx** now.” UI writes `{ "rev": 8, "user_name": "Alyx", ... }`.

**Bug to reproduce:** Retrieval reads memory at **rev=7** while generation already reads **rev=8** ⇒ the answer mixes “Alex” and “Alyx”.

---

## 3) Root causes

* **Race conditions**: write-after-read (memory updated while the turn is executing).
* **Inconsistent caching**: different components cache memory independently with different TTLs.
* **Side-channel updates**: an agent writes memory mid-turn; another agent doesn’t see it.
* **Implicit memory**: prompt injects “what the model thinks it remembers” with no authoritative store.

---

## 4) Standard fix (ordered, minimal, measurable)

**Step 1 — Snapshot at ingress**

* At the **very start** of the turn, read memory **once** and freeze it: `mem_rev`, `mem_hash`, `mem_obj`.
* Propagate these into **every** stage (retrieval, ranking, generation, auditor).

**Step 2 — Bind & echo**

* Include `mem_rev` and `mem_hash` in prompts and require the model to **echo** them in JSON output (`context_id`).
* If echoed values mismatch the snapshot → **reject**.

**Step 3 — Single-writer rule**

* Disallow memory **writes** during a turn. Queue writes for **post-turn commit** with `rev+1`.

**Step 4 — Cache discipline**

* One cache only. All components read through a **shared memory proxy** keyed by `rev`. Cache invalidation uses `rev` equality, not time.

**Step 5 — Gate on consistency**

* Acceptance gate (Example 04) verifies `context_id.mem_rev/hash` before shipping the text.

---

## 5) Reference implementation (Python / Node)

### 5.1 Python — snapshot + echo contract

```python
# mem_guard.py
import json, hashlib, urllib.request, os

def load_mem(path="data/memory.json"):
    m = json.load(open(path, encoding="utf8"))
    h = hashlib.sha256(json.dumps(m, sort_keys=True).encode()).hexdigest()[:16]
    return m, m["rev"], h

def prompt(question, evidence, mem_rev, mem_hash):
    ctx = "\n\n".join(f"[{c['id']}] {c['text']}" for c in evidence)
    return (
        "Use only the evidence. If not provable, reply exactly: not in context.\n"
        "Output JSON with fields: claim, citations:[id,...], context_id:{mem_rev:int, mem_hash:str}.\n\n"
        f"Question: {question}\n"
        f"Context-ID: {{\"mem_rev\": {mem_rev}, \"mem_hash\": \"{mem_hash}\"}}\n\n"
        f"Evidence:\n{ctx}\n"
    )

def call_openai(prompt_text, model=os.getenv("OPENAI_MODEL","gpt-4o-mini")):
    api_key = os.getenv("OPENAI_API_KEY"); assert api_key, "OPENAI_API_KEY"
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps({"model":model,"messages":[{"role":"user","content":prompt_text}],"temperature":0}).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {api_key}"}
    )
    with urllib.request.urlopen(req) as r:
        j = json.loads(r.read().decode())
        return j["choices"][0]["message"]["content"]

def parse_json_block(txt):
    s,e = txt.find("{"), txt.rfind("}")
    return json.loads(txt[s:e+1]) if s>=0 and e>s else None

def check_context(out, mem_rev, mem_hash):
    cid = (out or {}).get("context_id") or {}
    return cid.get("mem_rev")==mem_rev and cid.get("mem_hash")==mem_hash

# usage
mem, rev, h = load_mem()
ev = [{"id":"p1#1","text":"X is a constrained mapping."}]
ans = call_openai(prompt("What is X?", ev, rev, h))
out = parse_json_block(ans)
assert check_context(out, rev, h), "MEM_DESYNC"
```

### 5.2 Node — same contract

```js
// mem_guard.mjs
import fs from "node:fs"; import https from "node:https"; import crypto from "node:crypto";

function loadMem(path="data/memory.json"){
  const m = JSON.parse(fs.readFileSync(path,"utf8"));
  const h = crypto.createHash("sha256").update(JSON.stringify(m)).digest("hex").slice(0,16);
  return { m, rev: m.rev, hash: h };
}

function buildPrompt(q, chunks, rev, hash){
  const ctx = chunks.map(c=>`[${c.id}] ${c.text}`).join("\n\n");
  return `Use only the evidence. If not provable, reply exactly: not in context.
Output JSON with fields: claim, citations:[id,...], context_id:{mem_rev:int, mem_hash:str}.

Question: ${q}
Context-ID: {"mem_rev": ${rev}, "mem_hash": "${hash}"}

Evidence:
${ctx}
`;
}

async function callOpenAI(p, model=process.env.OPENAI_MODEL || "gpt-4o-mini"){
  const key = process.env.OPENAI_API_KEY; if(!key) throw new Error("OPENAI_API_KEY");
  const body = JSON.stringify({ model, messages:[{role:"user",content:p}], temperature:0 });
  return await new Promise((resolve,reject)=>{
    const req = https.request("https://api.openai.com/v1/chat/completions",{
      method:"POST", headers:{ "Content-Type":"application/json","Authorization":`Bearer ${key}` }
    }, r=>{ let d=""; r.on("data",x=>d+=x); r.on("end",()=>resolve(JSON.parse(d).choices[0].message.content)); });
    req.on("error",reject); req.write(body); req.end();
  });
}

function parseJson(txt){ const s=txt.indexOf("{"), e=txt.lastIndexOf("}"); if(s<0||e<=s) return null; try{return JSON.parse(txt.slice(s,e+1))}catch{return null} }
function checkContext(out, rev, hash){ return out?.context_id?.mem_rev===rev && out?.context_id?.mem_hash===hash; }

// usage
const { m, rev, hash } = loadMem();
const ev = [{id:"p1#1", text:"X is a constrained mapping."}];
const out = parseJson(await callOpenAI(buildPrompt("What is X?", ev, rev, hash)));
if(!checkContext(out, rev, hash)) throw new Error("MEM_DESYNC");
```

---

## 6) Acceptance criteria (ship/no-ship)

A response **may ship** only if **all** hold:

1. `context_id.mem_rev/hash` **match** the turn snapshot.
2. Guarded template passes (citations or exact refusal).
3. If multi-agent is used, **both** Scholar and Auditor echo the **same** `context_id`.
4. Eval gates (Example 08) meet thresholds.

Otherwise → refuse and **re-run** the turn **after** memory is stable.

---

## 7) Prevention (contracts & defaults)

* **Turn snapshot**: `(mem_rev, mem_hash, mem_obj)` captured once at ingress; immutable for the turn.
* **Post-turn commit**: queued writes apply as `rev+1` only after acceptance.
* **One cache policy**: read-through cache by `rev`; disable in-component caches.
* **Handoff schema**: include `context_id` in all agent handoffs (Example 04).
* **UI truth**: only the memory store is authoritative; the model never “remembers” outside it.

---

## 8) Debug workflow (10 minutes)

1. Add `context_id` echo to your prompt and output schema.
2. Reproduce a correction (Alex→Alyx) mid-session.
3. Inspect traces: any stage with mismatched `mem_rev/hash` is the culprit.
4. Enforce single-writer; move writes to post-turn queue.
5. Re-run and confirm **no** `MEM_DESYNC` events in logs.

---

## 9) Common traps & fixes

* **Background “auto-learning”**: LLM writes to memory during the same turn. **Disable**; queue it.
* **In-flight UI changes**: user edits profile while answering → snapshot at ingress; if `rev` changes before ship, **abort** and restart with new snapshot.
* **Multiple memory sources**: product DB vs vector memory vs session vars → consolidate behind a **single proxy** keyed by `rev`.

---

## 10) Minimal checklist (copy into PR)

* [ ] Prompts and outputs carry `context_id` with `mem_rev/hash`.
* [ ] Single memory read at ingress; no mid-turn writes.
* [ ] Cache keyed by `rev`; no stale per-component caches.
* [ ] Acceptance gate verifies `context_id` across all agents.
* [ ] Example 08 gates pass before rollout.

---

## References to hands-on examples

* **Example 01** — Guarded template
* **Example 02** — Drift triage (labels help spot desync side-effects)
* **Example 04** — Multi-agent handoff; add `context_id` to schema
* **Example 07** — Readiness; include memory probe in sentinel
* **Example 08** — Quality gates catch oscillations post-fix

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
