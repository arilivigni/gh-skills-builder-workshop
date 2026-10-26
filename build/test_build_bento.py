import importlib.util
import io
import json
import re
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SPEC = importlib.util.spec_from_file_location("build_bento", Path(__file__).with_name("build-bento.py"))
bento = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bento)

MEDIA = {
    key: ("image/webp", b"webp")
    for key in ("rail", "headshot", "texture", "art-agent-skills", "art-lifecycle", "art-review-circuit", "og-image")
}
MEDIA["qr"] = ("image/png", b"png")
MEDIA["github-mark"] = ("image/svg+xml", b'<svg xmlns="http://www.w3.org/2000/svg"><path fill="#FFFFFF"/></svg>')


def element(el_id, **fx):
    el = {"id": el_id}
    if fx:
        el["fx"] = fx
    return el


class HelperTests(unittest.TestCase):
    def test_esc_escapes_markup_and_joins_lines(self):
        self.assertEqual(bento.esc("a <b> & c", "next"), "a &lt;b&gt; &amp; c<br>next")

    def test_serialize_keeps_script_tags_out_of_the_block(self):
        doc = {"html": "</script><b>x</b>", "n": 1}
        raw = bento.serialize(doc)
        self.assertNotIn("<", raw)
        self.assertEqual(json.loads(raw), doc)

    def test_splice_replaces_only_the_document_block(self):
        page = '<p>a</p><script type="application/bento+json" id="bento-doc">{}</script><p>b</p>'
        spliced = bento.splice(page, {"title": "<x>"})
        self.assertTrue(spliced.startswith("<p>a</p>") and spliced.endswith("</script><p>b</p>"))
        self.assertEqual(bento.read_doc(spliced), {"title": "<x>"})

    def test_clean_svg_drops_theme_classes_without_duplicate_fills(self):
        office = ('<svg xmlns="http://www.w3.org/2000/svg"><style>\n.MsftOfcThm_Text1_Fill_v2 { fill:#FFFFFF; }\n</style>'
                  '<path d="M0 0" class="MsftOfcThm_Text1_Fill_v2" stroke="none" fill="#FFFFFF"/>'
                  '<path d="M1 1" class="MsftOfcThm_Text1_Fill_v2"/></svg>')
        self.assertEqual(
            bento.clean_svg(office),
            '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0" stroke="none" fill="#FFFFFF"/>'
            '<path fill="#FFFFFF" d="M1 1"/></svg>',
        )

    def test_clean_svg_rejects_unknown_classes(self):
        with self.assertRaisesRegex(bento.BuildError, "unexpected class"):
            bento.clean_svg('<svg xmlns="http://www.w3.org/2000/svg"><path class="other"/></svg>')

    def test_clean_svg_uses_lf_line_endings(self):
        # Git stores LF, so CRLF output would make --check fail on a fresh clone.
        office = '<svg xmlns="http://www.w3.org/2000/svg">\r\n<path d="M0 0" fill="#FFFFFF"/>\r\n</svg>\r\n'
        self.assertEqual(bento.clean_svg(office), '<svg xmlns="http://www.w3.org/2000/svg">\n<path d="M0 0" fill="#FFFFFF"/>\n</svg>')


class MorphTests(unittest.TestCase):
    def test_morph_partners_lose_entrances_but_keep_other_effects(self):
        slides = [
            {"transition": "fade", "elements": [element("title", enter="fade-up", order=0)]},
            {"transition": "morph", "elements": [
                element("title", enter="fade-up", order=0, countUp=True),
                {"id": "pill", "morphId": "chip", "fx": {"enter": "fade", "order": 2, "ambient": "float"}},
                element("new", enter="fade-up", order=1),
            ]},
        ]
        slides[0]["elements"].append({"id": "chip"})
        result = bento.drop_morphing_entrances(slides)
        title, pill, new = result[1]["elements"]
        self.assertNotIn("fx", title)
        self.assertEqual(pill["fx"], {"ambient": "float"})
        self.assertEqual(new["fx"], {"enter": "fade-up", "order": 1})
        self.assertEqual(result[0]["elements"][0]["fx"], {"enter": "fade-up", "order": 0})

    def test_fade_slides_keep_entrances_for_repeated_ids(self):
        slides = [
            {"transition": "fade", "elements": [element("title", enter="fade-up", order=0)]},
            {"transition": "fade", "elements": [element("title", enter="fade-up", order=0)]},
        ]
        self.assertEqual(bento.drop_morphing_entrances(slides)[1]["elements"][0]["fx"],
                         {"enter": "fade-up", "order": 0})


class DocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notes = bento.load_sync_notes().parse(bento.NOTES_SOURCE.read_text(encoding="utf-8"))
        cls.doc = bento.build_doc(MEDIA, notes)

    def test_every_slide_has_notes_and_a_unique_id(self):
        ids = [s["id"] for s in self.doc["slides"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(s["notes"] for s in self.doc["slides"]))

    def test_element_ids_are_unique_per_slide_and_assets_resolve(self):
        assets = self.doc["assets"]
        slide_ids = {s["id"] for s in self.doc["slides"]}
        for s in self.doc["slides"]:
            ids = [el["id"] for el in s["elements"]]
            self.assertEqual(len(ids), len(set(ids)), s["id"])
            for el in s["elements"]:
                if el["type"] == "image":
                    self.assertIn(el["src"].removeprefix("asset:"), assets, el["id"])
                if el["type"] == "svg":
                    self.assertIn(el["asset"], assets, el["id"])
                if "link" in el:
                    self.assertTrue(el["link"] in slide_ids or re.match(r"https?://", el["link"]), el["link"])

    def test_fonts_reference_bare_asset_keys(self):
        for font in self.doc["fonts"]:
            self.assertIn(font["asset"], self.doc["assets"])
            self.assertTrue(self.doc["assets"][font["asset"]].startswith("data:font/woff2;base64,"))

    def test_og_image_stays_out_of_the_deck(self):
        self.assertNotIn("og-image", self.doc["assets"])

    def test_public_copy_is_read_only_without_notes(self):
        public = bento.public_doc(self.doc)
        self.assertTrue(public["readonly"])
        self.assertTrue(all(s["notes"] == "" for s in public["slides"]))
        self.assertNotIn("readonly", self.doc)
        self.assertTrue(all(s["notes"] for s in self.doc["slides"]))


class RenderTests(unittest.TestCase):
    SHELL = '<p>{app}</p><script type="application/bento+json" id="bento-doc"></script>'

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "deck.bento.html"

    @staticmethod
    def doc_with(color):
        buf = io.BytesIO()
        Image.new("RGB", (4, 4), color).save(buf, "PNG")
        return {"title": "t", "assets": {"qr": bento.data_uri("image/png", buf.getvalue())}}

    def write(self, app, doc):
        self.path.write_text(bento.render(self.path, self.SHELL.format(app=app), doc), encoding="utf-8")

    def test_unchanged_deck_is_left_alone(self):
        self.write("v1", self.doc_with("black"))
        self.assertIsNone(bento.render(self.path, self.SHELL.format(app="v1"), self.doc_with("black")))

    def test_same_size_image_swap_rewrites_the_deck(self):
        self.write("v1", self.doc_with("black"))
        page = bento.render(self.path, self.SHELL.format(app="v1"), self.doc_with("white"))
        self.assertIsNotNone(page)
        self.assertEqual(bento.read_doc(page)["assets"], self.doc_with("white")["assets"])

    def test_reshell_moves_an_unchanged_deck_into_the_new_app(self):
        self.write("v1", self.doc_with("black"))
        before = bento.read_doc(self.path.read_text(encoding="utf-8"))
        page = bento.render(self.path, self.SHELL.format(app="v2"), self.doc_with("black"), reshell=True)
        self.assertTrue(page.startswith("<p>v2</p>"))
        self.assertEqual(bento.read_doc(page), before)


if __name__ == "__main__":
    unittest.main()
