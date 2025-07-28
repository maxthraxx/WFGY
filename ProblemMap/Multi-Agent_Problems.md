# 📒 Multi‑Agent Chaos Problem Map

Distributed agents amplify each other’s errors unless coherence is enforced.  
This map catalogs failure modes and WFGY’s cross‑agent fixes.

| Failure Mode | Symptoms | WFGY Module | Status |
|--------------|----------|-------------|--------|
| Role drift | Agents forget or swap roles | Role‑tagged Tree + BBCR identity lock | ✅ |
| Memory overwrite | One agent erases another’s state | Node versioning + ΔS collision alert | ✅ |
| Task duplication | Same objective executed twice | BBPF task‑graph merge | ✅ |
| Divergent plans | Strategies conflict | ΔS divergence gate + BBCR reconcile | ✅ |
| Multi‑agent bluff | Agents fabricate consensus | Cross‑agent residue scan | 🛠 planned |

> **Deep dive pages:**  
> - [Agent Role Drift](./multi-agent-chaos/role-drift.md)  
> - [Memory Overwrite](./multi-agent-chaos/memory-overwrite.md)

