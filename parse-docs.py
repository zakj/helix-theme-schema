# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "beautifulsoup4",
# ]
# ///

import json
from collections import OrderedDict
from urllib import request

from bs4 import BeautifulSoup, Tag


def is_ui_table(tag: Tag) -> bool:
    return bool(
        tag.name == "table" and tag("th", string="Key") and tag("th", string="Notes")
    )


def fetch_scopes() -> dict[str, str | None]:
    fp = request.urlopen("https://docs.helix-editor.com/themes.html")
    content = fp.read().decode("utf8")
    soup = BeautifulSoup(content, "html.parser")
    ui_table = soup.find(is_ui_table)
    if not isinstance(ui_table, Tag):
        raise Exception("could not find ui table")
    scopes = {}
    for row in ui_table("tr"):
        cells = row("td")
        if len(cells) == 1:
            scopes[cells[0].string] = None
        elif len(cells) == 2:
            scopes[cells[0].string] = cells[1].string
    return scopes


def main() -> None:
    with open("theme.tmpl.json", "r") as fp:
        schema = json.load(fp, object_pairs_hook=OrderedDict)
    props = schema["properties"]
    # Taplo will ignore a description on a property that has a top-level `$ref`,
    # so we keep refs inside `oneOf`.
    definition = {"oneOf": [{"$ref": "#/$defs/style"}, {"$ref": "#/$defs/color"}]}
    for key, desc in fetch_scopes().items():
        props[key] = definition.copy()
        if desc is not None:
            props[key]["description"] = desc
    with open("theme.json", "w") as fp:
        json.dump(schema, fp, indent=2)


if __name__ == "__main__":
    main()
