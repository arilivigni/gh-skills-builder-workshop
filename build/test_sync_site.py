import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SPEC = importlib.util.spec_from_file_location("sync_site", Path(__file__).with_name("sync-site.py"))
site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(site)


def notes(slide, body):
    return (
        f"<!-- speaker-notes slide={slide} -->\n"
        + "\n".join((">" if not line else "> " + line) for line in body.splitlines())
        + "\n<!-- /speaker-notes -->\n"
    )


class FenceTests(unittest.TestCase):
    def test_collects_fences_per_slide_in_order_and_strips_quote_markers(self):
        markdown = (
            notes(2, "Say this.\n```bash\necho one\n```\n```text\nfirst line\n\n  indented\n```")
            + "```bash\nnot in notes\n```\n"
            + notes(2, "```text\nlater block\n```")
        )
        self.assertEqual(
            site.fences(markdown),
            {2: [("bash", "echo one"), ("text", "first line\n\n  indented"), ("text", "later block")]},
        )

    def test_quote_marker_without_space_is_stripped(self):
        markdown = "<!-- speaker-notes slide=1 -->\n>```text\n>tight\n>```\n<!-- /speaker-notes -->\n"
        self.assertEqual(site.fences(markdown), {1: [("text", "tight")]})

    def test_unclosed_fence_is_an_error(self):
        with self.assertRaisesRegex(site.SiteError, "left open"):
            site.fences(notes(3, "```text\nnever closed"))

    def test_unclosed_block_is_an_error(self):
        with self.assertRaisesRegex(site.SiteError, "never closed"):
            site.fences("<!-- speaker-notes slide=3 -->\n> words\n")

    def test_every_site_prompt_is_found_in_run_of_show(self):
        found = site.prompts(site.SOURCE.read_text(encoding="utf-8"))
        self.assertEqual(set(found), set(site.PROMPTS))
        self.assertTrue(found["install"].startswith("copilot plugin install gh-skills-builder@awesome-copilot"))
        self.assertIn("/publish-github-skills-exercise", found["prompt-4"])

    def test_moved_prompt_is_reported(self):
        markdown = notes(4, "```bash\nsomething else\n```")
        with self.assertRaisesRegex(site.SiteError, "install: slide 4 code block 1"):
            site.prompts(markdown)


class RenderTests(unittest.TestCase):
    def test_escapes_html_and_marks_reader_placeholders_only(self):
        self.assertEqual(
            site.render("cd <workshop-repo> && echo '<approved title>' > \"x\""),
            'cd <mark class="ph">&lt;workshop-repo&gt;</mark> &amp;&amp; echo \'&lt;approved title&gt;\' &gt; "x"',
        )

    def test_marks_adjacent_placeholders_once_each(self):
        self.assertEqual(
            site.render("<demo-owner>/<approved-name>"),
            '<mark class="ph">&lt;demo-owner&gt;</mark>/<mark class="ph">&lt;approved-name&gt;</mark>',
        )

    def test_markup_cannot_escape_the_code_block(self):
        rendered = site.render("</code></pre><script>alert(1)</script>")
        self.assertNotIn("<", rendered)


class FillTests(unittest.TestCase):
    PAGE = (
        "<pre><code><!-- prompt:a --><!-- /prompt --></code></pre>\n"
        "<pre><code><!-- prompt:b -->stale\ntext<!-- /prompt --></code></pre>\n"
    )

    def test_fills_every_region_and_is_idempotent(self):
        once = site.fill(self.PAGE, {"a": "x < y", "b": "<you>"})
        self.assertIn("<!-- prompt:a -->x &lt; y<!-- /prompt -->", once)
        self.assertIn('<!-- prompt:b --><mark class="ph">&lt;you&gt;</mark><!-- /prompt -->', once)
        self.assertNotIn("stale", once)
        self.assertEqual(site.fill(once, {"a": "x < y", "b": "<you>"}), once)

    def test_unknown_region_is_an_error(self):
        with self.assertRaisesRegex(site.SiteError, "unknown prompt 'b'"):
            site.fill(self.PAGE, {"a": "x"})

    def test_missing_region_is_an_error(self):
        with self.assertRaisesRegex(site.SiteError, "no region for: c"):
            site.fill(self.PAGE, {"a": "x", "b": "y", "c": "z"})


class MainTests(unittest.TestCase):
    def run_main(self, root, *args):
        paths = {
            "ROOT": root,
            "SOURCE": root / "run-of-show.md",
            "PAGE": root / "site" / "index.html",
            "HANDOFF": root / "handoff.sh",
            "DOWNLOAD": root / "site" / "downloads" / "handoff.sh",
        }
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.multiple(site, **paths), mock.patch.dict(site.PROMPTS, clear=True), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            site.PROMPTS["one"] = (1, 0, "bash", "echo")
            code = site.main(list(args))
        return code, out.getvalue() + err.getvalue()

    def test_check_reports_stale_files_then_sync_fixes_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "site").mkdir()
            (root / "run-of-show.md").write_text(notes(1, "```bash\necho <you>\n```"), encoding="utf-8")
            (root / "site" / "index.html").write_text("<code><!-- prompt:one --><!-- /prompt --></code>", encoding="utf-8")
            (root / "handoff.sh").write_bytes(b"#!/usr/bin/env bash\n")

            code, output = self.run_main(root, "--check")
            self.assertEqual(code, 1)
            self.assertIn("site/index.html: out of date", output)
            self.assertIn("site/downloads/handoff.sh: out of date", output)

            self.assertEqual(self.run_main(root)[0], 0)
            self.assertIn('echo <mark class="ph">&lt;you&gt;</mark>', (root / "site" / "index.html").read_text())
            download = root / "site" / "downloads" / "handoff.sh"
            self.assertEqual(download.read_bytes(), b"#!/usr/bin/env bash\n")
            self.assertTrue(download.stat().st_mode & 0o111)

            code, output = self.run_main(root, "--check")
            self.assertEqual(code, 0, output)


if __name__ == "__main__":
    unittest.main()
