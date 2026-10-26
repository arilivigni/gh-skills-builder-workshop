# Workshop visuals

## Delivery scope update

The decks and their speaker notes use the three-step Tailspin quick-start (repository instructions, quality-checks reporting, and a report-only QA agent) and the 60-minute agenda in `../run-of-show.md`. Slide text changed on slides 2, 5, 9, 10, and 13 to match; layouts and artwork are unchanged. Filtering, Agent Merge, MCP, and canvases are extensions, not required live activities.

The decks have 14 presented slides, plus the original title slide kept as a hidden backup (slide 15). They use the six Gemini-generated JPEGs, paired in light and dark themes. They are embedded losslessly as PNGs, preserving the original pixels and aspect ratio. Each composition includes its own title, so no second title is overlaid.

| Gemini artwork | Deck placement | Teaching point |
| --- | --- | --- |
| Agent/skill map | Slide 7 | One coordinating agent loads five skills, including the orchestration skill. |
| Approval-gated lifecycle | Slide 8 | Four phases, human approval between stages, explicit publication authorization. |
| Review/fix circuit | Slide 11 | Review is report-only. Approved fixes use a separate bootstrap round, followed by build approval and re-review. |

Source mapping is recorded in `build/build-workshop-v2.py`. `visual-contact-sheet.png` previews the earlier drawn PNGs, not the Gemini artwork. Those original PNGs remain available but are not used in the rebuilt decks.

## Bento deck and website

`build/build-bento.py` takes the dark deck's artwork (the three Gemini images, the title-slide rail, the headshot, the background texture, and the QR code) straight from `gh-skills-builder-workshop-dark.pptx`. It does not use the files in this folder. The Bento deck keeps the same slide numbers, and the website shows the three Gemini images in its lifecycle section. Both use WebP copies, at most 1920 pixels wide, to keep the page light. The QR code is copied byte for byte from the deck, so it scans exactly as it does on slides 4 and 14.

## Typography

Native slide text uses the template's Mona Sans Display and Mona Sans fonts. Text inside the Gemini images is baked into the artwork; its exact font family cannot be verified or edited as PowerPoint text.

The earlier drawn PNGs use Mona Sans Display Bold for titles, Mona Sans Regular for body text, and Hubot Sans Bold/SemiBold for labels. Hubot Sans (SIL OFL) is bundled in `build/fonts/` with its licence.

## Label mapping

- Orchestration skill: `/orchestrate-github-skills-exercise`
- Outline: `/create-github-skills-outline`
- Bootstrap: `/bootstrap-github-skills-exercise`
- Review: `/review-github-skills-exercise`
- Publish: `/publish-github-skills-exercise`
- Agent: `@github-skills-orchestrator`

The illustrated review is the orchestrator's self-review, not an independent reviewer or a tool-permission boundary. A repeated finding after two fix rounds must be escalated.

## QR and installation

The supplied `gh-qr-gh-skills-builder.png` is embedded unchanged on slides 4 and 14. Its accompanying link is https://gh.io/gh-skills-builder, which resolves to the Awesome Copilot plugin listing.

The primary CLI command is `copilot plugin install gh-skills-builder@awesome-copilot`. Older/custom installations may need `copilot plugin marketplace add github/awesome-copilot` once first. The slide 4 section of `../run-of-show.md` includes sources, installation alternatives, and the distinction between marketplace-pinned releases and unreleased local changes.
