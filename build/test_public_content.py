import re
import unittest
import zipfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
TEXT_SUFFIXES = {".md", ".html", ".py", ".sh", ".yml", ".yaml", ".css", ".js", ".txt", ".json"}
DECK = "slides/gh-skills-builder-workshop.bento.html"

# Skill names before gh-skills-builder 3.0.0, plus the old plugin-name typo. Built from
# parts so this file does not match its own scan.
LEGACY = re.compile(
    "|".join(
        [
            r"\b(?:orchestrate|bootstrap|review|publish)-github-skills-" + "exercise",
            r"\bcreate-github-skills-" + "outline",
            r"\bgh-skills-builder-" + "plugin",
        ]
    )
)


def text_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES and not SKIP_DIRS & set(path.relative_to(ROOT).parts):
            yield path


def pptx_xml():
    for path in ROOT.glob("*.pptx"):
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if name.endswith(".xml"):
                    yield f"{path.name}:{name}", archive.read(name).decode("utf-8", "replace")


class LegacyNameTests(unittest.TestCase):
    def test_no_pre_3_0_skill_names_in_text_files(self):
        hits = [
            f"{path.relative_to(ROOT)}: {match.group(0)}"
            for path in text_files()
            for match in LEGACY.finditer(path.read_text(encoding="utf-8", errors="replace"))
        ]
        self.assertEqual(hits, [])

    def test_no_pre_3_0_skill_names_in_decks(self):
        hits = [f"{name}: {match.group(0)}" for name, xml in pptx_xml() for match in LEGACY.finditer(xml)]
        self.assertEqual(hits, [])


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_nav = 0
        self.in_header = False
        self.in_hero = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        if tag == "header" and "site-header" in classes:
            self.in_header = True
        if tag == "section" and attrs.get("id") == "top":
            self.in_hero = True
        if tag == "nav" and "site-nav" in classes:
            self.in_nav += 1
        if tag == "a":
            self.links.append(
                {
                    "href": attrs.get("href"),
                    "target": attrs.get("target"),
                    "rel": attrs.get("rel") or "",
                    "in_header": self.in_header,
                    "in_hero": self.in_hero,
                    "in_nav": bool(self.in_nav),
                }
            )

    def handle_endtag(self, tag):
        if tag == "nav" and self.in_nav:
            self.in_nav -= 1
        if tag == "header":
            self.in_header = False
        if tag == "section":
            self.in_hero = False


class SlideLinkTests(unittest.TestCase):
    def setUp(self):
        parser = LinkCollector()
        parser.feed((ROOT / "site" / "index.html").read_text(encoding="utf-8"))
        self.links = parser.links

    def deck_links(self, region):
        return [link for link in self.links if link["href"] == DECK and link[region]]

    def test_header_links_to_deck_in_new_tab(self):
        (link,) = self.deck_links("in_header")
        self.assertEqual(link["target"], "_blank")
        self.assertIn("noopener", link["rel"])

    def test_hero_links_to_deck_in_new_tab(self):
        (link,) = self.deck_links("in_hero")
        self.assertEqual(link["target"], "_blank")
        self.assertIn("noopener", link["rel"])

    def test_section_nav_only_holds_in_page_anchors(self):
        # site.js runs querySelector on every .site-nav link href.
        hrefs = [link["href"] for link in self.links if link["in_nav"]]
        self.assertTrue(hrefs)
        self.assertTrue(all(href.startswith("#") for href in hrefs), hrefs)


if __name__ == "__main__":
    unittest.main()
