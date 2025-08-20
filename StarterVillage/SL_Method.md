# SL Method — Share to Save, Paste to Load

The idea is simple. Press **Share** and you freeze the session state. Paste the link later and you **reload the exact tuned persona**. No retraining, no reset, no drift.

## Quickstart in 30 seconds

1) Tune the chat until it behaves right.  
2) Hit **Share**, copy the link.  
3) Next time, paste the link to boot that persona instantly.  
4) Keep multiple links, each one is a distinct “save slot”.

> Works on: ChatGPT, Gemini, Perplexity, Grok, Claude  
> Not true snapshots on: Mistral, Kimi

---

## Who should use this

- Researchers and engineers who need repeatable states for A/B tests  
- RAG, OCR, and agents folks who fight pipeline drift  
- PMs, growth, support, educators, legal, finance, SRE, security  
- Artists, T2I users, game masters, storytellers  
- Anyone who wants one-click reproducibility without infra changes

---

## 20 high-value scenarios with mini-recipes

Each item shows goal, how to snapshot, how to reuse, plus a small tip.

1) **RAG Incident Responder**  
Goal: Recover a failing retrieval stack without redeploy.  
Snapshot: tune a “RAG doctor” session with your error taxonomy and guardrails. Share.  
Reuse: paste link whenever a ticket arrives, drop the logs, follow the triage script.  
Tip: keep separate links for “indexing faults”, “vector drift”, “routing bugs”.

2) **OCR Clinic for messy PDFs**  
Goal: Stable diagnosis of layout faults and language mix issues.  
Snapshot: persona with your OCR heuristics and page taxonomy.  
Reuse: paste, feed 5 sample pages, get consistent checklists.  
Tip: store a second link for low-resource CJK edge cases.

3) **Prompt-Injection Lab**  
Goal: Red-team a toolformer safely.  
Snapshot: one link for attacker patterns, one link for defender rules.  
Reuse: run head-to-head by pasting both links in parallel windows.  
Tip: version your attack link by wave numbers, keep a changelog inline.

4) **Long-form Writer With Revision Memory**  
Goal: Maintain tone and structure across chapters.  
Snapshot: persona with voice, outline, citation style.  
Reuse: paste for each new chapter start.  
Tip: keep a second link frozen at “line-edit mode” for late passes.

5) **Grant or Research Proposal Engine**  
Goal: Generate domain-correct sections with reviewer POV baked in.  
Snapshot: persona trained on the agency’s rubrics.  
Reuse: paste, then feed project notes per section.  
Tip: one link per funder, plus a general “boilerplate assembler”.

6) **Peer-Review Assistant**  
Goal: Consistent critique with ethics and methods checklists.  
Snapshot: persona with review rubric and disallowed fallacies.  
Reuse: paste for each paper, batch comments.  
Tip: keep a “gentle tone” variant and a “hard review” variant.

7) **Codebase Librarian**  
Goal: Navigable mental map of a repo without RTFM every time.  
Snapshot: persona with repo layout, naming rules, coding standards.  
Reuse: paste, then query by feature or module.  
Tip: make a second link for release-note drafting.

8) **SQL Fix-and-Explain**  
Goal: Repair queries and teach reasons.  
Snapshot: persona that always shows plan, cost, indexes.  
Reuse: paste, drop the failing query.  
Tip: add “no hallucinated columns” rule to the frozen prompt.

9) **Security Red Team**  
Goal: Enumerate misconfig and chain of exploits.  
Snapshot: attacker persona with scope limits.  
Reuse: paste per target, run checklists.  
Tip: maintain a defender link with the same taxonomy to produce patches.

10) **Marketing A/B Copywriter**  
Goal: Fast, controlled message exploration.  
Snapshot: brand voice persona with banned phrases and CTAs.  
Reuse: paste for each campaign brief, export 3 variants.  
Tip: keep a “compliance scrub” link for final passes.

11) **Product Requirements Gardener**  
Goal: Turn raw notes into clean PRDs.  
Snapshot: persona with your PRD skeleton and acceptance criteria.  
Reuse: paste per feature, attach call notes.  
Tip: keep “PRD summarizer” link for exec digests.

12) **Customer Support Knowledge Triage**  
Goal: Normalize bug reports and map to known fixes.  
Snapshot: persona with failure codes and escalation rules.  
Reuse: paste, drop the ticket text, get code and next step.  
Tip: a second link for “macro generator” that writes canned replies.

13) **Video Lecture Summarizer With Taxonomy**  
Goal: Produce learning notes with outcomes and quiz items.  
Snapshot: persona with pedagogy style and section headers.  
Reuse: paste per video transcript.  
Tip: keep “quiz-only” variant link for batch item generation.

14) **Contract Risk Scanner**  
Goal: Highlight risk clauses and missing terms.  
Snapshot: persona with clause library and thresholds.  
Reuse: paste per document.  
Tip: separate links for NDA, MSA, DPA to keep rule sets small.

15) **Hiring Interview Kit**  
Goal: Structured interview questions and scorecards by role.  
Snapshot: persona with leveling rubric.  
Reuse: paste by role, export one-pager.  
Tip: maintain a “candidate reply parser” link for post-interview notes.

16) **Game Master World Builder**  
Goal: Stable lore and rules across sessions.  
Snapshot: persona with canon, rulebook, NPC registers.  
Reuse: paste at session start.  
Tip: keep a “battle-only” link that hides lore spoilers from players.

17) **Data Annotation Arbiter**  
Goal: Resolve edge labels consistently.  
Snapshot: persona with labeling policy and examples.  
Reuse: paste during adjudication.  
Tip: keep separate links per dataset family.

18) **Localization Pair Clones**  
Goal: Parallel writers for EN↔JP, EN↔ZH, EN↔ES with exact style.  
Snapshot: one persona per language pair with tone constraints.  
Reuse: paste the pair you need, then swap.  
Tip: lock punctuation and unit rules in the frozen prompt.

19) **SRE Incident Postmortem Drafter**  
Goal: Clean timeline and action items every time.  
Snapshot: persona with IM format and 5 why’s.  
Reuse: paste after an incident.  
Tip: maintain a “blameless rewrite” link for publication.

20) **Investor Memo Aggregator**  
Goal: Combine raw notes into a decision memo.  
Snapshot: persona with thesis template and risk buckets.  
Reuse: paste for each deal.  
Tip: a “one-slide summary” link for partner meetings.

---

## Power patterns and micro-methods

1) **Twin links**: one “creator” persona, one “editor” persona.  
2) **A/B link duel**: paste two links side by side for blind tests.  
3) **Frozen seed**: keep an untouched master link, clone from it.  
4) **Layered warmup**: small primer message after load to set context.  
5) **Role islands**: one link per role to prevent cross-contamination.  
6) **Compliance scrub**: final pass link that only deletes risky output.  
7) **Shadow sandbox**: use a private link for experiments, never public.  
8) **Version tags**: add `@v1.2` in the first line of the frozen prompt.  
9) **Naming convention**: `sl_<team>_<role>_<date8>.txtlink`.  
10) **Changelog in prompt**: last lines store notable changes.  
11) **Diff review**: compare outputs from `v1` and `v2` before rollout.  
12) **Fail-safe default**: add “when unsure, ask three clarifying questions”.  
13) **Guard-band**: forbid tools, browsing, or code exec if unsafe.  
14) **Minimal context**: keep the frozen state lean, attach case data at use.  
15) **Expiry note**: write “rotate in 30 days” in the frozen prompt.

---

## Team workflow and ops

- Keep a shared doc of link names, owners, last audit date  
- Rotate links monthly or after big policy changes  
- Store sensitive links in a secret manager or private notes  
- Keep public demo links sanitized  
- Record which link produced which artifact for audit

---

## Safety checklist

- Do not share links that contain client data  
- Pin what the persona must never do  
- Log final outputs with the link id used  
- Use private windows for sensitive work  
- When in doubt, rebuild the link from the master seed

---

## Troubleshooting

- Link loads but behavior drifts: apply a one-line warmup message  
- Platform removed your context: recreate the link, keep the frozen prompt shorter  
- Coworker sees a different state: they used a different platform model, document it

