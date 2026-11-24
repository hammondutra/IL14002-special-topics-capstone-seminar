"""Structure and source-fidelity checks for the writing portfolio (no extra packages)."""
import json
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_index import generate  # noqa: E402


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_prose = False
        self.current = None
        self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and 'article-prose' in attrs.get('class', '').split():
            self.in_prose = True
        if tag == 'p' and self.in_prose:
            self.current = ''

    def handle_data(self, data):
        if self.current is not None:
            self.current += data

    def handle_endtag(self, tag):
        if tag == 'p' and self.current is not None:
            self.paragraphs.append(self.current)
            self.current = None
        if tag == 'div' and self.in_prose and self.current is None:
            self.in_prose = False


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.article = (ROOT / 'writings/op-ed/index.html').read_text(encoding='utf-8')

    def test_oped_copy_matches_approved_source(self):
        parser = Reader()
        parser.feed(self.article)
        source = (ROOT / 'content/op-ed/article-source.txt').read_text(encoding='utf-8')
        self.assertEqual(source.strip().split('\n\n')[1:], parser.paragraphs)
        self.assertEqual(10, len(parser.paragraphs))

    def test_oped_has_no_added_subheadings(self):
        self.assertEqual(1, self.article.count('class="article-prose"'))
        for phrase in ('The Arup fraud', 'Detection and provenance', 'Legal responses', 'Verification procedures', 'chapter-sidebar', 'chapter-heading', 'data-chapter', 'Undergraduate student at Minerva University'):
            self.assertNotIn(phrase, self.article)
        self.assertIn('https://www.linkedin.com/in/hammon-dutra/', self.article)

    def test_frozen_references_are_visible(self):
        self.assertEqual(7, self.article.count('<li><span class="source-org">'))
        self.assertEqual(7, len([line for line in (ROOT/'content/op-ed/references.md').read_text().splitlines() if line.startswith('- ')]))

    def test_registry_matches_homepage(self):
        self.assertEqual(generate(), (ROOT/'index.html').read_text(encoding='utf-8'))
        for entry in json.loads((ROOT/'content/writings.json').read_text()):
            self.assertIn(f'href="{entry["path"]}"', generate())

    def test_internal_paths_and_assets(self):
        self.assertTrue((ROOT/'writings/op-ed/styles.css').is_file())
        self.assertTrue((ROOT/'writings/op-ed/script.js').is_file())
        self.assertIn('href="../../"', self.article)
        self.assertIn('href="../film-review/"', self.article)
        self.assertIn('prefers-reduced-motion', (ROOT/'writings/op-ed/styles.css').read_text())
        self.assertNotIn('CASE FILE // 001', self.article)
        self.assertNotIn('portrait-svg', self.article)
        self.assertNotIn('focus-toggle', self.article)
        for phrase in ('VERIFY THE REQUEST', 'NOT JUST THE FACE', 'RECOGNITION IS NOT AUTHENTICATION', 'THE IDENTITY ISSUE', 'Core distinction'):
            self.assertNotIn(phrase.lower(), self.article.lower())
        self.assertIn('url=../writings/op-ed/', (ROOT/'op-ed/index.html').read_text())

    def test_new_publications_match_final_sources(self):
        for slug in ('academic-minute', 'time-capsule', 'author-profile'):
            parser = Reader()
            parser.feed((ROOT / 'writings' / slug / 'index.html').read_text(encoding='utf-8').replace('<br>', '\x0b'))
            source = (ROOT / 'content' / slug / 'article-source.txt').read_text(encoding='utf-8').strip().split('\n\n')[1:]
            self.assertEqual(source, parser.paragraphs)
        minute = (ROOT / 'writings/academic-minute/index.html').read_text()
        self.assertIn('youtube-nocookie.com/embed/AoS5kuewdhs', minute)
        self.assertIn('Sophareth (Phareth) Hao', (ROOT / 'writings/author-profile/index.html').read_text())
        self.assertEqual(5, len(json.loads((ROOT / 'content/writings.json').read_text())))

    def test_each_portfolio_entry_has_safe_local_route(self):
        for entry in json.loads((ROOT/'content/writings.json').read_text()):
            self.assertTrue(entry['path'].startswith('writings/'))
            self.assertNotIn('..', entry['path'])
            self.assertTrue(entry['path'].endswith('/'))
            self.assertTrue((ROOT/entry['path']/'index.html').exists())


if __name__ == '__main__':
    unittest.main()
