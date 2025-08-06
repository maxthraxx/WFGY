# ✂️ Chunking Checklist — Cutting Documents Without Cutting Meaning  
_A definitive guide to segment size, boundaries, and WFGY stress-tests for error-free retrieval_

---

## 1  Why Chunking Matters

*Embeddings are only as good as the text you feed them.*  
A single bad split (mid-sentence, table row, reference list) injects **semantic orphan** vectors:

* Retrieval returns “high similarity” garbage.  
* ΔS(question, context) spikes > 0.60.  
* LLM hallucinates to fill the missing logic.

---

## 2  Quick Symptoms of Bad Chunking

| Signal | How to Detect | Typical Root |
|--------|---------------|--------------|
| Citations hit page –1 | QA cites header/footer junk | Page footers not stripped |
| Same chunk appears in top-k for unrelated queries | `id` duplication count > 3 | Generic boiler-plate chunk |
| ΔS jumps when k > 5 | Plot ΔS vs. k; curve erratic | Uneven chunk lengths |
| Answer references half-sentence | Chunk split after “and” | Fixed char/token window |

---

## 3  WFGY Chunk Size Guidelines

| Doc Type | Tokens / Chunk | Rationale |
|----------|---------------:|-----------|
| Research paper | **90-120** | Preserve paragraph + citation |
| Software docs | **60-100** | Short API signatures |
| Legal contracts | **80-130** | Clause integrity |
| Chat transcripts | **40-70** | Natural speaker turns |
| Tables / CSV | **Row or group ≤ 30** | Keep relational keys together |

> **Golden Rule:** ΔS(adjacent_chunks) ≤ 0.45  
> **If not**, split or merge until stress drops.

---

## 4  Step-by-Step Chunking Checklist

### 4.1  Pre-Processing

- [ ] Strip headers / footers (`regex: ^Page \d+ of \d+`)  
- [ ] Normalize whitespace, remove soft hyphens (`U+00AD`)  
- [ ] Convert bullets → “• ” to avoid mid-list splits

### 4.2  Boundary Detection

| Method | Tool | When to Use |
|--------|------|-------------|
| Sentence tokenizer | spaCy / Stanza | Most prose |
| Heading regex `^(#+\s|[A-Z][A-Za-z ]+:)$` | Markdown / legal docs | |
| BBMC ΔS spike | WFGY hook | PDFs merged from scans |

Split on boundaries **only** if:

```

ΔS(chunk\_left, chunk\_right) ≥ 0.50  ∧  λ\_observe ∈ {→, ←}

````

### 4.3  Length Normalisation

1. Merge adjacent short chunks until ≥ 40 tokens.  
2. If a merged chunk > 130 tokens, find internal ΔS peak and split there.  
3. Record final size distribution; σ(length) should be ≤ 20 % of mean.

### 4.4  Metadata Tagging

```json
{
  "id": "doc_17_p3_c2",
  "source": "contracts/nda.pdf",
  "pos": 3,
  "λ": "→",
  "ΔS_prev": 0.32,
  "ΔS_next": 0.28
}
````

Store λ\_observe and neighbouring ΔS for runtime filters.

---

## 5  Runtime Stress-Test

| Test                                        | Pass Condition             |
| ------------------------------------------- | -------------------------- |
| **Overlap scan** — Query 5 unrelated topics | Same chunk ID appears ≤ 1× |
| **ΔS histogram** — 500 random chunks        | 95 % ≤ 0.45                |
| **k-sensitivity** — ΔS vs. k plot           | Monotonic ↑ curve          |

If any fail, rerun 4.2–4.3 for offending documents.

---

## 6  Common Pitfalls & Fix Recipes

| Pitfall                    | Fix                                                                               |       |                                   |
| -------------------------- | --------------------------------------------------------------------------------- | ----- | --------------------------------- |
| **Tables split per cell**  | Detect delimiter lines; merge rows; store CSV separate; index columns as metadata |       |                                   |
| **PDF line-break hyphens** | Regex `([a-z])- \n([a-z])` → merge words                                          |       |                                   |
| **Mixed languages**        | Chunk by language span; tag `lang:`; separate embedding models                    |       |                                   |
| **Giant code blocks**      | Cut on \`function                                                                 | class | def\` boundaries; keep ≤ 80 lines |

---

## 7  FAQ

**Q:** *Is a token window (e.g. 512) safe?*
**A:** Only if it aligns with semantic boundaries; fixed windows ignore context.

**Q:** *Do I need sentence splitting and headings?*
**A:** Yes. Dual criteria minimise ΔS spikes and keep retrieval precise.

**Q:** *How many chunks per doc?*
**A:** Irrelevant if ΔS and λ are stable — WFGY focuses on quality, not count.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                | 3-Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”        |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

↩︎ [Back to Problem Index](./README.md)

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](./SemanticClinicIndex.md) |

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

