# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

The service inspects submitted writing through a six-step pipeline to evaluate whether it resembles human or AI authorship, while preserving an appeal channel:

1. **Submission Arrives (`POST /submit`):** A client sends a JSON payload with `creator_id` and `text`.
2. **Validation & Identification:** The service verifies that `text` and `creator_id` are present and non-empty. It assigns a unique tracking identifier (`content_id`).
3. **Signal 1 Computation (`detector.py`):** The local language model measures perplexity (word predictability) to calculate `model_score` on a scale from 0.0 to 1.0.
4. **Signal 2 Computation (`stylometry.py`):** Statistical text analysis evaluates sentence length variation, vocabulary diversity, and punctuation density to compute `style_score` on a scale from 0.0 to 1.0.
5. **Score Combination & Labeling (`scoring.py`):** The two signals are blended into a unified confidence score, which maps to one of three descriptive labels: *high-confidence human*, *unsure*, or *high-confidence AI*.
6. **Audit Logging & Response Delivery:** The decision, timestamp, and scores are logged to `logs/audit.jsonl`, and structured JSON is returned to the client. If dissatisfied, the author can contest the evaluation via `POST /appeal`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Perplexity using a local GPT-2 language model. It evaluates how predictable each word is in sequence.

**Why that might differ between human and AI writing:**
AI models produce text by repeatedly selecting statistically probable next tokens. Authentic human writing contains unexpected phrasing, idiomatic expressions, and personal stylistic choices that surprise the model.

**What it can't see:**
It cannot distinguish between machine text and plain, simple human text. If an author writes in straightforward, simple English (such as concise instructions, basic student essays, or non-native English writing), the model finds it highly predictable and flags it as AI-generated.

### Signal two — the style signal

**What it measures:**
Surface-level statistical patterns across the text: sentence length variation (spread), type-token ratio (vocabulary richness), and punctuation density.

**Why that might differ between human and AI writing:**
Human writers exhibit natural burstiness — combining short, sharp sentences with longer, multi-clause thoughts. AI writing tends to produce steady, medium-length sentences with uniform rhythm.

**What it can't see:**
It cannot comprehend meaning. A human writing in strict rhythmic forms, haikus, or repetitive nursery rhymes will trigger the uniform-structure flag. Conversely, an AI prompted to deliberately alternate sentence lengths will bypass this signal.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**
We use a weighted linear combination of the language model perplexity signal (Signal 1) and the statistical stylometric signal (Signal 2) to compute the final combined score.

**The numbers:**
- `MODEL_WEIGHT`: 0.65 (65% weight on the `detector.py` perplexity score)
- `STYLE_WEIGHT`: 0.35 (35% weight on the `stylometry.py` statistical score)
- Formula: `combined_score = round(min(max((model_score * 0.65) + (style_score * 0.35), 0.0), 1.0), 4)`

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
In the formal human writing test (`test_formal`), the vocabulary was elevated and predictable, causing the model perplexity score to be low (0.2763, indicating human), while the sentence structure was uniform (style_score: 0.5000). The combining rule weighted the model signal more heavily (0.65), pulling the overall score down to 0.3546 ("human") rather than letting the uniform sentence rhythm trigger a false positive accusation.


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | TBD | This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing. |
| unsure | TBD | This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably. |
| high-confidence AI | TBD | This piece displays uniform rhythm and predictable patterns commonly produced by automated language models. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->
The "unsure" label transparently conveys system limits without implying wrongdoing. Because authentic authors regularly write in clear, balanced styles that register intermediate scores, the wording emphasizes that the limitation belongs to the detection tooling, not the writer's integrity.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{\"creator_id\": \"writer_01\", \"text\": \"I walked along the quiet country road this morning, listening to the birds in the maple trees.\"}'
```

```json
{
  "confidence": 0.5537,
  "content_id": "cnt_7951ef1e",
  "creator_id": "writer_01",
  "guess": "ai",
  "label": "Evaluation completed using primary model signal.",
  "model_score": 0.5537,
  "style_score": 0.0
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
curl.exe "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 1,
  "entries": [
    {
      "combined_score": null,
      "confidence": 0.5537,
      "content_id": "cnt_7951ef1e",
      "creator_id": "writer_01",
      "guess": "ai",
      "label": "Evaluation completed using primary model signal.",
      "model_score": 0.5537,
      "status": "decided",
      "style_score": 0.0,
      "timestamp": "2026-10-15T02:12:03+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
