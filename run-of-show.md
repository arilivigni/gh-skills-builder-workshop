# Run of show: an idea to a small GitHub Skills exercise in 60 minutes

**Format:** presenter-led live walkthrough, not a full participant lab. Participants can follow the prompts later; do not wait for every attendee to install or build.
**Plugin:** [gh-skills-builder](https://gh.io/gh-skills-builder): one `@github-skills-orchestrator` agent and five skills.
**Companions:** [Prompt cards](prompts.md) and [pre-stage checklist](demo-prestage-checklist.md).

## The smaller scenario

Build *Cleared for Takeoff: A Copilot Quick-Start*, a **15–20-minute learner exercise** inside Tailspin Toys. This is a small slice inspired by the [Dev Days Copilot app lab](https://github-samples.github.io/copilot-workshops/real-world-development/app/), not a conversion of that whole workshop.

The learner makes exactly three small changes: add a TSDoc convention to `.github/copilot-instructions.md`, give the existing `quality-checks` skill a consistent evidence-based reporting format, and create a report-only `qa.agent.md`. No filtering feature, app installation, database, browser tooling, or feature merge is required.

We demonstrate outline, bootstrap, review/fix/re-review, and release readiness. We show the whole-loop orchestration prompt without running it again. Filtering, local modes, Agent Merge, MCP, and canvases are brief extensions, not additional live demos.

**Success at minute 60:** the audience has seen the full builder lifecycle, the outline-to-repo hand-off, observable learner validation and feedback, and explicit human approvals. The live build is not represented as publicly released or fully tested unless evidence supports it.

## Agenda and hard stops

Content ends at **0:45**. The **0:45–0:50 flex buffer** absorbs overruns; if it is not needed, open Q&A early. **Q&A from 0:50 is protected.**

| Time | Min | Segment | Slides | Hard stop / fallback |
| --- | --- | --- | --- | --- |
| 0:00–0:06 | 6 | Stage: plugin, install, scenario, agent and skills | 1–8 | Install demo 60 seconds at most, or skip it. |
| 0:06–0:12 | 6 | Phase I: outline and Gate 1 | 9 | **0:12:** saved `fallback/exercise-outline.md`. |
| 0:12–0:16 | 4 | Hand-off Authorization and project session | 9 (stay) | **0:16:** rehearsal project at `00-idea`. |
| 0:16–0:27 | 11 | Phase II: bootstrap and one fail-to-pass check | 10 | **0:19:** stop waiting; use rehearsal `02-bootstrapped`. |
| 0:27–0:35 | 8 | Phase III: report-only review and one approved fix | 11 | **0:30:** saved review. **0:35:** no more rounds. |
| 0:35–0:41 | 6 | Phase IV: readiness, no publication | 12 | **0:38:** saved readiness report. |
| 0:41–0:45 | 4 | Recap: fifth skill shown, not run | 13 | Content ends at 0:45. |
| 0:45–0:50 | 5 | Flex buffer | 13–14 | Absorb overruns; if unused, start Q&A. |
| 0:50–1:00 | 10 | Protected Q&A and plugin link | 14 | Never start another build. |

## Session settings and decks

Use **one quick chat** for Prompt 1, Gate 1, and Hand-off Authorization. Then use **one project session** for Phases II–IV. Choose **Interactive** throughout, with **Auto → Intelligence** for the outline and **Auto → Balance** for the project session, if those controls are available. Rehearse the actual app version and settings. Do not treat mode selection as an enforced authorization boundary or promise a particular routed model.

The light and dark decks match this run-of-show: slide text and speaker notes use the quick-start scenario, and each slide's notes start with its time window. If a note and this document ever disagree, follow this document. Do not use recordings or checkpoint builds from the earlier five-step filtering exercise.

## 0:00–0:06: set the stage (slides 1–8)

- **0:00–0:01 (slides 1–2):** welcome and promise: "We'll build a small exercise that teaches three Copilot customization habits, and see all four builder phases." Point at the flight plan: content ends at 0:45, and Q&A starts by 0:50.
- **0:01–0:03 (slides 3–4):** define a plugin as an installable bundle of reusable capabilities, not another model. Show [the listing](https://gh.io/gh-skills-builder), the QR, and the installed plugin. **Cap any install demo at 60 seconds, or skip it.** CLI: `copilot plugin install gh-skills-builder@awesome-copilot`; marketplace registration if needed: `copilot plugin marketplace add github/awesome-copilot`.
- **0:03–0:04 (slide 5):** explain the three learner artifacts. "We are building the learning journey, not coding a Tailspin feature." The Tailspin app is MIT starter context.
- **0:04–0:05 (slide 6):** builder to architect. Take a 10-second show of hands at most; skip it if behind.
- **0:05–0:06 (slides 7–8):** distinguish the one agent from five skills. Four skills do the stage work; the orchestration skill sequences them. Humans approve the outline, build acceptance, fixes, and publication.

## 0:06–0:12: Phase I, a small outline (slide 9)

Paste **Prompt 1** in the quick chat. Narrate one Theory/Activity pair and its validation signal while it generates. Ask: "What would prove the learner changed the reporting contract, rather than merely created a file?"

Show three title/name candidates; cap the vote at 30 seconds and use the rehearsed default if needed. Send **Gate 1 once**, then check the returned artifact starts with the approved title, `Repository name:`, and `Learner copy:`. Copy the entire block. It is not saved to a repo yet.

**Hard stop 0:12:** if the response is unfinished, use `fallback/exercise-outline.md`, disclose that it is from rehearsal, and match its identity to the target repo. Do not spend the rest of the workshop waiting for the outline.

## 0:12–0:16: Hand-off Authorization (stay on slide 9)

Say: "Gate 1 approved the idea and created nothing. This is a separate Hand-off Authorization for one private authoring repo. Publishing a public template is a different gate."

In the **same quick chat**, send the Hand-off Authorization from `prompts.md`, with the correct owner, repository name, and `<workshop-repo>` path. Inspect any permission request before approval. `handoff.sh` creates the private repo and imports Tailspin as one MIT starter commit, without the upstream issue sources, issue-seeding and triage workflows, or CODEOWNERS. Step 0 will open only the exercise instructions issue.

If chat execution is unavailable, run the same authorized command in the terminal. If a command may already be running or has partly succeeded, inspect its output and local/remote state first; do not launch a duplicate or delete the partial repo.

Add the printed local folder as a project and open a new session on `main`, Interactive, Auto → Balance. The outline must be pasted because this session cannot see the quick chat.

**Hard stop 0:16:** switch to the pre-added rehearsal project at `00-idea` if necessary. Match the outline header to that repo and identify the fallback explicitly.

## 0:16–0:27: Phase II, scaffold and one feedback loop (slide 10)

Paste **Prompt 2**, replacing only its outline placeholder with the complete approved artifact. Show `.github/exercise-outline.md`, the README and Copy Exercise badge, three learner step files, completion material, and workflow chaining. The learner's work must remain unsolved.

**Cap waiting for live generation at three minutes.** At **0:19**, if output is not ready to inspect, move to the rehearsal project's `02-bootstrapped` state. Say: "This is the same small scope built during rehearsal."

Use the remaining time to show one short example, ideally step 1:

1. Untouched starter fails with an actionable message.
2. Add the required TSDoc workshop section in a separate disposable learner copy, not the authoring template.
3. Show that check passing and the next step becoming available.

Use a rehearsed learner copy and saved evidence or a short clip if GitHub Actions is slow. Label saved output honestly. Do not run the entire learner journey or install app dependencies live. Explain that the check validates a written artifact, not future Copilot behavior.

**Gate 2, by 0:27:** accept the build only if its evidence supports acceptance, then request the report-only review. Otherwise use the known-good rehearsal build and state the live build's remaining problems.

## 0:27–0:35: Phase III, review then an approved fix (slide 11)

Paste **Prompt 3**. Show the three key review questions: does untouched starter fail, does correct learner work pass, and is the feedback clear and safe?

**Hard stop 0:30:** use saved review findings if live review is unfinished. Pick one actual supported finding; do not manufacture a defect. Explain that review has edited nothing.

For a real live finding, use **Prompt 3b**, inspect the targeted change and its check results, then explicitly accept the fix round before re-review. If the live report has no findings, show a labeled rehearsal finding and its before/after fix instead. The rehearsal finding must come from the small exercise, not the old filtering scenario.

**Hard stop 0:35:** start no additional rounds. Use `03-reviewed` evidence if needed. Say that self-review is not independent review. Give **Gate 3** only for a build with no known release blockers; otherwise state the blockers and show the reviewed rehearsal build for Phase IV.

## 0:35–0:41: Phase IV, readiness without publication (slide 12)

Paste **Prompt 4** or show the saved `04-publish-ready` materials. Keep the output short: observed validation evidence, untested risks, PR description, release notes, and launch checklist.

Show the rehearsal's fresh learner-copy result if available. Local checks alone do not establish the exercise works on a fresh GitHub copy.

Send **Prompt 4b** with a named target to show the plan and explicit publication boundary. **Do not authorize it.** The earlier private repo creation was not permission to publish, transfer, change visibility, push, or create a public template here.

**Hard stop 0:38:** if generation is unfinished, show the saved readiness report and planned commands. End this phase at 0:41.

## 0:41–0:45: all features, without another build (slide 13)

Show the `/orchestrate-github-skills-exercise` recap prompt without executing it. We have now covered all five builder skills and the single agent.

Mention filtering/tests, local Plan/Autopilot practice, PR/Agent Merge, MCP, and canvases as extensions that deserve a longer exercise. Do not demo them. Contrast a classroom convention with a team onboarding policy: same lifecycle, different content.

Close by 0:45: "Keep the learner task small. Make success observable. Let the agent draft; keep humans at the decisions."

## 0:45–0:50: flex buffer

This time absorbs overruns; it is not for new content. If a phase ran long, finish its point here. If you are on time, move to slide 14 and open Q&A at 0:45. Never start another build or fix round in the buffer.

## 0:50–1:00: protected Q&A (slide 14)

Q&A starts no later than 0:50, or at 0:45 if the buffer was unused. Keep the plugin QR and [gh.io/gh-skills-builder](https://gh.io/gh-skills-builder) visible. Seed questions: what can Actions observe, why is review report-only, and what authorization is required to publish? Do not troubleshoot an individual installation or start another workflow.

## Fallbacks and recovery

| Hard stop | Problem | Recovery |
| --- | --- | --- |
| 0:12 | Outline unfinished | Saved `fallback/exercise-outline.md`, a file rather than a branch; update identity as needed. |
| 0:16 | Hand-off unfinished | Rehearsal project `00-idea`; inspect partial command state before any retry. |
| 0:19 | Build not ready to inspect | Rehearsal `02-bootstrapped`; show saved fail/pass evidence from `fallback/learner-validation.md`. |
| 0:30 | Review unfinished | `fallback/review-findings.md`; show one genuine rehearsal fix and re-review from `fallback/fix-and-rereview.md`. |
| 0:35 | Fix round still running | Stop; show `03-reviewed` and state what remains. |
| 0:38 | Readiness unfinished | `fallback/publish-readiness.md` and `04-publish-ready`; explain unresolved live risks. |
| Any | Network unavailable | Local clips, saved evidence, and Markdown; branches alone cannot demonstrate a new Actions run offline. |

Prepare `clips/phase-1.mp4` through `clips/phase-4.mp4`, about 60–90 seconds each, on the presenting laptop's local disk. Test-play each with the actual display and audio before the workshop. The outline fallback is a file; repo checkpoints are branches; reports and clips are separate saved artifacts, not guaranteed to exist because a branch exists. See the [fallback guide](fallback/README.md) and [clips guide](clips/README.md).

**If behind,** cut in this order: the show of hands, extra file browsing, the live fix round (show the saved before/after instead), and the live Prompt 4b run (describe the boundary instead). Keep the four phases and approval distinctions visible. Use the 0:45–0:50 buffer only for overruns, and start Q&A by 0:50 no matter what.
