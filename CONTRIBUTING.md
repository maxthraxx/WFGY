# Contributing to **WFGY**

Thank you for helping push semantic reasoning forward!  
This guide merges the original workflow with our new Failure‑Trace and Problem‑Page pipelines.

---

## 1 · Reporting Issues

| Step | Detail |
|------|--------|
| 1️⃣ Search first | Avoid duplicates—check Issues & Discussions. |
| 2️⃣ Pick a template | **Bug / Feature** or **💥 Failure Trace**. |
| 3️⃣ Provide essentials | • Clear description • Steps to reproduce • Environment (Python ≥ 3.10, OS, model, WFGY version). |
| 4️⃣ Security | Found a vulnerability? Follow `SECURITY.md`; do **not** post details publicly. |

---

## 2 · Failure Trace Workflow (New!)

> **Goal:** capture real prompts / responses that still break WFGY and add them to regression tests.

1. Select **💥 Failure Trace** template when opening an Issue.  
2. Paste **5‑20 lines** of prompt‑response log.  
3. Pick the closest **Problem Category** (RAG, Multi‑Agent, Symbolic, …).  
4. Optional: add framework info (LangChain, AutoGen, etc.).  
5. We’ll tag the trace, reproduce it, and add tests / docs.

---

## 3 · Fork & Local Setup

```bash
git clone https://github.com/onestardao/WFGY.git
cd WFGY

python -m venv venv             # Python ≥ 3.10
source venv/bin/activate        # macOS / Linux
# .\venv\Scripts\Activate.ps1   # Windows

pip install -r requirements.txt
git checkout -b feature/<slug>
````

---

## 4 · Adding / Updating Code

| Task        | Command                                   |
| ----------- | ----------------------------------------- |
| Format code | `black .`  & `isort .`                    |
| Run tests   | `pytest tests/`                           |
| Pre‑commit  | `pre-commit run --all-files` (if enabled) |
| Add dep     | Update `requirements.txt` + note in PR    |

---

## 5 · Adding a **Problem Page** (Map entry)

1. Copy `/ProblemMap/_template.md` (or any existing page).
2. Fill the **eight‑section** structure: Intro → Root Cause → WFGY Fix → Demo → Cheat‑Sheet → Status → Tips → Quick‑Start.
3. Place under the correct folder, e.g.

   * `ProblemMap/multi-agent-chaos/new-issue.md`
4. Add at least **one regression trace** under `/tests/failure-traces/<slug>.txt`.
5. Update the relevant Specialized Map table (`Multi-Agent_Problems.md`) with the new row.

---

## 6 · Submitting a Pull Request

| Item              | Detail                                                                |
| ----------------- | --------------------------------------------------------------------- |
| **Title**         | `Add: <feature>` or `Fix: <bug>`                                      |
| **Description**   | Motivation · summary · test steps · `Closes #<issue>`                 |
| **Target branch** | `main`                                                                |
| **Checklist**     | Tests pass · docs updated · minimal commits (squash/rebase as needed) |

A **PR template** auto‑loads—fill the checkboxes before requesting review.

---

## 7 · Documentation & Release Notes

* Update any affected docs (`README`, examples, API) **in the same PR**.
* Maintainers handle version tags; open an Issue titled `[Release Candidate]` if you think a new release is ready.

---

## 8 · Communication Channels

| Channel                | Use                                                                     |
| ---------------------- | ----------------------------------------------------------------------- |
| **GitHub Discussions** | Q\&A, Failure‑Trace sharing, design RFCs                                |
| **Telegram**           | Quick chat with @PSBigBig                                               |
| **Email**              | [hello@onestardao.com](mailto:hello@onestardao.com) for private matters |

Follow the **Code of Conduct**—be respectful.

---

## 9 · Large or Breaking Changes

* Open an **RFC Issue** before coding large refactors.
* Mark the PR as **Draft / WIP** until consensus is met.
* Label accordingly (`architecture`, `breaking‑change`).

---

## 10 · Acknowledgements

Every PR—docs, code, examples, bug reports—moves WFGY closer to bullet‑proof reasoning.
Drop a ⭐ if this repo helps you; it fuels the next feature.

**Thank you for contributing!**
