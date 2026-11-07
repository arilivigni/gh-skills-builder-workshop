import hashlib
import json
import re
import struct
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


class TrailerCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.stack = []
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section":
            self.stack.append(attrs.get("id"))
            self.sections.append(attrs.get("id"))
        if "trailer" in self.stack:
            self.tags.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag == "section":
            self.stack.pop()

    def handle_data(self, data):
        if "trailer" in self.stack:
            self.text.append(data)


class TrailerTests(unittest.TestCase):
    def setUp(self):
        self.site = ROOT / "site"
        self.media = self.site / "assets" / "video"
        self.prefix = "gh-skills-builder-workshop-trailer"
        self.parser = TrailerCollector()
        self.parser.feed((self.site / "index.html").read_text())

    def tags(self, name):
        return [attrs for tag, attrs in self.parser.tags if tag == name]

    def test_trailer_immediately_follows_hero(self):
        sections = self.parser.sections
        self.assertEqual(sections.count("trailer"), 1)
        self.assertEqual(sections[sections.index("top"):sections.index("top") + 3],
                         ["top", "trailer", "plugin"])

    def test_native_player_is_accessible_and_user_initiated(self):
        (video,) = self.tags("video")
        for attribute in ("controls", "playsinline"):
            self.assertIn(attribute, video)
        for attribute in ("autoplay", "loop"):
            self.assertNotIn(attribute, video)
        self.assertEqual(video["preload"], "metadata")
        self.assertEqual((video["width"], video["height"]), ("1920", "1080"))
        self.assertEqual(video["aria-labelledby"], "trailer-title")
        self.assertEqual(video["aria-describedby"], "trailer-description")
        self.assertTrue((self.site / video["poster"]).read_bytes().startswith(b"\xff\xd8"))
        (track,) = self.tags("track")
        self.assertEqual(track["kind"], "captions")
        self.assertEqual(track["srclang"], "en")
        self.assertIn("default", track)
        self.assertEqual(track["src"], f"assets/video/{self.prefix}.vtt")

    def test_standalone_and_download_links_share_the_player_asset(self):
        (source,) = self.tags("source")
        self.assertEqual(source["type"], "video/mp4")
        self.assertEqual(source["src"], f"assets/video/{self.prefix}.mp4")
        links = [link for link in self.tags("a") if link.get("href") == source["src"]]
        (opened,) = [link for link in links if link.get("target") == "_blank"]
        self.assertIn("noopener", opened.get("rel", "").split())
        self.assertEqual(len([link for link in links if "download" in link]), 1)
        for attrs in [source, *self.tags("track"), *self.tags("a")]:
            path = attrs.get("src") or attrs.get("href")
            if path and path.startswith("assets/video/"):
                self.assertTrue((self.site / path).is_file(), path)

    def test_transcript_and_credits_are_available_without_javascript(self):
        self.assertEqual(len(self.tags("details")), 1)
        self.assertEqual(len(self.tags("summary")), 1)
        inline = " ".join(" ".join(self.parser.text).split())
        transcript = (self.media / f"{self.prefix}-transcript.txt").read_text()
        self.assertIn("Install the plugin from the awesome-copilot marketplace "
                      "in the Copilot app or CLI.", transcript)
        for paragraph in transcript.strip().split("\n\n")[2:]:
            self.assertIn(" ".join(paragraph.split()), inline)
        credits = (self.media / "credits.txt").read_text()
        for credit in ("Kevin MacLeod", "creativecommons.org/licenses/by/4.0/",
                       "Qwen3-TTS", "synthetic speech"):
            self.assertIn(credit, credits)

    def test_caption_formats_agree_and_cues_fit_the_video(self):
        vtt = (self.media / f"{self.prefix}.vtt").read_text()
        srt = (self.media / f"{self.prefix}.srt").read_text()
        self.assertTrue(vtt.startswith("WEBVTT\n\n"))
        self.assertEqual(re.sub(r"(\d{2}:\d{2}:\d{2})\.(\d{3})", r"\1,\2",
                                vtt[len("WEBVTT\n\n"):]), srt)
        previous_end = 0
        cues = re.findall(r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> "
                          r"(\d{2}:\d{2}:\d{2}\.\d{3})\n(.*?)(?:\n\n|$)",
                          vtt, re.S)
        self.assertGreater(len(cues), 10)
        for start, end, text in cues:
            def seconds(value):
                h, m, s = value.split(":")
                return int(h) * 3600 + int(m) * 60 + float(s)
            self.assertLessEqual(previous_end, seconds(start))
            self.assertLess(seconds(start), seconds(end))
            self.assertLessEqual(seconds(end), 120)
            self.assertLessEqual(len(text.splitlines()), 2)
            self.assertTrue(all(len(line) <= 42 for line in text.splitlines()))
            previous_end = seconds(end)
        self.assertIn("gh-skills-builder", vtt)
        spoken = " ".join(" ".join(text.split()) for _, _, text in cues)
        self.assertIn("Install the plugin from the awesome-copilot marketplace "
                      "in the Copilot app or CLI", spoken)

    def test_media_size_checksum_and_recorded_encoding(self):
        path = self.media / f"{self.prefix}.mp4"
        self.assertGreater(path.stat().st_size, 0)
        self.assertLessEqual(path.stat().st_size, 40 * 1024 * 1024)
        info = json.loads((self.media / "media-info.json").read_text())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), info["sha256"])
        self.assertEqual(info["bytes"], path.stat().st_size)
        self.assertEqual((info["width"], info["height"]), (1920, 1080))
        self.assertEqual(info["frame_rate"], "30/1")
        self.assertEqual(info["video_frames"], 3600)
        self.assertAlmostEqual(info["duration_seconds"], 120, delta=1 / 30)
        self.assertEqual((info["video_codec"], info["audio_codec"]), ("h264", "aac"))

    def test_mp4_metadata_precedes_media_for_fast_start(self):
        path = self.media / f"{self.prefix}.mp4"
        atoms = []
        with path.open("rb") as stream:
            while stream.tell() < path.stat().st_size:
                start = stream.tell()
                size, kind = struct.unpack(">I4s", stream.read(8))
                header_size = 8
                if size == 1:
                    size = struct.unpack(">Q", stream.read(8))[0]
                    header_size = 16
                if size == 0:
                    size = path.stat().st_size - start
                self.assertGreaterEqual(size, header_size)
                self.assertLessEqual(start + size, path.stat().st_size)
                atoms.append(kind)
                stream.seek(start + size)
        self.assertEqual(atoms[0], b"ftyp")
        self.assertIn(b"moov", atoms)
        self.assertIn(b"mdat", atoms)
        self.assertLess(atoms.index(b"moov"), atoms.index(b"mdat"))


if __name__ == "__main__":
    unittest.main()
