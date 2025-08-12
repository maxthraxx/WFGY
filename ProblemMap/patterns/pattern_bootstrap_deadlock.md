# Pattern — Bootstrap Deadlock (No.14 Startup Ordering)

**Scope**  
Service boots, logs look “healthy,” but readiness never flips. Components wait on each other in a cycle (model ⇄ retriever ⇄ policy ⇄ index), or a probe marks “ready” before dependencies are actually warm, causing stuck loops or flapping.

**Why it matters**  
Deadlocks at startup burn deploy time, mask real regressions, and create ghost 500s. Fixing them requires **explicit dependency graphs**, **single-owner warmup**, and **deterministic gates**.

---

## 1) Signals & fast triage

**Likely symptoms**
- `/readyz` stays red forever, while `/livez` is green.
- Warmup logs repeat: “waiting for model,” “waiting for index,” with no progress counter.
- First request after rollout returns 503/timeout even though probes were green for a moment (flap).
- Two components each wait on the other’s warm signal (classic cycle).

**Deterministic checks (no LLM)**
- Build a **dependency DAG** (JSON/YAML). **Reject boot** if a cycle exists (topological sort fails).
- Require a **monotonic heartbeat** per phase; if no delta in N seconds → flag **STALL**.
- Enforce **single warmup owner** (mutex/lock) so concurrent warmups can’t interleave.

---

## 2) Minimal reproducible case

**Bad sequence (cycle)**  
- Retriever waits for Model “ready” to run sentinel query.  
- Model waits for Retriever to provide a sample vector to warm the head.  
→ Neither proceeds. `/readyz` hangs.

**Bad probe**  
- `/readyz` returns 200 once the HTTP server binds, even though FAISS/embeddings aren’t loaded.  
→ First live request 500s; probe flaps.

---

## 3) Root causes

- **Implicit dependencies** hidden in code paths (e.g., readiness calls the real query path which itself checks readiness).  
- **Multiple warmup owners** racing to initialize the same cache/index.  
- **Circular waits** across microservices (A waits for B’s `/readyz`, B waits for A’s `/readyz`).  
- **Probe confusion**: liveness vs readiness mixed; readiness not tied to real artifacts.

---

## 4) Standard fix (ordered, minimal, measurable)

**Step 1 — Declare the DAG**  
A machine-readable dependency list. Example:

```json
{
  "nodes": ["config","manifest","model","index","policy","sentinel"],
  "edges": [["config","manifest"],["manifest","model"],["model","index"],["index","policy"],["policy","sentinel"]]
}
````

**Step 2 — Validate at boot**

* **Toposort** the DAG; **abort** if a cycle exists.
* Persist the order and run warmup phases exactly in that order.

**Step 3 — Single warmup owner**

* Acquire a **process-wide lock** before warmup. Other threads read `READY=false` and return 503.

**Step 4 — Readiness = artifacts**

* Flip `READY=true` only after: config loaded, manifest validated, models reachable, index loaded, guard/policy loaded, **sentinel query** passes (same path as prod).

**Step 5 — Timeouts + heartbeats**

* Each phase updates a heartbeat counter (`ok_count`) and a timestamp.
* If no progress within `T_deadline`, log **STALL** and **retry from phase 0** (not from mid-phase).

**Step 6 — External waits are banned**

* Never wait on **other services’** `/readyz` in your readiness. Use local mocks/sentinels.

---

## 5) Reference implementation — Python (DAG + deadlock detector)

Create `ops/boot_guard.py`.

```python
# ops/boot_guard.py -- DAG validation, single-owner warmup, heartbeats, readiness flag
import json, os, time, threading, http.server, socketserver

READY = False
LOCK  = threading.Lock()
STATE = {"phase":"init","hb":{},"errors":[]}

def topo(nodes, edges):
    from collections import defaultdict, deque
    g = defaultdict(list); indeg = {n:0 for n in nodes}
    for a,b in edges: g[a].append(b); indeg[b]+=1
    q=deque([n for n in nodes if indeg[n]==0]); order=[]
    while q:
        u=q.popleft(); order.append(u)
        for v in g[u]:
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    if len(order)!=len(nodes): raise RuntimeError("CYCLE in bootstrap DAG")
    return order

def hb(phase): STATE["hb"][phase] = {"ts": time.time(), "ok_count": STATE["hb"].get(phase,{}).get("ok_count",0)+1}

def warm_phase(name, fn):
    STATE["phase"] = name
    fn(); hb(name)

def p_config():   time.sleep(0.1)            # load env, secrets
def p_manifest(): time.sleep(0.1)            # compare manifest vs runtime (see Example 05)
def p_model():    time.sleep(0.2)            # ping LLM: respond "ok"
def p_index():    time.sleep(0.2)            # map index files + ids
def p_policy():   time.sleep(0.1)            # load guard templates/policies
def p_sentinel(): time.sleep(0.2)            # run end-to-end question; check template/refusal

PHASE_FUN = {
    "config":p_config, "manifest":p_manifest, "model":p_model,
    "index":p_index, "policy":p_policy, "sentinel":p_sentinel
}

def warmup():
    global READY
    dag = json.loads(os.getenv("BOOT_DAG", '{"nodes":["config","manifest","model","index","policy","sentinel"],"edges":[["config","manifest"],["manifest","model"],["model","index"],["index","policy"],["policy","sentinel"]]}'))
    order = topo(dag["nodes"], dag["edges"])
    start = time.time()
    for name in order:
        warm_phase(name, PHASE_FUN[name])
        # heartbeat watchdog
        last = STATE["hb"][name]["ts"]
        if time.time() - last > float(os.getenv("PHASE_DEADLINE","10")):
            raise RuntimeError(f"STALL at {name}")
    READY = True; STATE["phase"]="ready"

class H(http.server.BaseHTTPRequestHandler):
    def _j(self,code,obj): self.send_response(code); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(json.dumps(obj).encode())
    def log_message(self, *a, **kw): pass
    def do_GET(self):
        if self.path=="/livez": return self._j(200, {"live":True,"phase":STATE["phase"]})
        if self.path=="/readyz": return self._j(200 if READY else 503, {"ready":READY,"phase":STATE["phase"],"hb":STATE["hb"],"errors":STATE["errors"][-3:]})
        return self._j(404, {"error":"not found"})

def main():
    # single-owner warmup
    with LOCK:
        try: warmup()
        except Exception as e: STATE["errors"].append({"phase":STATE["phase"],"err":str(e)})
    with socketserver.TCPServer(("",8081), H) as s:
        s.serve_forever()

if __name__=="__main__": main()
```

Run:

```bash
python ops/boot_guard.py
curl -s localhost:8081/livez
curl -s localhost:8081/readyz
```

**What it guarantees**

* Any cycle in your declared DAG fails fast with `CYCLE in bootstrap DAG`.
* Readiness flips **only** after all phases heartbeat.
* A stalled phase triggers an exception instead of hanging forever.

---

## 6) Reference implementation — Node (same contract)

Create `ops/boot_guard.mjs`.

```js
// ops/boot_guard.mjs -- DAG validation + single-owner warmup + readiness
import http from "node:http";

let READY = false;
const STATE = { phase:"init", hb:{}, errors:[] };

function topo(nodes, edges){
  const indeg = Object.fromEntries(nodes.map(n=>[n,0]));
  const g = Object.fromEntries(nodes.map(n=>[n,[]]));
  for(const [a,b] of edges){ g[a].push(b); indeg[b]++; }
  const q = nodes.filter(n=>indeg[n]===0); const order=[];
  while(q.length){ const u=q.shift(); order.push(u); for(const v of g[u]){ if(--indeg[v]===0) q.push(v); } }
  if(order.length!==nodes.length) throw new Error("CYCLE in bootstrap DAG");
  return order;
}
function hb(name){ const prev=(STATE.hb[name]?.ok_count||0); STATE.hb[name]={ ts:Date.now(), ok_count:prev+1 }; }

async function warmPhase(name, fn){ STATE.phase=name; await fn(); hb(name); }

// mock phases; swap with real ones
const phases = {
  config:   async()=>{},
  manifest: async()=>{},
  model:    async()=>{},
  index:    async()=>{},
  policy:   async()=>{},
  sentinel: async()=>{}
};

async function warmup(){
  const dag = JSON.parse(process.env.BOOT_DAG || '{"nodes":["config","manifest","model","index","policy","sentinel"],"edges":[["config","manifest"],["manifest","model"],["model","index"],["index","policy"],["policy","sentinel"]]}');
  const order = topo(dag.nodes, dag.edges);
  for(const name of order){
    await warmPhase(name, phases[name]);
    const last = STATE.hb[name].ts;
    const deadline = Number(process.env.PHASE_DEADLINE || 10000);
    if(Date.now() - last > deadline) throw new Error(`STALL at ${name}`);
  }
  READY = true; STATE.phase="ready";
}

const server = http.createServer((req,res)=>{
  const json=(c,o)=>{ res.writeHead(c,{"Content-Type":"application/json"}); res.end(JSON.stringify(o)); };
  if(req.url==="/livez")  return json(200,{live:true,phase:STATE.phase});
  if(req.url==="/readyz") return json(READY?200:503,{ready:READY,phase:STATE.phase,hb:STATE.hb,errors:STATE.errors.slice(-3)});
  json(404,{error:"not found"});
});

server.listen(8081, async ()=>{
  try { await warmup(); } catch(e){ STATE.errors.push({phase:STATE.phase, err:String(e)}); }
});
```

---

## 7) Acceptance criteria (ship/no-ship)

A build **may ship** only if:

1. DAG validated (no cycles).
2. Single-owner warmup completed; `READY=true`.
3. Sentinel passes using the **same** path as production query.
4. Readiness stays green for **N seconds** (e.g., 30s) without flap.
5. Example 07 readiness probe semantics are followed (liveness ≠ readiness).

---

## 8) Prevention (contracts & defaults)

* **No external `/readyz` waits** inside readiness. Use local mocks/sentinels only.
* **Artifacts-first readiness**: flip only after model ping, index map, guard/policy load, sentinel ok.
* **One lock** around warmup; idempotent phases.
* **Config freeze** during warmup; reject config reloads that would restart phases mid-flight.
* **Document the DAG** in repo (`ops/bootstrap.dag.json`) and pin it in CI.

---

## 9) Debug workflow (10 minutes)

1. Print the DAG and the computed toposort at boot.
2. Tail `/readyz`; if stuck, check `STATE.hb` for the last completed phase.
3. If **CYCLE**, fix edges and retry locally.
4. If **STALL**, increase logging inside that phase (model ping, file open, network).
5. After fixing, run a rolling restart; verify green readiness window.

---

## 10) Common traps & fixes

* **Using `/readyz` to warm** another service → cycle risk. Replace with **direct dependency probes** (e.g., TCP/socket or mock call).
* **Probes that always 200** → meaningless. Tie readiness to the artifact checklist.
* **Multiple warmers** (thread + health controller) → wrap with a mutex or leadership election.
* **Sentinel shortcut** that skips guards → green probe, broken prod. Run the **real** template.

---

## 11) Minimal checklist (copy into PR)

* [ ] `ops/bootstrap.dag.json` committed and validated at boot.
* [ ] Single warmup owner; no concurrent initializers.
* [ ] Readiness requires sentinel success on the **prod path**.
* [ ] No cross-service `/readyz` dependencies.
* [ ] Example 07 probes configured (live vs ready).

---

## References to hands-on examples

* **Example 07** — Bootstrap Ordering & Readiness Gate
* **Example 05** — Manifest validation before model/index warm
* **Example 03** — Use real retrieval in sentinel to catch hidden deps
* **Example 08** — Optional: run a micro-eval before flipping ready

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
