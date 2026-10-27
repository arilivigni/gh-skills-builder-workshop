# Demo pre-stage checklist: Tailspin quick-start

Prepare the **three-step** Copilot customization exercise, not the former five-step filtering lab. The presenter session is 60 minutes; the resulting learner exercise is about 15–20 minutes. The [run of show](run-of-show.md) has the hard stops, the speaker notes, and the exact wording of every prompt.

## Scope lock

- [ ] Exactly three graded steps: TSDoc repository instruction, evidence-based quality-checks reporting contract, and report-only QA agent.
- [ ] No required filtering, application changes, dependency installation, database, browser tests, feature PR/merge, or local-mode verification.
- [ ] Agent Merge, Plan/Autopilot, filtering, and MCP are discussion-only extensions. Prompt 3a is an optional read-only browser canvas preview for the presenter, not a graded learner task.
- [ ] `handoff.sh` imports Tailspin without its upstream issue sources (`.github/bootstrap-issues/`). Step 0 opens only the exercise instructions issue, not a separate feature issue.
- [ ] Do not reuse old five-step outline artifacts, checkpoint builds, review findings, or recordings as quick-start evidence.

## Rehearse the hand-off

- [ ] Confirm the presenting account can create the private demo repo and push workflow files. Check `gh auth status` and repository/org policy; request only the permissions actually needed.
- [ ] Clone this workshop repo to the presenting machine. In the Hand-off Authorization prompt, replace `<workshop-repo>` with the clone's absolute path; a quick chat has no working directory.
- [ ] Inspect `handoff.sh`. Rehearse its local `--dry-run` using a fresh destination (it still clones Tailspin, so it needs network), then a separately authorized throwaway remote run. Do not run against a production repo.
- [ ] Confirm the import preserves the Tailspin MIT license and expected instruction/skill files, and removes the upstream issue sources, issue-seeding and triage automation, and CODEOWNERS as documented.
- [ ] Expect two harmless leftovers after the hand-off push: Tailspin's own README still mentions its issue-seeding workflow and links the removed CODEOWNERS until Prompt 2 replaces the README, and Tailspin's `run-tests.yml` runs once on the push.
- [ ] In **one quick chat**, rehearse Prompt 1, Gate 1, and **Hand-off Authorization**. Confirm actual agent/command availability and any approval UI. Do not promise a dialog that the current configuration does not show.
- [ ] Rehearse the terminal fallback. If chat execution may already have started, inspect its result and local/remote state before retrying. Never duplicate an in-flight repo creation.
- [ ] Rehearse **Add project**, new session on `main`, Interactive / Auto → Balance, then pasting the full outline artifact into Prompt 2. Budget four minutes for the hand-off, not one.
- [ ] Keep the intended live repo name available. If it already exists, choose a fresh name and update the outline and commands; do not delete a repo as routine live setup.

## Build the rehearsal and fallback assets

- [ ] Create a separate rehearsal repo, for example `copilot-app-cleared-for-takeoff-rehearsal`, with the same script. Add it as a project ahead of time.
- [ ] Inspect the actual starter files before generating checks. Existing instructions or quality skill text must not accidentally satisfy the new learner criteria without a change.
- [ ] Run Prompts 1–4 against the three-step scope. Save the approved outline block, with title, `Repository name:`, and `Learner copy:`, as `fallback/exercise-outline.md` in your clone of this repo. This is a **file, not a branch**.
- [ ] Capture the following checkpoint branches in the rehearsal repo. Keep evidence files separately accessible; a branch alone does not preserve chat output or a live workflow result.

| Branch | State |
| --- | --- |
| `00-idea` | Tailspin starter commit; learner tasks not completed |
| `02-bootstrapped` | Approved outline, README/badge, three step files, completion material, exercise workflows and validators |
| `03-reviewed` | Reviewed three-step build; approved fix applied if there was a real finding |
| `04-publish-ready` | Reviewed build plus readiness materials; no implication that public release is authorized |

- [ ] Save `fallback/review-findings.md` with actual findings or an honest no-findings report. If a genuine finding is available, save the fix diff and re-review evidence as `fallback/fix-and-rereview.md`. Do not inject a defect to manufacture a live finding.
- [ ] Rehearse optional Prompt 3a: the browser canvas shows the full README, all numbered steps in numeric order, and completion material with working navigation and local images, without changing exercise files or uploading private content. Check that temporary preview files stay outside the repo and any server binds only to loopback. Leave the rehearsal project's canvas open as the fallback if the live one is unavailable or slow.
- [ ] Decide before presenting what Prompt 3a replaces. If it runs live, show the saved fix from `fallback/fix-and-rereview.md` instead of a live Prompt 3b fix round, so Phase III still ends by 0:35.
- [ ] Save `fallback/publish-readiness.md` with checks performed, risks, PR description, release notes, launch checklist, and unexecuted publication plan.
- [ ] Save `fallback/learner-validation.md` with a baseline-fail/correct-change-pass example and links or captured output identifying the tested revision and learner copy. Keep that copy separate from the authoring template.
- [ ] Pre-stage the learner copies for the Phase II fail-to-pass demo. The live authoring repo never becomes a template on stage, so these must come from the rehearsal build:
  1. In the rehearsal repo, turn on **Settings → Template repository**. It can stay private.
  2. Use **Use this template** to create two learner copies, one for the live demo and one as a backup. Wait for each Step 0 issue to open.
  3. In both copies, trigger a failing Step 1 run, for example with an incomplete `.github/copilot-instructions.md` edit, so the feedback comment is visible. Confirm the trigger in the generated step 1 workflow.
  4. Complete Step 1 in the backup copy only; it becomes the passed-state fallback. A copy can pass Step 1 only once, so don't rehearse the pass in the live copy.
  5. Save the correct TSDoc workshop section where you can paste it on stage.

## Validate the learner path before presenting

- [ ] Run the generated artifact validators without application dependency installs. Do not substitute an app test suite for the three learner checks.
- [ ] For each step, check untouched starter, incomplete/incorrect work, and correct work. Verify clear failure feedback, preservation of existing content/frontmatter, and appropriate progression.
- [ ] Check that the completed step 1 convention is scoped to new/changed exported TypeScript functions, not arbitrary comments.
- [ ] Check that step 2 requires command, status, evidence, and reasons for failed/blocked checks, and never presents fabricated results as observed.
- [ ] Check step 3 frontmatter plus evidence reporting, asking before implementation changes, and no commits/PRs. Do not describe policy text as proof of actual model behavior.
- [ ] Check least-privilege permissions, event/path filters, and interactions with retained Tailspin workflows. Exercise progression must not require unrelated app CI to finish.
- [ ] Separately authorize a throwaway template publication during rehearsal, then create a fresh learner copy with Copy Exercise. Confirm Step 0 opens only the normal exercise issue, each step advances, and completion works. Record actual evidence; do not mark this done from local inspection alone.
- [ ] Check MIT attribution and README identity/badge consistency. Do not publish a template with the learner solutions already present.

## Time and recordings

- [ ] Run the exact 60-minute agenda with a stopwatch, including three-name selection, outline transfer, repo creation, Add project, one feedback example, review, and readiness. Content should finish by 0:45 in rehearsal, leaving the 0:45–0:50 buffer unused.
- [ ] Rehearse hard stops: outline 0:12, hand-off 0:16, build wait 0:19, review fallback 0:30, last fix round 0:35, readiness fallback 0:38, content end 0:45, Q&A 0:50.
- [ ] Record `clips/phase-1.mp4` through `clips/phase-4.mp4`, about 60–90 seconds each. Label rehearsal output and any speed-up honestly. Use the same small scope and app settings as the live run. Clips are git-ignored; keep them on local disk.
- [ ] If no genuine live finding exists, rehearse showing the saved before/after example rather than asking the reviewer to invent one. If there is no genuine saved finding either, explain the fix approval prompt without claiming a fix was needed.

## Day before

- [ ] Install/enable the plugin from [gh.io/gh-skills-builder](https://gh.io/gh-skills-builder). CLI: `copilot plugin install gh-skills-builder@awesome-copilot`; if necessary register `copilot plugin marketplace add github/awesome-copilot` first.
- [ ] Record and rehearse the installed release. Marketplace availability is not the same as unreleased local changes.
- [ ] Confirm one agent and five skill commands: orchestrate, outline, bootstrap, review, publish. Rehearse actual app UI rather than assuming quick-chat tools or Auto tiers are available.
- [ ] Rehearse the install demonstration in at most 60 seconds, or plan to skip it. Attendees can install later; their setup is not a dependency for the presenter demo.
- [ ] Verify Interactive settings; prefer Auto → Intelligence for the quick chat and Auto → Balance for the project session, where available.
- [ ] Open the light/dark decks and confirm the QR resolves. Check that the slide 2 agenda matches the run-of-show times, and run `python3 build/sync-notes.py --check` to confirm both decks' speaker notes match the run of show.
- [ ] Keep the presenting machine's fonts/display setup and local backup artifacts ready; do not depend on downloading assets on stage.

## Day of: T-30 minutes

- [ ] Confirm auth, network, venue QR/link access, and backup connection. Do not expose tokens on screen.
- [ ] Put the chosen deck on the shared screen, and open the [run of show](run-of-show.md) on GitHub on your own display so its prompts have copy buttons. You don't need presenter view.
- [ ] Start a fresh quick chat. Keep the pre-added rehearsal project available and a terminal ready as the command fallback.
- [ ] Open the live learner copy at its failing Step 1 feedback, the passed backup copy, and the saved baseline-fail/correct-change-pass evidence. Keep the TSDoc section ready to paste.
- [ ] Keep the rehearsal project's browser canvas open as the Prompt 3a fallback.
- [ ] Open all fallback Markdown files and verify they describe the three-step quick-start. Match identity headers when using a different repo.
- [ ] Copy all clips and reports to local disk, not a network/cloud-only location. Test-play every clip with the actual display/audio. If any is unavailable, choose the matching saved evidence beforehand; repo branches alone do not replace an offline Actions result.
- [ ] Enable Do Not Disturb, use readable editor/app font sizes, and hide unrelated windows.
- [ ] Put a visible timer at 0:00. End content by 0:45 and protect the 0:50 Q&A start.

## Safety and honesty

- Private authoring repo creation requires **Hand-off Authorization**, separate from Gate 1.
- Public template publication, transfer, visibility changes, and merges are not authorized by a request to show their plan.
- Never claim generation succeeded, blockers were cleared, or fresh-copy tests passed without evidence.
- Stop live generation at the time boxes and disclose rehearsal fallbacks. Do not delete, overwrite, or force-switch a dirty live build to rescue the schedule.
