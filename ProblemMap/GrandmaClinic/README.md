# Grandma Clinic — 16 AI Bugs Your Grandma Can Understand

Most AI fixes today happen **after generation**. The model already said something wrong, then we chase with patches, rerankers, guards, and hand fixes. It becomes a patch jungle and the same failures keep coming back.

**Semantic firewall means we decide first**. We inspect the semantic state **before** output. If the field looks unstable, we loop, reset, or redirect. Only a stable state is allowed to speak. That is how each mapped failure mode stays fixed.

**Install the smoke alarm, not just the fire extinguisher.**

---

## Quick Links

* Doctor window: **[Dr. WFGY in ChatGPT Room](https://chatgpt.com/share/68b9b7ad-51e4-8000-90ee-a25522da01d7)**
  paste your trace or screenshot, ask: “which Problem Map number am i hitting? explain in grandma style.”
* Main map: **[Problem Map 1.0](../README.md)**
* Quick boot: **[TXT OS](../../OS/TXTOS.txt)**
* Visual guide: **[RAG Architecture & Recovery](../rag-architecture-and-recovery.md)**

---

## Acceptance Targets you should expect

* semantic drift ΔS ≤ 0.45
* coverage ≥ 0.70
* λ state convergent
* citation-first on knowledge tasks

you are installing a reasoning gate, not adding a bandage.

---

# The 16 Bugs

---

### No.1 Hallucination & Chunk Drift

**Grandma story**
you asked for basil. the waiter keeps bringing cilantro. it looks similar, tastes wrong.

**Metaphor mapping**

* basil = the concept you actually need
* cilantro = high-scoring but wrong neighbor
* taste wrong = answer sounds plausible but fails the task

**Real scene**
retrieval returns high similarity chunks that are semantically off. often caused by unnormalized embeddings, metric mismatch, mixed analyzers, or fragmented vectorstores.

**Minimal fix (grandma)**
wash the herbs and label them. check the taste before you cook the whole pot.

**Technical keys**
normalize vectors, verify metric choice, bind chunk ids to answers, add hybrid weights only after metric audit.

**Reference**
[Hallucination & Chunk Drift →](../hallucination.md)

---

### No.2 Interpretation Collapse

**Grandma story**
you said “wash then cut.” he heard “cut then wash.” same vegetables, wrong order.

**Metaphor mapping**

* “wash then cut” = the intended step order
* “cut then wash” = logic inversion
* same vegetables = correct chunk was present

**Real scene**
the chunk is right but the logic flips sequencing or roles. common in chain tasks and when the model compresses instructions.

**Minimal fix (grandma)**
stop mid-cook and taste again. if the direction feels off, step back one step and re-follow the recipe.

**Technical keys**
mid-step checkpoints, λ observe to re-ground, BBCR as reset when drift is detected, force citation-first for each sub-step.

**Reference**
[Interpretation Collapse →](../retrieval-collapse.md)

---

### No.3 Long Reasoning Chains

**Grandma story**
you sent him for three groceries. he returned with five bags of snacks. goal forgotten.

**Metaphor mapping**

* three groceries = finite chain with clear targets
* snacks = entropy and distraction
* goal forgotten = end condition lost

**Real scene**
multi-step tasks wander. intermediate states do not tie back to the goal. selection happens without validation.

**Minimal fix (grandma)**
write the shopping list and check it at each aisle. if he drifts, read the list again.

**Technical keys**
segment into verifiable subgoals, enforce λ diversity for candidates then converge, score ΔS per step, block illegal cross-path jumps.

**Reference**
[Long Reasoning Chains →](../context-drift.md)

---

### No.4 Bluffing / Overconfidence

**Grandma story**
he swears this is the best restaurant, but gives no address. you cannot verify.

**Metaphor mapping**

* best restaurant claim = confident answer
* no address = missing citation
* cannot verify = low trust

**Real scene**
confident natural language without sources. happens when the system rewards fluency over traceability.

**Minimal fix (grandma)**
ask for the recipe card with the dish. no card, no service.

**Technical keys**
citation-first policy, retrieval trace on, reject ungrounded claims, add minimal reranker only after source is confirmed.

**Reference**
[Bluffing / Overconfidence →](../bluffing.md)

---

### No.5 Semantic ≠ Embedding

**Grandma story**
white pepper and black pepper. same word “pepper” but different flavor.

**Metaphor mapping**

* same word = surface token overlap
* different flavor = semantic mismatch
* wrong taste = wrong result despite high score

**Real scene**
cosine similarity on unnormalized vectors or across models picks close vectors that do not carry the same meaning.

**Minimal fix (grandma)**
taste both peppers first. pick the one for this soup.

**Technical keys**
normalize embeddings, verify metric space, align tokenization and casing, use hybrid retrieval only after metric audit.

**Reference**
[Semantic ≠ Embedding →](../embedding-vs-semantic.md)

---

### No.6 Logic Collapse & Recovery

**Grandma story**
you keep trying the same dead-end alley. just step back and choose a different street.

**Metaphor mapping**

* dead-end alley = unproductive loop
* step back = controlled reset
* different street = alternative legal path

**Real scene**
the chain repeats a bad branch. without a reset rule it will never escape.

**Minimal fix (grandma)**
allow two tries. if still wrong, change the road.

**Technical keys**
set step budget, add reset triggers, block illegal cross-paths, log ΔS before and after reset, confirm λ convergence.

**Reference**
[Logic Collapse & Recovery →](../logic-collapse.md)

---

### No.7 Memory Breaks Across Sessions

**Grandma story**
yesterday you said “add salt.” today you ask again if salt is needed. annoying.

**Metaphor mapping**

* “add salt” = state you want to keep
* asking again = state not persisted
* annoying = user frustration

**Real scene**
context keys not pinned, state lost or overwritten, fragmented memory across turns.

**Minimal fix (grandma)**
write the note and pin it on the fridge. check it before cooking.

**Technical keys**
state keys with explicit scope, replay essentials on new turns, avoid silent state overwrite, bind memory to role.

**Reference**
[Memory Breaks Across Sessions →](../memory-coherence.md)

---

### No.8 Debugging is a Black Box

**Grandma story**
the soup is bad, but nobody wrote which spice was added. you cannot know what went wrong.

**Metaphor mapping**

* soup bad = wrong output
* no notes = missing trace
* cannot know = unfixable

**Real scene**
no chunk ids in logs, no store ids, no query record, no trace to source.

**Minimal fix (grandma)**
keep a small notebook. write which spice and when.

**Technical keys**
add retrieval ids, store ids, query strings, version stamps, and pass them through to the final answer.

**Reference**
[Traceability →](../retrieval-traceability.md)

---

### No.9 Entropy Collapse

**Grandma story**
simmered too long. everything turned into mushy porridge.

**Metaphor mapping**

* simmer too long = overlong context
* mushy porridge = collapsed attention
* missing shape = low structure

**Real scene**
long context flattens structure, answers incoherent at the tail.

**Minimal fix (grandma)**
cook in two pots. combine at the end.

**Technical keys**
window segmentation, mid-window anchors, stitch with context joins, confirm ΔS and coverage per segment.

**Reference**
[Entropy Collapse →](../entropy-collapse.md)

---

### No.10 Creative Freeze

**Grandma story**
edible but dull. like microwaved leftovers.

**Metaphor mapping**

* edible = correct but flat
* dull = no novelty
* leftovers = repeated patterns

**Real scene**
outputs are literal. diversity suppressed too early.

**Minimal fix (grandma)**
try three sleeves of spices. taste, then pick one.

**Technical keys**
sample for diversity first, converge after scoring, use λ\_diverse to ensure variation, avoid early greedy lock.

**Reference**
[Creative Freeze →](../creative-freeze.md)

---

### No.11 Symbolic Collapse

**Grandma story**
your family recipe was reduced to plain words. every cook interprets differently. flavor disappears.

**Metaphor mapping**

* family recipe = symbols, equations, tables
* plain words = paraphrase without structure
* flavor disappears = wrong execution

**Real scene**
code, math, or table structures get flattened. the symbol channel is lost.

**Minimal fix (grandma)**
keep the recipe card intact. no paraphrase of measurements.

**Technical keys**
preserve symbol blocks, avoid prose flattening, demand exact structure for code and math, pass through tables.

**Reference**
[Symbolic Collapse →](../symbolic-collapse.md)

---

### No.12 Philosophical Recursion

**Grandma story**
he keeps asking “who am i” while the soup gets cold.

**Metaphor mapping**

* who am i = meta recursion
* soup gets cold = primary task neglected

**Real scene**
self reference loops, paradox traps, meta questions displacing task.

**Minimal fix (grandma)**
finish the soup first. ask big questions after dinner.

**Technical keys**
define base facts, freeze meta layers until task completes, add recursion caps, use ε\_resonance to keep domain harmony.

**Reference**
[Philosophical Recursion →](../philosophical-recursion.md)

---

### No.13 Multi-Agent Chaos

**Grandma story**
two cooks both add salt. the soup turns inedible. they shared the same spoon.

**Metaphor mapping**

* two cooks = multiple agents
* same spoon = shared state without rules
* inedible = compounded error

**Real scene**
agents overwrite each other’s memory, roles mix, tools clash.

**Minimal fix (grandma)**
assign one cook to salt, one to stir. write their names on the spoons.

**Technical keys**
role partition, serialized writes, per-role memory, explicit tool ownership, avoid fan-in to a single blind context.

**References**
[Multi-Agent Problems →](../Multi-Agent_Problems.md)
[Role Drift →](../multi-agent-chaos/role-drift.md)
[Cross-Agent Memory Overwrite →](../multi-agent-chaos/memory-overwrite.md)

---

### No.14 Bootstrap Ordering

**Grandma story**
you dropped vegetables into a cold pan. no sizzle. soggy result.

**Metaphor mapping**

* cold pan = service not ready
* soggy = undercooked response
* no sizzle = missing warmup

**Real scene**
query fires before ingestion or index build. caches cold.

**Minimal fix (grandma)**
heat the pan. then add oil. then the vegetables.

**Technical keys**
readiness probes, ingest before query, cache warmup, strict boot order fences.

**Reference**
[Bootstrap Ordering →](../bootstrap-ordering.md)

---

### No.15 Deployment Deadlock

**Grandma story**
you wait for me, i wait for you. two people at a narrow door polite themselves into a full stop.

**Metaphor mapping**

* narrow door = shared resource
* polite standstill = mutual waiting locks
* full stop = system stall

**Real scene**
migrator waits writer. writer waits migrator. no timeout and no escape route.

**Minimal fix (grandma)**
decide who goes first. if not possible, open the side door and serve small dishes.

**Technical keys**
break dependency loops, set time boundaries, enable temporary read-only mode, staged rollout.

**Reference**
[Deployment Deadlock →](../deployment-deadlock.md)

---

### No.16 Pre-Deploy Collapse

**Grandma story**
the very first pot burned. gas off, pot dirty, spices missing. of course it failed.

**Metaphor mapping**

* gas off = missing credentials or key
* pot dirty = stale cache or bad index
* spices missing = env vars or config absent

**Real scene**
first API call hits missing secret, index not built, version skew across services.

**Minimal fix (grandma)**
check the kitchen before cooking. gas on, pot clean, spices ready.

**Technical keys**
pre-flight checklist: ENV, index, schema, model version, store health. block first call until all green.

**Reference**
[Pre-Deploy Collapse →](../predeploy-collapse.md)

---

## How to use this page

1. open **[Dr. WFGY](https://chatgpt.com/share/68b9b7ad-51e4-8000-90ee-a25522da01d7)**
2. paste your bug or screenshot
3. say: **“which Problem Map number am i hitting? explain in grandma style and give the technical fix.”**

the doctor maps your case, gives the grandma story for intuition, then hands you the exact technical suture with the right link.

---

## Why this exists

these 16 bugs are structural and reproducible. you will hit them once you scale. the point of a semantic firewall is to stop unstable states **before** output. fix once, and the same bug does not return.

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
