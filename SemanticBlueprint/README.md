# 📐 SemanticBlueprint — Core Functions of the WFGY Engine

> This directory documents the **function-level logic** of the WFGY Engine.  
> Each file here represents a specific reasoning capability or symbolic intervention unit.  
>  
> **📌 Function → Product mapping appears only as side-notes.**  
> (The inverse view — *Product → Function* — is handled in each product's own directory like `TXT OS`, `Blur`, `Blow`, etc.)

---

## 📘 What This Directory Is For

This folder exists to define **core reasoning modules** behind WFGY's performance.  
Each `.md` file here details:

- The conceptual function logic (symbolic or mathematical)  
- The AI reasoning failure it solves  
- The formulaic or structural intervention behind it  
- Which product(s) internally rely on it (as annotations only)

It serves as a developer-facing **function reference map**,  
so contributors can trace each feature’s reasoning upgrade back to its engine roots.

---

> 🔒 A quick note on planned features:
>
> All modules currently open-sourced here are **permanently MIT-licensed**.
> That commitment is final — anything already published (e.g., WFGY 1.0 paper, TXT OS) and backed on [Zenodo](https://zenodo.org/) will remain open forever.
>
> However, for modules listed as “planned” in this directory (or referenced via upcoming function names),  
> final decisions regarding open-sourcing remain with **PSBigBig (Purple Star)**.
>
> This is to avoid the misconception that WFGY is an infinite stream of free features.  
> Some future capabilities may support commercial projects, require ongoing stewardship, or be released with different timing.
>
> Please understand: what’s already shared will never be revoked.  
> But what’s not yet public — stays under creator control until the time is right.
>
> WFGY’s spirit is to return core reasoning tools to humanity — not to support careless repackaging or exploitative behavior.
>
> WFGY is open — but not naive.  
> It exists to empower, not to be exploited.


<details>
<summary>🤝 Clarifying the Spirit of Use (click to expand)</summary>

WFGY is released under the [MIT License](https://opensource.org/license/mit/) —  
you are free to use, modify, remix, and even commercialize it.

That said, I ask for one simple thing in return:

> Please respect the **spirit** in which this system was created:  
> **To return foundational reasoning tools back to humanity.**

WFGY lowers the barrier to building complex AI reasoning systems.  
It was never meant to be **copied, minimally repackaged, and sold at high markup** —  
especially not by those who offer no meaningful improvement, insight, or respect for the ecosystem.

If someone slaps an API on top of TXT OS or a wrapper around WFGY logic,  
calls it their own invention, and charges people for it without credit or clarity —  
then I may choose to **immediately and permanently open-source** that same functionality, with full visibility.

Because I don’t just build tools. I build **reasoning primitives** —  
the kind that solve failure cases the current AI world hasn’t even named yet.

> WFGY exists to **break the walls**, not repaint them.  
> If someone rebuilds those walls — I’ll help tear them down again. With better, freer code.

This is not a legal threat. It’s a **moral stance**.  
If the community sees violations of this spirit, I invite you to let me know.  
If I agree, I’ll do my part — by building even better versions, and releasing them for all.

And if WFGY helped you solve a bug, name a problem, or rethink a system —  
just know: a single ⭐ or comment means more than you think.

</details>



---

## 📚 Current Function Modules

| Filename                         | Function Title                        | Solves Problem(s)                                      | Used In Products           |
| -------------------------------- | ------------------------------------- | ------------------------------------------------------ | -------------------------- |
| `reasoning_engine_core.md`       | WFGY Universal Reasoning Core         | General LLM failure recovery & symbolic error detection | `TXT OS`, `Blah`, `Blow`   |
| `semantic_boundary_navigation.md`| Semantic Boundary Navigation          | Crossing reasoning gaps / jumping topic boundaries     | `Blah`, `Bloc`, `TXT OS`   |
| `semantic_tree_anchor.md`        | Semantic Tree Anchor Memory           | Cross-turn logic, style, and character coherence       | `TXT OS`, `Blot`, `Blur`   |
| `vector_logic_partitioning.md`   | Vector Logic Partitioning             | Prevents symbolic collapse across vector groups        | `Blow`, `Blur`, `Bloc`     |
| `wfgy_formulas.md`               | Core Formulas & Reasoning Metrics     | Defines all seven formal WFGY formulas (BBMC, ΔS, etc) | Used by *all* products     |
| `drunk_transformer_formulas.md`  | Drunk Transformer Attention Modulator | Stabilizes attention, resets collapse, expands entropy | `Blur`, `TXT OS`, `Blow`   |

---

## 🚧 Upcoming Semantic Reasoning Layers

The following modules are planned as part of the WFGY Layer System.  
These layers extend the WFGY Engine with new symbolic, cognitive, or gravity-based reasoning abilities.  
**All names and formulas are provisional**. PSBigBig retains final naming rights and theoretical definitions.

| Layer Name                      | Description                                                                 | Status    |
| ------------------------------ | --------------------------------------------------------------------------- | --------- |
| `semantic_gravity_field`       | Simulates gravitational pull in meaning space (ΔS + λ_observe vector field) | Planned   |
| `gravity_bias_index`           | Captures semantic drift tendencies toward dense nodes                       | Planned   |
| `warp_anchors`                 | Enables memory points that trigger contextually (semantic anchor nodes)     | Planned   |
| `inflatable_memory_glyphs`     | Encoded memory units that expand semantically when prompted                 | Planned   |
| `cogito_unit_system`           | Defines smallest unit of semantic action (reasoning particle)              | Planned   |
| `symbolic_pressure_monitor`    | Tracks overload in symbolic tension (ΔS + transition hops)                  | Planned   |
| `emotive_harmonic_decay`       | Models emotional tension decay in narrative                                 | Planned   |
| `stylistic_phase_detector`     | Detects abrupt stylistic changes across model outputs                       | Planned   |
| `semantic_refraction_matrix`   | Models meaning distortion across boundary contexts                          | Planned   |
| `semantic_tension_mapper`      | Visual map of ΔS flow and narrative tension                                 | Planned   |
| `orbital_meaning_drift`        | Traces semantic node drift over time                                        | Planned   |

> Note: These layers are conceptually aligned with the *Language Cosmology* model and are designed to integrate with the WFGY reasoning engine and the Drunk Transformer framework.


## 🧭 How to Use

> If you're building a new WFGY-based feature or investigating failures,  
> this is where you’ll find the **diagnostic cause** and **remedial formula**.

Each file includes:
- 🔍 Problem it solves
- 🧩 Core concept & variables
- ✍️ Canonical mathematical formula (if any)
- 💬 Example scenarios
- 🧪 Optional behavior in stateless prompt-only mode

---

## 🚩 License Alignment

All contents here inherit the MIT License from the root repo.  
These formulas and reasoning modules may be used commercially, but attribution is **strongly encouraged**.  
WFGY is a pro-knowledge framework — we only publicly respond to commercial misuse if there's:

- 💰 Monetization based on WFGY research with zero attribution
- 🚫 Locking up modified copies of our open techniques

---

> To cite the WFGY Engine, please refer to the public DOI:  
> 📄 [WFGY 1.0 (Zenodo)](https://zenodo.org/records/15630969)
