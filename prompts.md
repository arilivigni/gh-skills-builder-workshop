# Prompt cards: Tailspin quick-start

**60-minute presenter workshop:** build a small GitHub Skills exercise, not the entire Dev Days lab. The resulting learner exercise takes about **15–20 minutes** and has exactly **three graded steps**.

**Scenario:** a new Tailspin Toys teammate prepares Copilot to work consistently in the repository: add one repository instruction, customize one reusable skill, and create one report-only QA agent. Tailspin provides context, not an application feature to implement.

**Working title:** *Cleared for Takeoff: A Copilot Quick-Start*
**Default repository:** `copilot-app-cleared-for-takeoff`
**Learner copy:** `skills-copilot-app-cleared-for-takeoff`

## Scope and coverage

| Required learner step | Artifact | What validation can observe |
| --- | --- | --- |
| 1. Add a TypeScript documentation convention | `.github/copilot-instructions.md` | A new, clearly delimited workshop section requires TSDoc for new or changed exported TypeScript functions, preserving existing instructions. |
| 2. Make quality reporting consistent | `.github/skills/quality-checks/SKILL.md` | The existing skill preserves its frontmatter and gains a reporting contract: command, passed/failed/blocked status, evidence, and reason for any failure or blocked check; no invented results. |
| 3. Define a report-only QA agent | `.github/agents/qa.agent.md` | Valid name/description frontmatter and instructions to report requirements with evidence, ask before implementation changes, and never commit or open PRs. |

Validate artifact requirements, not whether a learner actually invoked Copilot, a mode, a skill, or an agent. Explain that checking written instructions does not prove future model compliance. Do not accept file existence alone.

**Demonstrate:** the one orchestrator agent, all four phase skills, approval gates, one review/fix/re-review loop, and the publish authorization boundary. **Show but do not execute** the fifth skill, `/orchestrate-github-skills-exercise`, during recap.

**Extensions only:** filtering with tests, Plan/Autopilot mode practice, feature PRs, Agent Merge, Playwright MCP, and canvases. No app feature implementation, database, browser install, or npm install is required for this quick-start.

## Before you start

- Plugin listing and QR destination: [gh.io/gh-skills-builder](https://gh.io/gh-skills-builder). CLI: `copilot plugin install gh-skills-builder@awesome-copilot`; if needed, first register `copilot plugin marketplace add github/awesome-copilot`.
- Confirm the installed release, agent availability, slash commands, and mode/model controls in rehearsal. Do not depend on an old release number or unreleased local changes.
- `@github-skills-orchestrator` is the **agent**; the slash commands are **skills**.
- Use **one quick chat** for Prompt 1, Gate 1, and Hand-off Authorization; then **one project session** for Prompts 2–4.
- Replace `<you>` with an authorized demo owner and `<workshop-repo>` with the absolute path of your clone of this repository. A quick chat has no working directory, so a relative path will not work.

| Prompt | Time | Slide | Session | Mode | Model |
| --- | --- | --- | --- | --- | --- |
| 1 + Gate 1 | 0:06–0:12 | 9 | Same quick chat | Interactive | Auto → Intelligence |
| Hand-off Authorization | 0:12–0:16 | 9 (stay) | Same quick chat | Interactive | Same setting |
| 2 + Gate 2 | 0:16–0:27 | 10 | Project session | Interactive | Auto → Balance |
| 3 + optional 3b + Gate 3 | 0:27–0:35 | 11 | Same project session | Interactive | Same setting |
| 4 + 4b | 0:35–0:41 | 12 | Same project session | Interactive | Same setting |
| Whole-loop example | 0:41–0:45 | 13 | Show prompt only | Do not run | Not applicable |
| Flex buffer | 0:45–0:50 | 13–14 | No new prompts | Not applicable | Not applicable |
| Q&A | 0:50–1:00 | 14 | No new build | Not applicable | Not applicable |

**Hard stops:** outline 0:12, hand-off 0:16, build wait 0:19, review 0:30, last fix round 0:35, readiness 0:38. Content ends at 0:45; Q&A starts by 0:50, or at 0:45 if the buffer is unused.

Interactive keeps the presenter in the approval loop; it is not a security boundary. Tool permissions and explicit authorization still matter. Prefer the rehearsed controls/settings if the app labels differ; do not troubleshoot model routing on stage.

## Prompt 1: outline a three-step exercise

```text
@github-skills-orchestrator Use /create-github-skills-outline to design a 15–20-minute GitHub Skills exercise for a new Tailspin Toys teammate.

Keep exactly three graded learner steps:
1. Add a clearly delimited workshop section to .github/copilot-instructions.md requiring TSDoc for new or changed exported TypeScript functions. Preserve existing instructions.
2. Customize .github/skills/quality-checks/SKILL.md so reports include command, passed/failed/blocked status, evidence, and reasons for failed or blocked checks. Preserve frontmatter. Never invent command results.
3. Create .github/agents/qa.agent.md with name and description frontmatter. It reports requirements with evidence, asks before implementation changes, and never commits or opens PRs.

For each step include a short Theory block, one Activity, success criteria, a repository-observable validation signal, and useful failure feedback. Validate the content of learner artifacts, not just file existence. Do not claim Actions can prove which local app mode or agent was used.

This is a small slice of the Dev Days Copilot app scenario, not a conversion of the full lab. Do not add filtering, application changes, dependency installation, database setup, browser tests, feature PR/merge requirements, or extra graded steps. Mention Agent Merge, MCP, and canvases only as optional next steps.

Propose a title and three lowercase-hyphenated repository names containing copilot-app, without a skills- prefix. Recommend one.

We are in a quick chat with no repository. After I approve the identity and outline, return the complete standalone exercise-outline.md content in one Markdown code block. Start with # <approved title>, then Repository name: <approved name>, then Learner copy: skills-<approved name>. Do not claim a file has been saved.
```

**Gate 1 — approve the idea, not repository creation.** Use the room's chosen identity; the following is the rehearsed default:

```text
Approved. Use "Cleared for Takeoff: A Copilot Quick-Start" and repository name copilot-app-cleared-for-takeoff. Keep exactly the three approved learner steps. Return the complete outline artifact in one Markdown code block, including the title, Repository name, and Learner copy header. Do not create a repository or claim to have saved a file.
```

Copy the whole returned block, including its identity header. Cap the vote at 30 seconds. At 0:12, use the saved outline if generation is unfinished; do not wait indefinitely.

## Hand-off Authorization: one quick chat to one project session

| Approval | Meaning | Side effect |
| --- | --- | --- |
| Gate 1 | Approve outline and identity | None |
| **Hand-off Authorization** | Run the existing script once | Private authoring repo, starter commit, and push |
| Phase IV publish authorization | Publish to the named owner/repository | Public learner-facing template; **not authorized on stage** |

In the **same quick chat**, replace `<workshop-repo>`, `<you>`, and the repository name below:

```text
Hand-off Authorization: I authorize running this existing workshop script once to create my private authoring repository, import the Tailspin starter code, commit, and push. This is not permission to publish a public template or run the exercise lifecycle.

<workshop-repo>/handoff.sh <you> copilot-app-cleared-for-takeoff

Show the output and local folder path. Do not create other repositories or files beyond the script's work.
```

`handoff.sh` imports Tailspin as one MIT starter commit. It keeps the license and supporting files, and drops the upstream issue sources (`.github/bootstrap-issues/`), the issue-seeding and triage workflows, and CODEOWNERS. Step 0 of the exercise opens only the exercise instructions issue.

1. Approve any command permission request after inspecting it. Do not assume a permission dialog will appear in every configuration.
2. If chat execution is unavailable, use the terminal for the same authorized command. If a run has started or its outcome is uncertain, stop and inspect its output, the remote repo, and the local folder before retrying. Do not run the script concurrently or blindly repeat repo creation.
3. In the Copilot app, **Add project** using the printed folder, then start a **New session** on `main`, **Interactive**, **Auto → Balance**.
4. Paste Prompt 2 plus the whole outline artifact. A new session cannot see the quick-chat history.

**Hard stop: 0:16.** If the hand-off is not complete, use the pre-added rehearsal project at `00-idea`. Say it is a rehearsal fallback. Match the outline identity to that repo before proceeding.

**Saved outline fallback:** `fallback/exercise-outline.md` is a file, not a checkpoint branch. Save it during rehearsal. If switching repos, update its title, repository name, and learner-copy header together.

## Prompt 2: bootstrap only the small exercise

```text
@github-skills-orchestrator Phase I is approved. Use /bootstrap-github-skills-exercise with this outline artifact:

<paste the approved outline artifact>

First save that artifact verbatim to .github/exercise-outline.md. Use its identity header for the README and Copy Exercise badge. Stop and ask if its repository name differs from this repo.

Build exactly three graded steps plus the standard completion/review material. Preserve Tailspin's MIT LICENSE and credit github-samples/tailspin-toys in the README.

Do not complete the learner tasks: leave the new TSDoc workshop section, the quality-reporting contract, and qa.agent.md for the learner to add. Inspect the existing starter files first so validation requires a meaningful learner change instead of passing the baseline.

Step 0 opens the normal exercise instructions issue only; do not seed any other issues. Keep existing Tailspin workflows intact, but do not depend on their checks for exercise progression.

Use lightweight artifact checks for all three steps. Do not run or require npm ci, app builds, database setup, Playwright, or application tests. Check frontmatter and required reporting/behavioral instructions with helpful failure feedback, not file-exists or arbitrary whole-file text matching alone.

Follow the GitHub Skills workflow contract, use scoped permissions, and inspect workflow event/path interactions. Report what was actually validated and what remains untested. Do not publish or create another repository.
```

Cap waiting at three minutes: at 0:19, switch to the rehearsal `02-bootstrapped` state if the build is not ready to inspect.

**Gate 2 — approve the build before review:**

```text
I accept this build round. Do not make more changes. I will send the report-only review request next.
```

Now send Prompt 3. If the build has unresolved failures, do not claim acceptance or move it toward publication; show the known-good rehearsal build instead.

## Prompt 3: report-only review

```text
@github-skills-orchestrator Use /review-github-skills-exercise. Report findings without editing files.

Check the approved three-step scope, learner clarity and accessibility, workflow safety, and validation reliability. In particular:
- The untouched starter must not already pass the three learner checks.
- Each correct learner artifact should pass; an incomplete or incorrect artifact should fail with useful feedback. Inspect and, where feasible, exercise those cases.
- Step 0 must open only the exercise instructions issue and create no other issues.
- No grade should depend on npm, an app build, browser tooling, or proof that the learner used a local Copilot mode.
- Repository-observable checks of written policies must not be described as proof of model behavior.

Prioritize actual release blockers and include evidence and untested risks. If no findings are supported, say so; do not invent a finding for the demo.
```

### Prompt 3b: one bounded fix round, only for a real finding

Replace `<finding-id>` with the actual finding you choose:

```text
I approve a bootstrap fix round for <finding-id> only. Make the targeted fix and run its relevant checks. Stop for my build approval before running the review again.
```

After inspecting the fix:

```text
I accept the fix round. Re-run the report-only review with the same criteria.
```

If no live finding needs fixing, show a clearly labeled rehearsal finding and before/after example instead. At 0:30, use the saved review if the live one is unfinished. At 0:35, start no further fix rounds.

**Gate 3 — only if supported by the review:**

```text
No known release blockers remain in the reviewed build. Prepare release-readiness materials only; do not publish.
```

If blockers remain, show their status honestly and use the reviewed rehearsal build for the next phase.

## Prompt 4: release readiness, not live publication

```text
@github-skills-orchestrator Use /publish-github-skills-exercise for the approved three-step exercise. Read its identity from .github/exercise-outline.md.

Prepare a short readiness report: validation evidence, untested risks, a PR description, brief release notes, and a launch checklist. Clearly separate completed checks from required fresh-copy testing.

Do not create or transfer repositories, change visibility, push, or publish. Stop at the authorization boundary.
```

### Prompt 4b: show the public-template authorization boundary

Set an actual demo owner and the approved name, but **do not authorize execution**:

```text
Use /publish-github-skills-exercise to show, without executing, a plan for publishing this exercise to <demo-owner>/<approved-name> as a public template.

Show the exact target, visibility, changes, commands, and readiness blockers. Wait for separate explicit authorization. This message is not authorization to create, push, transfer, change settings, or publish.
```

The private authoring repo and public learner template have different purposes. The live workshop ends with readiness evidence and a proposed publication plan, not a claim that the live build has been released.

At 0:38, show the saved readiness report if generation is unfinished. End Phase IV by 0:41.

## Recap: the fifth skill (show, do not run)

```text
@github-skills-orchestrator Use /orchestrate-github-skills-exercise to coordinate the same three-step Tailspin quick-start. Read the approved outline from .github/exercise-outline.md. Stop after each build for approval; review without edits; request separate approval for fixes and any publication. Do not expand the scope or publish without explicit authorization.
```

Explain that this skill sequences the same lifecycle; it is not a second agent. Do not start a second full build during recap. Content ends by 0:45.

## Extensions and persona swaps (discussion only)

| Extension | What changes in a longer exercise |
| --- | --- |
| Filter games | Add feature implementation and behavioral tests, with its own issue and app prerequisites. |
| Plan and Autopilot | Practice local app modes; grade resulting artifacts, not unobservable mode usage. |
| PR and Agent Merge | Add a feature PR and separately authorized merge flow; inspect repository policies first. |
| MCP and canvases | Optional local exploration, not required for Actions grading. |
| Educator | Apply the same three artifact types to a classroom coding convention. |
| Maintainer | Teach contributor instructions, quality reporting, and review expectations. |
| Enterprise | Onboard a teammate to team-specific policies with explicit approval boundaries. |
