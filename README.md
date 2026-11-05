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
| high-confidence human | 0.0000 - 0.4000 | This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing. |
| unsure | 0.4001 - 0.6200 | This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably. |
| high-confidence AI | 0.6201 - 1.0000 | This piece displays uniform rhythm and predictable patterns commonly produced by automated language models. |

These ranges match `HUMAN_THRESHOLD = 0.4000` and `AI_THRESHOLD = 0.6200` in `config.py`. The AI threshold was raised from 0.5300 in unit 8; see The Improvement.

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
curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{\"content_id\": \"cnt_fe3d854f\", \"reasoning\": \"I wrote this text myself for a technical presentation without using AI generators.\"}'
```

```json
{
  "content_id": "cnt_fe3d854f",
  "message": "Appeal recorded successfully. The evaluation is now under review.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
curl.exe "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.5478,
      "confidence": 0.5478,
      "content_id": "cnt_fe3d854f",
      "creator_id": "writer_ai",
      "guess": "ai",
      "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
      "model_score": 0.5735,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-10-15T02:34:32+00:00"
    },
    {
      "content_id": "cnt_fe3d854f",
      "creator_id": "writer_ai",
      "event": "appeal",
      "reasoning": "I wrote this text myself for a technical presentation without using AI generators.",
      "status": "under_review",
      "timestamp": "2026-10-15T02:36:04+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked Claude to implement the stylometric signal in `stylometry.py` measuring sentence length variance, type-token ratio, and punctuation density.
- *What came back:* Claude provided the complete functions and combined them into a single `style_score` between 0.0 and 1.0.
- *What I changed:* When testing with a single sentence, sentence length spread returned 0.0. I ensured the scoring rule and edge cases handled short inputs gracefully without unfairly penalizing normal human sentences.

**Moment 2**

- *What I asked for:* I asked Claude to implement the `POST /appeal` endpoint in `app.py` to verify `content_id` in `audit.jsonl` and update its status.
- *What came back:* Claude wrote the Flask route handling JSON payloads, checking existing entries via `audit.entries_for()`, calling `audit.log_appeal()`, and returning a 200 response.
- *What I changed:* I added explicit 400 validation checks to ensure both `content_id` and `reasoning` fields are provided and non-empty before querying the audit log.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
We selected 10 requests per minute to give legitimate human writers ample room to draft, test, and revise their work naturally without interruption. Meanwhile, it swiftly caps automated scripts from spamming the system or mapping out detection thresholds. The daily allowance of 200 requests accommodates heavy daily workflows while preventing bulk automated scraping and denial-of-service attempts.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->
Each `creator_id` is counted separately. If a request has no usable `creator_id`, it is counted by the caller's IP address instead (`rate_limit_key` in `app.py`).

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```text
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

5 of 15 requests were rate limited with HTTP 429 status codes. Every blocked request was logged to `audit.jsonl` with its timestamp and limiting rule to ensure full visibility.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Source: `results/attack_run_2026-11-04_1956.md` (`run_attacks.py::main`), 56 attacks. The script auto-marked the two HTTP 500 crashes (MF02, RQ07) as BROKE. The other Verdict cells are blank because they depend on my thresholds; the diagnoses below are where I judge them.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `cnt_cae8030f` | human | 0.326 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `cnt_a33cd491` | ai | 0.524 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `cnt_c7828894` | ai | 0.602 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `cnt_6715f26d` | ai | 0.613 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `cnt_05b2e0c1` | human | 0.307 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `cnt_e5f5db03` | human | 0.482 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `cnt_47b7682d` | ai | 0.539 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `cnt_ac88f17b` | human | 0.391 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `cnt_36e54cdb` | ai | 0.591 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `cnt_f53d5f97` | ai | 0.818 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `cnt_30a35561` | ai | 0.566 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `cnt_ca2398d5` | ai | 0.716 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `cnt_e5f0fed8` | ai | 0.729 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `cnt_1c01d184` | ai | 0.745 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `cnt_0bffbcfa` | ai | 0.780 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `cnt_96b82cbd` | ai | 0.740 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `cnt_6fccb3f2` | ai | 0.787 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `cnt_ed98f93d` | human | 0.447 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `cnt_c8981e1f` | human | 0.454 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `cnt_b076ceb4` | human | 0.288 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `cnt_7d95e22a` | ai | 0.546 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `cnt_8c737cb1` | human | 0.456 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `cnt_fd3ccac4` | human | 0.436 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `cnt_035a4e79` | ai | 0.534 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `cnt_9df11dbb` | human | 0.175 |  |
| MF04 | malformed | text is only punctuation | 200 | `cnt_92c9a110` | human | 0.182 |  |
| MF05 | malformed | text is a very long single word | 200 | `cnt_aa9aa309` | ai | 0.823 |  |
| MF06 | malformed | text is emoji only | 200 | `cnt_577cb702` | ai | 0.823 |  |
| MF07 | malformed | text is right-to-left script | 200 | `cnt_3a62d0ef` | ai | 0.764 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `cnt_272f072f` | ai | 0.871 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `cnt_c3c02b47` | human | 0.207 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_a1839a4c` | human | 0.194 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_f0af625f` | human | 0.194 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_4112286e` | human | 0.194 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_dead43e1` | human | 0.194 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_775de53f` | human | 0.194 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_c492bb64` | human | 0.194 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_6031958e` | human | 0.194 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_8e126f50` | human | 0.194 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_ff8f0e49` | human | 0.194 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_f600a51c` | human | 0.194 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

Covers: false positives (FP01, FP02), evasions that came back "human" (EV01, EV05, EV06, EV08), prompt injection (PI01, PI02), a crash (MF02) and a rate-limit rejection. Entries are from `logs/audit.jsonl`, except MF02: the 500 crashed before anything was logged, so that one is the attack run's own record. RQ07 crashed the same way and also left no log entry. The rate-limit entry is from the flood (`attacker_flood`) and does not carry a content_id.

```json
[
{
  "timestamp": "2026-11-05T00:56:14+00:00",
  "content_id": "cnt_30a35561",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "model_score": 0.6175,
  "style_score": 0.4701,
  "combined_score": 0.5659,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "status": "decided",
  "confidence": 0.5659
},
{
  "timestamp": "2026-11-05T00:56:14+00:00",
  "content_id": "cnt_ca2398d5",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "model_score": 0.7387,
  "style_score": 0.6741,
  "combined_score": 0.7161,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "status": "decided",
  "confidence": 0.7161
},
{
  "timestamp": "2026-11-05T00:56:10+00:00",
  "content_id": "cnt_cae8030f",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "model_score": 0.1635,
  "style_score": 0.628,
  "combined_score": 0.3261,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "status": "decided",
  "confidence": 0.3261
},
{
  "timestamp": "2026-11-05T00:56:12+00:00",
  "content_id": "cnt_05b2e0c1",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "model_score": 0.3212,
  "style_score": 0.2806,
  "combined_score": 0.307,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "status": "decided",
  "confidence": 0.307
},
{
  "timestamp": "2026-11-05T00:56:12+00:00",
  "content_id": "cnt_e5f5db03",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "model_score": 0.5727,
  "style_score": 0.3125,
  "combined_score": 0.4816,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "status": "decided",
  "confidence": 0.4816
},
{
  "timestamp": "2026-11-05T00:56:13+00:00",
  "content_id": "cnt_ac88f17b",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "model_score": 0.2452,
  "style_score": 0.6616,
  "combined_score": 0.3909,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "status": "decided",
  "confidence": 0.3909
},
{
  "timestamp": "2026-11-05T00:56:16+00:00",
  "content_id": "cnt_c8981e1f",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "model_score": 0.4625,
  "style_score": 0.4394,
  "combined_score": 0.4544,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "status": "decided",
  "confidence": 0.4544
},
{
  "timestamp": "2026-11-05T00:56:17+00:00",
  "content_id": "cnt_b076ceb4",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "model_score": 0.2044,
  "style_score": 0.4445,
  "combined_score": 0.2884,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "status": "decided",
  "confidence": 0.2884
},
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "ValueError: Text is too short to score — a few sentences at least. (HTTP 500, Werkzeug debugger page; nothing was written to logs/audit.jsonl)",
  "verdict": "BROKE"
},
{
  "timestamp": "2026-11-05T00:56:26+00:00",
  "creator_id": "attacker_flood",
  "event": "rejected",
  "status": "rejected",
  "reason": "rate_limited",
  "limit": "10 per 1 minute"
}
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP01 and FP02.** Authentic human writing was labelled "high-confidence AI". FP01 (plain, clear human writing) scored 0.5659 and FP02 (human writing in a formal register) scored 0.7161. Both were told: "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models."

That is the worst failure because an innocent author is accused with a confident label, and it is the outcome the service exists to avoid. One false accusation like this can destroy a writer's trust in the whole platform. An evasion bypass (EV01, EV05, EV06, EV08) only means some AI text got through, which a secondary review can still catch.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Source: `results/run_2026-11-04_2014_before.md`, produced by `run_eval.py::main` against `app.py::submit`, scored by `scoring.py::combine_signals`. Targets are from `criteria.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | at most 1 of 10 | 2/10 | 2/10 | 2/10 | MISSED |
| 2. Score separation, raw AI vs human | average difference of at least 0.35 | 0.3353 | 0.3353 | 0.3353 | MISSED |
| 3. Label coverage | each of the 3 labels at least 2 times in 15 | human 4, unsure 0, AI 11 | human 4, unsure 0, AI 11 | human 4, unsure 0, AI 11 | MISSED |
| 4. Appeal changes status in the audit log | 100% (5 of 5) | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input returns 400 without crashing | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criterion 4 was tested manually, not by `run_eval.py`. In each of 3 trials I sent 5 consecutive POST /submit requests, then a valid POST /appeal with 'reasoning' for each, so 15 appeals in total. In every trial 5/5 (100%) transitioned to 'under_review' in `logs/audit.jsonl`, which fulfils the manual evaluation required for the appeal path.

Criterion 2 is the mean `confidence` of the 5 raw AI texts (0.7758) minus the mean of the 5 human texts (0.4405). All three trials gave the same numbers.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Everything below is Trial 1, copied from `results/run_2026-11-04_2014_before.md`. `run_eval.py::main` sent each text to `POST /submit`, and `app.py::submit` produced these responses. `sent` is the first 70 characters of what was sent.

**Criterion 1 — false positives on human writing**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.301,
    "model_score": 0.3457,
    "style_score": 0.2179,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "My grandmother kept her recipes on index cards, and half of them were "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5965,
    "model_score": 0.6333,
    "style_score": 0.5283,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "I missed the last bus by about ten seconds. The driver looked right at"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4033,
    "model_score": 0.4393,
    "style_score": 0.3365,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "sent": "The dog hates the vacuum, the doorbell, and Tuesdays. Nobody knows why"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4911,
    "model_score": 0.5388,
    "style_score": 0.4025,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "sent": "Dad taught me to drive in an empty church parking lot, one stalled eng"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4106,
    "model_score": 0.4099,
    "style_score": 0.4119,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "sent": "I can't tell you why I kept the ticket stub. The concert was loud, my "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3462,
    "model_score": 0.3871,
    "style_score": 0.2702,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "It rained the whole week we moved. Boxes went soft, the couch wouldn't"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.562,
    "model_score": 0.6201,
    "style_score": 0.4542,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Writing my first story felt like talking in an empty room. I'd type a "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2772,
    "model_score": 0.2261,
    "style_score": 0.3722,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "The market opens before dawn, and the old man at the corner stall alre"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3703,
    "model_score": 0.4519,
    "style_score": 0.2187,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "My brother and I haven't spoken in a year over something so small I ca"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3628,
    "model_score": 0.3562,
    "style_score": 0.3751,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "I learned to swim at thirty-one, which is embarrassing and also true. "
  }
]
```

**Criterion 2 — score separation: human texts**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.301,
    "model_score": 0.3457,
    "style_score": 0.2179,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "My grandmother kept her recipes on index cards, and half of them were "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5965,
    "model_score": 0.6333,
    "style_score": 0.5283,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "I missed the last bus by about ten seconds. The driver looked right at"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4033,
    "model_score": 0.4393,
    "style_score": 0.3365,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "sent": "The dog hates the vacuum, the doorbell, and Tuesdays. Nobody knows why"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4911,
    "model_score": 0.5388,
    "style_score": 0.4025,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "sent": "Dad taught me to drive in an empty church parking lot, one stalled eng"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4106,
    "model_score": 0.4099,
    "style_score": 0.4119,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "sent": "I can't tell you why I kept the ticket stub. The concert was loud, my "
  }
]
```

**Criterion 2 — score separation: raw AI texts**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7723,
    "model_score": 0.8277,
    "style_score": 0.6693,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Artificial intelligence has transformed numerous industries in recent "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7253,
    "model_score": 0.759,
    "style_score": 0.6627,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Effective communication is essential for success in any professional e"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8038,
    "model_score": 0.8804,
    "style_score": 0.6616,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Climate change represents one of the most significant challenges facin"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8236,
    "model_score": 0.9107,
    "style_score": 0.6617,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Regular exercise offers numerous benefits for both physical and mental"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7538,
    "model_score": 0.8304,
    "style_score": 0.6116,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Time management is a critical skill that enables individuals to achiev"
  }
]
```

**Criterion 3 — label coverage**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3462,
    "model_score": 0.3871,
    "style_score": 0.2702,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "It rained the whole week we moved. Boxes went soft, the couch wouldn't"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.562,
    "model_score": 0.6201,
    "style_score": 0.4542,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Writing my first story felt like talking in an empty room. I'd type a "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2772,
    "model_score": 0.2261,
    "style_score": 0.3722,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "The market opens before dawn, and the old man at the corner stall alre"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3703,
    "model_score": 0.4519,
    "style_score": 0.2187,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "My brother and I haven't spoken in a year over something so small I ca"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3628,
    "model_score": 0.3562,
    "style_score": 0.3751,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "sent": "I learned to swim at thirty-one, which is embarrassing and also true. "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5721,
    "model_score": 0.6838,
    "style_score": 0.3646,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "The meeting ran long, mostly because nobody wanted to be the one to sa"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6373,
    "model_score": 0.7426,
    "style_score": 0.4416,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Moving to a new city comes with a lot of adjustments. You learn the ne"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.705,
    "model_score": 0.7554,
    "style_score": 0.6114,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Our team shipped the update on Friday after a few late nights. The new"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6281,
    "model_score": 0.7689,
    "style_score": 0.3665,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "I think learning a second language is mostly about showing up every da"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7405,
    "model_score": 0.8629,
    "style_score": 0.5132,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "The restaurant was fine. The service was friendly, the portions were g"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7723,
    "model_score": 0.8277,
    "style_score": 0.6693,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Artificial intelligence has transformed numerous industries in recent "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7253,
    "model_score": 0.759,
    "style_score": 0.6627,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Effective communication is essential for success in any professional e"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8038,
    "model_score": 0.8804,
    "style_score": 0.6616,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Climate change represents one of the most significant challenges facin"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8236,
    "model_score": 0.9107,
    "style_score": 0.6617,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Regular exercise offers numerous benefits for both physical and mental"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7538,
    "model_score": 0.8304,
    "style_score": 0.6116,
    "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
    "sent": "Time management is a critical skill that enables individuals to achiev"
  }
]
```

**Criterion 5 — bad input**

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "   \n\t  "
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": \"This text has no creator.\"}"
  }
]
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

**Broken attacks (HTTP 500)**

- **MF02 (text is a single character) — stage: signal one, uncaught in the route.** The route's check only rejects empty or whitespace-only text, so a one-character string passes it. `detector.py::perplexity` then raises `ValueError("Text is too short to score — a few sentences at least.")` because fewer than 3 tokens can't be scored, and `app.py::submit` has no `try/except` around `detector.model_signal`. The exception escapes as a 500 and nothing is written to `logs/audit.jsonl`. The stylometry signal is not the cause; it handles short text without raising. Fix: catch the `ValueError` in `submit` and return a 400 with an explanatory message (and log the rejection).
- **RQ07 (body is a JSON array) — stage: the route.** `request.get_json(silent=True) or {}` returns the list as is, because a non-empty list is truthy, so `payload.get("text")` raises `AttributeError: 'list' object has no attribute 'get'`. The rate limiter's key function already guards against non-dict bodies, so the crash is in the handler's own line in `app.py::submit`, not before it. `appeal()` has the same line and the same weakness. Fix: if the payload isn't a dict, return a 400 before reading any field.

**Missed criteria**

All three missed criteria trace back to the same cause: signal one (`model_score`) reads plain, predictable writing as AI, and it carries 65% of the combined score.

- **Criterion 1 (2/10 labelled AI, target at most 1) — stage: signal one, amplified by the combining rule.** The two flagged human texts were the missed-bus story (combined 0.5965; model 0.6333, style 0.5283) and the first-story text (combined 0.562; model 0.6201, style 0.4542). Both have a model score above 0.62, and `MODEL_WEIGHT = 0.65` carried them over the 0.53 threshold. For the second text, style (0.4542) was below the threshold on its own, so signal one alone pushed it into "high-confidence AI". These are not formal texts. They are ordinary, plain personal writing, which is the blind spot I named for signal one. All three trials gave identical results, so this is not noise.
- **Criterion 2 (separation 0.3353, target at least 0.35) — stage: signal two, plus one text on signal one.** The AI mean was 0.7758 and the human mean 0.4405. The combined difference is a weighted average of the two signals' differences: signal one separated the groups by about 0.37 (0.8416 vs 0.4734) and signal two by about 0.27 (0.6534 vs 0.3794). Stylometry separates less, so it pulls the combined gap below the model signal's 0.37, and no weighting can push the combined gap above signal one's own. The human mean was also lifted by the missed-bus text (0.5965).
- **Criterion 3 (0 "unsure" labels, target at least 2 each) — stage: signal one and the label mapping.** The 15 texts split into human 4 and AI 11, with 0 in the "unsure" band (0.4001–0.5300). All five borderline texts scored well above 0.53 (0.5721, 0.6373, 0.705, 0.6281, 0.7405), because plain writing gets a model score of 0.68–0.86 and so reads as AI. The band is reachable: three human texts from the criterion 1 set did land in "unsure" (0.4033, 0.4911, 0.4106). So the label can be produced, but this test set didn't land any text in the band. The band is also only 0.13 wide, and widening it up to 0.53 alone would not have captured these five.

---

## The Improvement

**What I changed:**

One change: `AI_THRESHOLD` in `config.py` (line 75), raised from `0.5300` to `0.6200`. This widens the "unsure" band from 0.4001–0.5300 to 0.4001–0.6200, so only scores above 0.62 get the "high-confidence AI" label. Nothing else changed: not the weights, not the signals, not the route validation.

**Which diagnosis pointed at it:**

Criteria 1 and 3. The two human texts wrongly called "high-confidence AI" scored 0.5965 and 0.562, and every borderline text sat just above the old 0.53 line, so "unsure" was never used. Both are threshold problems on the label mapping. I did not touch the two 500 crashes (MF02, RQ07): they are route bugs and a separate change.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Source: `results/attack_run_2026-11-04_2035_after.md` (`run_attacks.py::main`), 56 attacks. As before, only the two HTTP 500 crashes are auto-marked BROKE. The Guess column is the `guess` field (0.5 cut-off), so it doesn't change with the threshold; the label counts below do.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `cnt_26f20fd1` | human | 0.326 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `cnt_d2aca4f9` | ai | 0.524 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `cnt_83a7d382` | ai | 0.602 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `cnt_578550a8` | ai | 0.613 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `cnt_15bbcf30` | human | 0.307 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `cnt_1c1336d8` | human | 0.482 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `cnt_20adcfbe` | ai | 0.539 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `cnt_a890b648` | human | 0.391 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `cnt_1b0532cc` | ai | 0.591 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `cnt_f54a5019` | ai | 0.818 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `cnt_e040800b` | ai | 0.566 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `cnt_85034f7c` | ai | 0.716 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `cnt_808b195c` | ai | 0.729 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `cnt_a27b6424` | ai | 0.745 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `cnt_c14a1550` | ai | 0.780 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `cnt_bad227e6` | ai | 0.740 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `cnt_59d9d1fb` | ai | 0.787 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `cnt_c8c52860` | human | 0.447 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `cnt_cb66ffaf` | human | 0.454 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `cnt_66d37c39` | human | 0.288 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `cnt_f5245013` | ai | 0.546 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `cnt_d2a55133` | human | 0.456 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `cnt_d19a265c` | human | 0.436 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `cnt_b8b2a32c` | ai | 0.534 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `cnt_8171c8dc` | human | 0.175 |  |
| MF04 | malformed | text is only punctuation | 200 | `cnt_b2b4db1a` | human | 0.182 |  |
| MF05 | malformed | text is a very long single word | 200 | `cnt_09b8c74d` | ai | 0.823 |  |
| MF06 | malformed | text is emoji only | 200 | `cnt_0e1d3462` | ai | 0.823 |  |
| MF07 | malformed | text is right-to-left script | 200 | `cnt_43824d87` | ai | 0.764 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `cnt_827fe3cc` | ai | 0.871 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `cnt_5a048b55` | human | 0.207 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_b7d19265` | human | 0.194 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_08962f89` | human | 0.194 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_7da5b3fb` | human | 0.194 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_e6c75df5` | human | 0.194 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_af900c7a` | human | 0.194 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_ea52ec32` | human | 0.194 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_089fe0f0` | human | 0.194 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_1be01bf3` | human | 0.194 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_b1e2d639` | human | 0.194 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cnt_3d67a9fa` | human | 0.194 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

**Before vs after, by what the label said** (200 responses only; the 400s, 429s and 500s are identical)

| Family | Before | After |
|---|---|---|
| evasion (10) | AI 5, unsure 2, human 3 | AI 1, unsure 6, human 3 |
| false_positive (8) | AI 7, unsure 1 | AI 6, unsure 2 |
| prompt_injection (6) | AI 2, unsure 3, human 1 | AI 0, unsure 5, human 1 |
| malformed (20) | 400 ×11, 500 ×2, AI 4, human 3 | identical |
| flood_same_creator (12) | human 10, 429 ×2 | identical |

Seven attacks moved from "AI" to "unsure" and nothing moved the other way: EV03, EV04, EV07, EV09, FP01, PI03, PI06. Broken attacks stayed at 2 (MF02 and RQ07), as expected, because I deliberately left the route alone.

**Run log, before vs after** (three trials each; every trial in a set gave identical results)

| Criterion | Target | Before (Run 1 / 2 / 3) | After (Run 1 / 2 / 3) | Verdict before → after |
|---|---|---|---|---|
| 1. Own writing flagged as AI | at most 1 of 10 | 2/10, 2/10, 2/10 | 0/10, 0/10, 0/10 | MISSED → MET |
| 2. Score separation, raw AI vs human | at least 0.35 | 0.3353 ×3 | 0.3353 ×3 | MISSED → MISSED |
| 3. Label coverage | each label at least 2 of 15 | human 4, unsure 0, AI 11 ×3 | human 4, unsure 2, AI 9 ×3 | MISSED → MET |
| 4. Appeal changes status | 5 of 5 | 5/5 ×3 | not re-run | MET → unchanged (the threshold doesn't touch the appeal path) |
| 5. Bad input returns 400 | 5 of 5 | 5/5 ×3 | 5/5 ×3 | MET → MET |

Source: `results/run_2026-11-04_2035_after.md` (`run_eval.py::main`).

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

It helped on the two criteria it targeted and cost some AI sensitivity: it moved the false-positive count from 2/10 to 0/10 and put two texts in the "unsure" band, in exchange for 7 attack inputs that used to be labelled AI now reading as "unsure", which is the usual classifier trade of fewer false accusations for more missed detections.

- **What it fixed:** the two false positives in criterion 1 (0.5965 and 0.562) are now "unsure", and criterion 3 now has 2 texts in the unsure band, the exact minimum.
- **What it cost:** four evasion inputs (EV03 a pasted quotation, EV04 unusual words, EV07 punctuation padding, EV09 a human opening bolted on) and two prompt-injection inputs (PI03, PI06) that used to be called AI now come back "unsure". The formal AI texts in the eval all scored 0.7253 or higher and are still caught, so only AI text in the 0.53–0.62 range is affected.
- **What it did not fix:** only 1 of the 8 false-positive attacks (FP01) was rescued. FP02–FP07 scored 0.716–0.787 and are still called "high-confidence AI". Criterion 2 is unchanged at 0.3353, because it measures raw scores and a threshold doesn't change them. The two crashes remain.
- **Caveats:** I picked 0.62 after looking at these same test scores, so it is tuned to this set. Both passes are thin: the nearest false positive sits at 0.5965 (0.0235 under the line), and criterion 3 has exactly 2 unsure texts.


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
