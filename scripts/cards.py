"""Counts the stars and languages of my projects, draws their cards, and renders the README.

    python3 scripts/cards.py    # needs Pillow, and a GitHub token in GITHUB_TOKEN or a signed-in `gh`

Projects come from sources.json, colours from theme.json. Stars and language shares come from the GitHub
API and land in cards/stats.json, which mairwunnx.com reads too. A repository written as “owner/*” stands
for every public repository of that organization or user, forks aside. A project with a fixed `languages`
map skips the language count: that’s for repositories GitHub can’t read yet.

GitHub strips CSS from READMEs, so each card is an image: one per project, language, and colour scheme.
Cards in one row share their row positions, so descriptions, tags, and language bars line up.
A workflow runs this every night, so the numbers stay current without my help.
"""
import functools
import html
import json
import os
import subprocess
import urllib.request
from collections import namedtuple

from PIL import ImageFont

import readme

CARDS = readme.ROOT / "cards"
THEME = readme.load("theme.json")

WIDTH, FULL_WIDTH, PAD = 410, 830, 18
DESC_LH, TAG_H, TAG_GAP, LEG_LH = 19, 20, 6, 16
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
STAR = "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"


def font(size, *candidates):
    """The first font that exists: Helvetica and Menlo on a Mac, their metric twins on Linux."""
    for path, index in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size, index=index)
    raise SystemExit(f"no font among {candidates}")


LIBERATION = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
MENLO = (("/System/Library/Fonts/Menlo.ttc", 0), ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 0))
F_DESC = font(13, ("/System/Library/Fonts/Helvetica.ttc", 0), (LIBERATION, 0))
F_MONO, F_STARS = font(10, *MENLO), font(11, *MENLO)
# The viewer's fonts differ from the measuring ones, so text gets some room.
SLACK = 1.08


# ---------- GitHub numbers ----------

@functools.lru_cache(maxsize=None)
def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def api(path):
    req = urllib.request.Request("https://api.github.com/" + path)
    req.add_header("Authorization", f"Bearer {token()}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-cards")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def expand(repo):
    owner, name = repo.split("/")
    if name != "*":
        return [repo]
    kind = "orgs" if api(f"users/{owner}")["type"] == "Organization" else "users"
    found, page = [], 1
    while True:
        batch = api(f"{kind}/{owner}/repos?type=public&per_page=100&page={page}")
        found += [r["full_name"] for r in batch if not r["fork"]]
        if len(batch) < 100:
            return sorted(found)
        page += 1


def shares(sizes):
    """Top four languages by bytes, the rest as Other."""
    whole = sum(sizes.values())
    if not whole:
        return []
    ranked = sorted(sizes.items(), key=lambda kv: -kv[1])
    top = [(name, round(size / whole * 100, 1)) for name, size in ranked[:4]]
    rest = round(100 - sum(pct for _, pct in top), 1)
    return top + [("Other", rest)] if rest >= 0.5 else top


def count(project):
    """Stars summed over the project's repositories, and its language shares.
    Build and config languages say nothing about the code, so they don't count."""
    fixed = project.get("languages")
    stars, sizes = 0, {}
    for repo in [r for pattern in project["repos"] for r in expand(pattern)]:
        stars += api(f"repos/{repo}")["stargazers_count"]
        if not fixed:
            for name, size in api(f"repos/{repo}/languages").items():
                if name not in readme.SOURCES["noise"]:
                    sizes[name] = sizes.get(name, 0) + size
    top = [(name, float(pct)) for name, pct in fixed.items()] if fixed else shares(sizes)
    colors = THEME["languages"]
    return {"stars": stars, "languages": [[name, pct, colors.get(name, colors["Other"])] for name, pct in top]}


# ---------- Layout ----------

Frame = namedtuple("Frame", "width y_tags y_langs height")


def text_width(f, text):
    return f.getlength(text) * SLACK


def wrap(text, limit):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if text_width(F_DESC, trial) <= limit or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def flow(items, limit, measure, gap):
    """Places inline boxes left to right with wrapping. Returns rows of (x, item, w)."""
    rows, row, x = [], [], 0
    for item in items:
        w = measure(item)
        if row and x + w > limit:
            rows.append(row)
            row, x = [], 0
        row.append((x, item, w))
        x += w + gap
    return rows + ([row] if row else [])


def layout(project, languages, lang, w):
    inner = w - 2 * PAD
    return dict(
        desc=wrap(project["description"][lang], inner),
        tags=flow(project["tags"], inner, lambda t: text_width(F_MONO, t) + 16, TAG_GAP),
        legend=flow([x for x in languages if x[1] >= 1], inner,
                    lambda x: text_width(F_MONO, f"{x[0]} {x[1]:.0f}%") + 14, 14),
    )


def frame(layouts, w):
    """The row's tallest description and tag block set where tags and languages start on every card in it."""
    y_tags = PAD + 22 + max(len(l["desc"]) for l in layouts) * DESC_LH + 8
    y_langs = y_tags + max(len(l["tags"]) * (TAG_H + TAG_GAP) for l in layouts) + 6
    height = y_langs + 12 + 6 + max(len(l["legend"]) for l in layouts) * LEG_LH + PAD - 4
    return Frame(w, y_tags, y_langs, height)


# ---------- SVG ----------

e = html.escape


def header(name, w, h, t):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{e(name)}">',
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{t["background"]}" stroke="{t["border"]}"/>',
            f'<text x="{PAD}" y="{PAD + 14}" font-family="{SANS}" font-size="16" font-weight="600" fill="{t["name"]}">{e(name)}</text>',
            f'<text x="{w - PAD}" y="{PAD + 13}" text-anchor="end" font-family="{SANS}" font-size="14" fill="{t["arrow"]}">↗</text>']


def star_count(stars, w, t):
    """A star icon and the number, left of the arrow, in the legend's colours. Nothing at zero."""
    if not stars:
        return []
    label = f"{stars:,}".replace(",", " ")
    right = w - PAD - 22
    x = right - F_STARS.getlength(label) - 4 - 12
    return [f'<text x="{right}" y="{PAD + 12}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["legend"]}">{label}</text>',
            f'<path transform="translate({x:.1f} {PAD + 2}) scale(0.75)" d="{STAR}" fill="{t["percent"]}"/>']


def description(lines, t):
    top = PAD + 22 + 14
    return [f'<text x="{PAD}" y="{top + i * DESC_LH}" font-family="{SANS}" font-size="13" fill="{t["description"]}">{e(line)}</text>'
            for i, line in enumerate(lines)]


def tags(rows, y, t):
    out = []
    for row in rows:
        for x, tag, tw in row:
            out.append(f'<rect x="{PAD + x:.1f}" y="{y}" width="{tw:.1f}" height="{TAG_H}" rx="10" fill="{t["tag_background"]}" fill-opacity="{t["tag_background_opacity"]}"/>')
            out.append(f'<text x="{PAD + x + 8:.1f}" y="{y + 13.5}" font-family="{MONO}" font-size="10" fill="{t["tag"]}">{e(tag)}</text>')
        y += TAG_H + TAG_GAP
    return out


def language_bar(key, languages, w, y, t):
    """A rule, then one bar split by share. Tiny shares keep a sliver so their colour still shows."""
    inner = w - 2 * PAD
    gaps = 2 * (len(languages) - 1)
    out = [f'<line x1="{PAD}" y1="{y}" x2="{w - PAD}" y2="{y}" stroke="{t["rule"]}"/>']
    y += 12
    out.append(f'<clipPath id="bar-{key}"><rect x="{PAD}" y="{y}" width="{inner}" height="6" rx="3"/></clipPath><g clip-path="url(#bar-{key})">')
    x = PAD
    for _, pct, color in languages:
        seg = max(3, (inner - gaps) * pct / 100)
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{seg:.1f}" height="6" fill="{color}"/>')
        x += seg + 2
    out.append("</g>")
    return out


def legend(rows, y, t):
    out = []
    for row in rows:
        for x, (name, pct, color), _ in row:
            out.append(f'<circle cx="{PAD + x + 4}" cy="{y - 3.5}" r="4" fill="{color}"/>')
            out.append(f'<text x="{PAD + x + 12}" y="{y}" font-family="{MONO}" font-size="10" fill="{t["legend"]}">{e(name)} '
                       f'<tspan fill="{t["percent"]}">{pct:.0f}%</tspan></text>')
        y += LEG_LH
    return out


def svg(project, numbers, l, f, t):
    w = f.width
    return "\n".join(header(project["name"], w, f.height, t)
                     + star_count(numbers["stars"], w, t)
                     + description(l["desc"], t)
                     + tags(l["tags"], f.y_tags, t)
                     + language_bar(project["key"], numbers["languages"], w, f.y_langs, t)
                     + legend(l["legend"], f.y_langs + 12 + 6 + 16, t)
                     + ["</svg>"])


def draw_row(row, lang, stats):
    """Writes the SVGs of one row and returns their file names."""
    w = WIDTH if len(row) == 2 else FULL_WIDTH
    layouts = [layout(p, stats[p["key"]]["languages"], lang, w) for p in row]
    f = frame(layouts, w)
    written = []
    for project, l in zip(row, layouts):
        for scheme, t in THEME["schemes"].items():
            name = f"{project['key']}-{lang}-{scheme}.svg"
            (CARDS / name).write_text(svg(project, stats[project["key"]], l, f, t) + "\n", encoding="utf-8")
            written.append(name)
    return written


def main():
    stats = {p["key"]: count(p) for p in readme.projects()}
    written = set()
    for category in readme.SOURCES["categories"]:
        for row in readme.rows(category):
            for lang in readme.LANGS:
                written.update(draw_row(row, lang, stats))
    # Cards of a removed or renamed project would linger otherwise.
    for old in CARDS.glob("*.svg"):
        if old.name not in written:
            old.unlink()
    (CARDS / "stats.json").write_text(json.dumps({"projects": stats}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    readme.write()
    print("stars:", {k: s["stars"] for k, s in stats.items() if s["stars"]})


if __name__ == "__main__":
    main()
