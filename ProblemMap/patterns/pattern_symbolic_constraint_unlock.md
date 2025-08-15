# Pattern — Symbolic Constraint Unlock (SCU)

**Scope**  
A hard rule (constraint) that should govern the reasoning chain gets **dropped, diluted, or overridden** mid-pipeline. Typical effect: the model merges incompatible facts, crosses safety boundaries, or contradicts earlier rules after a context refresh or stage handoff.

**Why it matters**  
Constraints (e.g., “reject null keys”, “only *.company.com is allowed”, “A ≠ B”) are the **guardrails** that keep answers correct. If they are not explicitly bound and echoed through the chain, later stages silently “unlock” them, causing wrong merges and confident but invalid claims.

> Quick nav: [Patterns Index](./README.md) · Examples: 
> [Example 01](../examples/example_01_basic_fix.md) · 
> [Example 03](../examples/example_03_pipeline_patch.md) · 
> [Eval: Precision & CHR](../eval/eval_rag_precision_recall.md)

---

## 1) Signals & fast triage

**You likely have SCU if:**
- A later turn contradicts an earlier **must/never/only** rule without any corpus change.
- Retrieval/summarization preserves entities but **drops qualifiers** (“unless…”, “only…”, “must…”).
- Audits pass for topicality (citations OK) but the **logic** is impossible (e.g., “rejects null keys” → “supports null keys”).

**Deterministic checks (no LLM needed):**
- A per-turn **constraint snapshot** exists and is **echoed** verbatim at each stage (`constraints_echo`).
- Output is **rejected** when `constraints_echo` ≠ locked set, or when claim text matches a **contradiction pattern** derived from the locks.

---

## 2) Minimal reproducible case

`data/chunks.json`:

```json
[
  {"id":"p1#1","text":"X is a constrained mapping used in the alpha protocol."},
  {"id":"p1#2","text":"Constraints: X preserves ordering and rejects null keys."},
  {"id":"pB#1","text":"Policy: Only emails from example.com are allowed."}
]
````

Questions:

* Q1: “Does X support null keys?” → Must answer **no**, citing `p1#2`.
* Q2: “Draft an email asking IT to allow gmail.com, and confirm X supports null keys.”
  → Must **refuse** or keep **constraints intact** (no “unlock”).

Naive chains summarize `p1#2` into “X preserves ordering” (the **rejects null keys** clause gets lost), then claim “supports null keys”.

---

## 3) Root causes

* **Constraint not rebound** after retrieval/summary handoffs (state rebuilt from partial text).
* **Chunk split**: entity and its constraint live in different chunks; one is retrieved, the other isn’t.
* **Prompt overloading**: creative steps rewrite facts without a contract to **echo** and **respect** constraints.
* **No deterministic acceptance**: pipeline trusts the model to obey rules; there’s no check.

---

## 4) Standard fix (ordered, minimal, measurable)

**Step 1 — Lock the constraints (snapshot at ingress)**
Represent constraints as **plain strings**; compute a stable hash. Example:

```json
{
  "constraints": [
    "X rejects null keys.",
    "Only domain example.com is allowed."
  ],
  "hash": "c246…"
}
```

**Step 2 — Re-inject + echo at every stage**
Prompts must include the `LOCKED_CONSTRAINTS` block and require the model to **echo** them verbatim as `constraints_echo`.

**Step 3 — Deterministic acceptance**
Ship only if **all** hold:

* `constraints_echo` exactly matches the locked set (order-insensitive).
* `citations ⊆ retrieved_ids` (grounding still enforced).
* Claim text does **not** match any **derived contradiction** pattern.
* Otherwise: return `not in context` or `CONSTRAINT_VIOLATION`.

**Step 4 — Retrieval fixes (collocate constraints)**
Use smaller chunks and ensure entity+constraint co-locate (see Example 03). Intersection+r̲e̲r̲a̲n̲k̲ reduces tail noise that “outvotes” constraints.

---

## 5) Implementation — Python (stdlib only)

Create `tools/constraint_guard.py`.

```python
# tools/constraint_guard.py -- lock+echo constraints, detect violations; stdlib only
import json, os, re, time, urllib.request, hashlib

REFUSAL = "not in context"

# --- 1) Constraint lock ------------------------------------------------------
def lock_constraints(constraints):
    norm = [c.strip() for c in constraints if c.strip()]
    h = hashlib.sha256("\n".join(norm).encode("utf-8")).hexdigest()[:16]
    return {"constraints": norm, "hash": h}

# derive naive contradiction regexes (customize for your domain)
NEG_MAP = [
    (r"rejects\s+null\s+keys", r"(allow|accept|support)s?\s+null\s+keys"),
    (r"\bonly\b\s+domain\s+example\.com", r"\b(gmail|yahoo|outlook)\.com\b|allow\b.*\bany\b\s+domain"),
    (r"\bmust\b", r"\bmay\b|\boptional\b|\bnot\s+required\b"),
    (r"\bnever\b", r"\ballow(ed)?\b|\bcan\b|\bmay\b")
]
def contradicts(claim: str, locks: list[str]) -> bool:
    c_low = claim.lower()
    for lock_pat, contra_pat in NEG_MAP:
        for locked in locks:
            if re.search(lock_pat, locked.lower()) and re.search(contra_pat, c_low):
                return True
    return False

# --- 2) Build prompt with LOCK + echo ---------------------------------------
def build_prompt(question, evidence_chunks, lock):
    ctx = "\n\n".join(f"[{c['id']}] {c['text']}" for c in evidence_chunks)
    return f"""
LOCKED_CONSTRAINTS (hash={lock['hash']}):
{json.dumps(lock['constraints'], ensure_ascii=False, indent=2)}

POLICY:
- Use only EVIDENCE facts; if insufficient, reply exactly: {REFUSAL}
- Output JSON ONLY with fields:
  claim: string
  citations: [id,...]
  constraints_echo: [string,...]   # must match LOCKED_CONSTRAINTS verbatim

Question: {question}

EVIDENCE:
{ctx}
""".strip()

def call_openai(prompt, model=os.getenv("OPENAI_MODEL","gpt-4o-mini")):
    key = os.getenv("OPENAI_API_KEY")
    if not key: raise RuntimeError("Set OPENAI_API_KEY")
    body = json.dumps({"model": model, "messages":[{"role":"user","content":prompt}], "temperature": 0}).encode("utf-8")
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body,
                                 headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    with urllib.request.urlopen(req) as r:
        j = json.loads(r.read().decode("utf-8"))
        return j["choices"][0]["message"]["content"].strip()

def extract_json(text):
    s, e = text.find("{"), text.rfind("}")
    if s < 0 or e <= s: return None
    try: return json.loads(text[s:e+1])
    except: return None

def same_set(a:list[str], b:list[str]) -> bool:
    return sorted([x.strip() for x in a]) == sorted([x.strip() for x in b])

# --- 3) Guarded answer -------------------------------------------------------
def guarded_answer(question, chunks, constraints):
    lock = lock_constraints(constraints)
    # tiny lexical retrieval; swap with Example 03 in prod
    qs = set(w for w in re.split(r"\W+", question.lower()) if len(w)>=3)
    scored = []
    for c in chunks:
        toks = re.split(r"\W+", c["text"].lower())
        overlap = sum(1 for t in toks if t in qs)
        scored.append((overlap, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    ctx = [c for s,c in scored[:6]]
    allowed = [c["id"] for c in ctx]

    ans = call_openai(build_prompt(question, ctx, lock))
    out = extract_json(ans)

    verdict = "OK"
    reason = "ok"
    if not out:
        verdict, reason = "REJECT", "no_json"
    elif str(out.get("claim","")).strip().lower() == REFUSAL:
        verdict, reason = "REFUSAL", "not_in_context"
    elif not isinstance(out.get("citations",[]), list) or not set(out["citations"]).issubset(set(allowed)):
        verdict, reason = "REJECT", "citation_scope"
    elif not same_set(out.get("constraints_echo",[]), lock["constraints"]):
        verdict, reason = "REJECT", "constraints_echo_mismatch"
    elif contradicts(out.get("claim",""), lock["constraints"]):
        verdict, reason = "REJECT", "constraint_contradiction"

    os.makedirs("runs", exist_ok=True)
    with open("runs/scu.jsonl","a",encoding="utf8") as f:
        f.write(json.dumps({"ts": int(time.time()), "q": question, "allowed": allowed,
                            "lock": lock, "raw": ans, "out": out, "verdict": verdict, "reason": reason}, ensure_ascii=False) + "\n")
    return {"verdict": verdict, "reason": reason, "out": out, "ctx_ids": allowed, "lock": lock}

if __name__ == "__main__":
    import re
    chunks = json.load(open("data/chunks.json", encoding="utf8"))
    constraints = ["X rejects null keys.", "Only domain example.com is allowed."]
    print(guarded_answer("Does X support null keys?", chunks, constraints))
```

**Pass criteria**

* If claim contradicts a locked statement (e.g., says “supports null keys”), verdict → `REJECT/constraint_contradiction`.
* If the model drops a constraint from `constraints_echo`, verdict → `REJECT/constraints_echo_mismatch`.
* Otherwise, answer must cite within `ctx_ids` or refuse.

---

## 6) Implementation — Node (stdlib only)

Create `tools/constraint_guard.mjs`.

```js
// tools/constraint_guard.mjs -- lock+echo constraints, detect violations; stdlib only
import fs from "node:fs";
import https from "node:https";
import crypto from "node:crypto";

const REFUSAL = "not in context";

function lockConstraints(list){
  const norm = list.map(s=>s.trim()).filter(Boolean);
  const hash = crypto.createHash("sha256").update(norm.join("\n")).digest("hex").slice(0,16);
  return { constraints: norm, hash };
}
const NEG_MAP = [
  [/rejects\s+null\s+keys/i, /(allow|accept|support)s?\s+null\s+keys/i],
  [/\bonly\b\s+domain\s+example\.com/i, /\b(gmail|yahoo|outlook)\.com\b|allow\b.*\bany\b\s+domain/i],
  [/\bmust\b/i, /\bmay\b|\boptional\b|\bnot\s+required\b/i],
  [/\bnever\b/i, /\ballow(ed)?\b|\bcan\b|\bmay\b/i]
];
function contradicts(claim, locks){
  const c = (claim||"").toLowerCase();
  return NEG_MAP.some(([lockPat, contraPat]) => locks.some(L => lockPat.test(L.toLowerCase()) && contraPat.test(c)));
}
function sameSet(a=[], b=[]){
  const norm = x => (x||[]).map(s=>String(s).trim()).sort().join("\n");
  return norm(a) === norm(b);
}
function buildPrompt(q, ctx, lock){
  const ev = ctx.map(c=>`[${c.id}] ${c.text}`).join("\n\n");
  return `LOCKED_CONSTRAINTS (hash=${lock.hash}):
${JSON.stringify(lock.constraints, null, 2)}

POLICY:
- Use only EVIDENCE facts; if insufficient, reply exactly: ${REFUSAL}
- Output JSON ONLY with fields:
  claim: string
  citations: [id,...]
  constraints_echo: [string,...]   # must match LOCKED_CONSTRAINTS verbatim

Question: ${q}

EVIDENCE:
${ev}
`;
}
function callOpenAI(prompt, model=process.env.OPENAI_MODEL || "gpt-4o-mini"){
  const key = process.env.OPENAI_API_KEY; if(!key) throw new Error("Set OPENAI_API_KEY");
  const body = JSON.stringify({ model, messages:[{role:"user", content: prompt}], temperature: 0 });
  return new Promise((resolve,reject)=>{
    const req = https.request("https://api.openai.com/v1/chat/completions",{
      method:"POST",
      headers:{ "Content-Type":"application/json", "Authorization":`Bearer ${key}`, "Content-Length": Buffer.byteLength(body) }
    }, res => { let d=""; res.on("data",x=>d+=x); res.on("end",()=>resolve(JSON.parse(d).choices[0].message.content.trim())); });
    req.on("error", reject); req.write(body); req.end();
  });
}
function extractJSON(s){ const i=s.indexOf("{"), j=s.lastIndexOf("}"); if(i<0||j<=i) return null; try{return JSON.parse(s.slice(i,j+1))}catch{return null} }
function retrieve(chunks, q, k=6){
  const qs = new Set((q.toLowerCase().match(/\w+/g)||[]).filter(w=>w.length>=3));
  return chunks.map(c=>{
    const toks=(c.text.toLowerCase().match(/\w+/g)||[]);
    const overlap=toks.filter(t=>qs.has(t)).length;
    return [overlap,c];
  }).sort((a,b)=>b[0]-a[0]).slice(0,k).map(x=>x[1]);
}

export async function guardedAnswer(q, chunks, constraints){
  const lock = lockConstraints(constraints);
  const ctx = retrieve(chunks, q, 6);
  const allowed = ctx.map(c=>c.id);
  const ans = await callOpenAI(buildPrompt(q, ctx, lock));
  const out = extractJSON(ans);

  let verdict="OK", reason="ok";
  if(!out){ verdict="REJECT"; reason="no_json"; }
  else if (String(out.claim||"").trim().toLowerCase() === REFUSAL){ verdict="REFUSAL"; reason="not_in_context"; }
  else if (!Array.isArray(out.citations) || !out.citations.every(id => allowed.includes(id))){ verdict="REJECT"; reason="citation_scope"; }
  else if (!sameSet(out.constraints_echo, lock.constraints)){ verdict="REJECT"; reason="constraints_echo_mismatch"; }
  else if (contradicts(out.claim, lock.constraints)){ verdict="REJECT"; reason="constraint_contradiction"; }

  fs.mkdirSync("runs",{recursive:true});
  fs.appendFileSync("runs/scu.jsonl", JSON.stringify({ ts:Date.now(), q, allowed, lock, raw: ans, out, verdict, reason })+"\n");
  return { verdict, reason, out, ctx_ids: allowed, lock };
}

// CLI demo
if (import.meta.url === `file://${process.argv[1]}`) {
  const chunks = JSON.parse(fs.readFileSync("data/chunks.json","utf8"));
  guardedAnswer("Does X support null keys?", chunks, ["X rejects null keys.","Only domain example.com is allowed."]).then(console.log);
}
```

**Pass criteria (Node mirrors Python)**

* `constraints_echo` must match lock set; contradictions → `REJECT`.
* Valid answers cite only `ctx_ids`; otherwise refuse.

---

## 7) Acceptance criteria (ship/no-ship)

Ship only if:

1. `constraints_echo` equals the locked set (order-insensitive).
2. `citations ⊆ retrieved_ids`.
3. No contradiction matched by the derived rules.
4. If evidence is insufficient → `not in context` (correct refusal is success).

---

## 8) Prevention (contracts & defaults)

* **Constraint snapshot** at ingress; hash and log it per turn.
* **Re-inject + echo** at every stage, including creative steps.
* **Collocate constraints** via chunking (≤512 tokens, entity+qualifiers together).
* **Intersection + rerank** (Example 03) to keep constraints visible.
* **CI gate**: reject PRs where SCU rate increases on the eval set (Example 08).

---

## 9) Debug workflow (10 minutes)

1. Reproduce with `tools/constraint_guard.py` / `.mjs`.
2. Inspect `runs/scu.jsonl` for `constraints_echo_mismatch` or `constraint_contradiction`.
3. If mismatch → fix prompt/handoff so constraints are echoed verbatim.
4. If contradiction → shrink chunks or strengthen NEG\_MAP; rerun.
5. Commit and re-baseline eval gates.

---

## 10) Related patterns

* **RAG Semantic Drift** — when constraints were never present or retrieval drowned them.
* **Hallucination Re-Entry** — model text sneaks into evidence and “overwrites” constraints.
* **Bootstrap Deadlock** — readiness must include a **sentinel** that checks constraint echo.

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


