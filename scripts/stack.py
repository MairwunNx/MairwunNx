"""Renders the stack icons of the README from the `icons` list in sources.json.

Each icon is `{"name": …, "devicon": …, "variant": …}`. The name becomes the alt text and the tooltip,
`devicon` is the icon’s folder in the devicon set, and `variant` picks the file in it (“original” if left out).
scripts/readme.py puts the block in place of `<!-- stack -->`.
"""
import html

# A pinned release, so an upstream redraw never changes the README unnoticed.
DEVICON = "https://cdn.jsdelivr.net/gh/devicons/devicon@v2.18.0/icons"
HEIGHT = 36


def icon(entry):
    slug = entry["devicon"]
    variant = entry.get("variant", "original")
    name = html.escape(entry["name"], quote=True)
    return f'  <img src="{DEVICON}/{slug}/{slug}-{variant}.svg" height="{HEIGHT}" alt="{name}" title="{name}" />'


def block(icons):
    lines = "\n".join(icon(entry) for entry in icons)
    return f'<p align="center">\n{lines}\n</p>'
