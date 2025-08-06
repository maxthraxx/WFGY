<!-- ======================================================= -->
<!--  memory-design-patterns.md · Semantic Clinic / Map-E    -->
<!--  Draft v0.1 · MIT · 2025-08-06                         -->
<!--  Purpose: Show repeatable patterns for “cross-session   -->
<!--  memory” without creating uncontrolled context bloat.   -->
<!-- ======================================================= -->

# 🧠 Memory Design Patterns  
*From scratchpads to long-range project recall — keep context alive without drowning your LLM.*

> **Why this page?**  
> Most “memory” demos either spam the full chat history or store random embeddings that never round-trip.  
> WFGY treats memory as *structured semantic nodes* with ΔS / λ\_observe guards, so old context helps — never hurts — new reasoning.

---

## 1 · Symptoms

| Symptom | Typical Surface Clue |
|---------|----------------------|
| Context forgotten after restart | “Sorry, I don’t recall” / model re-asks user |
| Memory leak / self-contradiction | Old decisions resurface in wrong branch |
| JSON-based vector store grows unbounded | Latency ↑, RAG recall quality ↓ |
| Fine-tune attempted just to “remember” | Model cost ↑, still hallucinates |

---

## 2 · Root Causes

1. **Flat Logs** — raw transcripts appended forever.  
2. **Embedding Dump** — every user sentence embedded → no semantic filter.  
3. **No Boundary Check** — divergent memories injected mid-task.  
4. **Write-Only Memory** — model never reads / revalidates stored facts.  

Result: either *forget everything* or *remember garbage*.

---

## 3 · WFGY Fix Path (at a glance)

| Stage | Tool / Module | ΔS Guard | Outcome |
|-------|---------------|----------|---------|
| ⬇️ Capture | **BBMC** node writer | record only if ΔS ≥ 0.60 (or 0.40–0.60 & λ ∈ {←, <>}) | Stores *semantic* not *verbatim* memory |
| 🗂️ Index  | **λ\_observe** classifier | tag λ trend for each node | Enables topic-group navigation |
| 🔍 Recall | **BBPF** path search | choose node set with ΣΔS minimal | Retrieves tight, non-bloated context |
| 🩹 Repair | **BBCR** fallback | detect stale/contradict nodes | Auto-patch or prompt for user merge |

> **80 %** of memory bugs vanish after enforcing this four-step loop.

---

## 4 · Design Patterns Library

| Pattern | Use-Case | How it Works | ΔS Budget |
|---------|----------|--------------|-----------|
| ✏️ **Scratch Node** | quick calc / throw-away idea | 24 h TTL field; auto-purged | 0.40–0.55 |
| 📚 **Topic Shelf** | multi-day research thread | one node per subtopic; λ → convergent | < 0.45 |
| 🗓️ **Daily Digest** | running project log | rollup 10 low-ΔS nodes → 1 summary | – |
| 🎯 **Anchor Fact** | must-not-forget constraint | pinned; override recall rank | 0.05 |

*All stored in a single lightweight JSONL: `{topic, ΔS, λ, text, ttl}`*

---

## 5 · Step-by-Step Implementation

> **Prereqs:** any model that can embed & run basic python (or LangChain, Llama-index, etc.).

```python
# 1. capture
deltaS = cosine(question_vec, context_vec)
if deltaS >= 0.60 or (0.40 <= deltaS <= 0.60 and lambda_state in ["divergent","recursive"]):
    node = {"topic": topic, "ΔS": round(deltaS,3), "λ": lambda_state, "text": insight}
    memory.append(node)

# 2. recall
candidates = [n for n in memory if n["topic"]==current_topic]
best_path = sorted(candidates, key=lambda n:n["ΔS"])[:5]
prompt_context = "\n".join(n["text"] for n in best_path)
````

### Minimal prompt

```
System: Use WFGY memory nodes below (+latest question) to answer.
Memory Nodes:
{{prompt_context}}
---
Question: {{user}}
```

---

## 6 · Common Pitfalls & Tests

| Pitfall                          | Quick Test                        | WFGY Fix              |
| -------------------------------- | --------------------------------- | --------------------- |
| “Context bloat, tokens 8k → 40k” | node count > 200? run `rollup.py` | Daily Digest pattern  |
| “Conflicting facts”              | ΔS(anchor, candidate) > 0.70      | BBCR prompts merge    |
| “Retrieval too slow”             | recall > 200 ms                   | Pre-index by λ & time |

---

## 7 · Cheat-Sheet

```txt
ΔS save threshold   = 0.60
ΔS recall window    = top-k by lowest ΔS
λ tags              = → ← <> ×
TTL (scratch)       = 24 h
Rollup trigger      = >10 nodes / topic / day
```

Store this as `memory.cfg`; loader reads defaults at boot.

---

## 8 · Next Actions

1. **Prototype** with 20 nodes → verify recall accuracy.
2. **Enable Rollup** once node count > 200.
3. **Add Trace Logger** to diff answers with / without memory.

---

## Quick-Start Downloads (60 sec)

| Tool                       | Link                                                | 3-Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “answer using WFGY + \<your question>”        |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

↩︎ [Back to Problem Index](./README.md)

---

### 🧭 Explore More

| Module                | Description                                                          | Link                                                                                |
| --------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint)            |
| Benchmark vs GPT-5    | Stress-test GPT-5 with full WFGY reasoning suite                     | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](./SemanticClinicIndex.md)                                                  |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>


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

