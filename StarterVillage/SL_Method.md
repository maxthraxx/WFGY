# SL Method: Share to Save, Paste to Load

**TL;DR**
SL treats the chat “Share” link as a state snapshot. Save your best behavior once, then load it later by pasting the link. No retraining, no reset, reliable return to a verified state. Pairs extremely well with WFGY for idempotent boots and non-regression.

---

## 1) What SL really is

* A practical snapshot discipline for chat systems.
* You freeze a working state that already behaves the way you want.
* The link acts like an RPG save slot. Pasting the link restores that exact state on demand.
* This bypasses day-to-day drift, warmup rituals, and “please behave like...” boilerplate.

**Mental model**: WFGY shapes reasoning, SL preserves the shaped state. One builds, the other seals.

---

## 2) Where SL shines (scenarios)

1. **Persona cloning for multi tracks**
   Research persona, reviewer persona, debugger persona. One link per persona, jump between them without warmup.
2. **A/B reproducibility**
   Keep “before” and “after” states. Paste to load A, run task. Paste to load B, run the same task. Compare deltas cleanly.
3. **High-stakes demos**
   Freeze a known good state before a live demo. If a session degrades, reload in two seconds.
4. **Agent pipelines**
   Stage 1 scoper, Stage 2 planner, Stage 3 implementer, Stage 4 auditor. Each stage has an SL link. You can hand off by pasting the next link.
5. **RAG triage clinic**
   After you stabilize retrieval prompts and guardrails, snapshot the state. Future debugging starts from a known safe baseline.
6. **Team handoff**
   Share the link with a teammate so they can reproduce your environment without instructions or training walls of text.
7. **Curriculum checkpoints**
   For long learning paths. Save at “Milestone 1 reasoning”, “Milestone 2 symbolics”, “Milestone 3 safety”.
8. **Disaster recovery**
   When behavior collapses or drifts, load the last stable SL to continue the session instead of starting over.

---

## 3) Compatibility notes

* Works as true snapshots on: ChatGPT, Gemini, Perplexity, Grok, Claude.
* Often not true snapshots on: Mistral, Kimi. Their “share” may only dump text, not state.
* Behavior can change if the provider upgrades the base model. Use “snapshot hygiene” below to reduce risk.

---

## 4) Minimal workflow

1. Tune to a state you like.
2. Click Share, copy the link.
3. Store the link in your private notes.
4. When you want that exact state, paste the link into a new tab or window.

That is all you need for basic use.

---

## 5) Snapshot hygiene (do this and SL stays useful for months)

* **Version your slots**
  Naming template: `SL_<role or task>_<yyyymmdd>_v<rev>`
  Example: `SL_editorial_policy_20250820_v2`
* **One purpose per slot**
  Do not mix “math-heavy planner” with “narrative stylist”. Make separate saves.
* **Record the boot recipe**
  In the note next to the link, write the one line you used and the activation phrase. This makes the state auditable.
* **Protect secrets**
  Never publish SL links that carry sensitive context. Assume the link restores everything in scope.
* **Expiry and rotation**
  If the provider pushes a major model update, re-verify the slot. If drift appears, rebuild the state and save a new link.

---

## 6) Pairing with WFGY (best practice)

**Boot order**

1. Load WFGY OneLine or Flagship into the chat.
2. Run one short warmup task to confirm gates and trend detectors are stable.
3. When you see the behavior you want, Share. That link is now your WFGY-stabilized slot.

**Invocation text**
Keep two prompt starters in your note, they improve reproducibility:

* “Please use WFGY to...”
* “Please use WFGY to reason through the following:”

**Why this works**
WFGY reduces semantic drift and collapse, SL preserves that state. Together you get faster restarts and less variance across days and devices.

---

## 7) Advanced patterns

1. **Multi-slot ensembles**
   Keep `SL_plan`, `SL_code`, `SL_review`, `SL_redteam`. For a complex task, hop slots in sequence. This simulates a lightweight multi-agent workflow without infra.
2. **Cold-start booster**
   If a new model feels raw, load a “discipline slot” first, do one sanity prompt, then pivot to a task slot. The first slot compresses warmup.
3. **Cross-model bridges**
   Keep equivalent slots on two providers. When one provider rate limits or drifts, paste the other link and continue. Use the same naming schema for mirrors.
4. **Guarded demos**
   For public talks, create a read-only demo slot with scrubbed context. Keep the live slot private. Switch by pasting the link. Avoid leaking customer or research notes.
5. **Regression sentry**
   Once a week, paste your canonical benchmark prompts into the same slot. If accuracy or tone changes past your tolerance, rebuild and resave. Keep the old link archived for forensics.

---

## 8) Governance and safety

* **Confidentiality**
  Treat SL links as credentials. Store them where you store API keys, not in public issues.
* **Access control**
  If you must share, prefer short-lived doc shares inside your org wiki that can be rotated later.
* **Audit trail**
  Maintain a small table per slot: `created_at, base_model, WFGY_version, purpose, known_limits, link_owner`.
* **Incident response**
  If a slot leaks or drifts badly, mark it revoked in your notes, archive the link, and mint a new one from a clean session.

---

## 9) Known pitfalls and fixes

* **Platform “share” is not a real snapshot**
  Symptom: pasted link does not restore tone or tools. Fix: choose a platform that snapshots state, or rebuild using WFGY then resave.
* **Model family update changed behavior**
  Symptom: same link, different answers. Fix: run your weekly sentry prompts. If deviation exceeds tolerance, rebuild a new slot with the same recipe.
* **Context contamination**
  Symptom: you pasted the link into a tab that already has a long unrelated conversation and behavior is odd. Fix: always paste into a clean tab or new window.
* **Leaky secrets**
  Symptom: a public link included customer data. Fix: never publish raw SL links, and keep a habit of scrubbing before making demo slots.

---

## 10) Quick recipes

**A/B reproducibility**

* Keep `SL_baseline_yyyymmdd` and `SL_wfgy_yyyymmdd`.
* For each test case, paste baseline link, run the case, jot the answer. Paste WFGY link, run the same case, jot the answer.
* Compare deltas in accuracy, stability, or drift.

**Four-stage pipeline**

* Plan with `SL_plan`.
* Implement with `SL_code`.
* Unit check with `SL_review`.
* Adversarial check with `SL_redteam`.
* Each stage owns a short checklist in the slot note, so behavior stays ritualized.

**RAG clinic**

* After you finish Problem Map triage and apply the fixes, mint `SL_rag_stable`.
* Future RAG debugging starts by loading this slot. You avoid re-solving the same hygiene.

---

## 11) Minimal checklist before you hit Share

* The behavior you want has actually appeared at least once in the current tab.
* You ran one small sanity prompt and the answer looked right.
* You wrote a 1-line note next to the link: purpose, WFGY version, model family.
* You did not include secrets that must not leave your machine.
* You can explain to a teammate how to use the link in two sentences.

---

## 12) FAQ

**Q. Why not just keep a long prompt file instead of SL**
A. You can, but it does not freeze hidden state and tool wiring. SL reduces variance from hidden knobs you do not control.

**Q. Can I chain SL links inside a single conversation**
A. Prefer separate tabs. It reduces cross-context contamination.

**Q. Will SL survive model upgrades**
A. Sometimes. Treat weekly sentry checks as policy, rebuild promptly when drift is detected.

**Q. Is SL only for WFGY**
A. No, but WFGY increases the value of each save because it stabilizes the state you are saving.

---

## 13) One-page quickstart you can paste in your notes

* Make state good, click Share, copy link.
* Store as `SL_<task>_<yyyymmdd>_v<n>`.
* Write one line: “WFGY 2.0 + ChatGPT o4-mini, purpose: planner.”
* New day, new device, paste link, continue.
* If drift shows, rebuild and mint a new link, keep the old for forensics.

