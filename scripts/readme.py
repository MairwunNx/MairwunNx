"""Renders README.md from TEMPLATE.md and sources.json.

    python3 scripts/readme.py

TEMPLATE.md is plain Markdown with placeholders written as HTML comments: `<!-- projects:en -->` (also
`ru` and `es`) for the project categories and their cards, `<!-- stack -->` for the stack icons.
This step needs no network and no Pillow. scripts/cards.py counts stars, draws the card images,
and then calls it too.
"""
import html
import json
import pathlib
import re

import stack

ROOT = pathlib.Path(__file__).resolve().parent.parent
LANGS = ("en", "ru", "es")
PLACEHOLDER = re.compile(r"<!-- ([a-z]+(?::[a-z]+)?) -->")


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


SOURCES = load("sources.json")


def projects():
    found = [p for category in SOURCES["categories"] for p in category["projects"]]
    keys = [p["key"] for p in found]
    # Keys name the card files and the entries of stats.json, so two projects can't share one.
    if len(set(keys)) != len(keys):
        raise SystemExit(f"duplicate project keys in sources.json: {keys}")
    return found


def rows(category):
    """Two cards per row. A card alone in its row takes the full width."""
    found = category["projects"]
    return [found[i:i + 2] for i in range(0, len(found), 2)]


def card(project, lang, full):
    key = project["key"]
    alt = html.escape(f"{project['name']}: {project['description'][lang]}", quote=True)
    size = "98.4%" if full else "49%"
    return (f'<a href="{project["url"]}"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/{key}-{lang}-dark.svg">'
            f'<img src="cards/{key}-{lang}-light.svg" width="{size}" alt="{alt}"></picture></a>')


def category_block(category, lang):
    parts = [f"### {category['title'][lang]}"]
    if "intro" in category:
        parts.append(category["intro"][lang])
    for row in rows(category):
        cards = "\n".join(card(p, lang, len(row) == 1) for p in row)
        parts.append(f'<p align="center">\n{cards}\n</p>')
    return "\n\n".join(parts)


def blocks():
    found = {f"projects:{lang}": "\n\n".join(category_block(c, lang) for c in SOURCES["categories"]) for lang in LANGS}
    found["stack"] = stack.block(SOURCES["icons"])
    return found


def fill(template, values):
    used = set(PLACEHOLDER.findall(template))
    # A misspelt placeholder would silently drop a whole section, so both directions must match.
    if used != set(values):
        raise SystemExit(f"TEMPLATE.md placeholders {sorted(used)} don't match {sorted(values)}")
    return PLACEHOLDER.sub(lambda m: values[m.group(1)], template)


def write():
    projects()
    template = (ROOT / "TEMPLATE.md").read_text(encoding="utf-8")
    (ROOT / "README.md").write_text(fill(template, blocks()), encoding="utf-8")


if __name__ == "__main__":
    write()
