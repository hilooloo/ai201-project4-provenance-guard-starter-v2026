"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 score. ← TODO (Milestone 4)

    Both inputs point the same way: higher means more likely AI. Your output
    should too.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    ⚠️ **Write the rule down before you code it, and put the numbers in your
    README.** A weighted average is the obvious choice and it is not the only
    one. Things worth thinking about:

      - **What happens when they disagree?** One signal at 0.9 and the other at
        0.1 averages to 0.5 — "unsure". Is that what you want? It might be
        exactly right: two methods disagreeing IS uncertainty. Or you might
        decide one signal is more trustworthy when they split.

      - **Which way do you want to be wrong?** Weighting toward the signal that
        reads more human means fewer false accusations and more AI text
        getting through. There's no weighting that avoids the trade.

      - Milestone 4 asks you to find a case where your two signals split and
        write it down. That case is what this rule exists to handle.

    The weights in config.py are placeholders. Change them, or ignore them and
    write a different rule.
    """
    combined_score = (
        model_score * config.MODEL_WEIGHT + style_score * config.STYLE_WEIGHT
    )
    return round(max(0.0, min(1.0, combined_score)), 4)


def score_to_label(score: float) -> str:
    """
    Turn a combined score into the text a reader actually sees.

    Bands (thresholds and wording live in config.py):
        score <= HUMAN_THRESHOLD   high-confidence human
        score <= AI_THRESHOLD      unsure
        otherwise                  high-confidence AI

    The label text is written for someone who has never heard the word
    "threshold", and the "unsure" one admits the tool's limits without
    accusing the writer.
    """
    if score <= config.HUMAN_THRESHOLD:
        return config.LABEL_HUMAN
    elif score <= config.AI_THRESHOLD:
        return config.LABEL_UNSURE
    else:
        return config.LABEL_AI


def label_ranges() -> dict:
    """
    The score range each label covers, as [low, high]. Built from config.py so
    the numbers can't drift apart from the thresholds.
    """
    return {
        "high-confidence human": [0.0, config.HUMAN_THRESHOLD],
        "unsure": [config.HUMAN_THRESHOLD, config.AI_THRESHOLD],
        "high-confidence AI": [config.AI_THRESHOLD, 1.0],
    }
