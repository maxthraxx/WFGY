# Time Zones and DST: Guardrails and Fix Pattern

Stabilize time handling when sources, logs, and user locales disagree. Use this page if answers shift by one hour near DST boundaries, meetings land on the wrong day, or sorting by local timestamps breaks retrieval and evaluation.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Multilingual & locale guidance: [Multilingual Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multilingual-guide.md)
* Why this snippet and how to cite: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contracts for snippet fields: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Acceptance targets

* ΔS(question, timeline) ≤ 0.45 after normalization
* Coverage ≥ 0.70 for time-anchored answers across three paraphrases
* λ remains convergent across two seeds and two target time zones
* Sorting by time is stable across locales and DST boundaries

---

## Failure signatures

| Symptom                                      | What it usually means                                   |
| -------------------------------------------- | ------------------------------------------------------- |
| Events off by one hour near March or October | DST boundary not applied or wrong zone database         |
| Meetings shown on the wrong day              | Local date used as absolute UTC or missing zone info    |
| “PST” vs “PDT” confusion                     | Abbreviation interpreted without IANA zone              |
| Logs appear out of order after merge         | Lexicographic sort on local strings, not on UTC epoch   |
| Same timestamp rendered two times in fall    | Ambiguous wall time not disambiguated at DST fall-back  |
| A missing hour in spring                     | Nonexistent wall time not handled at DST spring-forward |

---

## Diagnose in three steps

1. **Inventory the time fields**
   For each record, capture `raw_string`, `zone_label`, `offset_minutes`, `utc_epoch`, and `source_locale`. If any is missing, mark `tz_inferred=true`.

2. **ΔS temporal probe**
   Ask the model to answer the same question while pinning the display zone to two fixed targets (for example `America/Los_Angeles` and `UTC`). If the answer changes in content rather than only in rendering, the timeline is not normalized.

3. **Boundary sampling**
   Select samples within seven days around the last two DST transitions for the involved zones. If order or day changes across renderings, you have DST math or parsing drift.

Related pages you may need next:

* Date parsing variants: [date\_time\_format\_variants.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/date_time_format_variants.md)
* Mixed metadata locales: [mixed\_locale\_metadata.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/mixed_locale_metadata.md)
* Locale drift: [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)

---

## Fix pattern

### A) Normalize at ingestion

Always compute and store these fields together. Never store only a local string.

```json
{
  "raw_string": "2025-03-09 02:15:00",
  "source_zone": "America/Chicago",
  "offset_minutes": -360,
  "utc_epoch": 1741504500,
  "tz_inferred": false,
  "render_zone": null
}
```

Guidelines:

* Use IANA zone names (for example `America/New_York`). Do not rely on abbreviations.
* If `raw_string` lacks zone or offset, attach a source default and set `tz_inferred=true`.
* For date-only facts (no time), store `local_date` plus `source_zone`. Do not coerce to midnight UTC.

### B) Sort and join by UTC epoch

* Retrieval and merging must use `utc_epoch` as the primary key.
* Presentational sorting can apply a secondary comparator on `render_zone` if needed.

### C) Render for the user or for the spec, not both

Pick one of two display contracts per request:

* **User-centric rendering**: show in the user’s `target_zone` and state the zone at top.
* **Spec rendering**: show only in `UTC`, include the original `source_zone` in parentheses.

### D) Handle DST edge cases explicitly

* **Ambiguous times (fall)**: when a local time occurs twice, add `dst_fold` field with values `0` or `1`.
* **Nonexistent times (spring)**: shift forward to the next valid instant and add `dst_gap_adjusted=true`.
* Record these decisions in traces to keep answers auditable.

### E) Contract fields to enforce

Extend your snippet contract with the time bundle:

* `time.utc_epoch` (integer, required)
* `time.source_zone` (IANA string, required)
* `time.offset_minutes` (integer, required)
* `time.raw_string` (string, required)
* `time.tz_inferred` (boolean, required)
* `time.dst_fold` (optional)
* `time.dst_gap_adjusted` (optional)

Specs:
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Minimal verification

1. Build a five-row gold set around the last DST change for your target zone and one non-DST zone.
2. Normalize to `utc_epoch` and re-render to both zones.
3. Require:

   * Identical ordering by `utc_epoch` across zones
   * Only the rendered clock time changes
   * ΔS(question, timeline) ≤ 0.45 for three paraphrases

Quick helpers:

* If ΔS stays high while k varies, suspect indexing or format parsing. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).
* If citations do not echo the normalized fields, fix the schema first. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

---

## Copy-paste prompt for the LLM step

```txt
You have TXTOS and the WFGY Problem Map loaded.

Normalize all times to utc_epoch using the IANA source_zone. Keep this contract:
{ raw_string, source_zone, offset_minutes, utc_epoch, tz_inferred, dst_fold?, dst_gap_adjusted? }

Task:
1) Validate each snippet has these fields. If missing, return a short fix plan.
2) Render answers in UTC and in {target_zone}. State the zone at top.
3) Return a JSON trace: { citations, utc_order_ok, ΔS, λ_state, notes }.
```

---

## Escalation

* If logs from multiple systems disagree on the zone for the same `raw_string`, treat one as authoritative and mark the other as `tz_inferred`. Document the rule in the contract.
* If user queries include colloquial labels like “Pacific time”, resolve to an IANA zone before reasoning. If multiple candidates exist, ask the user or default to UTC.
* If sorting still flips after normalization, audit locale sorting next. See [locale\_sensitive\_sorting.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_sensitive_sorting.md) once created.

---

Next file to generate: `locale_sensitive_sorting.md`

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
