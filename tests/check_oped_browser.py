"""Browser regression checks for the op-ed layout (run separately from unittest)."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "writings/op-ed/index.html").as_uri() + "#essay"
expected = json.loads((ROOT / "content/op-ed/inline-links.json").read_text())

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height in [(320, 568), (390, 844), (780, 900), (781, 900), (900, 700), (1024, 768), (1328, 1152), (1440, 900), (1920, 1080)]:
            page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce")
            page.route("https://**/*", lambda route: route.abort())
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(URL)
            page.wait_for_selector(".article-prose p")
            page.evaluate("document.fonts.ready")
            sidebar, article = page.locator(".chapter-sidebar"), page.locator(".article-body")
            assert page.locator(".chapter-heading").count() == 0
            assert page.locator(".article-prose p").count() == 10
            links = page.locator(".article-prose a").evaluate_all("(els) => els.map(a=>({text:a.textContent,url:a.getAttribute('href')}))")
            assert links == [{"text": x["text"], "url": x["url"]} for x in expected]
            assert page.locator(".article-prose a").first.evaluate("(a)=>getComputedStyle(a).textDecorationLine.includes('underline')")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (width, "overflow")
            if width > 780:
                assert sidebar.is_visible()
                for target in ["the-case", "the-detectors", "the-law", "the-response"]:
                    page.locator(f'.chapter-links a[href="#{target}"]').click()
                    page.wait_for_function("(id)=>document.querySelector('[data-chapter='+id+']').getAttribute('aria-current')==='location'", arg=target)
                    sb, ab = sidebar.bounding_box(), article.bounding_box()
                    assert sb["x"] + sb["width"] + 15 <= ab["x"], (width, target, sb, ab)
                    assert sb["y"] >= 0, (width, target, sb)
                    head = page.locator(".sidebar-head").bounding_box()
                    first = page.locator(".chapter-links a").first.bounding_box()
                    assert head["y"] + head["height"] <= first["y"], (width, target, "sidebar overlap")
            else:
                assert not sidebar.is_visible()
            assert not errors, errors
            print(f"{width}x{height}: layout, text links and navigation passed")
            page.close()
        browser.close()

if __name__ == "__main__":
    run()
