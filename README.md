# IL14002 — Public Writing Portfolio

Minerva University, Fall 2026. Five final course publications, with distinct designs and a shared portfolio homepage.

Live site: https://hammondutra.github.io/IL14002-special-topics-capstone-seminar/

| Assignment | Publication | Route |
| --- | --- | --- |
| 1 | Academic Minute Essay | [Read](writings/academic-minute/) |
| 2 | Vulnerability as a Transaction | [Read](writings/film-review/) |
| 3 | Panem et Circenses | [Read](writings/time-capsule/) |
| 4 | The Writing Assistant That Refuses to Write | [Read](writings/author-profile/) |
| 5 | Your Face Is No Longer Proof You Were There | [Read](writings/op-ed/) |

## Structure and maintenance

- `content/writings.json`: catalog and homepage metadata.
- `content/<slug>/article-source.txt`: manuscript text for the Academic Minute, letter, profile and op-ed. The film review remains the original self-contained HTML with its illustrations.
- `writings/<slug>/index.html`: publication pages; the three new pieces share `writings/publication.css` with distinct palettes and layouts.
- `templates/portfolio.html` and `scripts/build_index.py`: homepage generator.
- `tests/test_site.py`: content, links and structure checks.

The Academic Minute includes the supplied YouTube recording and the script from the submitted assignment. The letter is presented as fiction, not a factual forecast. The profile is jointly credited to Hammon Dutra and Sophareth (Phareth) Hao. The op-ed now uses the ten-paragraph final submission instead of the earlier expanded preview; its bibliography remains available. Academic cover pages, private document URLs, assignment reflections and appendices are not published as article text.

To add or revise a publication, update its source and HTML, update the catalog if needed, and run:

```sh
python scripts/build_index.py
python -m unittest discover -s tests -v
python scripts/build_index.py --check
```

GitHub Actions builds and tests the portfolio before deploying it to GitHub Pages on pushes to main.
