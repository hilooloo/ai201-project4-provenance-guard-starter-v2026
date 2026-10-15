"""
Signal two: the style signal.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────

# Punctuation that varies between writers. Full stops are left out on purpose:
# nearly everyone uses them at the same rate.
_PUNCT = set(",;:—–-\"'“”‘’()")

# Where each measure stops counting as evidence (see style_signal).
_SPREAD_HUMAN = 8.0    # std dev of sentence length (words) at/above this = fully human-like
_TTR_AI, _TTR_HUMAN = 0.45, 0.85
_PUNCT_AI, _PUNCT_HUMAN = 0.01, 0.06

# How much each measure counts toward the final score. Sums to 1.
_WEIGHTS = {"spread": 0.5, "ttr": 0.25, "punct": 0.25}


def sentence_length_spread(text: str) -> float:
    """
    Standard deviation of sentence lengths, in words.

    Scale: 0 upward, unbounded. HIGHER means more human (bursty); low means
    sentences march in step. Fewer than two sentences has no spread, so it
    returns 0.0 — style_signal checks the sentence count itself so that
    "no data" isn't mistaken for "perfectly uniform".
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    return statistics.stdev(lengths)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, lowercased.

    Scale: 0 to 1. HIGHER means more varied vocabulary (more human). Falls as
    text gets longer, so only compare texts of similar length.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def punctuation_density(text: str) -> float:
    """
    Commas, semicolons, colons, dashes, quotes and brackets per character.

    Scale: 0 to 1 in principle, ~0.01–0.06 in practice. HIGHER means more
    varied punctuation use (more human).
    """
    if not text:
        return 0.0
    return sum(1 for ch in text if ch in _PUNCT) / len(text)


# ── Combining them ───────────────────────────────────────────────────────────

def _scale(value: float, low: float, high: float) -> float:
    """Map value onto 0–1 linearly, clamped: low -> 0, high -> 1."""
    if high == low:
        return 0.0
    return max(0.0, min(1.0, (value - low) / (high - low)))


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Each measure points toward "human" when high, so each is scaled to 0–1 and
    flipped (1 - x) to point toward AI, then the three are averaged with
    _WEIGHTS. Sentence spread carries the most weight because uniform rhythm
    is the clearest AI tell; vocabulary and punctuation are weaker hints.

    Edge cases: empty text returns 0.5 (no evidence either way). With fewer
    than two sentences there is no spread to measure, so that component is
    neutral (0.5) rather than "perfectly uniform".
    """
    if not words(text):
        return 0.5

    n_sentences = len([s for s in sentences(text) if words(s)])
    if n_sentences < 2:
        spread_ai = 0.5
    else:
        spread_ai = 1.0 - _scale(sentence_length_spread(text), 0.0, _SPREAD_HUMAN)

    ttr_ai = 1.0 - _scale(type_token_ratio(text), _TTR_AI, _TTR_HUMAN)
    punct_ai = 1.0 - _scale(punctuation_density(text), _PUNCT_AI, _PUNCT_HUMAN)

    score = (
        _WEIGHTS["spread"] * spread_ai
        + _WEIGHTS["ttr"] * ttr_ai
        + _WEIGHTS["punct"] * punct_ai
    )
    return round(max(0.0, min(1.0, score)), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text):.4f}   (higher = more human)")
    print(f"type_token_ratio         {type_token_ratio(text):.4f}   (higher = more human)")
    print(f"punctuation_density      {punctuation_density(text):.4f}   (higher = more human)")
    print(f"style_score              {style_signal(text):.4f}   (higher = more likely AI)")
