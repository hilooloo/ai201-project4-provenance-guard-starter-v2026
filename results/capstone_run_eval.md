# Capstone run: Trial 1 raw output

- Produced by: `eval_capstone.py` · 2026-11-04 21:39
- Service: `app.py::submit` and `app.py::appeal`, called through Flask's test client
- 3 trials ran; this file holds the raw responses and log entries for trial 1

## Run log

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Non-object JSON body returns 400 (/submit and /appeal) | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Single-character text returns 400, no crash | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Rejected requests are in the audit log | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 4. Legitimate submissions still get a full evaluation | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Error handling under 50 ms | at least 9 of 10 | 10/10 (max 2.8 ms) | 10/10 (max 3.7 ms) | 10/10 (max 2.9 ms) | MET |

## Criterion 1: non-object JSON body returns 400

```json
[
  {
    "body_sent": [
      1,
      2
    ],
    "submit": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "appeal": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "passed": true
  },
  {
    "body_sent": [],
    "submit": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "appeal": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "passed": true
  },
  {
    "body_sent": "hi",
    "submit": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "appeal": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "passed": true
  },
  {
    "body_sent": 42,
    "submit": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "appeal": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "passed": true
  },
  {
    "body_sent": [
      true
    ],
    "submit": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "appeal": {
      "status": 400,
      "response": {
        "error": "invalid_input",
        "message": "Request body must be a valid JSON object."
      }
    },
    "passed": true
  }
]
```

## Criterion 2: single-character text returns 400

```json
[
  {
    "body_sent": {
      "text": "a",
      "creator_id": "cap1_short_0"
    },
    "status": 400,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    },
    "passed": true
  },
  {
    "body_sent": {
      "text": "x",
      "creator_id": "cap1_short_1"
    },
    "status": 400,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    },
    "passed": true
  },
  {
    "body_sent": {
      "text": ".",
      "creator_id": "cap1_short_2"
    },
    "status": 400,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    },
    "passed": true
  },
  {
    "body_sent": {
      "text": "1",
      "creator_id": "cap1_short_3"
    },
    "status": 400,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    },
    "passed": true
  },
  {
    "body_sent": {
      "text": "?",
      "creator_id": "cap1_short_4"
    },
    "status": 400,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    },
    "passed": true
  }
]
```

## Criterion 3: rejections recorded in logs/audit.jsonl

Malformed-body rejections logged: 5. Too-short rejections logged: 5.

```json
[
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_0",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_1",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_2",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_3",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_4",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  }
]
```

## Criterion 4: legitimate submissions

```json
[
  {
    "body_sent": {
      "text": "I walked along the quiet country road this morning, listenin...",
      "creator_id": "cap1_valid_0"
    },
    "status": 200,
    "response": {
      "combined_score": 0.5338,
      "confidence": 0.5338,
      "content_id": "cnt_54fd744d",
      "creator_id": "cap1_valid_0",
      "guess": "ai",
      "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
      "model_score": 0.5537,
      "style_score": 0.4968
    },
    "passed": true
  },
  {
    "body_sent": {
      "text": "My grandmother kept her recipes on index cards, and half of ...",
      "creator_id": "cap1_valid_1"
    },
    "status": 200,
    "response": {
      "combined_score": 0.1675,
      "confidence": 0.1675,
      "content_id": "cnt_229115f3",
      "creator_id": "cap1_valid_1",
      "guess": "human",
      "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
      "model_score": 0.0918,
      "style_score": 0.3081
    },
    "passed": true
  },
  {
    "body_sent": {
      "text": "The dog hates the vacuum, the doorbell, and Tuesdays. Nobody...",
      "creator_id": "cap1_valid_2"
    },
    "status": 200,
    "response": {
      "combined_score": 0.4259,
      "confidence": 0.4259,
      "content_id": "cnt_6e7c0180",
      "creator_id": "cap1_valid_2",
      "guess": "human",
      "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
      "model_score": 0.3937,
      "style_score": 0.4856
    },
    "passed": true
  },
  {
    "body_sent": {
      "text": "Dad taught me to drive in an empty church parking lot, one s...",
      "creator_id": "cap1_valid_3"
    },
    "status": 200,
    "response": {
      "combined_score": 0.424,
      "confidence": 0.424,
      "content_id": "cnt_25c7be8c",
      "creator_id": "cap1_valid_3",
      "guess": "human",
      "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
      "model_score": 0.4725,
      "style_score": 0.3339
    },
    "passed": true
  },
  {
    "body_sent": {
      "text": "It rained the whole week we moved. Boxes went soft, the couc...",
      "creator_id": "cap1_valid_4"
    },
    "status": 200,
    "response": {
      "combined_score": 0.3636,
      "confidence": 0.3636,
      "content_id": "cnt_f51ab988",
      "creator_id": "cap1_valid_4",
      "guess": "human",
      "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
      "model_score": 0.4551,
      "style_score": 0.1936
    },
    "passed": true
  }
]
```

## Criterion 5: error latency

```json
[
  {
    "kind": "non-object body",
    "body_sent": [
      1,
      2
    ],
    "status": 400,
    "milliseconds": 2.75,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Request body must be a valid JSON object."
    }
  },
  {
    "kind": "non-object body",
    "body_sent": [],
    "status": 400,
    "milliseconds": 2.23,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Request body must be a valid JSON object."
    }
  },
  {
    "kind": "non-object body",
    "body_sent": "hi",
    "status": 400,
    "milliseconds": 2.33,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Request body must be a valid JSON object."
    }
  },
  {
    "kind": "non-object body",
    "body_sent": 42,
    "status": 400,
    "milliseconds": 2.37,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Request body must be a valid JSON object."
    }
  },
  {
    "kind": "non-object body",
    "body_sent": [
      true
    ],
    "status": 400,
    "milliseconds": 2.18,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Request body must be a valid JSON object."
    }
  },
  {
    "kind": "single character",
    "body_sent": {
      "text": "a",
      "creator_id": "cap1_lat_0"
    },
    "status": 400,
    "milliseconds": 2.07,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    }
  },
  {
    "kind": "single character",
    "body_sent": {
      "text": "x",
      "creator_id": "cap1_lat_1"
    },
    "status": 400,
    "milliseconds": 2.08,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    }
  },
  {
    "kind": "single character",
    "body_sent": {
      "text": ".",
      "creator_id": "cap1_lat_2"
    },
    "status": 400,
    "milliseconds": 1.77,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    }
  },
  {
    "kind": "single character",
    "body_sent": {
      "text": "1",
      "creator_id": "cap1_lat_3"
    },
    "status": 400,
    "milliseconds": 1.83,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    }
  },
  {
    "kind": "single character",
    "body_sent": {
      "text": "?",
      "creator_id": "cap1_lat_4"
    },
    "status": 400,
    "milliseconds": 2.33,
    "under_50ms": true,
    "response": {
      "error": "invalid_input",
      "message": "Text is too short to score: please submit at least 10 characters (a few sentences works best)."
    }
  }
]
```

## Every audit log entry written during trial 1

```json
[
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_0",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_1",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_2",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_3",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "creator_id": "cap1_short_4",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:26+00:00",
    "content_id": "cnt_54fd744d",
    "creator_id": "cap1_valid_0",
    "guess": "ai",
    "model_score": 0.5537,
    "style_score": 0.4968,
    "combined_score": 0.5338,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "status": "decided",
    "confidence": 0.5338
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "content_id": "cnt_229115f3",
    "creator_id": "cap1_valid_1",
    "guess": "human",
    "model_score": 0.0918,
    "style_score": 0.3081,
    "combined_score": 0.1675,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "status": "decided",
    "confidence": 0.1675
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "content_id": "cnt_6e7c0180",
    "creator_id": "cap1_valid_2",
    "guess": "human",
    "model_score": 0.3937,
    "style_score": 0.4856,
    "combined_score": 0.4259,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "status": "decided",
    "confidence": 0.4259
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "content_id": "cnt_25c7be8c",
    "creator_id": "cap1_valid_3",
    "guess": "human",
    "model_score": 0.4725,
    "style_score": 0.3339,
    "combined_score": 0.424,
    "label": "This text presents mixed stylistic and structural signals, so its authorship cannot be determined reliably.",
    "status": "decided",
    "confidence": 0.424
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "content_id": "cnt_f51ab988",
    "creator_id": "cap1_valid_4",
    "guess": "human",
    "model_score": 0.4551,
    "style_score": 0.1936,
    "combined_score": 0.3636,
    "label": "This piece shows strong personal style and varied sentence rhythm consistent with authentic human writing.",
    "status": "decided",
    "confidence": 0.3636
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "malformed_payload_not_json_object",
    "limit": "body must be a JSON object"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "cap1_lat_0",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "cap1_lat_1",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "cap1_lat_2",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "cap1_lat_3",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  },
  {
    "timestamp": "2026-11-05T02:39:27+00:00",
    "creator_id": "cap1_lat_4",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_short",
    "limit": "text must be at least 10 characters"
  }
]
```
