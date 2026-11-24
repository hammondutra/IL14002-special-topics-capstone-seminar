#!/usr/bin/env python3
"""Render the public-writing homepage from content/writings.json (stdlib only).

Run ``python scripts/build_index.py`` after editing the catalog, or
``python scripts/build_index.py --check`` to assert the checked-in HTML is current.
"""
from pathlib import Path
from html import escape
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "content/writings.json"
TEMPLATE = ROOT / "templates/portfolio.html"
OUTPUT = ROOT / "index.html"


def generate():
    items = json.loads(CATALOG.read_text(encoding="utf-8"))
    slugs = set()
    cards = []
    for item in items:
        slug = item["slug"]
        if slug in slugs:
            raise ValueError(f"Duplicate writing slug: {slug}")
        slugs.add(slug)
        path = item["path"]
        if not path.startswith("writings/") or ".." in path or not path.endswith("/"):
            raise ValueError(f"Unsafe or non-canonical writing path: {path}")
        style = {'dark': 'card-one', 'red': 'card-two', 'green': 'card-three', 'ochre': 'card-four', 'violet': 'card-five'}[item['style']]
        display_title = item['displayTitle']
        # Only intentionally formatted metadata is permitted: text, <br>, <em>.
        cleaned = display_title.replace('<br>', '').replace('<em>', '').replace('</em>', '')
        if '<' in cleaned or '>' in cleaned:
            raise ValueError(f"Unexpected markup in displayTitle: {slug}")
        cards.append(
            f'      <a class="work-card {style}" href="{escape(path, quote=True)}">'
            f'<span class="card-label">{int(item["assignment"]):02d} / {escape(item["type"].upper())}</span>'
            f'<div><h2>{display_title}</h2><p>{escape(item["description"])}</p></div>'
            f'<div class="card-footer"><span>{escape(item["label"])}</span><span aria-hidden="true">↗</span></div>'
            '<div class="circle-art" aria-hidden="true"></div></a>'
        )
    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count('<!-- WRITING_CARDS -->') != 1 or template.count('<!-- ARTICLE_COUNT -->') != 1:
        raise ValueError('Missing expected portfolio placeholders')
    html = template.replace('<!-- WRITING_CARDS -->', '\n'.join(cards)).replace('<!-- ARTICLE_COUNT -->', f'{len(items):02d} WORKS')
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    generated = generate()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != generated:
            raise SystemExit('index.html out of date: run python scripts/build_index.py')
        print('index.html matches content/writings.json')
    else:
        OUTPUT.write_text(generated, encoding="utf-8")
        print('Updated index.html')


if __name__ == '__main__':
    main()
