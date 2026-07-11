# /// script
# requires-python = ">=3.13"
# dependencies = ["requests", "htpy"]
# ///
"""
Generate a report summarizing the current state of Chinese flashcards, including:
- List unique hanzi in the cards
- List sloppily-reviewed cards in the past 7 days
- List new cards added since a specific day in the past
- All the cards currently in the Test deck
"""

import os
from pathlib import Path

import requests
from htpy import (
    html,
    head,
    meta,
    title,
    body,
    h1,
    h2,
    details,
    summary,
    ul,
    li,
    a as anchor,
)


output_file = Path(os.environ["OUTPUT_DIR"]) / "index.html"


def main():
    notes = get_chinese_notes()
    unique_chars = get_unique_chars(notes)
    generate_report(unique_chars)


def invoke(action, **params):
    data = {"action": action, "version": 6}
    if params:
        data["params"] = params
    r = requests.post("http://127.0.0.1:8765", json=data)
    return r.json()


def get_chinese_notes():
    note_ids = invoke("findNotes", query="note:Chinese")["result"]
    print(f"Found {len(note_ids)} Chinese notes")
    return invoke("notesInfo", notes=note_ids)["result"]


def get_unique_chars(notes):
    def gen():
        for note in notes:
            for c in note["fields"]["Front"]["value"]:
                if ord(c) > 255:
                    yield c

    return sorted(set(gen()))


def write_to_file(content):
    title_text = "Chinese Flashcards Report"
    doc = html[
        head[
            meta(charset="utf-8"),
            meta(name="viewport", content="width=device-width,initial-scale=1"),
            title[title_text],
        ],
        body[
            h1[title_text],
            *content,
        ],
    ]

    with open(output_file, "w") as fp:
        fp.write(str(doc))
    print(f"Generated report to {output_file}")


def generate_report(unique_chars):
    def content():
        yield details[
            summary[f"Unique characters ({len(unique_chars)})"],
            ", ".join(unique_chars),
        ]

    write_to_file(content())


if __name__ == "__main__":
    main()
