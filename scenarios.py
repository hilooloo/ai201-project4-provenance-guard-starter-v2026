"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# Texts are grouped so criteria 2 and 3 can reuse the same kinds of writing.
# Each is several sentences long: the detector refuses text that is too short.

HUMAN_PERSONAL = [
    "My grandmother kept her recipes on index cards, and half of them were stained past reading. I found the one for plum cake last week, soaked in butter, with \"too much sugar??\" scrawled in the margin in her blue pen. I made it anyway. It came out lopsided, and the kitchen smelled exactly like her house in August.",
    "I missed the last bus by about ten seconds. The driver looked right at me in his mirror and kept going, which I still think about. So I walked, forty minutes in the drizzle, rehearsing what I'd say to my sister. By the time I got there I'd forgotten all of it and just laughed.",
    "The dog hates the vacuum, the doorbell, and Tuesdays. Nobody knows why Tuesdays. He sits by the window from about four o'clock, ears up, like he's waiting for a verdict. Today he fell asleep halfway through and snored on the rug until dinner.",
    "Dad taught me to drive in an empty church parking lot, one stalled engine at a time. He never raised his voice; he just gripped the door handle a little harder each time. I passed on the second try. He still tells people it was the first.",
    "I can't tell you why I kept the ticket stub. The concert was loud, my feet hurt, and I lost my jacket somewhere near the merch table. But it's pinned above my desk now, curling at the corners. Some nights are just worth pinning.",
    "It rained the whole week we moved. Boxes went soft, the couch wouldn't fit through the door, and Marco cried over a broken lamp that wasn't even good. We ate cold noodles on the floor that night, laughing at nothing. Best dinner I've had in that apartment.",
    "Writing my first story felt like talking in an empty room. I'd type a line, hate it, delete it, type the same line again. Then one afternoon a sentence just showed up, whole, and the rest followed like it had been waiting. I don't know where it came from, and I'm afraid to ask.",
    "The market opens before dawn, and the old man at the corner stall already has his radio going. He sells peaches, mostly, bruised ones cheaper. Last summer he slipped an extra one into my bag and winked. I've bought from nobody else since.",
    "My brother and I haven't spoken in a year over something so small I can't even say it out loud. I drafted a message three times tonight. Deleted it twice. The third one is still sitting there, unsent, with the cursor blinking at me like it knows.",
    "I learned to swim at thirty-one, which is embarrassing and also true. The instructor was nineteen and endlessly patient. The first time I floated on my own, I swallowed half the pool and grinned like an idiot. I still go every Thursday.",
]

AI_FORMAL = [
    "Artificial intelligence has transformed numerous industries in recent years. It enables organizations to analyze large volumes of data efficiently and accurately. Furthermore, it provides valuable insights that support informed decision-making. As a result, businesses can improve productivity and enhance customer satisfaction.",
    "Effective communication is essential for success in any professional environment. It fosters collaboration, builds trust, and ensures that objectives are clearly understood. Moreover, strong communication skills contribute to improved team performance. In conclusion, organizations should prioritize communication training for all employees.",
    "Climate change represents one of the most significant challenges facing humanity today. Rising temperatures contribute to extreme weather events and loss of biodiversity. Additionally, it affects food security and economic stability worldwide. Therefore, it is crucial for governments and individuals to take coordinated action.",
    "Regular exercise offers numerous benefits for both physical and mental health. It helps maintain a healthy weight, strengthens the cardiovascular system, and reduces stress. Furthermore, it improves sleep quality and boosts overall energy levels. Consequently, individuals are encouraged to incorporate physical activity into their daily routines.",
    "Time management is a critical skill that enables individuals to achieve their goals efficiently. By prioritizing tasks and setting realistic deadlines, people can reduce stress and increase productivity. Additionally, effective planning allows for a better work-life balance. Overall, mastering time management leads to long-term personal and professional success.",
]

BORDERLINE = [
    "The meeting ran long, mostly because nobody wanted to be the one to say the plan wasn't working. We went through the numbers twice. By the end, a few of us agreed to revisit it next month. It was productive, in a way.",
    "Moving to a new city comes with a lot of adjustments. You learn the neighborhoods, find a favorite coffee shop, and slowly build a routine. I still get lost sometimes, but it's starting to feel like home. That counts for something.",
    "Our team shipped the update on Friday after a few late nights. The new feature works well and users seem to like it so far. There are still some bugs to fix, but overall it went smoothly. We plan to review the feedback next week.",
    "I think learning a second language is mostly about showing up every day. You make a lot of mistakes and feel silly. But after a while the words start to stick, and you notice you're understanding more than you expected. It's worth the effort.",
    "The restaurant was fine. The service was friendly, the portions were generous, and the prices were fair. Nothing stood out, but nothing went wrong either. We'd probably go back if we were in the area.",
]

SCENARIOS = [
    # Criterion 1: at most 1 of 10 human pieces labelled high-confidence AI.
    {
        "name": "false positives on human writing",
        "criterion": 1,
        "texts": HUMAN_PERSONAL,
    },
    # Criterion 2: average score of 5 AI pieces minus 5 human pieces >= 0.35.
    {
        "name": "score separation: human",
        "criterion": 2,
        "texts": HUMAN_PERSONAL[:5],
    },
    {
        "name": "score separation: raw AI",
        "criterion": 2,
        "texts": AI_FORMAL,
    },
    # Criterion 3: across 15 texts, each of the three labels at least twice.
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": HUMAN_PERSONAL[5:] + BORDERLINE + AI_FORMAL,
    },
    # Criterion 5: bad input gets HTTP 400 and the server keeps running.
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": "   \n\t  ", "creator_id": "eval_bad_whitespace"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "This text has no creator."},        # no creator_id
        ],
    },

    # Criterion 4 (the appeal path) can't be tested by sending text alone: it
    # needs a submission first, then an appeal against the content_id that came
    # back. It is tested by hand with curl, not by run_eval.py.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
