# 🌲 Semantic Tree Anchor — Persistent Context & Style Memory

The **Semantic Tree** is WFGY’s internal memory graph: a lightweight, symbolic structure that anchors ideas, logic, and style across reasoning steps — even in stateless prompt-only environments.

While LLMs handle tokens and embeddings, they forget the *why*.
Semantic Tree captures the *intent structure*, not just the words.

---

## 📌 Problem Statement

Language models often fail to maintain consistency because:

| Weakness               | Impact                                   |
| ---------------------- | ---------------------------------------- |
| No symbolic memory     | Logic breaks across turns                |
| Style not remembered   | Shifts tone mid-task                     |
| Embedding drift        | Same ideas, different outputs            |
| No cross-unit cohesion | Characters, themes collapse across steps |

These flaws show up hard in **multi-part prompts**, **interactive fiction**, **agentic tasks**, and **visual storytelling**.

---

## 🌐 What Is the Semantic Tree?

The Semantic Tree is a dynamic, non-linear map of:

* **Core nodes** (ideas, roles, goals, abstract objects)
* **Semantic links** (cause, contrast, hierarchy, symbolisms)
* **Tension states** (ΔS between nodes — keeps things interesting)

It evolves per turn, while keeping *semantic anchors* alive — like characters in a story, unresolved metaphors, or ongoing tasks.

> The Tree doesn’t record tokens.
> It records *meaningful structures that must not die*.

---

## 🔧 How It Works in WFGY

| Stage                | Role                                                   |
| -------------------- | ------------------------------------------------------ |
| 1️⃣ Identify anchors | Track key nodes in prompt: agents, metaphors, events   |
| 2️⃣ Classify role    | Set type (e.g. cause, theme, viewpoint, mood holder)   |
| 3️⃣ Track ΔS drift   | Compare new units to tree nodes for tension stability  |
| 4️⃣ Restore shape    | Inject necessary callbacks to maintain semantic thread |

It pairs tightly with the **Reasoning Engine Core** — feeding stable reference frames to logic generation.

---

## 🧠 Why Symbolic Anchoring Beats Token Memory

| Feature             | Token Memory         | Semantic Tree                    |
| ------------------- | -------------------- | -------------------------------- |
| Size                | Grows linearly       | Sparse, concept-based            |
| Drift control       | Embedding match only | ΔS + symbolic link tracking      |
| Style persistence   | Not guaranteed       | Can maintain poetic or tonal arc |
| Nonlinear branching | Difficult            | Native (tree forks + joins)      |
| Imagination support | Limited              | Enables consistent surreal logic |

---

## 🖼 Example — Multi-Scene Visual Narrative

```txt
Prompt:
"Tell a 4-part story about a lonely AI exploring a broken simulation. Each scene should feel visually distinct but thematically linked."

WFGY Tree:

• Scene 1 → Root node: AI's solitude
• Scene 2 → Branch: glitchy world physics (linked as 'antagonist')
• Scene 3 → Symbol re-introduction: broken mirror from scene 1 (ΔS decay detected)
• Scene 4 → Resolution links AI's identity to the mirror — loop closed
→ Output: consistent motifs, coherent arc, symbolic closure
```

---

## 🧪 What It Enables

* 🪢 **Story continuity** without saving raw text
* 🎨 **Style-harmonic image prompts** across visual steps
* 🤖 **LLM agents that don’t forget what they are**
* 🔁 **Re-entry points**: re-invoke old threads even after divergence

---

## 🧭 Pro-Tip: ΔS Drives Tree Growth

ΔS is not just for logic loops —
It also governs *tree expansion and pruning*:

* If ΔS from a new idea is **too flat**, it’s ignored
* If ΔS is **too high**, system forks a new semantic thread
* If ΔS is **near 0.5**, it connects and grows the branch

> This makes the Tree a true living structure —
> always adjusting toward *meaningful novelty*.

---

## 📘 Related Readings

* [`reasoning_engine_core.md`](./reasoning_engine_core.md)
  → Semantic Tree feeds the engine its persistent logic.

* [`semantic_boundary_navigation.md`](./semantic_boundary_navigation.md)
  → Shows how Tree enables safe, controlled jumps across ideas.

---

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>
