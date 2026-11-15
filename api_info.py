# /// script
# dependencies = ["questionary", "requests", "rich"]
# ///
"""
Get info from the API and from API endpoints
"""

import json
from pathlib import Path

import questionary
import requests
from rich.console import Console
from rich.panel import Panel

output_file = Path("result.json")
note_type_names = [p.name for p in Path(__file__).parent.glob('Chinese*') if p.is_dir()]


def invoke(method, **params):
    data = {"method": method, "jsonrpc": "2.0", "id": 1}
    if params:
        data["params"] = params
    r = requests.post("http://127.0.0.1:8765/api/v1", json=data)
    output_file.write_text(json.dumps(r.json(), indent=2, ensure_ascii=False))


def main():
    console = Console()
    console.print(Panel("API Info", style="bold blue"))

    action = questionary.select(
        "Pick one", choices=["api.describe", "noteTypes.get", "exit"]
    ).ask()

    match action:
        case "api.describe":
            invoke("api.describe")
        case "noteTypes.get":
            name = questionary.select('Choose note type', note_type_names).ask()
            invoke('noteTypes.get', noteType={'name': name})

    console.print(f"Wrote output to [bold yellow]{output_file}[/bold yellow]")


if __name__ == "__main__":
    main()
