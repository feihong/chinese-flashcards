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


class SloppyReviewResult(NamedTuple):
    shortest_duration: int
    cards: list[dict]


def main():
    unique_chars = get_unique_chars()
    reviews = get_reviews()
    # sloppy_reviews = get_sloppy_reviews(reviews)
    # mature_correctness = get_mature_correctness(reviews)
    sloppy_reviews = mature_correctness = None
    new_notes = get_new_notes()
    test_notes = get_test_notes()

    generate_report(
        unique_chars, sloppy_reviews, mature_correctness, new_notes, test_notes
    )


def invoke(method, **params):
    data = {"method": method, "jsonrpc": "2.0", "id": 1}
    if params:
        data["params"] = params
    r = requests.post("http://127.0.0.1:8765/api/v1", json=data)
    result = r.json()["result"]
    match method:
        case "notes.search" | "cards.search":
            return result["ids"]
        case "notes.getMany" | "cards.getMany":
            return [item["result"] for item in result["items"]]
        case "reviews.list":
            return result["items"]
        case _:
            raise LookupError(f"Unknown API method {method}")


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
    card_ids = invoke("cards.search", query="rated:7")
    print(f"Found {len(card_ids)} cards studied within the past 7 days")

    reviews = invoke("reviews.list", cardIds=card_ids, limit=1000)
    # print(f'Found {len(reviews)} reviews')
    return reviews


def get_sloppy_reviews(reviews) -> SloppyReviewResult:
    # import pdb; pdb.set_trace()
    cr_map = {}  # dict mapping card_id to review time
    shortest_duration = 1_000_000
    for card_id, reviews in reviews.items():
        review = reviews[-1]  # only look at latest review
        shortest_duration = min(shortest_duration, review["time"])

        if review["time"] < 500:
            cr_map[int(card_id)] = review["id"]

    card_ids = list(cr_map.keys())
    cards = invoke("cards.getMany", ids=card_ids)
    # Sort by review time, most recent on the top
    cards.sort(key=lambda c: cr_map[c["cardId"]], reverse=True)
    return SloppyReviewResult(shortest_duration=shortest_duration, cards=cards)


def get_mature_card_items(card_map, cards_map) -> Iterable[(str, bool)]:
    for card_id, correct in card_map.items():
        card = cards_map[card_id]
        try:
            front = card["fields"]["Front"]["value"]
        except:
            # Cloze cards don't have Front field, but we don't care about them
            continue
        question = html2text.html2text(card["question"])
        yield f"{front} | {question}", correct


def get_mature_correctness(reviews_map) -> Iterable:
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
    print(f"Found {len(note_ids)} new notes added within the past 30 days (that are not in Test deck)")
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
                    value="cid:"
                    + ",".join(str(c["cardId"]) for c in sloppy_reviews.cards),
                ),
            ]

            yield ol[
                (
                    li[f"{c['cardId']}: {html2text.html2text(c['question'])}"]
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
