# Stopword and Morphology Controls · Global Fix Map

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


Lock language specific stopwords and morphology so retrieval remains stable across scripts and locales. Protect entities from stopword removal, version your lemmatizer, and verify with ΔS, λ, and coverage targets.

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Traceability schema → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contract the payload → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Tokenizer variance → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale normalization → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* Romanization rules → [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)
* Proper nouns and aliases → [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)
* Language detection → [query\_language\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)
* Analyzer routing → [query\_routing\_and\_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)
* Bilingual eval sets → [code\_switching\_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 on three paraphrases and two seeds
* Coverage of target section ≥ 0.70
* λ convergent when switching between inflected forms and lemmas
* Removing stopwords never drops a required entity or negation token
* Rank\@k does not regress more than 2 points after morphology changes

---

## What usually breaks

| Symptom                                      | Likely cause                                            | Open this                                                                                                                                         |
| -------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Named entities vanish after preprocessing    | stopword list removes particles that are part of names  | [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)                  |
| Wrong meaning for negated statements         | stopword filter removes “not” class tokens              | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)                                    |
| Duplicate docs across lemma and surface form | inconsistent stemming across index and query            | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)                     |
| CJK recall collapses after adding stopwords  | imported Latin stopword list applied to CJK             | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)                               |
| Turkish i and ı behave inconsistently        | locale fold differs across stages                       | [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)                                 |
| Romanized queries fail while native works    | alias view absent and morphology applied only to native | [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) |

---

## Language family controls

### Latin and Germanic

* Case fold with locale aware rules.
* Use light stemming or lemmatization, not both.
* Keep negation terms out of stopwords. Maintain a protected list.

### Romance

* Normalize accents consistently.
* Prefer lemmatization for verbs and nouns.
* Maintain a protected list for names with articles or particles.

### CJK

* Do not apply generic stopword lists.
* Use bigram or language specific tokenizers.
* Keep entities in dedicated fields without stopword removal.

### Semitic RTL

* Normalize diacritics and width consistently.
* Use lemmatization that preserves roots only if evaluation passes ΔS and coverage.
* Keep a protected list for clitics that change meaning.

### Indic

* Avoid generic lists from other languages.
* Use language specific analyzers and verify with bilingual eval.
* Protect named entities that share forms with common words.

### Cyrillic and Greek

* Apply accent and width normalization.
* Prefer lemmatization over aggressive stemming.
* Maintain a protected entity list for inflected forms.

---

## Deterministic pipeline checklist

1. Version every component: `stoplist_v`, `stemmer_v`, `lemma_v`, `normalize_v`.
2. Define no stop zones for entity fields and citation fields.
3. Keep words filter with a protected list per language code.
4. Apply normalization before morphology, not after.
5. Use the same pipeline for indexing and querying.
6. Log a morphology fingerprint in traces and eval reports.

---

## Copy snippets

**A. Protected term filter sketch**

```json
{
  "analysis": {
    "filter": {
      "keep_entities_en": {
        "type": "keep",
        "keep_words": ["New York", "AT&T", "Côte d'Ivoire", "Íñigo", "İstanbul"]
      }
    }
  }
}
```

**B. Minimal morphology config record**

```json
{
  "language": "tr",
  "stoplist_v": "tr_core_1.2",
  "lemma_v": "tr_lemma_0.9",
  "normalize_v": "nfkc_fold_tr",
  "no_stop_fields": ["title_exact", "entity_exact"],
  "protected_list_hash": "sha256:..."
}
```

**C. Trace fields to log**

```
{
  "ΔS": 0.42,
  "λ_state": "<>",
  "coverage": 0.74,
  "language": "ar",
  "morph_fingerprint": "stop:ar_1.1|lemma:ar_0.8|norm:nfkc_1.0|keep:hash"
}
```

---

## Eval protocol

* Use bilingual and code switching sets from [code\_switching\_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md).
* For each query, test with and without stopword removal and with two morphology settings.
* Accept only if ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent, and no loss of entity recall.
* Report Rank\@k deltas for lemma vs surface forms.

---

## When to escalate

* ΔS stays ≥ 0.60 after morphology and stopword tuning → revisit analyzer routing and re chunking, see [query\_routing\_and\_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md) and [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).
* Good top k but citations inconsistent → enforce schema and fix at the prompting layer, see [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

---

## Copy paste prompt for the LLM step

```
You have TXTOS and the WFGY Problem Map loaded.

Task:
1) For {lang, script}, choose stopword and morphology settings that protect entities and negation.
2) Run cite then explain. If ΔS(question, retrieved) ≥ 0.60, propose the minimal structural fix.
3) Return JSON:
{ "stoplist_v": "...", "lemma_or_stem": "lemma|stem|none", "protected_terms": [...], "ΔS": 0.xx, "coverage": 0.xx, "λ_state": "→|←|<>|×" }
Keep it auditable and short.
```

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

