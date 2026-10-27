#!/usr/bin/env python3
"""Copy the prompts in run-of-show.md into the workshop website.

The website (site/index.html) shows every prompt and command from the session.
Each one sits in a region like

    <pre><code><!-- prompt:prompt-1 -->...<!-- /prompt --></code></pre>

and this script fills it with the matching fenced code block from the speaker
notes in run-of-show.md, HTML-escaped, with the known placeholders highlighted.
It also copies handoff.sh to site/downloads/ so visitors can download it.

Standard library only, so the Pages workflow can run it without python-pptx.

    python3 build/sync-site.py            # update the site
    python3 build/sync-site.py --check    # exit 1 if the site is out of date
"""
import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "run-of-show.md"
PAGE = ROOT / "site" / "index.html"
HANDOFF = ROOT / "handoff.sh"
DOWNLOAD = ROOT / "site" / "downloads" / "handoff.sh"
START = re.compile(r"^<!-- speaker-notes slide=(\d+) -->$")
END = "<!-- /speaker-notes -->"
REGION = re.compile(r"<!-- prompt:([a-z0-9-]+) -->.*?<!-- /prompt -->", re.S)

# id: (slide, fence index within that slide's notes, fence language, text the prompt must contain)
PROMPTS = {
    "install": (4, 0, "bash", "copilot plugin install gh-skills-builder@awesome-copilot"),
    "marketplace-add": (4, 1, "bash", "marketplace add"),
    "plugin-list": (4, 2, "bash", "plugin list"),
    "prompt-1": (9, 0, "text", "/create-github-skills-outline"),
    "gate-1": (9, 1, "text", "Approved."),
    "handoff": (9, 2, "text", "Hand-off Authorization"),
    "handoff-terminal": (9, 3, "bash", "handoff.sh"),
    "prompt-2": (10, 0, "text", "/bootstrap-github-skills-exercise"),
    "gate-2": (10, 1, "text", "I accept this build round"),
    "prompt-3": (11, 0, "text", "/review-github-skills-exercise"),
    "prompt-3a": (11, 1, "text", "browser canvas"),
    "prompt-3b": (11, 2, "text", "<finding-id>"),
    "fix-accept": (11, 3, "text", "Re-run the report-only review"),
    "gate-3": (11, 4, "text", "No known release blockers"),
    "prompt-4": (12, 0, "text", "/publish-github-skills-exercise"),
    "prompt-4b": (12, 1, "text", "<demo-owner>/<approved-name>"),
    "orchestrate": (13, 0, "text", "/orchestrate-github-skills-exercise"),
}

# Placeholders the reader must replace. Other <...> text in a prompt, such as
# "<approved title>" in Prompt 1, is an instruction to the model and stays plain.
PLACEHOLDERS = [
    "<workshop-repo>",
    "<you>",
    "<paste the approved outline artifact>",
    "<finding-id>",
    "<demo-owner>",
    "<approved-name>",
]


class SiteError(Exception):
    pass


def fences(markdown):
    """Return {slide number: [(language, code), ...]} from the speaker notes, in document order."""
    found, current, lang, code = {}, None, None, None
    for lineno, line in enumerate(markdown.splitlines(), 1):
        match = START.match(line.strip())
        if match:
            if current is not None:
                raise SiteError(f"line {lineno}: speaker-notes block opened before the previous one closed")
            current = int(match.group(1))
            continue
        if line.strip() == END:
            if code is not None:
                raise SiteError(f"line {lineno}: code fence left open in the notes for slide {current}")
            current = None
            continue
        if current is None:
            continue
        if line.startswith("> "):
            line = line[2:]
        elif line.startswith(">"):
            line = line[1:]
        if code is None:
            if line.startswith("```"):
                lang, code = line[3:].strip(), []
        elif line.strip() == "```":
            found.setdefault(current, []).append((lang, "\n".join(code)))
            code = None
        else:
            code.append(line)
    if current is not None:
        raise SiteError(f"speaker-notes block for slide {current} is never closed")
    return found


def prompts(markdown):
    """Return {prompt id: code} for every prompt the site shows."""
    blocks = fences(markdown)
    result = {}
    for pid, (slide, index, lang, needle) in PROMPTS.items():
        slide_blocks = blocks.get(slide, [])
        if index >= len(slide_blocks):
            raise SiteError(f"{pid}: slide {slide} has {len(slide_blocks)} code blocks, expected at least {index + 1}")
        got_lang, code = slide_blocks[index]
        if got_lang != lang or needle not in code:
            raise SiteError(f"{pid}: slide {slide} code block {index + 1} is not the expected {lang} block "
                            f"containing {needle!r}; update PROMPTS in build/sync-site.py")
        result[pid] = code
    return result


PLACEHOLDER_RE = re.compile("|".join(re.escape(html.escape(p, quote=False))
                                     for p in sorted(PLACEHOLDERS, key=len, reverse=True)))


def render(code):
    """Escape a prompt for <pre><code> and highlight the placeholders."""
    return PLACEHOLDER_RE.sub(lambda m: f'<mark class="ph">{m.group(0)}</mark>', html.escape(code, quote=False))


def fill(page, values):
    """Replace every prompt region in the page; every region must have a value."""
    seen = set()

    def sub(match):
        pid = match.group(1)
        if pid not in values:
            raise SiteError(f"site/index.html has a region for unknown prompt {pid!r}")
        seen.add(pid)
        return f"<!-- prompt:{pid} -->{render(values[pid])}<!-- /prompt -->"

    result = REGION.sub(sub, page)
    missing = sorted(set(values) - seen)
    if missing:
        raise SiteError(f"site/index.html has no region for: {', '.join(missing)}")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if the site is out of date")
    args = parser.parse_args(argv)

    try:
        page = PAGE.read_text(encoding="utf-8")
        updated = fill(page, prompts(SOURCE.read_text(encoding="utf-8")))
    except SiteError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    script = HANDOFF.read_bytes()

    stale = []
    if updated != page:
        stale.append(PAGE)
    if not DOWNLOAD.exists() or DOWNLOAD.read_bytes() != script:
        stale.append(DOWNLOAD)

    if args.check:
        for path in stale:
            print(f"{path.relative_to(ROOT)}: out of date; run python3 build/sync-site.py", file=sys.stderr)
        if not stale:
            print("Site prompts and downloads are up to date")
        return 1 if stale else 0

    if PAGE in stale:
        PAGE.write_text(updated, encoding="utf-8")
    if DOWNLOAD in stale:
        DOWNLOAD.parent.mkdir(parents=True, exist_ok=True)
        DOWNLOAD.write_bytes(script)
        DOWNLOAD.chmod(0o755)
    for path in stale:
        print(f"{path.relative_to(ROOT)}: updated")
    if not stale:
        print("Site prompts and downloads are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
