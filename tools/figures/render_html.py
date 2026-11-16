#!/usr/bin/env python3
"""Рендер HTML-візуалізацій у PNG.

tools/figures/<шлях>/NN-name.html -> public/images/<шлях>/NN-name.png

Запуск (потрібен Playwright з Chromium):
  python3 tools/figures/render_html.py tools/figures/ddd/domain-analysis/business-domains-and-subdomains
  python3 tools/figures/render_html.py tools/figures/ddd/.../01-name.html   (один файл)
У HTML кореневий елемент — <div id="fig">; знімається саме він, у масштабі 2x.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

FIGURES = Path(__file__).resolve().parent
PUBLIC = FIGURES.parent.parent / "public" / "images"


def targets(args):
    for a in args:
        p = Path(a).resolve()
        if p.is_dir():
            yield from sorted(p.glob("*.html"))
        else:
            yield p


def main():
    files = list(targets(sys.argv[1:]))
    if not files:
        print(__doc__)
        return 1
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except Exception:  # немає потрібної збірки Chromium — беремо встановлений Google Chrome
            browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1250, "height": 900}, device_scale_factor=2)
        for f in files:
            out = PUBLIC / f.parent.relative_to(FIGURES) / f"{f.stem}.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            page.goto(f.as_uri())
            page.wait_for_load_state("networkidle")
            page.locator("#fig").screenshot(path=str(out))
            print(out)
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
