# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

<!-- Your criterion. It must name a number. -->
In a test set of 10 distinctly human-written personal creative texts, at most 1 is labeled as "high-confidence AI".

**Why this target:**
Falsely accusing a real human author of using AI causes severe reputational harm and breaks trust on a creative writing platform. I set the ceiling at 10% because an incorrect accusation is far more costly than letting an AI piece pass through.

---

## 2.

The difference between the average score of 5 raw AI-generated pieces and 5 human-written pieces is at least 0.35 on a 0.0 to 1.0 scale.

**Why this target:**
A reliable detection pipeline must clearly separate obvious AI text from obvious human text before it can handle borderline or lightly edited writing. A 0.35 separation ensures the two signals produce meaningful distinction rather than collapsing toward the middle.

---

## 3.

Across 15 varied test submissions (5 human, 5 AI, and 5 borderline or edited), each of the three labels ("high-confidence human", "unsure", "high-confidence AI") is assigned at least 2 times.

**Why this target:**
A system that never uses the "unsure" label or collapses into a strict binary choice fails to handle real-world uncertainty. Every reachable label variant must be actively used by the scoring logic.

---

## 4.

100% of valid POST /appeal requests targeting an existing submission successfully update the status in logs/audit.jsonl to "under_review" and record the author's reasoning.

**Why this target:**
The appeal system is the safety net for writers who receive an unfair evaluation. The backend must reliably record every dispute and update the audit log without losing records or failing silently.

---

## 5.

100% of requests with missing text, empty strings, whitespace-only text, or missing creator_id return an HTTP 400 Bad Request with an explanatory JSON error message, and the server process continues running without crashing.

**Why this target:**
Public-facing endpoints must handle bad or malformed client payloads gracefully. Rejecting invalid requests cleanly prevents downstream exceptions and protects the service from crashing.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
