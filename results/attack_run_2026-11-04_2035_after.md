# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 20:35
- Auto-marked BROKE (5xx, crash, no response): **2**
- Left for you to judge: **54**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

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

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 2 | 18 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "cnt_26f20fd1",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3261,
  "model_score": 0.1635,
  "style_score": 0.628,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "cnt_d2aca4f9",
  "creator_id": "attacker_EV02",
  "guess": "ai",
  "confidence": 0.5244,
  "model_score": 0.5943,
  "style_score": 0.3946,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "cnt_83a7d382",
  "creator_id": "attacker_EV03",
  "guess": "ai",
  "confidence": 0.6015,
  "model_score": 0.6662,
  "style_score": 0.4814,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "cnt_578550a8",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6131,
  "model_score": 0.6114,
  "style_score": 0.6164,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "cnt_15bbcf30",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.307,
  "model_score": 0.3212,
  "style_score": 0.2806,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "cnt_1c1336d8",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.4816,
  "model_score": 0.5727,
  "style_score": 0.3125,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "cnt_20adcfbe",
  "creator_id": "attacker_EV07",
  "guess": "ai",
  "confidence": 0.5389,
  "model_score": 0.5862,
  "style_score": 0.4511,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "cnt_a890b648",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3909,
  "model_score": 0.2452,
  "style_score": 0.6616,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "cnt_1b0532cc",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.5906,
  "model_score": 0.7042,
  "style_score": 0.3795,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "cnt_f54a5019",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8184,
  "model_score": 0.9792,
  "style_score": 0.5199,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "cnt_e040800b",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.5659,
  "model_score": 0.6175,
  "style_score": 0.4701,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "cnt_85034f7c",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7161,
  "model_score": 0.7387,
  "style_score": 0.6741,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "cnt_808b195c",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7285,
  "model_score": 0.8051,
  "style_score": 0.5862,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "cnt_a27b6424",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7447,
  "model_score": 0.8329,
  "style_score": 0.5809,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "cnt_c14a1550",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7801,
  "model_score": 0.8005,
  "style_score": 0.7421,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "cnt_bad227e6",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7396,
  "model_score": 0.8814,
  "style_score": 0.4762,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "cnt_59d9d1fb",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7866,
  "model_score": 0.8816,
  "style_score": 0.6102,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "cnt_c8c52860",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.4467,
  "model_score": 0.3223,
  "style_score": 0.6778,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "cnt_cb66ffaf",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.4544,
  "model_score": 0.4625,
  "style_score": 0.4394,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "cnt_66d37c39",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2884,
  "model_score": 0.2044,
  "style_score": 0.4445,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "cnt_f5245013",
  "creator_id": "attacker_PI03",
  "guess": "ai",
  "confidence": 0.5456,
  "model_score": 0.5943,
  "style_score": 0.4552,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "cnt_d2a55133",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.4561,
  "model_score": 0.4998,
  "style_score": 0.3748,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "cnt_d19a265c",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.4364,
  "model_score": 0.6401,
  "style_score": 0.0581,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "cnt_b8b2a32c",
  "creator_id": "attacker_PI06",
  "guess": "ai",
  "confidence": 0.5341,
  "model_score": 0.5583,
  "style_score": 0.4892,
  "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
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
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "cnt_8171c8dc",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.175,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "cnt_b2b4db1a",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.1823,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "cnt_09b8c74d",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8234,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "cnt_0e1d3462",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.823,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "cnt_43824d87",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7642,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "cnt_827fe3cc",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8713,
  "model_score": 0.9876,
  "style_score": 0.6554,
  "label": "This piece displays uniform rhythm and predictable patterns commonly produced by automated language models.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "cnt_5a048b55",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.207,
  "model_score": 0.0492,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "cnt_b7d19265",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "cnt_08962f89",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "cnt_7da5b3fb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "cnt_e6c75df5",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "cnt_af900c7a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "cnt_ea52ec32",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "cnt_089fe0f0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "cnt_1be01bf3",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "cnt_b1e2d639",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "cnt_3d67a9fa",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1937,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
