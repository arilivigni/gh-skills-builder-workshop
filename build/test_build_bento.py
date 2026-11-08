import importlib.util
import io
import json
import re
import shutil
import subprocess
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
LIGHT_MEDIA = {key: ("image/webp", b"light") for key in ("rail", "texture", *bento.ART)}
LIGHT_MEDIA["github-mark"] = ("image/svg+xml", b'<svg xmlns="http://www.w3.org/2000/svg"><path fill="#000000"/></svg>')
SHELL = '<p>app</p><script type="application/bento+json" id="bento-doc">{}</script><p>tail</p>'


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

    def test_clean_svg_takes_the_fill_from_the_theme_class(self):
        # The light deck's mark says fill="#FFFFFF" but its theme class paints it black.
        office = ('<svg xmlns="http://www.w3.org/2000/svg"><style>\n.MsftOfcThm_Background1_Fill_v2 { fill:#000000; }\n'
                  '</style><path d="M0 0" class="MsftOfcThm_Background1_Fill_v2" fill="#FFFFFF"/></svg>')
        self.assertEqual(bento.clean_svg(office),
                         '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0" fill="#000000"/></svg>')

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

    def test_agenda_counts_only_the_duration_without_replacing_the_heading(self):
        agenda = next(s for s in self.doc["slides"] if s["id"] == "flight-plan")
        elements = {el["id"]: el for el in agenda["elements"]}
        counter = elements["agenda-duration"]
        self.assertEqual(counter["html"], "60")
        self.assertTrue(counter["fx"]["countUp"])
        self.assertEqual(
            "".join(elements[key]["html"] for key in ("agenda-title", "agenda-duration", "agenda-unit"))
            + " " + elements["agenda-title-rest"]["html"],
            "Our 60-minute flight plan",
        )

    def test_visible_slides_are_numbered_in_the_clear_footer(self):
        self.assertNotIn("slide-number-1", {el["id"] for el in self.doc["slides"][0]["elements"]})
        for number, slide in enumerate(self.doc["slides"][1:], start=2):
            elements = {el["id"]: el for el in slide["elements"]}
            page = elements.get(f"slide-number-{number}")
            if slide.get("hidden"):
                self.assertIsNone(page, slide["id"])
                continue
            self.assertIsNotNone(page, slide["id"])
            self.assertEqual(page["html"], str(number))
            self.assertEqual((page["x"], page["y"], page["w"], page["h"]), (1190, 688, 32, 20))
            for element in slide["elements"]:
                if element.get("type") != "text" or element is page:
                    continue
                self.assertFalse(
                    page["x"] < element["x"] + element["w"]
                    and element["x"] < page["x"] + page["w"]
                    and page["y"] < element["y"] + element["h"]
                    and element["y"] < page["y"] + page["h"],
                    f"{page['id']} overlaps {element['id']} on {slide['id']}",
                )

    def test_scenario_uses_working_title_copy(self):
        scenario = next(s for s in self.doc["slides"] if s["id"] == "scenario")
        elements = {el["id"]: el for el in scenario["elements"]}
        self.assertEqual(elements["scenario-title-vote"]["html"], "Working Title: Copilot app Cleared for Takeoff")

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


class ThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notes = bento.load_sync_notes().parse(bento.NOTES_SOURCE.read_text(encoding="utf-8"))
        cls.doc = bento.public_doc(bento.build_doc(MEDIA, notes))
        cls.overlay = bento.light_overlay(LIGHT_MEDIA)

    @staticmethod
    def layout(slide):
        return [(el["id"], el.get("type"), el.get("x"), el.get("y"), el.get("w"), el.get("h"), el.get("morphId"))
                for el in slide["elements"]]

    def test_light_slides_match_the_dark_slides_one_for_one(self):
        # deck-theme.js swaps slides by position and falls back to dark if the ids disagree.
        dark, light = self.doc["slides"], self.overlay["slides"]
        self.assertEqual([s["id"] for s in light], [s["id"] for s in dark])
        for d, l in zip(dark, light):
            self.assertEqual(self.layout(l), self.layout(d), d["id"])
            self.assertEqual((l.get("transition"), l.get("hidden")), (d.get("transition"), d.get("hidden")), d["id"])
            self.assertEqual(l["notes"], "")

    def test_light_slides_use_only_light_colors(self):
        light_json = json.dumps(self.overlay["slides"]).upper()
        dark_only = set(bento.PALETTES["dark"].values()) - set(bento.PALETTES["light"].values()) - {"transparent"}
        self.assertEqual(sorted(c for c in dark_only if c.upper() in light_json), [])
        self.assertEqual(self.overlay["theme"]["background"], bento.PALETTES["light"]["bg"])

    def test_drawing_light_slides_leaves_the_dark_palette_in_place(self):
        before = bento.build_slides()
        bento.build_slides("light")
        self.assertIs(bento.P, bento.PALETTES["dark"])
        self.assertEqual(bento.build_slides(), before)

    def test_overlay_assets_replace_only_themed_images_and_resolve(self):
        self.assertEqual(set(self.overlay["assets"]), {"rail", "texture", "github-mark", *bento.ART})
        assets = {**self.doc["assets"], **self.overlay["assets"]}
        for s in self.overlay["slides"]:
            for el in s["elements"]:
                if el["type"] == "image":
                    self.assertIn(el["src"].removeprefix("asset:"), assets, el["id"])
                if el["type"] == "svg":
                    self.assertIn(el["asset"], assets, el["id"])

    def test_region_parses_back_and_cannot_close_its_script_early(self):
        region = bento.theme_region(self.overlay)
        data = re.search(r'<script type="application/json" id="ghsb-light">(.*?)</script>', region, re.S).group(1)
        self.assertNotIn("<", data)
        self.assertEqual(json.loads(data), self.overlay)
        script = re.search(r"<script>\n(.*)\n</script>", region, re.S).group(1)
        self.assertEqual(script, bento.DECK_THEME_JS.read_text(encoding="utf-8").strip())
        self.assertNotIn("</", script)
        self.assertEqual(region.count("</script>"), 2)

    @unittest.skipUnless(shutil.which("node"), "needs node")
    def test_inlined_switch_script_is_valid_javascript(self):
        script = re.search(r"<script>\n(.*)\n</script>", bento.theme_region(self.overlay), re.S).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "deck-theme.js"
            path.write_text(script, encoding="utf-8")
            result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_apply_theme_follows_the_document_block_and_is_idempotent(self):
        once = bento.apply_theme(SHELL, self.overlay)
        self.assertEqual(bento.apply_theme(once, self.overlay), once)
        region = bento.theme_region(self.overlay)
        self.assertEqual(bento.read_theme_region(once), region)
        self.assertIn('id="bento-doc">{}</script>\n' + region + "<p>tail</p>", once)
        self.assertIsNone(bento.read_theme_region(SHELL))

    def test_apply_theme_needs_exactly_one_document_block(self):
        with self.assertRaisesRegex(bento.BuildError, "expected one #bento-doc block"):
            bento.apply_theme("<p>no deck</p>", self.overlay)

    def test_site_images_add_the_light_texture_and_artwork(self):
        files = bento.site_images(MEDIA, LIGHT_MEDIA)
        light = sorted(name for name in files if "-light." in name)
        self.assertEqual(light, sorted(f"{key}-light.webp" for key in ("texture", *bento.ART)))
        self.assertEqual(bento.site_images(MEDIA), {k: v for k, v in files.items() if "-light." not in k})


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

    OVERLAY = {"theme": {}, "slides": [], "assets": {}}

    def write_themed(self, app, doc):
        page = bento.themed_page(None, bento.render(self.path, self.SHELL.format(app=app), doc), self.OVERLAY)
        self.path.write_text(page, encoding="utf-8")
        return page

    def test_themed_page_keeps_new_slides_from_a_shell_that_already_has_the_region(self):
        # --shell pointing at the saved website deck: its region is already current.
        saved = self.write_themed("v1", self.doc_with("black"))
        rendered = bento.render(self.path, saved, self.doc_with("white"), reshell=True)
        self.assertEqual(bento.apply_theme(rendered, self.OVERLAY), rendered)
        page = bento.themed_page(saved, rendered, self.OVERLAY)
        self.assertIsNotNone(page)
        self.assertEqual(bento.read_doc(page)["assets"], self.doc_with("white")["assets"])
        self.assertEqual(bento.read_theme_region(page), bento.theme_region(self.OVERLAY))

    def test_themed_page_keeps_a_new_app_from_a_shell_that_already_has_the_region(self):
        saved = self.write_themed("v1", self.doc_with("black"))
        shell = bento.apply_theme(self.SHELL.format(app="v2"), self.OVERLAY)
        page = bento.themed_page(saved, bento.render(self.path, shell, self.doc_with("black"), reshell=True), self.OVERLAY)
        self.assertTrue(page.startswith("<p>v2</p>"))
        self.assertEqual(bento.read_doc(page), bento.read_doc(saved))

    def test_themed_page_is_none_only_when_the_file_is_current(self):
        saved = self.write_themed("v1", self.doc_with("black"))
        self.assertIsNone(bento.themed_page(saved, None, self.OVERLAY))
        same = bento.render(self.path, saved, self.doc_with("black"), reshell=True)
        self.assertIsNone(bento.themed_page(saved, same, self.OVERLAY))
        plain = self.SHELL.format(app="v1")
        self.assertEqual(bento.read_theme_region(bento.themed_page(plain, None, self.OVERLAY)), bento.theme_region(self.OVERLAY))

    def test_a_shell_taken_from_the_website_deck_loses_its_theme_region(self):
        plain = self.SHELL.format(app="v1")
        self.path.write_text(bento.apply_theme(plain, self.OVERLAY), encoding="utf-8")
        self.assertEqual(bento.load_shell(False, self.path), plain)


if __name__ == "__main__":
    unittest.main()
