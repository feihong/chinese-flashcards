# /// script
# requires-python = ">=3.13"
# dependencies = ["requests", "htpy", "html2text"]
# ///
"""
Generate a report summarizing the current state of Chinese flashcards, including:
- State the total number of Chinese notes
- List unique hanzi that appear on the front of notes
- List sloppily-reviewed cards in the past 7 days
- List new notes added since a specific day in the past
- List all notes currently in the Test deck
- TODO: Correctness percentage of mature cards
"""

from collections import defaultdict
from collections.abc import Iterable
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import NamedTuple

import html2text
import requests
from htpy import (
    body,
    details,
    h1,
    h2,
    head,
    html,
    li,
    meta,
    ol,
    p,
    style,
    summary,
    table,
    td,
    title,
    tr,
    ul,
)
from htpy import (
    input as input_,
)

output_file = Path(__file__).parent / "index.html"


STYLE = """
body { margin: 1em; }
table { border-collapse: collapse; }
th, td { border: 1px solid #777; padding: 1em; }
"""


class UniqueCharsResult(NamedTuple):
    notes_count: int
    unique_hanzi: Iterable[str]


class SloppyReviewCard(NamedTuple):
    card_id: str
    question: str
    answered_at: datetime


class SloppyReviewResult(NamedTuple):
    shortest_duration: int
    cards: list[SloppyReviewCard]


def main():
    unique_chars = get_unique_chars()
    reviews = get_reviews()
    sloppy_reviews = get_sloppy_reviews(reviews)
    mature_correctness = None  # get_mature_correctness(reviews)
    new_notes = get_new_notes()
    test_notes = get_test_notes()

    generate_report(
        unique_chars, sloppy_reviews, mature_correctness, new_notes, test_notes
    )


def invoke(method, **params):
    data = {"method": method, "jsonrpc": "2.0", "id": 1, "params": params}
    return_value = {}

    def transform_result(result):
        match method:
            case "cards.render":
                return result
            case "notes.search" | "cards.search":
                return result["ids"]
            case "notes.getMany" | "cards.getMany":
                return [item["result"] for item in result["items"]]
            case "reviews.list":
                return result["items"]
            case _:
                raise LookupError(f"Unknown API method {method}")

    def gen():
        while True:
            r = requests.post("http://127.0.0.1:8765/api/v1", json=data)
            reply = r.json()
            if "error" in reply:
                raise RuntimeError(reply["error"])

            result = r.json()["result"]
            real_result = transform_result(result)
            if isinstance(real_result, list):
                yield from real_result
            else:
                return_value["value"] = real_result
                return
            if (cursor := result.get("nextCursor")) is None:
                break
            else:
                data["params"]["cursor"] = cursor

    loop_result = list(gen())
    if return_value:
        return return_value["value"]
    else:
        return loop_result


def get_unique_chars() -> UniqueCharsResult:
    note_ids = invoke("notes.search", query="note:Chinese", limit=1000)
    print(f"Found {len(note_ids)} Chinese notes")
    notes = invoke("notes.getMany", ids=note_ids)

    def gen():
        for note in notes:
            for c in note["fields"]["Front"]:
                if ord(c) > 255:
                    yield c

    return UniqueCharsResult(notes_count=len(note_ids), unique_hanzi=sorted(set(gen())))


def get_reviews() -> list[dict]:
    """
    Get reviews from past 7 days. Change 'answeredAt' value from string to datetime.
    """
    card_ids = invoke("cards.search", query="rated:7", limit=1000)
    print(f"Found {len(card_ids)} cards studied within the past 7 days")

    def gen():
        reviews = invoke("reviews.list", cardIds=card_ids)

        now = datetime.now().astimezone()
        for review in reviews:
            dt = datetime.fromisoformat(review["answeredAt"]).astimezone()
            delta = now - dt
            if delta.days <= 7:
                review["answeredAt"] = dt
                yield review

    reviews = list(gen())
    print(f"Found {len(reviews)} reviews")
    return list(gen())


def get_sloppy_reviews(reviews) -> SloppyReviewResult:
    """
    Return all cards that were reviewed within the past 7 days and which were seen for less than 500 ms
    """
    card_times = {}  # map card ID to when it was reviewed
    shortest_duration = None

    for review in reviews:
        elapsed = review["elapsedMs"]
        if elapsed < 500:
            card_times[review["cardId"]] = review["answeredAt"]
            shortest_duration = (
                min(elapsed, shortest_duration)
                if shortest_duration is not None
                else elapsed
            )

    cards = invoke("cards.getMany", ids=list(card_times.keys()))

    def get_question(card):
        render = invoke("cards.render", id=card["id"])
        return html2text.html2text(render["questionHtml"])

    cards = [
        SloppyReviewCard(
            card_id=c["id"], question=get_question(c), answered_at=card_times[c["id"]]
        )
        for c in cards
    ]
    return SloppyReviewResult(shortest_duration=shortest_duration, cards=cards)


def get_mature_card_items(card_map, cards_map) -> Iterable[(str, bool)]:
    for card_id, correct in card_map.items():
        card = cards_map[card_id]
        front = card["fields"]["Front"]
        question = html2text.html2text(card["question"])
        yield f"{front} | {question}", correct


def get_mature_correctness(reviews) -> Iterable:
    """
    Get the correctness percentage of mature cards (cards whose interval is greater than or equal to 21 days)
    """
    cut_off = date.today() - timedelta(days=7)
    date_map = defaultdict(dict)
    card_ids = set()

    for card_id, reviews in reviews_map.items():
        for review in reviews:
            date_ = (datetime.fromtimestamp(review["id"] / 1000)).date()
            if review["lastIvl"] >= 21 and date_ >= cut_off:
                card_id = int(card_id)
                card_ids.add(card_id)
                date_map[date_][card_id] = review["lastIvl"] < review["ivl"]

    cards = invoke("cards.getMany", ids=list(card_ids))
    cards_map = {c["cardId"]: c for c in cards}

    def gen():
        date_lst = sorted(date_map.items(), key=lambda p: p[0])
        for date, card_map in date_lst:
            yield date, list(get_mature_card_items(card_map, cards_map))

    return gen()


def get_new_notes() -> list[dict]:
    note_ids = invoke(
        "notes.search",
        query="-deck:Test added:30",
    )
    print(
        f"Found {len(note_ids)} new notes added within the past 30 days (that are not in Test deck)"
    )
    return invoke("notes.getMany", ids=note_ids)


def get_test_notes() -> list[dict]:
    note_ids = invoke(
        "notes.search",
        query="deck:Test",
    )
    print(f"Found {len(note_ids)} notes in Test deck")
    return invoke("notes.getMany", ids=note_ids)


def write_to_file(content):
    title_text = "Chinese Flashcards Report"
    doc = html[
        head[
            meta(charset="utf-8"),
            meta(name="viewport", content="width=device-width,initial-scale=1"),
            title[title_text],
            style[STYLE],
        ],
        body[
            h1[title_text],
            p[f"Generated {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}"],
            *content,
        ],
    ]

    with open(output_file, "w") as fp:
        fp.write(str(doc))
    print(f"Generated report to {output_file}")


def notes_to_table(notes):
    def row(num, note):
        numtd = td(style="text-align: right")[str(num)]

        match note["noteType"]["name"]:
            case "Chinese Simple" | "Chinese Example":
                front = note["fields"]["Front"]
                back = note["fields"]["Back"]
                return tr[numtd, td[front], td(colspan="3")[back]]
            case "Chinese":
                field_names = ("Front", "pinyin", "gloss")
                return tr[numtd, (td[note["fields"][n]] for n in field_names)]

    return table[(row(i, n) for i, n in enumerate(notes, 1))]


def mature_correctness_detail(date, items):
    correct = sum(item[1] for item in items)
    total = len(items)

    return details[
        summary[f"{date.isoformat()} ({correct / total * 100:0.0f})%"],
        ul[(li[f"{label} {'✅' if correct else '❌'}"] for label, correct in items)],
    ]


def generate_report(
    unique_chars, sloppy_reviews, mature_correctness, new_notes, test_notes
):
    def content():
        yield p[f"Number of Chinese notes: {unique_chars.notes_count}"]

        yield details[
            summary[f"Unique characters ({len(unique_chars.unique_hanzi)})"],
            ", ".join(unique_chars.unique_hanzi),
        ]

        if sloppy_reviews:
            yield h2[
                f"Sloppy reviews within the past 7 days ({len(sloppy_reviews.cards)})"
            ]

            yield p[f"Shortest review: {sloppy_reviews.shortest_duration} ms"]

            yield details[
                summary["Anki query"],
                input_(
                    readonly=True,
                    size=40,
                    value="cid:" + ",".join(c.card_id for c in sloppy_reviews.cards),
                ),
            ]

            yield ol[
                (
                    li[f"{c.answered_at:%Y-%m-%d at %I:%M %p}: {c.question}"]
                    for c in sloppy_reviews.cards
                )
            ]

        if mature_correctness:
            yield h2["Correctness rate of mature cards"]

            yield [
                mature_correctness_detail(date, items)
                for date, items in mature_correctness
            ]

        yield h2[f"Cards added within the past 30 days ({len(new_notes)})"]

        yield notes_to_table(new_notes)

        yield h2[f"Cards in Test deck ({(len(test_notes))})"]

        yield notes_to_table(test_notes)

    write_to_file(content())


if __name__ == "__main__":
    main()
