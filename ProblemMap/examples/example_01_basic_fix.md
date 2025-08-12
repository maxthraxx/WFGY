# Example 01 — Basic Guarded Answer (No.1 Hallucination & Chunk Drift)

**Goal**  
Stop the model from fabricating content. The model must answer only from provided evidence or return `not in context`.  
This is the smallest change that gives a visible quality jump. Works with any LLM and any framework. No SDK lock-in.

**Problem Map link**  
Targets **No.1 Hallucination and Chunk Drift**. Also improves traceability for No.2 and No.4.

**Outcome**  
- Answers either cite real chunks or refuse politely  
- You get a machine-readable trace for every question  
- This takes 10–15 minutes on a laptop

---

## 1) Inputs

We use a tiny corpus so you can reproduce without extra tools.

Create `data/pages.json` and `data/chunks.json`.

```json
// data/pages.json
[
  {"id":"p1","page":1,"text":"The library defines X. X is a constrained mapping. See also Y."},
  {"id":"p2","page":2,"text":"Y is unrelated to X. It describes a separate protocol."}
]
````

```json
// data/chunks.json
[
  {"id":"p1#1","page":1,"text":"X is a constrained mapping."},
  {"id":"p2#1","page":2,"text":"Y is unrelated to X. It describes a separate protocol."}
]
```

---

## 2) Evidence-only template

Use the same template for Python or Node.

```text
Use only the evidence. If not provable, reply exactly: not in context.
Answer format:
- claim
- citations: [id,...]
```

---

## 3) Path A — Python (no external packages required)

Create `run.py`.

```python
# run.py  -- minimal guarded answer with trace (no external deps)
import json, os, time, urllib.request

# 1) tiny in-memory "retriever" for the demo
def retrieve(question, chunks, k=2):
    # naive keyword score to keep this example dependency-free
    qs = set(question.lower().split())
    scored = []
    for c in chunks:
        score = sum(1 for w in c["text"].lower().split() if w in qs)
        scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:k]]

# 2) prompt builder with the evidence-only template
def build_prompt(q, chunks):
    ctx = "\n\n".join(f"[{c['id']}] {c['text']}" for c in chunks)
    return (
        "Use only the evidence. If not provable, reply exactly: not in context.\n"
        "Answer format:\n"
        "- claim\n- citations: [id,...]\n\n"
        f"Question: {q}\n\nEvidence:\n{ctx}\n"
    )

# 3) simple OpenAI call via HTTP (replace API key or swap to your LLM)
def call_openai(prompt, model=os.getenv("OPENAI_MODEL","gpt-4o-mini")):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY first")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps({
            "model": model,
            "messages": [{"role":"user","content":prompt}],
            "temperature": 0
        }).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )
    with urllib.request.urlopen(req) as r:
        j = json.loads(r.read().decode("utf-8"))
        return j["choices"][0]["message"]["content"].strip()

# 4) guard + trace
def guarded_answer(q, all_chunks):
    picks = retrieve(q, all_chunks, k=2)
    prompt = build_prompt(q, picks)
    txt = call_openai(prompt)
    ok = "not in context" in txt.lower() or "citations" in txt.lower()
    rec = {
        "ts": int(time.time()),
        "q": q,
        "chunks": [{"id": c["id"]} for c in picks],
        "answer": txt,
        "ok": ok
    }
    os.makedirs("runs", exist_ok=True)
    with open("runs/trace.jsonl","a",encoding="utf8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec

if __name__ == "__main__":
    chunks = json.load(open("data/chunks.json",encoding="utf8"))
    # test A: should answer with citation [p1#1]
    print(guarded_answer("What is X?", chunks))
    # test B: should refuse
    print(guarded_answer("What is Z?", chunks))
```

Run:

```bash
OPENAI_API_KEY=sk-xxx python run.py
```

Pass criteria:

* For “What is X?” the answer must contain “X is a constrained mapping.” and cite `[p1#1]`
* For “What is Z?” the answer must be exactly `not in context`
* Two lines appear in `runs/trace.jsonl`

---

## 4) Path B — Node (no SDK, single file)

Create `run.mjs`.

```js
// run.mjs  -- minimal guarded answer with trace (no extra deps)
import fs from "node:fs";
import https from "node:https";

function retrieve(question, chunks, k = 2) {
  const qs = new Set(question.toLowerCase().split(/\s+/));
  return [...chunks]
    .map(c => [c.text.toLowerCase().split(/\s+/).filter(w => qs.has(w)).length, c])
    .sort((a,b)=>b[0]-a[0])
    .slice(0,k)
    .map(([_,c]) => c);
}

function buildPrompt(q, chunks) {
  const ctx = chunks.map(c => `[${c.id}] ${c.text}`).join("\n\n");
  return `Use only the evidence. If not provable, reply exactly: not in context.
Answer format:
- claim
- citations: [id,...]

Question: ${q}

Evidence:
${ctx}
`;
}

async function callOpenAI(prompt, model=process.env.OPENAI_MODEL || "gpt-4o-mini") {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error("Set OPENAI_API_KEY first");
  const body = JSON.stringify({
    model,
    messages: [{ role: "user", content: prompt }],
    temperature: 0
  });
  const res = await new Promise((resolve, reject) => {
    const req = https.request("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`,
        "Content-Length": Buffer.byteLength(body)
      }
    }, r => {
      let data=""; r.on("data", d => data += d);
      r.on("end", () => resolve(JSON.parse(data)));
    });
    req.on("error", reject);
    req.write(body); req.end();
  });
  return res.choices[0].message.content.trim();
}

async function guardedAnswer(q, allChunks) {
  const picks = retrieve(q, allChunks, 2);
  const prompt = buildPrompt(q, picks);
  const txt = await callOpenAI(prompt);
  const ok = txt.toLowerCase().includes("not in context") || txt.toLowerCase().includes("citations");
  const rec = {
    ts: Date.now(),
    q, chunks: picks.map(c => ({id: c.id})),
    answer: txt, ok
  };
  fs.mkdirSync("runs", { recursive: true });
  fs.appendFileSync("runs/trace.jsonl", JSON.stringify(rec) + "\n");
  return rec;
}

const chunks = JSON.parse(fs.readFileSync("data/chunks.json","utf8"));
console.log(await guardedAnswer("What is X?", chunks));
console.log(await guardedAnswer("What is Z?", chunks));
```

Run:

```bash
OPENAI_API_KEY=sk-xxx node run.mjs
```

Pass criteria are the same as Python.

---

## 5) Why this works

* The template blocks any text that is not derived from evidence
* The citations requirement forces explainability and makes debugging easy
* Refusal is a valid outcome when evidence is insufficient
* The trace file is a permanent breadcrumb. You can inspect drift by looking at query, chosen chunks, and the final answer

This removes a large class of hallucinations without any model-specific tricks. It also gives you a baseline that you can evaluate after every change.

---

## 6) Common mistakes and quick fixes

* **The model still fabricates**
  Make sure your template appears at the very end of the system prompt and that nothing after it can override the rule. Keep temperature at 0 for tests.

* **Citations look wrong**
  Ensure you pass chunk ids through the entire path. If your UI formats citations, keep the raw ids in the trace.

* **Refusal rate is too high**
  You probably need better retrieval. Start with intersection of BM25 and embeddings then rerank, as in `getting-started.md`.

* **Trace file is empty**
  Check write permissions and make sure you call the guard wrapper, not a direct model call elsewhere.

---

## 7) Next steps

* Move to **Example 03** to add intersection and rerank which usually improves citation hit rate
* Use the **Eval** examples to measure precision, refusal, and citation overlap on a small question set
* If you use Ollama or LangChain, keep this guard layer exactly as is. Call your LLM behind `call_openai` or replace it with your local client

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

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>

