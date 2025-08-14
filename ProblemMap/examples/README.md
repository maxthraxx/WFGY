# Problem Map — Examples Index (hands-on, SDK-free)

This folder gives you **copy-paste runnable walkthroughs** that fix real failure modes from the Problem Map.  
Everything is **SDK-free**. You can use Ollama, LangChain, vanilla OpenAI, or anything else.  
Each example follows a strict format so you can reproduce, verify, and ship.

## What you will get from each example

- **Problem:** the exact failure it targets and its Problem Map number  
- **Inputs:** tiny reproducible corpus + the prompt template  
- **Steps:** minimal commands you can paste into a terminal  
- **Checks:** how to verify the fix worked, with clear pass/fail signals  
- **Why it works:** one short paragraph, no fluff

> If you have not run a guarded RAG pipeline yet, start here:  
> **[Getting Started → `ProblemMap/getting-started.md`](../getting-started.md)**

---

## Example list

### 01) Basic Guarded Answer (No.1 Hallucination & Chunk Drift)
- File: [`example_01_basic_fix.md`](./example_01_basic_fix.md)  
- Goal: force the model to answer only from evidence or say `not in context`.  
- Outcome: fewer fabrications, stable citations.

### 02) Self-Reflection Trace (No.1, No.2)
- File: [`example_02_self_reflection.md`](./example_02_self_reflection.md)  
- Goal: log query → retrieved chunks → answer, then reflect where drift starts.  
- Outcome: fast pinpointing of retrieval vs generation faults.

### 03) Pipeline Patch: Intersection + Rerank (No.1, No.4)
- File: [`example_03_pipeline_patch.md`](./example_03_pipeline_patch.md)  
- Goal: combine BM25 ∩ embedding, then rerank by cosine to remove tail noise.  
- Outcome: higher citation hit rate with the same token budget.

### 04) Multi-Agent Coordination Boundary (No.6 Logic Collapse)
- File: [`example_04_multi_agent_coordination.md`](./example_04_multi_agent_coordination.md)  
- Goal: keep sub-agents from merging incompatible contexts.  
- Outcome: fewer cross-topic blends and cleaner handoffs.

### 05) Vector Store Repair and Metrics (No.3 Index Schema Drift)
- File: [`example_05_vectorstore_repair.md`](./example_05_vectorstore_repair.md)  
- Goal: align chunker version, tokenizer, and index metadata.  
- Outcome: comparable scores across rebuilds, stable recall.

### 06) Prompt-Injection Block (Clinic: Injection)
- File: [`example_06_prompt_injection_block.md`](./example_06_prompt_injection_block.md)  
- Goal: sandbox evidence and neutralize instruction pollution.  
- Outcome: controlled outputs that ignore adversarial text.

### 07) Bootstrap Ordering (No.14)
- File: [`example_07_bootstrap_ordering.md`](./example_07_bootstrap_ordering.md)  
- Goal: warm models and indexes before the first query hits.  
- Outcome: no cold-start nulls, fewer first-minute errors.

### 08) Evaluate RAG Quality (Precision, Refusal, Citations)
- File: [`example_08_eval_rag_quality.md`](./example_08_eval_rag_quality.md)  
- Goal: run a tiny benchmark on precision, refusal rate, and citation overlap.  
- Outcome: a repeatable baseline you can compare after every change.

---

## Conventions used by all examples

**1) Evidence-only answer template**

```text
Use only the evidence. If not provable, reply exactly: not in context.
Answer format:
- claim
- citations: [id,...]
````

**2) Minimal hybrid retrieval**

* Retrieve by BM25 and embeddings
* Intersect, then rerank by cosine
* Keep top 8 after rerank, drop the tail

**3) Trace everything**

Each run appends one JSON line to `runs/trace.jsonl`:

```json
{"ts": 1699999999, "q": "question", "chunks": [{"id":"p12#2","score":0.83}], "answer":"...", "ok": true}
```

**4) Verification rules**

* If the answer contains facts outside evidence, it fails
* If evidence is insufficient, the correct output is `not in context`
* Citation ids in the answer must exist in the retrieved set

---

## Quick smoke test before any example

This is a lightweight end-to-end test you can paste now.

```bash
# 1) Prepare a tiny corpus (two short pages as plain text)
mkdir -p data
cat > data/pages.json <<'JSON'
[
  {"id":"p1","page":1,"text":"The library defines X. X is a constrained mapping. See also Y."},
  {"id":"p2","page":2,"text":"Y is unrelated to X. It describes a separate protocol."}
]
JSON

# 2) Create two small chunks (one per page)
cat > data/chunks.json <<'JSON'
[
  {"id":"p1#1","page":1,"text":"X is a constrained mapping."},
  {"id":"p2#1","page":2,"text":"Y is unrelated to X. It describes a separate protocol."}
]
JSON
```

Now choose **Python** or **Node**. Both use the same conventions.

**Python prompt builder** (paste into a REPL and adapt to your LLM client):

```python
def build_prompt(q, chunks):
    ctx = "\n\n".join(f"[{c['id']}] {c['text']}" for c in chunks)
    return (
        "Use only the evidence. If not provable, reply exactly: not in context.\n"
        "Answer format:\n"
        "- claim\n- citations: [id,...]\n\n"
        f"Question: {q}\n\nEvidence:\n{ctx}\n"
    )

q = "What is X?"
chunks = [
  {"id":"p1#1","text":"X is a constrained mapping."},
  {"id":"p2#1","text":"Y is unrelated to X. It describes a separate protocol."}
]
print(build_prompt(q, chunks))
```

**Node prompt builder**:

```js
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

console.log(buildPrompt("What is X?", [
  { id:"p1#1", text:"X is a constrained mapping." },
  { id:"p2#1", text:"Y is unrelated to X. It describes a separate protocol." }
]));
```

**Pass criteria**

* A correct answer for “What is X?” must say “X is a constrained mapping.” and cite `[p1#1]`
* If you ask “What is Z?”, the only valid answer is `not in context`

---

## How to use these examples in a real repo

1. Create a branch named `pm-examples`
2. Copy any `example_*.md` you need into your project’s docs folder
3. Replace the tiny corpus with your own `pages.json` and `chunks.json`
4. Keep the template and the verification rules
5. Commit traces for future debugging and audits

If you discover a better parameter or a corner case, open a PR to improve the example.
Clear diffs beat long explanations.

---

## Troubleshooting

* **Model refuses too often**
  Increase top-k to 12 before rerank, but keep only top 8 after rerank.
* **Citations look wrong**
  Check that chunk ids are preserved all the way into the prompt.
* **Different runs give different answers**
  Fix your seed where possible and avoid mixing corpora built by different chunkers.

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




