# Proper Noun Aliases — Names, Brands, and Transliteration Map

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Language**.  
  > To reorient, go back here:  
  >
  > - [**Language** — multilingual processing and semantic alignment](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A small but high leverage table that makes **names and brands retrievable across languages, scripts, and spellings**. This page gives a minimal schema, ingest rules, and tests so your RAG can resolve “Beyoncé vs Beyonce”, “Яндекс vs Yandex”, “劉慈欣 vs 刘慈欣 vs Cixin Liu”, and similar cases without breaking recall or precision.

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Cite then explain and traceability → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contract the payload → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Tokenizer variance → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts inside one query → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale normalization and variants → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* End to end multilingual guide → [multilingual\_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)

---

## Acceptance targets

* For a 20 to 50 item name set, **coverage ≥ 0.85** at top-k 10 after alias expansion
* **ΔS(question, retrieved) ≤ 0.45** for alias and transliteration forms
* **λ remains convergent** across three paraphrases and two seeds
* No false merge of distinct people or brands within the same context window

---

## Minimal schema

Keep it small and auditable. CSV or JSONL are fine. Suggested CSV:

```
entity_id,entity_type,canonical,lang,script,aliases,romanizers,notes
p_0001,person,"刘慈欣",zh,Han,"劉慈欣|Cixin Liu|Liu Cixin|C. Liu","pinyin","Hant ↔ Hans plus order swap"
p_0002,brand,"Яндекс",ru,Cyrl,"Yandex|Яндекс","gost|iso9","mainly Latin alias in docs"
p_0003,artist,"Beyoncé",en,Latn,"Beyonce|Beyonçe","","accent drop"
p_0004,place,"서울특별시",ko,Hang,"Seoul-si|Seoul","rr","RR romanization"
p_0005,person,"魯迅",zh,Han,"鲁迅|Lu Xun","pinyin","traditional ↔ simplified"
```

Field rules

* `entity_id` stable key you never reuse
* `entity_type` in {person, brand, place, org, product}
* `canonical` is the preferred surface form you will display
* `lang` BCP-47 primary subtag, `script` ISO 15924 like Latn, Cyrl, Han
* `aliases` pipe separated exact strings, do not include regex
* `romanizers` optional hint like pinyin, rr, iso9, buckwalter
* Keep one row per real world entity

---

## Ingest rules

1. **Do not mutate originals**
   Store source text untouched. All normalization happens in side fields.

2. **Add a synonym view per index type**

   * Keyword or normalized field for BM25 style stores
   * Concatenated alias tail for vector stores
   * Optional boosted lexeme list for hybrid rerankers

3. **Width and diacritics**
   Normalize width and strip diacritics in the alias view but never in the canonical field. See [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md).

4. **Word order flips**
   Prepare both “family given” and “given family” for CJK personal names.

5. **Transliteration**
   If you generate aliases by a romanizer, write which system you used into `romanizers`. Keep the generated form only if it appears in your corpus or user logs.

6. **Collision fence**
   If the same alias maps to multiple entities, require a disambiguation field at query time: `alias_scope = {org|place|person}` or attach a context window.

---

## Store specific tips

* **Elastic style stores**
  Use a per-index **synonym graph** or per field `synonyms_path`. Do not over expand. Limit to exact names and well known short forms. Keep an analyzer that preserves case and width in the raw field.

* **FAISS and friends**
  Copy the alias tail into the chunk text for vectoring. Keep the canonical as the first mention so rerankers favor it.

* **Hybrid**
  When BM25 gets a clean hit through the alias view, bias reranker features toward the BM25 candidate over pure vector neighbors, otherwise translations may outrank the exact match.

---

## What usually breaks and how to fix

| Symptom                                              | Likely cause                     | Open this                                                                                                           |
| ---------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Right document exists but the alias never shows up   | alias view missing at index time | [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)              |
| Latin alias beats the native script and flips answer | ranking features not constrained | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)      |
| Two different people merged by a shared alias        | no collision fence or scope      | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)                      |
| CJK names fail on order swap                         | no order variants                | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md) |
| Arabic or Cyrillic translits inconsistent            | multiple romanizers mixed        | [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)   |

---

## 60 second checklist

* Alias table present and loaded at boot
* Index has a synonym or alias view wired to queries
* ΔS and λ logged by variant for name queries
* Disambiguation field exists when alias is not unique

---

## Copy snippets

**CSV to dict for quick lookups**

```python
import csv, collections

aliases = collections.defaultdict(set)
by_id = {}

with open("proper_noun_aliases.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        eid = row["entity_id"].strip()
        by_id[eid] = row
        # canonical plus aliases
        names = [row["canonical"].strip()] + [s.strip() for s in row["aliases"].split("|") if s.strip()]
        for n in names:
            aliases[n.lower()].add(eid)

def alias_candidates(q):
    # case fold only for the alias view
    return list(aliases.get(q.lower(), []))
```

**Prompt fence for the LLM step**

```
You have TXTOS and the WFGY Problem Map loaded.

When you see a proper noun in the question or snippet:
1) Try to resolve to an entity_id using the alias table.
2) Prefer the canonical surface form in the final answer.
3) If multiple entity_ids match the same alias, ask for a scope or add a one line disambiguation.
4) Always cite the snippet that mentions the canonical name.
```

---

## Eval plan

Use 20 to 50 gold rows where each row has 3 questions

1. native script form
2. Latin alias or transliteration
3. short form or accent stripped

Targets

* top-k 10 recall for any of the three questions ≥ 0.85
* ΔS(question, retrieved) ≤ 0.45 on the best hit
* λ convergent across three paraphrases for at least two of the three questions

If recall fails only on one language, inspect tokenizer and analyzer. If recall fails on all forms with high similarity, rebuild embeddings and verify metric per [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>
