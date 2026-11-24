# IL14002 — Public Writing Portfolio

**Minerva University · Fall 2026**

This repository hosts an evolving portfolio of original public writing produced for **IL14002: Special Topics Capstone Seminar**. Each published piece has its own visual identity; the homepage is a shared directory, not a single article.

**Live portfolio:** https://hammondutra.github.io/IL14002-special-topics-capstone-seminar/

## Published writing

| Assignment | Format | Work | Website |
| --- | --- | --- | --- |
| 02 | Film review | **Vulnerability as a Transaction** — a reading of *Black Mirror: White Christmas* | [`writings/film-review/`](writings/film-review/) |
| 05 | Opinion essay | **Your Face Is No Longer Proof You Were There** — deepfakes, impersonation, and identity verification | [`writings/op-ed/`](writings/op-ed/) |

Other IL14002 assignments (Academic Minute, Time Capsule Letter, Interview and Public Profile, Final Portfolio) may be added as and when they are ready to publish. Their inclusion in the curriculum does not imply that they are already publicly available here.

## Repository layout

```text
.
├── index.html                    # Generated homepage (public portfolio)
├── content/
│   ├── writings.json             # Single source of truth for portfolio cards
│   └── op-ed/
│       ├── article-source.txt    # Frozen publication text for fidelity tests
│       └── references.md         # Bibliography for the opinion essay
├── writings/
│   ├── index.html                # Redirect to homepage (old portfolio-preview URL)
│   ├── film-review/index.html    # Original film review, copied exactly
│   └── op-ed/
│       ├── index.html            # Op-ed article
│       ├── styles.css
│       └── script.js
├── op-ed/index.html              # Redirect from short preview URL
├── templates/portfolio.html      # Portfolio presentation template
├── scripts/build_index.py       # Build the homepage from catalog metadata
├── tests/test_site.py           # Content and structural regression tests
└── .github/workflows/pages.yml  # Test, build and deploy via GitHub Pages
```

## Adding another piece

1. Create a new self-contained folder under `writings/<short-slug>/`, with an `index.html` and any local assets. Follow relative links so the page also works under GitHub Pages' project prefix.
2. Add a new entry to `content/writings.json` with a unique `slug`, title, assignment number, type, short description, `path`, `style` (`dark` or `red`), and call-to-action label. Keep the title's `displayTitle` formatting to `<br>` and `<em>` only.
3. Run `python scripts/build_index.py` to regenerate the homepage. You can customize the global portfolio template in `templates/portfolio.html` without changing each article's theme.
4. Run `python -m unittest discover -s tests -v` and `python scripts/build_index.py --check`, then commit the new work, updated catalog, and generated homepage together.

All code is plain HTML/CSS/JavaScript plus a **standard-library-only Python build script**. There is no Node install and no framework runtime. Google Fonts is optional; local/system fallbacks remain available.

## Publication provenance

The op-ed webpage uses the **14-paragraph, polished version supplied for the web preview**. It is intentionally not silently replaced with the shorter manuscript currently in the Google Doc's “Final Draft” tab. The text and references are stored in `content/op-ed/`, and the regression test ensures the public article matches that frozen source. Its appendix on research and revision craft is maintained in the original Google Doc.

The film review was the original site at the repository root. It has been copied *byte-for-byte* to `writings/film-review/index.html` so its embedded imagery and design survive the transition to a portfolio homepage. Git history preserves the original root page.

## CI and publishing

The GitHub Pages workflow runs structural/content tests, checks the generated homepage, and deploys the root directory on pushes to `main`. Individual piece URLs remain stable as more writings are added.
