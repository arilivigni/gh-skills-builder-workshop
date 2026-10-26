# Run of show: an idea to a small GitHub Skills exercise in 60 minutes

**Format:** presenter-led live walkthrough, not a full participant lab. Participants can follow the prompts later; do not wait for every attendee to install or build.
**Plugin:** [gh-skills-builder](https://gh.io/gh-skills-builder): one `@github-skills-orchestrator` agent and five skills.
**Prepare with:** the [pre-stage checklist](demo-prestage-checklist.md). On stage, this file is all you need.

## How to use this document

This file is the whole show: talk track, slide changes, prompts, and fallbacks, in presenting order. You don't need presenter view or any other file on stage.

- **🖥️ Purple banners** tell you which slide to put on screen, when, and whether to switch to the Copilot app.
- **The quoted block under each banner is that slide's speaker notes**, word for word as they appear in both decks. Each one runs in order: **SAY** (talk track), **DO** (what to click, paste, or check), and **CLOCK** (time checks and hard stops).
- **Everything you paste or run is in a code block.** On GitHub, hover the block and click its copy button. Replace any `<placeholder>` before you send.
- **"More detail" sections** are collapsed preparation notes. They are not in the deck notes.
- **To change the speaker notes, edit them here**, then run `python3 build/sync-notes.py` to copy them into both decks. Don't edit notes in PowerPoint; the next sync overwrites them. See [build/README.md](build/README.md).

## The smaller scenario

Build *Cleared for Takeoff: A Copilot Quick-Start*, a **15–20-minute learner exercise** with exactly **three graded steps**, inside Tailspin Toys. This is a small slice inspired by the [Dev Days Copilot app lab](https://github-samples.github.io/copilot-workshops/real-world-development/app/), not a conversion of that whole workshop.

A new Tailspin Toys teammate prepares Copilot to work consistently in the repository: add one repository instruction, customize one reusable skill, and create one report-only QA agent. Tailspin provides context, not an application feature to implement.

- **Rehearsed title:** *Cleared for Takeoff: A Copilot Quick-Start*. The room can vote for another at Gate 1.
- **Default repository:** `copilot-app-cleared-for-takeoff`
- **Learner copy:** `skills-copilot-app-cleared-for-takeoff`

| Required learner step | Artifact | What validation can observe |
| --- | --- | --- |
| 1. Add a TypeScript documentation convention | `.github/copilot-instructions.md` | A new, clearly delimited workshop section requires TSDoc for new or changed exported TypeScript functions, preserving existing instructions. |
| 2. Make quality reporting consistent | `.github/skills/quality-checks/SKILL.md` | The existing skill preserves its frontmatter and gains a reporting contract: command, passed/failed/blocked status, evidence, and reason for any failure or blocked check; no invented results. |
| 3. Define a report-only QA agent | `.github/agents/qa.agent.md` | Valid name/description frontmatter and instructions to report requirements with evidence, ask before implementation changes, and never commit or open PRs. |

Validate artifact requirements, not whether a learner actually invoked Copilot, a mode, a skill, or an agent. Checking written instructions does not prove future model compliance. Do not accept file existence alone. No filtering feature, app installation, database, browser tooling, or feature merge is required.

**Demonstrate:** the one orchestrator agent, all four phase skills, the approval gates, one review/fix/re-review loop, and the publish authorization boundary. **Show but do not run** the fifth skill, `/orchestrate-github-skills-exercise`, during the recap. Filtering, local modes, Agent Merge, MCP, and canvases are brief extensions, not additional live demos.

**Success at minute 60:** the audience has seen the full builder lifecycle, the outline-to-repo hand-off, observable learner validation and feedback, and explicit human approvals. The live build is not represented as publicly released or fully tested unless evidence supports it.

## Agenda and hard stops

Content ends at **0:45**. The **0:45–0:50 flex buffer** absorbs overruns; if it is not needed, open Q&A early. **Q&A from 0:50 is protected.** The decks have 14 presented slides; slide 15 is a hidden backup.

| Time | Min | Segment | On screen | Hard stop / fallback |
| --- | --- | --- | --- | --- |
| 0:00–0:06 | 6 | Stage: plugin, install, scenario, agent and skills | Slides 1–8 | Install demo 60 seconds at most, or skip it. |
| 0:06–0:12 | 6 | Phase I: outline and Gate 1 | Slide 9, then quick chat | **0:12:** saved `fallback/exercise-outline.md`. |
| 0:12–0:16 | 4 | Hand-off Authorization and project session | Stay on slide 9; quick chat | **0:16:** rehearsal project at `00-idea`. |
| 0:16–0:27 | 11 | Phase II: bootstrap and one fail-to-pass check | Slide 10, then project session | **0:19:** stop waiting; use rehearsal `02-bootstrapped`. |
| 0:27–0:35 | 8 | Phase III: report-only review and one approved fix | Slide 11, then project session | **0:30:** saved review. **0:35:** no more rounds. |
| 0:35–0:41 | 6 | Phase IV: readiness, no publication | Slide 12, then project session | **0:38:** saved readiness report. |
| 0:41–0:45 | 4 | Recap: fifth skill shown, not run | Slide 13 | Content ends at 0:45. |
| 0:45–0:50 | 5 | Flex buffer | Slide 13 or 14 | Absorb overruns; if unused, start Q&A. |
| 0:50–1:00 | 10 | Protected Q&A and plugin link | Slide 14 | Never start another build. |

## Before you start

Finish the [pre-stage checklist](demo-prestage-checklist.md) first. On stage, fill in these placeholders as you reach them:

| Placeholder | Replace with |
| --- | --- |
| `<workshop-repo>` | The **absolute** path of your clone of this repository. A quick chat has no working directory, so a relative path will not work. |
| `<you>` | The authorized demo owner for the private authoring repository. |
| `<paste the approved outline artifact>` | The whole outline block returned after Gate 1. |
| `<finding-id>` | The real review finding you choose to fix. |
| `<demo-owner>/<approved-name>` | The publication target to show, but not authorize, in Prompt 4b. |

Install the plugin from the Copilot app's Plugins page, or from the CLI:

```bash
copilot plugin install gh-skills-builder@awesome-copilot
```

If the CLI says the marketplace is unknown, register it once, then rerun the install:

```bash
copilot plugin marketplace add github/awesome-copilot
```

Confirm the install:

```bash
copilot plugin list
```

Confirm the installed release, agent availability, slash commands, and mode/model controls in rehearsal. Do not depend on an old release number or unreleased local changes. `@github-skills-orchestrator` is the **agent**; the slash commands are **skills**.

Use **one quick chat** for Prompt 1, Gate 1, and Hand-off Authorization. Then use **one project session** for Prompts 2–4.

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

Interactive keeps the presenter in the approval loop; it is not a security boundary. Tool permissions and explicit authorization still matter. Rehearse the actual app version and settings, prefer the rehearsed controls if the app labels differ, and do not troubleshoot model routing on stage or promise a particular routed model. Do not use recordings or checkpoint builds from the earlier five-step filtering exercise.

## Approvals at a glance

| Approval | When | What it approves | Side effect |
| --- | --- | --- | --- |
| Gate 1 | 0:06–0:12 | The outline and the exercise identity | None |
| **Hand-off Authorization** | 0:12–0:16 | Running `handoff.sh` once | Private authoring repo, starter commit, and push |
| Gate 2 | By 0:27 | Accepting the build before review | None |
| Fix round (Prompt 3b) | 0:30–0:35 | One targeted fix for one real finding | Edits in the authoring repo |
| Gate 3 | By 0:35 | No known release blockers; prepare readiness only | None |
| Publication (Prompt 4b) | 0:35–0:41 | A public template at a named owner/repository | **Never given on stage** |

## 0:00–0:06 · Set the stage (slides 1–8)

### Slide 1 · Welcome

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 1 of 14** · Turn any idea into a Hands-on GitHub Exercise · 0:00–0:01

<!-- speaker-notes slide=1 -->

> **0:00–0:01 · Slide 1 of 14 · Welcome**
>
> **SAY:** Welcome! I'm Ari LiVigni, Sr. Learning Advocate and Agentic AI Engineer at GitHub. In the next 60 minutes we'll turn one small idea into a self-paced, hands-on GitHub Skills exercise, using the GitHub Copilot app and the gh-skills-builder plugin.
>
> **SAY:** The exercise is Cleared for Takeoff: a 15–20-minute Copilot quick-start inside Tailspin Toys, with three graded steps. Most of this session is live. The slides set the stage, then we build it in the Copilot app and see all four builder phases: outline, bootstrap, review, and publish.
>
> **DO:** Before you start talking, have the Copilot app open with a new quick chat ready (Interactive, Auto → Intelligence) and the rehearsal project already added as a fallback.
>
> **CLOCK:** Move to slide 2 within the first minute.

<!-- /speaker-notes -->

### Slide 2 · Flight plan

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 2 of 14** · Our 60-minute flight plan · 0:00–0:01

<!-- speaker-notes slide=2 -->

> **0:00–0:01 · Slide 2 of 14 · Our 60-minute flight plan**
>
> **SAY:** Here's our flight plan. Six minutes to get oriented. Then we outline the exercise and hand it off to a private repo, bootstrap it into real files, review it, and get it ready to publish. We recap by 0:45, and Q&A starts by 0:50.
>
> **SAY:** It's mostly live, so I saved a checkpoint for every phase. If something runs slow, I'll switch to the checkpoint and tell you. You'll still see every step.
>
> **DO:** Nothing to paste. Point at each row as you name it; don't read the times aloud.
>
> **CLOCK:** Budget: orientation 0:00–0:06, outline 0:06–0:12, hand-off 0:12–0:16, bootstrap 0:16–0:27, review 0:27–0:35, publish readiness 0:35–0:41, recap 0:41–0:45, flex buffer 0:45–0:50, protected Q&A 0:50–1:00.
>
> **CLOCK:** Hard stops: saved outline at 0:12, rehearsal `00-idea` at 0:16, `02-bootstrapped` at 0:19, saved review at 0:30, no more fix rounds at 0:35, saved readiness at 0:38. If the buffer isn't needed, open Q&A at 0:45.

<!-- /speaker-notes -->

### Slide 3 · What is a plugin?

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 3 of 14** · What is a plugin? · 0:01–0:03

<!-- speaker-notes slide=3 -->

> **0:01–0:03 · Slide 3 of 14 · What is a plugin?**
>
> **SAY:** A plugin is an installable toolkit that adds reusable capabilities to GitHub Copilot. Instead of copying prompts and customization files from repo to repo, you install a bundle once and reuse it.
>
> **SAY:** gh-skills-builder bundles one agent and five skills. The agent, `@github-skills-orchestrator`, coordinates the work and asks for your approval. The skills are reusable workflows the agent loads for each job: outline, bootstrap, review, publish, and one that runs the whole loop.
>
> **SAY:** Two things a plugin is not. It's not a separate AI model; it customizes the Copilot you already use. And skills guide the agent's behavior; they don't guarantee correctness or replace your approvals.
>
> **DO:** Nothing to paste. Point at the agent, then at the skills.
>
> **CLOCK:** Slides 3 and 4 together end by 0:03.

<!-- /speaker-notes -->

<details>
<summary>More detail (not in the deck notes)</summary>

- Other plugins can bundle additional kinds of supported customizations.
- Source: [Awesome Copilot plugins](https://github.com/github/awesome-copilot/blob/main/docs/README.plugins.md).

</details>

### Slide 4 · Install the toolkit

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 4 of 14** · Add the toolkit. Start building. · 0:01–0:03

<!-- speaker-notes slide=4 -->

> **0:01–0:03 · Slide 4 of 14 · Add the toolkit. Start building.**
>
> **SAY:** gh-skills-builder is in the Awesome Copilot marketplace. Find it, review it, install it, and use it. The QR opens the plugin's listing; it doesn't install anything by itself.
>
> **SAY:** Always review an external plugin's source before you install it.
>
> **DO:** Optional: 60 seconds at most, or skip it and leave the QR up. In the Copilot app, open Plugins, find gh-skills-builder, review it, then install and enable it for this session. Or use the CLI:
>
> ```bash
> copilot plugin install gh-skills-builder@awesome-copilot
> ```
>
> **DO:** If the CLI says the marketplace is unknown, register it once, then rerun the install:
>
> ```bash
> copilot plugin marketplace add github/awesome-copilot
> ```
>
> **DO:** Confirm the install:
>
> ```bash
> copilot plugin list
> ```
>
> **CLOCK:** Leave slide 4 by 0:03. Help attendees with installation after the session, not during it.

<!-- /speaker-notes -->

<details>
<summary>More detail (not in the deck notes)</summary>

- In an interactive CLI session: `/plugin install gh-skills-builder@awesome-copilot`.
- VS Code: search Extensions for `@agentPlugins`, or run **Chat: Plugins** from the Command Palette.
- The marketplace listing is pinned to a release. New local or unreleased skill changes are not available from that listing.
- Sources: [Install a plugin](https://github.com/github/awesome-copilot#install-a-plugin) and the [gh-skills-builder listing](https://awesome-copilot.github.com/plugin/gh-skills-builder/).

</details>

### Slide 5 · Today's scenario

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 5 of 14** · Today's scenario: Tailspin Toys · 0:03–0:04

<!-- speaker-notes slide=5 -->

> **0:03–0:04 · Slide 5 of 14 · Today's scenario: Tailspin Toys**
>
> **SAY:** Here's what we'll build: Cleared for Takeoff, a 15–20-minute Copilot quick-start inside Tailspin Toys. Tailspin is a real, MIT-licensed sample app. Here it's starter code, not a feature to build.
>
> **SAY:** The learner practices three habits, one graded step each. First, add a TSDoc convention to the repository instructions. Second, give the existing quality-checks skill a consistent, evidence-based report format. Third, create a report-only QA agent.
>
> **SAY:** We're building the learning journey, not coding a Tailspin feature. No filtering, no npm install, no database, no browser tooling.
>
> **SAY:** Cleared for Takeoff is the title I rehearsed. In a minute the agent proposes a title and three repository names, and you get to vote on the exercise's identity. If we can't decide in 30 seconds, we keep this one.
>
> **DO:** Nothing to paste. Point at the three habits, then at the rehearsed title line.
>
> **CLOCK:** Move on by 0:04.

<!-- /speaker-notes -->

<details>
<summary>More detail (not in the deck notes)</summary>

- Source scenario: the [Dev Days Copilot app lab](https://github-samples.github.io/copilot-workshops/real-world-development/app/). Starter: [github-samples/tailspin-toys](https://github.com/github-samples/tailspin-toys) (MIT).
- We do not copy the Tailspin template. `handoff.sh` imports the app as one MIT starter commit and drops the upstream issue sources and their self-deleting seeding workflow, so Step 0 opens only the exercise issue.
- Prompt 1 asks for repository names explicitly, so it works with the currently indexed plugin release. Learner copies use `skills-<repo>`.

</details>

### Slide 6 · From builder to architect

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 6 of 14** · From builder to architect · 0:04–0:05

<!-- speaker-notes slide=6 -->

> **0:04–0:05 · Slide 6 of 14 · From builder to architect**
>
> **SAY:** Quick show of hands: who teaches, onboards contributors, runs events, or trains teams? Keep it to 10 seconds, and skip it if you're behind.
>
> **SAY:** Whichever you are, the pattern is the same. The agent does the heavy lifting: it drafts the step content, scaffolds the repository files, and wires up validation and feedback. You keep the human decisions: you set the learner outcomes, approve the outline and the fixes, and authorize publication.
>
> **SAY:** Your role shifts from builder to architect and reviewer, but you're still responsible for the result. Today's learner is a new Tailspin teammate, learning the team's Copilot conventions.
>
> **DO:** Nothing to paste. Raise your own hand to prompt the room.
>
> **CLOCK:** Move on by 0:05.

<!-- /speaker-notes -->

### Slide 7 · One agent, five skills

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 7 of 14** · One agent. Five skills. · 0:05–0:06

<!-- speaker-notes slide=7 -->

> **0:05–0:06 · Slide 7 of 14 · One agent. Five skills.**
>
> **SAY:** One agent, five skills. Four of the skills each own one phase: outline, bootstrap, review, and publish. The fifth, orchestrate, runs those four in order and stops at every approval.
>
> **SAY:** Skills are workflows the agent loads, not five more agents. You choose `@github-skills-orchestrator`, then either call one phase skill with its slash command, or let the orchestrate skill run the whole loop.
>
> **SAY:** Today I'll call the four phase skills one at a time, so you can see each phase. At the end I'll show the orchestrate prompt without running it.
>
> **DO:** Nothing to paste. Point at the agent, then the four phase skills, then orchestrate.
>
> **CLOCK:** Slides 7 and 8 together end by 0:06.

<!-- /speaker-notes -->

### Slide 8 · From idea to exercise

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 8 of 14** · From idea to exercise. · 0:05–0:06

<!-- speaker-notes slide=8 -->

> **0:05–0:06 · Slide 8 of 14 · From idea to exercise.**
>
> **SAY:** Four phases, each ending at a human gate. Gate 1: approve the outline before anything is generated. Gate 2: accept the build before it's reviewed. Gate 3: after the review, choose fixes or sign off. And actually publishing needs its own, separate authorization.
>
> **SAY:** These gates are instructions the agent follows, not a permission system. That's why I'll say every approval out loud and check what the agent did.
>
> **DO:** Nothing to paste. Advance to slide 9. We start with only an idea, in a quick chat: no repo yet.
>
> **CLOCK:** It's minute 6. Start Prompt 1 by 0:06.

<!-- /speaker-notes -->

## 0:06–0:16 · Phase I: outline, Gate 1, and hand-off (slide 9)

### Outline and Gate 1

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 9 of 14** · Outline: decide what success looks like · 0:06–0:12 · then switch to the Copilot app quick chat

<!-- speaker-notes slide=9 -->

> **0:06–0:12 · Slide 9 of 14 · Outline: decide what success looks like**
>
> **SAY:** Phase I is the outline. We start with only an idea and decide three things: the outcome, the exercise's identity, meaning its title and repository name, and, for every graded step, what a workflow can actually check.
>
> **DO:** **SCREEN → Copilot app.** New quick chat: Interactive, Auto → Intelligence. Paste Prompt 1:
>
> ```text
> @github-skills-orchestrator Use /create-github-skills-outline to design a 15–20-minute GitHub Skills exercise for a new Tailspin Toys teammate.
>
> Keep exactly three graded learner steps:
> 1. Add a clearly delimited workshop section to .github/copilot-instructions.md requiring TSDoc for new or changed exported TypeScript functions. Preserve existing instructions.
> 2. Customize .github/skills/quality-checks/SKILL.md so reports include command, passed/failed/blocked status, evidence, and reasons for failed or blocked checks. Preserve frontmatter. Never invent command results.
> 3. Create .github/agents/qa.agent.md with name and description frontmatter. It reports requirements with evidence, asks before implementation changes, and never commits or opens PRs.
>
> For each step include a short Theory block, one Activity, success criteria, a repository-observable validation signal, and useful failure feedback. Validate the content of learner artifacts, not just file existence. Do not claim Actions can prove which local app mode or agent was used.
>
> This is a small slice of the Dev Days Copilot app scenario, not a conversion of the full lab. Do not add filtering, application changes, dependency installation, database setup, browser tests, feature PR/merge requirements, or extra graded steps. Mention Agent Merge, MCP, and canvases only as optional next steps.
>
> Propose a title and three lowercase-hyphenated repository names containing copilot-app, without a skills- prefix. Recommend one.
>
> We are in a quick chat with no repository. After I approve the identity and outline, return the complete standalone exercise-outline.md content in one Markdown code block. Start with # <approved title>, then Repository name: <approved name>, then Learner copy: skills-<approved name>. Do not claim a file has been saved.
> ```
>
> **SAY:** While it generates: every step gets a short Theory block, one Activity, success criteria, a validation signal the repository can observe, and useful feedback for when the learner gets it wrong.
>
> **SAY:** Ask the room: what would prove the learner changed the reporting contract, rather than merely created a file? A file-exists check isn't evidence. The check has to read what the learner wrote.
>
> **SAY:** And be honest about the limits. Actions can check what the learner wrote. It can't see which app mode or agent they used, and it can't prove how the model will behave later.
>
> **DO:** Read the proposed title and three repository-name candidates aloud and take a vote: 30 seconds at most. If the room can't decide, keep the rehearsed default. Send Gate 1 once. If the room chose a different title or name, edit both in the message first:
>
> ```text
> Approved. Use "Cleared for Takeoff: A Copilot Quick-Start" and repository name copilot-app-cleared-for-takeoff. Keep exactly the three approved learner steps. Return the complete outline artifact in one Markdown code block, including the title, Repository name, and Learner copy header. Do not create a repository or claim to have saved a file.
> ```
>
> **SAY:** Gate 1 approves the idea and the name. It creates nothing: no repo, no files.
>
> **DO:** Check that the returned block starts with the approved title, then `Repository name:`, then `Learner copy:`. Copy the whole block. It isn't saved anywhere yet; you'll paste it into the project session.
>
> **CLOCK:** Hard stop 0:12. If the outline isn't finished, open the saved `fallback/exercise-outline.md`, say it's from rehearsal, and match its identity header to the target repo. Don't spend the workshop waiting for the outline.

<!-- /speaker-notes -->

### Hand-off Authorization

> [!IMPORTANT]
> 🖥️ **STAY ON SLIDE 9** · Hand-off Authorization · 0:12–0:16 · the screen stays on the same quick chat

<!-- speaker-notes slide=9 -->

> **0:12–0:16 · Still slide 9 · Hand-off Authorization**
>
> **SAY:** Gate 1 approved the idea and created nothing. Now I give a separate approval, the Hand-off Authorization. It lets the agent run one existing script, once, to create one private authoring repo. Publishing a public template is a different gate, much later.
>
> **DO:** **STAY on slide 9; the screen stays on the Copilot app.** In the same quick chat, replace `<workshop-repo>` with the absolute path of your clone of this workshop repo (a quick chat has no working directory), `<you>` with the demo owner, and the repository name if the room chose another. Then send:
>
> ```text
> Hand-off Authorization: I authorize running this existing workshop script once to create my private authoring repository, import the Tailspin starter code, commit, and push. This is not permission to publish a public template or run the exercise lifecycle.
>
> <workshop-repo>/handoff.sh <you> copilot-app-cleared-for-takeoff
>
> Show the output and local folder path. Do not create other repositories or files beyond the script's work.
> ```
>
> **DO:** Inspect the command permission request, then approve it out loud. Not every configuration shows one.
>
> **SAY:** handoff.sh creates the private repo and imports Tailspin Toys as one MIT starter commit. It keeps the license and supporting files, and drops the upstream issue sources, the issue-seeding and triage workflows, and CODEOWNERS. So when a learner starts, Step 0 opens just one issue: the exercise instructions.
>
> **DO:** If the chat can't run commands, run the same authorized command in a terminal, with the same replacements:
>
> ```bash
> <workshop-repo>/handoff.sh <you> copilot-app-cleared-for-takeoff
> ```
>
> **DO:** If a run started, or you're not sure how it ended, check its output, the remote repo, and the local folder before you retry. Never run the script twice at once, never blindly repeat repo creation, and don't delete a partial repo.
>
> **DO:** In the Copilot app, choose Add project and pick the folder the script printed. Start a New session on `main`: Interactive, Auto → Balance.
>
> **SAY:** This new session can't see the quick chat, so I'll paste the whole outline into it.
>
> **CLOCK:** Hard stop 0:16. If the hand-off isn't done, switch to the pre-added rehearsal project at `00-idea`, say it's a rehearsal fallback, and match the outline identity to that repo.

<!-- /speaker-notes -->

<details>
<summary>More detail (not in the deck notes)</summary>

- `handoff.sh` drops the upstream issue sources in `.github/bootstrap-issues/`. Step 0 of the exercise opens only the exercise instructions issue.
- The saved outline fallback, `fallback/exercise-outline.md`, is a file, not a checkpoint branch. Save it during rehearsal. If you switch repos, update its title, repository name, and learner-copy header together.

</details>

## 0:16–0:27 · Phase II: bootstrap and one feedback loop (slide 10)

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 10 of 14** · Bootstrap: make the outline runnable · 0:16–0:27 · then switch to the project session

<!-- speaker-notes slide=10 -->

> **0:16–0:27 · Slide 10 of 14 · Bootstrap: make the outline runnable**
>
> **SAY:** Phase II, bootstrap, turns the approved outline into a runnable exercise, right here in the private authoring repo. The learner gets a clear entry point with a Copy Exercise badge, issue-driven steps, and checks with useful feedback. Bootstrap doesn't create anything new on GitHub.
>
> **DO:** **SCREEN → Copilot app,** the new project session. Paste Prompt 2, replacing only `<paste the approved outline artifact>` with the whole outline block you copied:
>
> ```text
> @github-skills-orchestrator Phase I is approved. Use /bootstrap-github-skills-exercise with this outline artifact:
>
> <paste the approved outline artifact>
>
> First save that artifact verbatim to .github/exercise-outline.md. Use its identity header for the README and Copy Exercise badge. Stop and ask if its repository name differs from this repo.
>
> Build exactly three graded steps plus the standard completion/review material. Preserve Tailspin's MIT LICENSE and credit github-samples/tailspin-toys in the README.
>
> Do not complete the learner tasks: leave the new TSDoc workshop section, the quality-reporting contract, and qa.agent.md for the learner to add. Inspect the existing starter files first so validation requires a meaningful learner change instead of passing the baseline.
>
> Step 0 opens the normal exercise instructions issue only; do not seed any other issues. Keep existing Tailspin workflows intact, but do not depend on their checks for exercise progression.
>
> Use lightweight artifact checks for all three steps. Do not run or require npm ci, app builds, database setup, Playwright, or application tests. Check frontmatter and required reporting/behavioral instructions with helpful failure feedback, not file-exists or arbitrary whole-file text matching alone.
>
> Follow the GitHub Skills workflow contract, use scoped permissions, and inspect workflow event/path interactions. Report what was actually validated and what remains untested. Do not publish or create another repository.
> ```
>
> **DO:** When `.github/exercise-outline.md` appears, show it: the agent's first action saves the outline word for word. Then show the README and Copy Exercise badge, the three step files, the completion material, and how the workflows chain.
>
> **SAY:** Notice the learner's work stays unsolved. If the agent did the learner's work, every check would pass before anyone started. The Tailspin MIT license and credit stay in place.
>
> **CLOCK:** Wait three minutes at most. Hard stop 0:19: if the build isn't ready to inspect, switch to the rehearsal project's `02-bootstrapped` state and say: "This is the same small scope, built during rehearsal."
>
> **DO:** Show one fail-to-pass example for step 1, in a separate, disposable learner copy, never the authoring repo. First, the untouched starter fails with a message that says what to fix. Next, add the TSDoc workshop section. Then the check passes and the next step opens.
>
> **SAY:** That check reads what the learner wrote, which is much stronger than checking that a file exists. But it can't prove how Copilot will behave later.
>
> **DO:** If Actions is slow, use the rehearsed learner copy, the saved evidence in `fallback/learner-validation.md`, or a short clip, and say it's saved. Don't run the whole learner journey or install app dependencies live.
>
> **DO:** Gate 2, by 0:27. Accept the build only if its evidence supports acceptance:
>
> ```text
> I accept this build round. Do not make more changes. I will send the report-only review request next.
> ```
>
> **DO:** If the build has unresolved failures, don't accept it or move it toward publication. Name the remaining problems and switch to the known-good rehearsal build.
>
> **CLOCK:** Send Gate 2 by 0:27, then go to slide 11.

<!-- /speaker-notes -->

## 0:27–0:35 · Phase III: review, then one approved fix (slide 11)

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 11 of 14** · Feedback is a circuit. · 0:27–0:35 · then switch to the project session

<!-- speaker-notes slide=11 -->

> **0:27–0:35 · Slide 11 of 14 · Feedback is a circuit.**
>
> **SAY:** Phase III is review, and it's a loop: review, fix, review again. The review only reports; it changes nothing. Fixes happen only when I approve them, one at a time.
>
> **SAY:** Three questions matter. Does the untouched starter fail? Does correct learner work pass? And is the feedback clear and safe?
>
> **DO:** **SCREEN → Copilot app,** same project session, same settings. Paste Prompt 3:
>
> ```text
> @github-skills-orchestrator Use /review-github-skills-exercise. Report findings without editing files.
>
> Check the approved three-step scope, learner clarity and accessibility, workflow safety, and validation reliability. In particular:
> - The untouched starter must not already pass the three learner checks.
> - Each correct learner artifact should pass; an incomplete or incorrect artifact should fail with useful feedback. Inspect and, where feasible, exercise those cases.
> - Step 0 must open only the exercise instructions issue and create no other issues.
> - No grade should depend on npm, an app build, browser tooling, or proof that the learner used a local Copilot mode.
> - Repository-observable checks of written policies must not be described as proof of model behavior.
>
> Prioritize actual release blockers and include evidence and untested risks. If no findings are supported, say so; do not invent a finding for the demo.
> ```
>
> **CLOCK:** Hard stop 0:30. If the live review isn't finished, use the saved review in `fallback/review-findings.md`.
>
> **DO:** Pick one real, supported finding, such as a weak check, a workflow collision, or a learner accessibility issue. Don't invent a defect for the demo. Point out that the review hasn't changed any files.
>
> **DO:** Prompt 3b approves a fix for that one finding. Replace `<finding-id>` with the finding you chose:
>
> ```text
> I approve a bootstrap fix round for <finding-id> only. Make the targeted fix and run its relevant checks. Stop for my build approval before running the review again.
> ```
>
> **DO:** Inspect the change and its check results. Then accept the fix round and ask for a fresh review:
>
> ```text
> I accept the fix round. Re-run the report-only review with the same criteria.
> ```
>
> **DO:** If the live review found nothing to fix, show the labeled rehearsal finding and its before and after from `fallback/fix-and-rereview.md` instead. It must come from this small exercise, not the old filtering scenario.
>
> **SAY:** This is the agent reviewing its own work, which isn't the same as an independent review. And report-only is an instruction; it doesn't take away the agent's edit permissions. If the same finding survives two rounds, stop and escalate to a person.
>
> **CLOCK:** Hard stop 0:35: start no more fix rounds. If needed, show the `03-reviewed` checkpoint and say what remains.
>
> **DO:** Gate 3, only if no known release blockers remain:
>
> ```text
> No known release blockers remain in the reviewed build. Prepare release-readiness materials only; do not publish.
> ```
>
> **DO:** If blockers remain, name them honestly and use the reviewed rehearsal build for Phase IV.

<!-- /speaker-notes -->

## 0:35–0:41 · Phase IV: readiness without publication (slide 12)

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 12 of 14** · Publish: prepare first. Authorize separately. · 0:35–0:41 · then switch to the project session

<!-- speaker-notes slide=12 -->

> **0:35–0:41 · Slide 12 of 14 · Publish: prepare first. Authorize separately.**
>
> **SAY:** Phase IV, publish, has two halves. First, prepare the handoff: validation evidence, PR copy and release notes, a launch checklist, and known risks. Second, pause for authorization: confirm the exact owner, repository, and visibility before anything is created, pushed, or transferred.
>
> **SAY:** Release-ready content isn't permission to publish it. Today we stop at that line.
>
> **DO:** **SCREEN → Copilot app,** same project session. Stay in Interactive; never Autopilot here, because the authorization gate has to stop for you. Paste Prompt 4, or show the saved `04-publish-ready` materials:
>
> ```text
> @github-skills-orchestrator Use /publish-github-skills-exercise for the approved three-step exercise. Read its identity from .github/exercise-outline.md.
>
> Prepare a short readiness report: validation evidence, untested risks, a PR description, brief release notes, and a launch checklist. Clearly separate completed checks from required fresh-copy testing.
>
> Do not create or transfer repositories, change visibility, push, or publish. Stop at the authorization boundary.
> ```
>
> **DO:** Keep the output short: observed validation evidence, untested risks, PR description, release notes, and launch checklist. If you have the rehearsal's fresh learner-copy result, show it.
>
> **SAY:** Local checks alone don't prove the exercise works in a fresh copy on GitHub. That test is on the launch checklist.
>
> **DO:** Prompt 4b shows the publication plan. Replace `<demo-owner>/<approved-name>` with a real demo owner and the approved name, for example `<demo-owner>/copilot-app-cleared-for-takeoff`. Send it, show the plan, and do not authorize it:
>
> ```text
> Use /publish-github-skills-exercise to show, without executing, a plan for publishing this exercise to <demo-owner>/<approved-name> as a public template.
>
> Show the exact target, visibility, changes, commands, and readiness blockers. Wait for separate explicit authorization. This message is not authorization to create, push, transfer, change settings, or publish.
> ```
>
> **SAY:** Creating the private repo earlier wasn't permission to publish, transfer, change visibility, push, or create a public template. Publish can create a GitHub repository, but only with an explicit yes for the exact owner, repository, and visibility. Before that, make sure the README badge points at the approved target.
>
> **SAY:** The private authoring repo and the public learner template have different jobs. We end with readiness evidence and a proposed publication plan, not a claim that the live build has been released.
>
> **CLOCK:** Hard stop 0:38: if generation isn't finished, show the saved readiness report in `fallback/publish-readiness.md` and its planned commands. End this phase by 0:41.

<!-- /speaker-notes -->

## 0:41–0:45 · Recap: all five skills, without another build (slide 13)

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 13 of 14** · One workflow. Many learning experiences. · 0:41–0:45 · flip to the app only to show the recap prompt

<!-- speaker-notes slide=13 -->

> **0:41–0:45 · Slide 13 of 14 · One workflow. Many learning experiences.**
>
> **SAY:** That's all five skills and the one agent. The fifth skill, orchestrate, runs the same lifecycle with the same gates from one prompt. It's not a second agent. I won't run it; we just did every step by hand.
>
> **DO:** **SCREEN → Copilot app.** Show this prompt without sending it:
>
> ```text
> @github-skills-orchestrator Use /orchestrate-github-skills-exercise to coordinate the same three-step Tailspin quick-start. Read the approved outline from .github/exercise-outline.md. Stop after each build for approval; review without edits; request separate approval for fixes and any publication. Do not expand the scope or publish without explicit authorization.
> ```
>
> **DO:** **SCREEN → back to slide 13.**
>
> **SAY:** Four takeaways. Repeatable: reuse the same authoring loop for any audience. Observable: check what learners wrote, not whether a file exists. Inclusive: review clarity, navigation, and accessibility. Human-led: people approve the decisions and the final release.
>
> **SAY:** Same lifecycle, different content. An educator could teach a classroom coding convention; an enterprise could onboard teammates to a team policy. The outline and review skills work for other tutorials too; bootstrap targets the GitHub Skills format.
>
> **SAY:** A longer exercise could add filtering with tests, Plan and Autopilot practice, PRs and Agent Merge, MCP, or canvases. We won't demo those today.
>
> **SAY:** Keep the learner task small. Make success observable. Let the agent draft; keep humans at the decisions.
>
> **CLOCK:** Content ends at 0:45. The 0:45–0:50 buffer only absorbs overruns. If you don't need it, go to slide 14 and open Q&A.

<!-- /speaker-notes -->

<details>
<summary>More detail (not in the deck notes)</summary>

- SemVer and plugin CI describe plugin release hygiene. They don't guarantee that a generated exercise works; run and review it with a learner.
- Extensions and persona swaps are listed in [Extensions and persona swaps](#extensions-and-persona-swaps-discussion-only).

</details>

## 0:45–0:50 · Flex buffer

> [!IMPORTANT]
> 🖥️ **STAY ON SLIDE 13** if you're finishing a point, or **SHOW SLIDE 14** if you're on time · 0:45–0:50

This time absorbs overruns; it is not for new content. If a phase ran long, finish its point here. If you are on time, move to slide 14 and open Q&A at 0:45. Never start another build or fix round in the buffer.

## 0:50–1:00 · Protected Q&A (slide 14)

> [!IMPORTANT]
> 🖥️ **SHOW SLIDE 14 of 14** · Your next exercise starts here. · 0:50–1:00, or from 0:45 · leave it up until the end

<!-- speaker-notes slide=14 -->

> **0:50–1:00 · Slide 14 of 14 · Your next exercise starts here.**
>
> **SAY:** Your next exercise starts here. Bring an idea, and build a hands-on experience. Scan the QR or go to gh.io/gh-skills-builder: it opens the plugin's Awesome Copilot page, with one orchestrator and five Agent Skills.
>
> **SAY:** So: what could you turn into an exercise?
>
> **DO:** Leave this slide and its QR up through Q&A. If someone asks for the install command, paste it in the chat:
>
> ```bash
> copilot plugin install gh-skills-builder@awesome-copilot
> ```
>
> **DO:** If the room is quiet, seed a question. What can Actions observe? Why is review report-only? What authorization does publishing need? What would your audience practice?
>
> **CLOCK:** Q&A starts by 0:50, or at 0:45 if the buffer wasn't used. Don't troubleshoot individual installations or start another workflow. End at 1:00.

<!-- /speaker-notes -->

<details>
<summary>More detail (not in the deck notes)</summary>

- [gh.io/gh-skills-builder](https://gh.io/gh-skills-builder) resolves to the Awesome Copilot gh-skills-builder page, not directly to the source repository.

</details>

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

## Appendix: hidden slide 15

Slide 15 is the original "LIVE WORKSHOP / 60 MINUTES" title slide. It is hidden in both decks and is not presented.

<!-- speaker-notes slide=15 -->

> **Hidden backup slide · not presented**
>
> This is the original title slide, kept as a backup. If slide 1 can't be used, unhide this slide in PowerPoint, move it to the front, and present it with the slide 1 notes.

<!-- /speaker-notes -->
