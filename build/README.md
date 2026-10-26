# Rebuilding the decks and the website

The committed decks in the repository root are ready to present. Speaker notes are maintained in [`../run-of-show.md`](../run-of-show.md), not in the build script; see [Speaker notes](#speaker-notes). Rebuild the PowerPoint decks only after changing slide text or artwork in `build-workshop-v2.py`. The [Bento deck](#bento-deck) and the [website](#website) are generated from the dark PowerPoint deck and the run of show, and need neither the template nor PowerPoint.

> [!WARNING]
> The committed decks include hand edits made after the last build: slide 1 is the title slide from the 2026 GitHub presentation template, and the original title slide is now slide 15, hidden. `build-workshop-v2.py` does not reproduce those edits, so rerunning it overwrites them. After a rebuild, reapply them in PowerPoint, then run `sync-notes.py`.

## Speaker notes

Each slide's notes are a blockquote in `run-of-show.md` between `<!-- speaker-notes slide=N -->` and `<!-- /speaker-notes -->`. A slide can have more than one block (slide 9 has two); they are joined in order. Every slide, including hidden slide 15, needs at least one block.

After editing the notes, copy them into both decks from the repository root:

```bash
python3 build/sync-notes.py
```

The script rewrites only the notes parts of each deck and copies every other part byte for byte, so hand edits to the slides are preserved. It needs only `python-pptx` from `build/requirements.txt`, not the template. To check that both decks match the run of show without changing them:

```bash
python3 build/sync-notes.py --check
```

Inside a notes block, use only `**bold**`, single-backtick inline code (shown without backticks), `- ` bullets, and fenced code blocks (shown in Courier New, one notes paragraph per line). Markdown characters inside code stay literal. The script rejects unbalanced backticks, unsupported emphasis, links, headings, numbered lists, and a raw `<` outside code, so the Markdown and the deck notes stay identical.

The check compares visible text as well as bold and code formatting, including line breaks or fields inserted in PowerPoint. Run the synchronization regression tests with:

```bash
python3 -m unittest discover -s build -p 'test_sync_notes.py'
```

The Bento deck has the same notes, so run `python3 build/build-bento.py` after `sync-notes.py`.

## Bento deck

`build-bento.py` writes three things from `gh-skills-builder-workshop-dark.pptx` and `run-of-show.md`:

- `gh-skills-builder-workshop-dark.bento.html`: the [Bento](https://bento.page) deck, with speaker notes.
- `site/slides/gh-skills-builder-workshop.bento.html`: a read-only copy for the website, without notes.
- `site/assets/img/`: the slide images, recompressed as WebP for the web, plus the favicon and the social preview image.

A `.bento.html` file is the Bento app plus one `<script type="application/bento+json" id="bento-doc">` block that holds the slides as JSON. The script rewrites only that block, so the slide layouts live in `build-bento.py`: changes made in the Bento editor are overwritten by the next run. Images come from the PowerPoint deck, so artwork changes there carry over. The fonts are the Mona Sans files in `site/assets/fonts/`.

```bash
python3 build/build-bento.py                  # update the decks and site images
python3 build/build-bento.py --check          # exit 1 if anything is out of date
python3 build/build-bento.py --refresh-shell  # download the latest Bento app first
python3 build/build-bento.py --shell FILE     # or use a Bento app saved locally
```

It needs Python 3.11 or later with `python-pptx` and `Pillow` from `requirements.txt`. Without `--refresh-shell` or `--shell`, it reuses the Bento app already in the committed deck, so it works offline. An unchanged deck is left alone, so its `modified` time only moves when the slides change. Images are compared byte for byte, so replaced artwork is always picked up. Pillow is pinned because another version can encode the images differently, which `--check` reports as out of date.

## Website

`site/` is static HTML, CSS, and JavaScript with no build step. Each prompt and command on the page sits in a region marked `<!-- prompt:ID -->…<!-- /prompt -->`, filled from the matching fenced code block in `run-of-show.md`. `sync-site.py` fills those regions, highlights the known `<placeholders>`, and copies `handoff.sh` to `site/downloads/`:

```bash
python3 build/sync-site.py          # update the site
python3 build/sync-site.py --check  # exit 1 if the site is out of date
```

It uses only the standard library. To show another prompt, add an empty region with a new ID to `site/index.html`, then add the ID to `PROMPTS` in `sync-site.py` with its slide, code-block position, and a phrase it must contain. The script fails if a region has no prompt, a prompt has no region, or a run-of-show block moved, so a reordered prompt is never copied into the wrong place.

[`../.github/workflows/pages.yml`](../.github/workflows/pages.yml) runs `test_sync_site.py` and `sync-site.py --check` on pull requests that touch the site, `run-of-show.md`, or `handoff.sh`, and deploys `site/` to GitHub Pages on each push to `main`. It does not rebuild the Bento deck, so run `build-bento.py --check` yourself after changing the PowerPoint deck.

## Tests

Run every build test from the repository root:

```bash
python3 -m unittest discover -s build -p 'test_*.py'
```

`test_sync_site.py` needs only the standard library. `test_sync_notes.py` and `test_build_bento.py` need `requirements.txt`.

## Requirements

- Python 3.11 or later, plus `pip install -r build/requirements.txt`.
- The **2026 GitHub Presentation Template** (`.potx`). It is not included in this repository. Put it at `template/2026 GitHub Presentation Template.potx` (the `template/` folder is git-ignored), or set `GH_TEMPLATE_POTX` to its path.
- The [pptx Agent Skill](https://github.com/anthropics/skills/tree/main/skills/pptx) scripts, used to prune unused template parts and to validate the result. The build looks in `~/.copilot/installed-plugins/anthropic-agent-skills/document-skills/skills/pptx/scripts` by default; set `PPTX_SKILL_SCRIPTS` to use another copy.
- [Mona Sans](https://github.com/github/mona-sans), installed on any machine that presents or previews the decks.

## Build

From the repository root:

```bash
GH_TEMPLATE_POTX="/path/to/2026 GitHub Presentation Template.potx" python3 build/build-workshop-v2.py
```

The script writes `gh-skills-builder-workshop-light.pptx` and `gh-skills-builder-workshop-dark.pptx` to the repository root. It also writes `template/template-inspect.pptx`, a git-ignored presentation copy of the template used as the validation baseline. The notes it writes are outdated; reapply the hand edits above, then run `python3 build/sync-notes.py`.

`build-from-template.py` is the shared template helper that `build-workshop-v2.py` imports (template conversion, package pruning, and shape utilities). Running it directly only prints a pointer to `build-workshop-v2.py`.

## Validate

Validate both decks against the template baseline:

```bash
for theme in light dark; do
  python3 "$PPTX_SKILL_SCRIPTS/office/validate.py" "gh-skills-builder-workshop-$theme.pptx" \
    --original template/template-inspect.pptx
done
```

Set `PPTX_SKILL_SCRIPTS` to the skill's `scripts` folder first if you have not already.

## Preview without PowerPoint (optional)

`render-workshop.py` draws an approximate PNG of each slide and contact sheets, and prints any text it estimates will overflow:

```bash
python3 build/render-workshop.py gh-skills-builder-workshop-light.pptx render/light
python3 build/render-workshop.py gh-skills-builder-workshop-dark.pptx render/dark --slide 10
```

It reads Mona Sans from `/Library/Fonts` (macOS) and rasterizes the template's SVG artwork with Node.js and [sharp](https://sharp.pixelplumbing.com/). Install sharp with `npm install --no-save --prefix build sharp`, or set `SHARP_MODULE` to an existing `sharp` package folder. The preview is a layout check, not a faithful rendering; for example, it drops leading spaces. Always do a final pass in PowerPoint.

## Diagrams (optional)

`create-visuals.py` regenerates the earlier drawn diagrams in `visuals/` (`01`–`03` in light and dark, plus `visual-contact-sheet.png`) using the bundled Hubot Sans. The current decks use the Gemini artwork and QR code instead; see [`../visuals/slide-placement.md`](../visuals/slide-placement.md).
