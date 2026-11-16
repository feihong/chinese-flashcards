# /// script
# dependencies = ["requests"]
# ///
"""
Update the templates for Anki note types
"""

from pathlib import Path

import requests

here = Path(__file__).parent
build_dir = here / "_build"
note_type_names = [p.name for p in Path(__file__).parent.glob("Chinese*") if p.is_dir()]


def invoke(method, **params):
    data = {"method": method, "jsonrpc": "2.0", "id": 1, "params": params}
    r = requests.post("http://127.0.0.1:8765/api/v1", json=data)
    return r.json()


def get_note_type_edits(model_dir: Path):
    def gen():
        for dir in model_dir.iterdir():
            if not dir.is_dir():
                continue

            yield {
                "op": "updateTemplate",
                "name": dir.name,
                "patch": {
                    "questionHtml": (dir / "front.html").read_text(),
                    "answerHtml": (dir / "back.html").read_text(),
                },
            }

    return list(gen())


def update_note_type(note_type_dir: Path):
    name = note_type_dir.name

    print(f'Updating {name}')
    result = invoke(
        "noteTypes.editStructure",
        noteType={
            "name": name,
        },
        edits=get_note_type_edits(note_type_dir),
    )
    if error := result.get('error'):
        raise Exception(error)
    else:
        print(f"Updated template for {name}")


for name in note_type_names:
    update_note_type(build_dir / name)
