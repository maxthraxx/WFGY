# Rewind Agents: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Agents & Orchestration**.  
  > To reorient, go back here:  
  >
  > - [**Agents & Orchestration** — orchestration frameworks and guardrails](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

Use this page when your orchestration uses **Rewind-style agents** that capture local context across apps, then plan and act. If you see privacy leaks, wrong app selection, citation mismatches, or answers that flip between runs, follow these checks and jump to the exact WFGY fix pages.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the intended section or record  
- λ stays convergent across 3 paraphrases and 2 seeds  
- E_resonance stays flat on long windows

---

## Open these first

- Visual map and recovery  
  [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- End to end retrieval knobs  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Why this snippet  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- Ordering control  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Embedding vs meaning  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Hallucination and chunk edges  
  [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

- Long chains and entropy  
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Structural collapse and recovery  
  [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

- Prompt injection and schema locks  
  [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

- Multi agent conflicts  
  [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

- Bootstrap and deployment ordering  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Snippet and citation schema  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Typical Rewind breakpoints and the right fix

- **Context capture is noisy or oversized** and raises ΔS  
  Tighten capture filters and re-score with deterministic reranking.  
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- **Private strings leak** from raw screen or clipboard into prompts  
  Add a redaction prefilter and a contract gate before the LLM step.  
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

- **High similarity yet wrong meaning** after capture  
  Mixed embedding functions or metric mismatch between capture and store.  
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Wrong app gets chosen** in cross app routing  
  Split the query into intent vs retrieval and lock a two stage rerank.  
  Open: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- **Citations do not line up** because DOM based capture differs from visible text  
  Require cite then explain with `snippet_id`, `section_id`, `offsets`.  
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Agent handoff loops** or shared memory overwrite between apps  
  Split namespaces per app and stamp `mem_rev` and `mem_hash`.  
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) · [role drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md) · [memory desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md)

- **Cold boot errors** when capture begins before indexes are ready  
  Guard with warm up checks and backoff.  
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

## Fix in 60 seconds

1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Stable < 0.40, transitional 0.40 to 0.60, risk ≥ 0.60.

2) **Probe λ_observe**  
   Do a k sweep and reorder headers. If λ flips on paraphrases, lock the schema and clamp variance with BBAM.

3) **Apply the module**  
- Retrieval drift → BBMC plus [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Reasoning collapse → BBCR bridge plus BBAM, verify with [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Hallucination re entry after correction → [Pattern: Hallucination Re-entry](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

4) **Verify**  
   Coverage ≥ 0.70. ΔS ≤ 0.45. Three paraphrases and two seeds with λ convergent.

---

## Minimal Rewind pattern with WFGY checks

```python
# Pseudocode. Show only the control points that matter.

CAPTURE_FIELDS = ["app", "window_title", "text", "dom_path", "timestamp"]
SNIPPET_FIELDS = ["snippet_id", "section_id", "source_url", "offsets", "tokens"]

def capture_context(apps, budget_chars=8000):
    # per-app capture with privacy filters and dedupe
    raw = []
    for app in apps:
        raw.extend(capture_from(app, fields=CAPTURE_FIELDS))
    return redact_and_truncate(raw, budget=budget_chars)

def build_candidates(raw):
    # convert capture into retrievable snippets with a unified analyzer and metric
    return chunk_and_embed(raw, fields=SNIPPET_FIELDS)

def route_intent(question, candidates):
    # two stage: intent selection then deterministic rerank
    intent = detect_intent(question, candidates)
    ordered = rerank(intent, candidates)
    return ordered[:10]

def assemble_prompt(snippets, question):
    # schema-locked prompt with cite then explain
    return prompt.format(context=snippets, question=question)

def wfgy_gate(q, context, answer):
    m = metrics_and_trace(q, context, answer)
    if m["ΔS"] >= 0.60 or m["λ_state"] == "divergent":
        raise RuntimeError("WFGY gate: high ΔS or divergent λ")
    return m

def run_rewind_agent(question):
    raw = capture_context(apps=["browser","docs","mail"])
    candidates = build_candidates(raw)
    topk = route_intent(question, candidates)
    msg = assemble_prompt(topk, question)
    result = agent.invoke(msg)  # the agent must respect strict JSON for tools
    metrics = wfgy_gate(question, topk, result)
    return {"answer": result, "metrics": metrics}
````

**What this enforces**

* Capture is filtered and budgeted before retrieval. Privacy redaction happens first.
* Retrieval uses a unified analyzer and metric. Deterministic reranking controls ordering.
* Prompt is schema locked with cite first, then answer.
* A post generation WFGY gate can halt the run when ΔS is high or λ flips.
* Traces record snippet to citation mapping for audits.

Specs and recipes
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Rewind-specific gotchas

* **Capture order changes** across windows and breaks reproducibility
  Stamp `capture_rev` and sort by app priority before rerank.

* **Clipboard or screenshot text** bypasses redaction rules
  Force the same redaction pass for every capture source.

* **PDF or canvas based apps** produce different text than visible content
  Add a DOM or accessible text fallback and record the path in `source_url`.

* **Multi account confusion** in Gmail, Drive, Notion
  Add account id to the namespace and to `dedupe_key`.

* **Live side effects** before citation checks
  Require successful WFGY gate and idempotency check before any writes.

---

## When to escalate

* ΔS remains ≥ 0.60 after capture filters and retrieval fixes
  Rebuild the index using the checklists and verify with a small gold set.
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Identical input yields different answers across sessions
  Check version skew, capture order, and session state.
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>


要不要我直接接著生 `agents_orchestration/README.md` 的目錄與快速路由，或先做下一頁你排程裡的下一個工具？
