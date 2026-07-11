# /// script
# requires-python = ">=3.13"
# dependencies = ["requests", "htpy", "html2text"]
# ///
"""
Generate a report summarizing the current state of Chinese flashcards, including:
- List unique hanzi that appear on the front of notes
- List sloppily-reviewed cards in the past 7 days
- List new notes added since a specific day in the past
- List all notes currently in the Test deck
- TODO: Percentage of 'Good' reviews for each day in the past 7 days
"""

import os
from pathlib import Path
from collections.abc import Iterable
from typing import NamedTuple
from datetime import datetime

import requests
import html2text
from htpy import (
    html,
    head,
    meta,
    title,
    style,
    body,
    h1,
    h2,
    details,
    summary,
    p,
    ol,
    li,
    table,
    tr,
    td,
)


output_file = Path(os.environ["OUTPUT_DIR"]) / "index.html"


STYLE = """
body { margin: 1em; }
ul { padding-left: 1em; }
table { border-collapse: collapse; }
th, td { border: 1px solid #777; padding: 1em; }
"""


class SloppyReviewResult(NamedTuple):
    shortest_duration: int
    cards: list[dict]


def main():
    unique_chars = get_unique_chars()
    sloppy_reviews = get_sloppy_reviews()
    new_notes = get_new_notes()
    test_notes = get_test_notes()

    generate_report(unique_chars, sloppy_reviews, new_notes, test_notes)


def invoke(action, **params):
    data = {"action": action, "version": 6}
    if params:
        data["params"] = params
    r = requests.post("http://127.0.0.1:8765", json=data)
    return r.json()


def get_unique_chars() -> Iterable[str]:
    note_ids = invoke("findNotes", query="note:Chinese")["result"]
    print(f"Found {len(note_ids)} Chinese notes")
    notes = invoke("notesInfo", notes=note_ids)["result"]

    def gen():
        for note in notes:
            for c in note["fields"]["Front"]["value"]:
                if ord(c) > 255:
                    yield c

    return sorted(set(gen()))


def get_sloppy_reviews() -> SloppyReviewResult:
    card_ids = invoke("findCards", query="rated:7")["result"]
    print(f"Found {len(card_ids)} cards studied within the past 7 days")

    reviews = invoke("getReviewsOfCards", cards=card_ids)["result"]
    # print(f'Found {len(reviews)} reviews')

    shortest_duration = 1_000_000
    for key in list(reviews.keys()):
        review = reviews[key][-1]  # only look at latest review
        shortest_duration = min(shortest_duration, review["time"])

        if review["time"] > 500:
            # ignore if review duration was more than 0.4 seconds
            del reviews[key]
        else:
            reviews[key] = review

    card_ids = [int(s) for s in reviews.keys()]
    cards = invoke("cardsInfo", cards=card_ids)["result"]
    return SloppyReviewResult(shortest_duration=shortest_duration, cards=cards)


def get_new_notes() -> list[dict]:
    note_ids = invoke(
        "findNotes",
        query="deck:Main note:Chinese added:30 OR deck:Main note:Cloze added:30",
    )["result"]
    print(
        f"Found {len(note_ids)} new Chinese or Cloze notes added within the past 30 days"
    )
    return invoke("notesInfo", notes=note_ids)["result"]


def get_test_notes() -> list[dict]:
    note_ids = invoke(
        "findNotes",
        query="deck:Test",
    )["result"]
    print(f"Found {len(note_ids)} notes in Test deck")
    return invoke("notesInfo", notes=note_ids)["result"]


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

        match note["modelName"]:
            case "Cloze":
                return tr[numtd, td(colspan="4")[note["fields"]["Text"]["value"]]]
            case "Chinese":
                field_names = ("Front", "pinyin", "gloss", "example")
                return tr[numtd, (td[note["fields"][n]["value"]] for n in field_names)]

    return table[(row(i, n) for i, n in enumerate(notes, 1))]


def generate_report(unique_chars, sloppy_reviews, new_notes, test_notes):
    def content():
        yield details[
            summary[f"Unique characters ({len(unique_chars)})"],
            ", ".join(unique_chars),
        ]

        yield h2[f"Sloppy reviews within the past 7 days ({len(sloppy_reviews.cards)})"]

        yield p[f"Shortest review: {sloppy_reviews.shortest_duration} ms"]

        yield details[
            summary["Anki query"],
            "cid:" + ",".join(str(c["cardId"]) for c in sloppy_reviews.cards),
        ]

        yield ol[(li[html2text.html2text(c["question"])] for c in sloppy_reviews.cards)]

        yield h2[f"Chinese cards added within the past 30 days ({len(new_notes)})"]

        yield notes_to_table(new_notes)

        yield h2[f"Cards in Test deck ({(len(test_notes))})"]

        yield notes_to_table(test_notes)

    write_to_file(content())


if __name__ == "__main__":
    main()
