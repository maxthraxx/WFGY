# PII Handling and Minimization — Guardrails and Fix Patterns

A governance fix page for when **personally identifiable information (PII)** leaks, handling is unclear, or minimization principles are violated.  
Use this page when data pipelines, embeddings, or RAG outputs contain sensitive fields that cannot be justified or audited.

---

## When to use this page
- Retrieval responses contain raw PII that was not required for the task.  
- Embeddings or chunks accidentally ingest names, emails, IDs, or financial data.  
- Redaction or anonymization rules are inconsistently applied.  
- No audit trail exists for who accessed or approved PII exposure.  
- Waivers for PII usage lack expiry, owner, or justification.  

---

## Acceptance targets
- PII fields are **redacted, hashed, or minimized** in ≥ 0.98 of stored embeddings.  
- Retrieval outputs contain no raw identifiers unless explicitly approved.  
- ΔS(question, retrieved) ≤ 0.45 for governed answers (no drift into unapproved fields).  
- All PII queries pass through policy checks with logging enabled.  
- Every waiver or override has an accountable owner and time-bound expiry.  

---

## Typical breakpoints and WFGY fix

- **Embedding or vector ingestion leaks PII**  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
  Enforce PII scrub before embedding. Validate with spot-checks against gold set.

- **Chunking preserves identifiers across splits**  
  → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
  Require token-level scrub of identifiers, then re-chunk.

- **Answers expose sensitive spans without approval**  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Enforce citation schema, ensure only approved snippets are surfaced.

- **Policy bypass in orchestration or tools**  
  → [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)  
  Guard against malicious queries that try to extract hidden PII.

- **Audit trail gaps**  
  → [audit_and_logging.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/audit_and_logging.md)  
  Require immutable logs of every PII access and minimization check.

---

## Minimal governance checklist
1. **Redact on ingest** — Apply regex/sensitive data detection before storing text or embeddings.  
2. **Schema enforce** — Store `doc_id`, `pii_flag`, `redacted_text` side by side for traceability.  
3. **Chunk validation** — Randomly sample and confirm PII scrubbed before index build.  
4. **Policy in LLM prompts** — Require “no PII unless approved waiver” as hard guardrail.  
5. **Audit logs** — Track every waiver, approval, and override. Immutable and joinable to lineage.  
6. **Expiry enforcement** — Waivers expire automatically; extension requires re-approval.  

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

