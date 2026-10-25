# Rebuilding the decks

The committed decks in the repository root are ready to present. Speaker notes are maintained in [`../run-of-show.md`](../run-of-show.md), not in the build script; see [Speaker notes](#speaker-notes). Rebuild the decks only after changing slide text or artwork in `build-workshop-v2.py`.

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

Inside a notes block, use only `**bold**`, inline code (shown without backticks), `- ` bullets, and fenced code blocks (shown in Courier New, one notes paragraph per line). The script rejects links, headings, numbered lists, and a raw `<` outside code, so the Markdown and the deck notes stay identical.

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
