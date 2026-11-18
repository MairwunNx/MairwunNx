"""Draws the project cards of this README and counts their stars and languages.

    python3 scripts/cards.py        # needs Pillow, and a GitHub token in GITHUB_TOKEN or a signed-in `gh`

Texts, tags, and repositories come from cards/data.json, written by my resume tools. Stars and language
shares come from the GitHub API and land in cards/stats.json, which mairwunnx.com reads too.
A workflow runs this every night, so the numbers stay current without my help.

GitHub strips CSS from READMEs, so each card is an image: one per project, language, and colour scheme.
Cards in one row share their row positions, so descriptions, tags, and language bars line up.
"""
import html
import json
import os
import pathlib
import re
import subprocess
import urllib.request

from PIL import ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"
DATA = json.loads((CARDS / "data.json").read_text(encoding="utf-8"))

W, FULL_W, PAD = 410, 830, 18
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"


def font(size, *candidates):
    """The first font that exists: Helvetica and Menlo on a Mac, their metric twins on Linux."""
    for path, index in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size, index=index)
    raise SystemExit(f"no font among {candidates}")


LIB = "/usr/share/fonts/truetype/liberation/"
F_DESC = font(13, ("/System/Library/Fonts/Helvetica.ttc", 0), (LIB + "LiberationSans-Regular.ttf", 0))
MENLO = (("/System/Library/Fonts/Menlo.ttc", 0), ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 0))
F_MONO, F_STARS = font(10, *MENLO), font(11, *MENLO)
SLACK = 1.08  # fonts differ between systems: leave room

THEMES = {
    "dark": dict(bg="#161b22", border="#30363d", name="#9fd65b", desc="#9198a1", tag_bg="#9fd65b", tag_bg_o="0.12",
                 tag="#c4cad1", rule="#30363d", legend="#9198a1", pct="#6e7681", arrow="#6e7681"),
    "light": dict(bg="#f6f8fa", border="#d0d7de", name="#3f6f0e", desc="#59636e", tag_bg="#3f6f0e", tag_bg_o="0.10",
                  tag="#424a53", rule="#d0d7de", legend="#59636e", pct="#818b98", arrow="#818b98"),
}
DESC_LH, TAG_H, TAG_GAP, LEG_LH = 19, 20, 6, 16


# ---------- GitHub numbers ----------

def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


TOKEN = token()


def api(path):
    req = urllib.request.Request("https://api.github.com/" + path)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-cards")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def stats(key, project):
    """Stars summed over the project's repositories, and language shares by GitHub's byte counts:
    top four, the rest as Other. Build and config languages say nothing about the code, so they don't count."""
    stars, total = 0, {}
    for repo in project["repos"]:
        stars += api(f"repos/{repo}")["stargazers_count"]
        for name, size in api(f"repos/{repo}/languages").items():
            if name not in DATA["noise"]:
                total[name] = total.get(name, 0) + size
    if project.get("languages"):
        top = [tuple(x) for x in project["languages"]]
    else:
        whole = sum(total.values())
        ranked = sorted(total.items(), key=lambda kv: -kv[1])
        top = [(n, round(b / whole * 100, 1)) for n, b in ranked[:4]] if whole else []
        rest = round(100 - sum(p for _, p in top), 1)
        if top and rest >= 0.5:
            top.append(("Other", rest))
    colors = DATA["colors"]
    return {"stars": stars, "languages": [[n, p, colors.get(n, colors["Other"])] for n, p in top]}


STATS = {key: stats(key, p) for key, p in DATA["projects"].items()}


# ---------- Layout ----------

def width(f, text):
    return f.getlength(text) * SLACK


def wrap(text, limit):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if width(F_DESC, trial) <= limit or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def flow(items, limit, measure, gap):
    """Places inline boxes left to right, wrapping; returns rows of (x, item, w)."""
    rows, row, x = [], [], 0
    for item in items:
        w = measure(item)
        if row and x + w > limit:
            rows.append(row)
            row, x = [], 0
        row.append((x, item, w))
        x += w + gap
    return rows + ([row] if row else [])


def layout(key, lang, w):
    inner = w - 2 * PAD
    tags = flow(DATA["projects"][key]["tags"], inner, lambda t: width(F_MONO, t) + 16, TAG_GAP)
    legend = flow([(n, p, c) for n, p, c in STATS[key]["languages"] if p >= 1], inner,
                  lambda x: width(F_MONO, f"{x[0]} {x[1]:.0f}%") + 14, 14)
    return dict(desc=wrap(DATA["texts"][lang][key], inner), tags=tags, legend=legend)


STAR = "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"


def svg(key, name, theme, w, l, y_tags, y_langs, h):
    t = THEMES[theme]
    e = html.escape
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{e(name)}">',
           f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>',
           f'<text x="{PAD}" y="{PAD + 14}" font-family="{SANS}" font-size="16" font-weight="600" fill="{t["name"]}">{e(name)}</text>',
           f'<text x="{w - PAD}" y="{PAD + 13}" text-anchor="end" font-family="{SANS}" font-size="14" fill="{t["arrow"]}">↗</text>']
    stars = STATS[key]["stars"]
    if stars:
        # The count sits left of the arrow: a star icon, then the number, in the legend's colours.
        label = f"{stars:,}".replace(",", " ")
        right = w - PAD - 22
        out.append(f'<text x="{right}" y="{PAD + 12}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["legend"]}">{label}</text>')
        x = right - F_STARS.getlength(label) - 4 - 12
        out.append(f'<path transform="translate({x:.1f} {PAD + 2}) scale(0.75)" d="{STAR}" fill="{t["pct"]}"/>')
    y = PAD + 22 + 14
    for line in l["desc"]:
        out.append(f'<text x="{PAD}" y="{y}" font-family="{SANS}" font-size="13" fill="{t["desc"]}">{e(line)}</text>')
        y += DESC_LH
    y = y_tags
    for row in l["tags"]:
        for x, tag, tw in row:
            out.append(f'<rect x="{PAD + x:.1f}" y="{y}" width="{tw:.1f}" height="{TAG_H}" rx="10" fill="{t["tag_bg"]}" fill-opacity="{t["tag_bg_o"]}"/>')
            out.append(f'<text x="{PAD + x + 8:.1f}" y="{y + 13.5}" font-family="{MONO}" font-size="10" fill="{t["tag"]}">{e(tag)}</text>')
        y += TAG_H + TAG_GAP
    y = y_langs
    out.append(f'<line x1="{PAD}" y1="{y}" x2="{w - PAD}" y2="{y}" stroke="{t["rule"]}"/>')
    y += 12
    inner = w - 2 * PAD
    langs = STATS[key]["languages"]
    gaps = 2 * (len(langs) - 1)
    out.append(f'<clipPath id="bar-{key}"><rect x="{PAD}" y="{y}" width="{inner}" height="6" rx="3"/></clipPath><g clip-path="url(#bar-{key})">')
    x = PAD
    for n, pct, color in langs:
        seg = max(3, (inner - gaps) * pct / 100)
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{seg:.1f}" height="6" fill="{color}"/>')
        x += seg + 2
    out.append("</g>")
    y += 6 + 16
    for row in l["legend"]:
        for x, (n, pct, color), _ in row:
            out.append(f'<circle cx="{PAD + x + 4}" cy="{y - 3.5}" r="4" fill="{color}"/>')
            out.append(f'<text x="{PAD + x + 12}" y="{y}" font-family="{MONO}" font-size="10" fill="{t["legend"]}">{e(n)} '
                       f'<tspan fill="{t["pct"]}">{pct:.0f}%</tspan></text>')
        y += LEG_LH
    out.append("</svg>")
    return "\n".join(out)


def render_row(keys, lang):
    """Writes the SVGs of one row and returns its HTML for the README."""
    w = W if len(keys) == 2 else FULL_W
    ls = [layout(k, lang, w) for k in keys]
    desc_end = PAD + 22 + max(len(l["desc"]) for l in ls) * DESC_LH
    y_tags = desc_end + 8
    tags_end = y_tags + max(len(l["tags"]) * (TAG_H + TAG_GAP) for l in ls)
    y_langs = tags_end + 6
    h = y_langs + 12 + 6 + max(len(l["legend"]) for l in ls) * LEG_LH + PAD - 4
    parts = []
    for key, l in zip(keys, ls):
        p = DATA["projects"][key]
        for theme in THEMES:
            (CARDS / f"{key}-{lang}-{theme}.svg").write_text(svg(key, p["name"], theme, w, l, y_tags, y_langs, h) + "\n", encoding="utf-8")
        alt = html.escape(f"{p['name']}: {DATA['texts'][lang][key]}", quote=True)
        size = "49%" if len(keys) == 2 else "98.4%"
        parts.append(
            f'<a href="{p["url"]}"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/{key}-{lang}-dark.svg">'
            f'<img src="cards/{key}-{lang}-light.svg" width="{size}" alt="{alt}"></picture></a>')
    return '<p align="center">\n' + "\n".join(parts) + "\n</p>"


# ---------- README ----------

URL_TO_KEY = {p["url"]: key for key, p in DATA["projects"].items()}
BLOCK = re.compile(r'(?:<p align="center">\n(?:<a href="[^"]+"><picture>.*?</picture></a>\n)+</p>\n\n?)+')


def redraw(section, lang):
    """Each run of card rows becomes rows of two again, from the current data."""
    def repl(m):
        keys = [URL_TO_KEY[u] for u in re.findall(r'<a href="([^"]+)"><picture>', m.group(0))]
        rows = [keys[i:i + 2] for i in range(0, len(keys), 2)]
        tail = "\n" if m.group(0).endswith("\n\n") else ""
        return "\n\n".join(render_row(r, lang) for r in rows) + "\n" + tail
    return BLOCK.sub(repl, section)


readme = (ROOT / "README.md").read_text(encoding="utf-8")
ru_at = readme.index("<summary>Русская версия</summary>")
es_at = readme.index("<summary>Versión en español</summary>")
readme = redraw(readme[:ru_at], "en") + redraw(readme[ru_at:es_at], "ru") + redraw(readme[es_at:], "es")
(ROOT / "README.md").write_text(readme, encoding="utf-8")
(CARDS / "stats.json").write_text(json.dumps({"projects": STATS}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("stars:", {k: s["stars"] for k, s in STATS.items() if s["stars"]})
