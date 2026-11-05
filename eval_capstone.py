#!/usr/bin/env python3
"""
Capstone evaluation: Provenance Guard, Shape B (harden against failure).

Runs the five capstone acceptance criteria three times each, in-process, with
Flask's test client, and prints the Run Log table.

    python eval_capstone.py

It writes to the REAL audit log (logs/audit.jsonl) on purpose, because
criterion 3 checks that log. Raw responses and the log entries for trial 1 are
saved to results/capstone_run_eval.md.

Two details keep the trials honest:
  * The model is loaded once before the trials (a warm-up call that writes no
    log entry), so criterion 5 measures error handling, not model loading.
  * Every request gets its own creator_id, and requests with a non-object body
    (which the rate limiter keys by IP address) get their own REMOTE_ADDR, so
    the rate limiter never turns a result into a 429.
"""

import json
import time

import app as service
import audit
import config
import detector

TRIALS = 3

NON_DICT_BODIES = [[1, 2], [], "hi", 42, [True]]
SHORT_TEXTS = ["a", "x", ".", "1", "?"]
VALID_TEXTS = [
    "I walked along the quiet country road this morning, listening to the birds in the maple trees.",
    "My grandmother kept her recipes on index cards, and half of them were stained past reading. I made the plum cake anyway.",
    "The dog hates the vacuum, the doorbell, and Tuesdays. Nobody knows why Tuesdays. He sits by the window from four o'clock, waiting.",
    "Dad taught me to drive in an empty church parking lot, one stalled engine at a time. He never raised his voice. I passed on the second try.",
    "It rained the whole week we moved. Boxes went soft, the couch wouldn't fit through the door, and we ate cold noodles on the floor that night.",
]
REQUIRED_FIELDS = ("model_score", "style_score", "combined_score", "label")
LATENCY_LIMIT_MS = 50.0


def count_log() -> int:
    return len(audit.read_entries())


def post_json(client, path, body, addr):
    """POST a body exactly as JSON. Returns (status, parsed_json, milliseconds)."""
    start = time.perf_counter()
    resp = client.post(
        path,
        data=json.dumps(body),
        content_type="application/json",
        environ_overrides={"REMOTE_ADDR": addr},
    )
    ms = (time.perf_counter() - start) * 1000
    return resp.status_code, resp.get_json(silent=True), ms


def run_trial(client, trial: int) -> dict:
    """Run all five criteria once. Returns results plus the raw evidence."""
    ev = {}
    tag = f"cap{trial}"
    log_start = count_log()

    # 1. Non-object JSON bodies get a 400 from both routes.
    rows, ok = [], 0
    for i, body in enumerate(NON_DICT_BODIES):
        addr = f"10.{trial}.1.{i + 1}"
        s_status, s_json, _ = post_json(client, "/submit", body, addr)
        a_status, a_json, _ = post_json(client, "/appeal", body, addr)
        both = s_status == 400 and a_status == 400
        ok += both
        rows.append({
            "body_sent": body,
            "submit": {"status": s_status, "response": s_json},
            "appeal": {"status": a_status, "response": a_json},
            "passed": both,
        })
    ev["c1"] = {"passed": ok, "total": len(NON_DICT_BODIES), "rows": rows}

    # 2. Single-character text gets a 400, not a crash.
    rows, ok = [], 0
    for i, text in enumerate(SHORT_TEXTS):
        body = {"text": text, "creator_id": f"{tag}_short_{i}"}
        status, js, _ = post_json(client, "/submit", body, f"10.{trial}.2.{i + 1}")
        ok += status == 400
        rows.append({"body_sent": body, "status": status, "response": js,
                     "passed": status == 400})
    ev["c2"] = {"passed": ok, "total": len(SHORT_TEXTS), "rows": rows}

    # 3. Those 10 rejected submissions are in the audit log. Criteria 1 and 2
    #    sent 5 non-object bodies and 5 short texts to /submit, which are the
    #    rejections /submit logs. (/appeal does not write a rejection entry.)
    new = audit.read_entries()[log_start:]
    wanted = [e for e in new if e.get("event") == "rejected"
              and e.get("reason") in ("malformed_payload_not_json_object", "text_too_short")]
    n_bad = sum(e["reason"] == "malformed_payload_not_json_object" for e in wanted)
    n_short = sum(e["reason"] == "text_too_short" for e in wanted)
    # 5 of each expected; count how many of the 10 expected entries exist.
    found = min(n_bad, len(NON_DICT_BODIES)) + min(n_short, len(SHORT_TEXTS))
    ev["c3"] = {"passed": found, "total": 10, "malformed_logged": n_bad,
                "too_short_logged": n_short, "entries": wanted}

    # 4. Legitimate submissions still get a full evaluation.
    rows, ok = [], 0
    for i, text in enumerate(VALID_TEXTS):
        body = {"text": text, "creator_id": f"{tag}_valid_{i}"}
        status, js, _ = post_json(client, "/submit", body, f"10.{trial}.4.{i + 1}")
        good = status == 200 and isinstance(js, dict) and all(
            js.get(f) is not None for f in REQUIRED_FIELDS)
        ok += good
        rows.append({"body_sent": {"text": text[:60] + "...", "creator_id": body["creator_id"]},
                     "status": status, "response": js, "passed": good})
    ev["c4"] = {"passed": ok, "total": len(VALID_TEXTS), "rows": rows}

    # 5. Error handling stays fast: 10 error requests, at least 9 under 50 ms.
    rows, fast = [], 0
    errors = (
        [("non-object body", body, None) for body in NON_DICT_BODIES]
        + [("single character", {"text": t, "creator_id": f"{tag}_lat_{i}"}, None)
           for i, t in enumerate(SHORT_TEXTS)]
    )
    for i, (kind, body, _) in enumerate(errors):
        status, js, ms = post_json(client, "/submit", body, f"10.{trial}.5.{i + 1}")
        under = ms < LATENCY_LIMIT_MS
        fast += under
        rows.append({"kind": kind, "body_sent": body, "status": status,
                     "milliseconds": round(ms, 2), "under_50ms": under, "response": js})
    ev["c5"] = {"passed": fast, "total": len(errors),
                "max_ms": max(r["milliseconds"] for r in rows), "rows": rows}

    ev["log_entries_added"] = audit.read_entries()[log_start:]
    return ev


TARGETS = [
    ("1. Non-object JSON body returns 400 (/submit and /appeal)", "5 of 5", "c1", 5),
    ("2. Single-character text returns 400, no crash", "5 of 5", "c2", 5),
    ("3. Rejected requests are in the audit log", "10 of 10", "c3", 10),
    ("4. Legitimate submissions still get a full evaluation", "5 of 5", "c4", 5),
    ("5. Error handling under 50 ms", "at least 9 of 10", "c5", 9),
]


def cell(ev, key):
    r = ev[key]
    text = f"{r['passed']}/{r['total']}"
    if key == "c5":
        text += f" (max {r['max_ms']:.1f} ms)"
    return text


def table(trials):
    lines = ["| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
             "|---|---|---|---|---|---|"]
    for name, target, key, need in TARGETS:
        verdict = "MET" if all(t[key]["passed"] >= need for t in trials) else "MISSED"
        cells = " | ".join(cell(t, key) for t in trials)
        lines.append(f"| {name} | {target} | {cells} | {verdict} |")
    return "\n".join(lines)


def write_report(trial_one, tbl, stamp):
    out = config.RESULTS_DIR / "capstone_run_eval.md"
    config.RESULTS_DIR.mkdir(exist_ok=True)

    def block(obj):
        return "```json\n" + json.dumps(obj, indent=2, ensure_ascii=False) + "\n```\n"

    parts = [
        "# Capstone run: Trial 1 raw output\n",
        f"- Produced by: `eval_capstone.py` · {stamp}\n"
        "- Service: `app.py::submit` and `app.py::appeal`, called through Flask's test client\n"
        f"- {TRIALS} trials ran; this file holds the raw responses and log entries for trial 1\n",
        "## Run log\n", tbl + "\n",
        "## Criterion 1: non-object JSON body returns 400\n", block(trial_one["c1"]["rows"]),
        "## Criterion 2: single-character text returns 400\n", block(trial_one["c2"]["rows"]),
        "## Criterion 3: rejections recorded in logs/audit.jsonl\n",
        f"Malformed-body rejections logged: {trial_one['c3']['malformed_logged']}. "
        f"Too-short rejections logged: {trial_one['c3']['too_short_logged']}.\n",
        block(trial_one["c3"]["entries"]),
        "## Criterion 4: legitimate submissions\n", block(trial_one["c4"]["rows"]),
        "## Criterion 5: error latency\n", block(trial_one["c5"]["rows"]),
        "## Every audit log entry written during trial 1\n", block(trial_one["log_entries_added"]),
    ]
    out.write_text("\n".join(parts), encoding="utf-8")
    return out


def main():
    if not config.RATE_LIMITING_ENABLED:
        print("note: rate limiting is off; trials still run.")

    # Load the model once, outside the timed trials. No request, no log entry.
    start = time.perf_counter()
    detector.model_signal("Warm up the model with two short sentences. That is all it takes.")
    print(f"model warm-up (not timed in trials): {time.perf_counter() - start:.2f} s\n")

    client = service.app.test_client()
    trials = []
    for n in range(1, TRIALS + 1):
        trials.append(run_trial(client, n))
        print(f"trial {n} done")

    tbl = table(trials)
    print("\n" + tbl)

    stamp = time.strftime("%Y-%m-%d %H:%M")
    path = write_report(trials[0], tbl, stamp)
    print(f"\nraw output for trial 1: {path}")


if __name__ == "__main__":
    main()
