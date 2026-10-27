# Copilot app Cleared for Takeoff
Repository name: copilot-app-cleared-for-takeoff
Learner copy: skills-copilot-app-cleared-for-takeoff

## Summary

In 15–20 minutes, a new Tailspin Toys teammate uses the GitHub Copilot app to add a team TSDoc rule, make quality-check reports evidence-based, and create a QA custom agent. That clears them for takeoff on feature work. Each change is graded by reading the committed files.

## Exercise identity

- **Title**: Copilot app Cleared for Takeoff (approved at Gate 1)
- **Repository name**: `copilot-app-cleared-for-takeoff` (approved at Gate 1). It starts with the product and ends with the exercise's aviation hook. It uses only lowercase letters and hyphens, has no `skills-` prefix, and is 31 characters long.
- **Learner copy name**: `skills-copilot-app-cleared-for-takeoff`
- **Target owner**: `arilivigni`. Name availability is checked at publish.
- **Copyright holder**: decide at publish. The starter `LICENSE` currently reads "Copyright GitHub, Inc."
- **Downstream use**: the README title, the Copy Exercise badge, and the default publish target use this title and repository name exactly.

## Approval record

- **Gate 1**: approved. The title, the repository name, and the three learner steps are final.
- **Steps**: three, all graded. Step 3 is the last step and posts the review.
- **Outline storage**: bootstrap saves this outline verbatim as `.github/exercise-outline.md` in the exercise repository.
- **Starter content**: the Tailspin Toys app (MIT), imported from `github-samples/tailspin-toys` at `b37109e`. Bootstrap adds exercise files on top of it. It must not modify `.github/copilot-instructions.md` or `.github/skills/quality-checks/SKILL.md`, and `.github/agents/qa.agent.md` must not exist.
- **Next**: hand off to `bootstrap-github-skills-exercise`.

## Welcome block

- **Who is this for**: developers joining Tailspin Toys, and anyone new to customizing Copilot, who use Copilot through the GitHub Copilot app.
- **What you'll learn**: how repository custom instructions, agent skills, and custom agents shape what Copilot does, and how to add to them without overwriting existing team guidance.
- **What you'll build**: a delimited TSDoc rule in `.github/copilot-instructions.md`, an evidence-based report format in the `quality-checks` skill, and a `qa` custom agent.
- **Prerequisites**:
  - A GitHub account with Copilot access.
  - The GitHub Copilot app, installed and signed in.
  - Git.
  - Basic Markdown and YAML.
  - You **don't** need Node.js. Nothing in the exercise builds the app, installs dependencies, or runs tests.
- **How long**: 15–20 minutes (three short steps).

## Learning objectives

1. Add a clearly delimited, team-specific rule to repository custom instructions while keeping every existing instruction.
2. Customize the body of an agent skill so it requires a structured, evidence-based report, without changing its frontmatter.
3. Create a custom agent with `name` and `description` frontmatter and explicit behavioral guardrails.
4. Use Copilot to draft each change, then review, commit, and push the change yourself.

## Scenario

It's your first day at Tailspin Toys, a crowdfunding site for developer-themed games, and the team builds with the GitHub Copilot app. Before you're cleared for takeoff on feature work, you complete three checks:

- Teach Copilot the team's documentation rule.
- Make sure quality-check reports show what actually ran and never fill in results that didn't happen.
- Recruit a QA co-pilot that reports with evidence but never takes the controls.

When all three pass, you're cleared for takeoff.

## Learner journey

### Step 1: Add a team TSDoc rule to Copilot's instructions (~5 min)

**📖 Theory: Repository custom instructions**

`.github/copilot-instructions.md` holds repository-wide custom instructions, which Copilot adds to its context for requests in this repository. That makes it the place for team conventions. Tailspin's file already contains agent notes, code standards, and npm guidance that teammates rely on, so you add to it rather than rewrite it. Begin and end markers around your addition let reviewers, and the grader, find, update, or remove it later. TSDoc is the standard doc-comment format for TypeScript: a `/** ... */` block with a summary plus tags such as `@param` and `@returns`.

**⌨️ Activity: Add a delimited TSDoc section**

1. In the GitHub Copilot app, add your exercise repository (`skills-copilot-app-cleared-for-takeoff`) and start a session. Use this session and its working copy for all three steps. — _(type: GitHub UI, plain instruction in the Copilot app)_
1. Send this prompt. — _(type: chat prompt)_

   ```prompt
   Update .github/copilot-instructions.md. Keep every existing line exactly as it is, and do not change any other file or run any commands. At the end of the file, add a section that starts with the line <!-- BEGIN WORKSHOP: TSDoc --> and ends with the line <!-- END WORKSHOP: TSDoc -->. Inside it, add the heading "## Workshop: TSDoc for exported functions" and a rule that every new or changed exported TypeScript function must have a TSDoc comment with a one-line summary, an @param tag for each parameter, and an @returns tag.
   ```

1. Review the diff. Only `.github/copilot-instructions.md` should change, and all of the new lines should be at the end of the file. — _(type: GitHub UI, plain instruction)_
1. Commit and push from the session's working copy. — _(type: terminal)_

   ```bash
   git add .github/copilot-instructions.md
   git commit -m "Add workshop TSDoc instructions"
   git push -u origin HEAD
   ```

   > [!NOTE]
   > You can push from any branch, including the session's own branch, and you don't need a pull request. If you push to `main`, the starter's **Run tests** workflow also runs. It isn't part of grading, so you can ignore its result.

1. Open the exercise issue and wait for the Step 1 result comment. — _(type: GitHub UI)_

**Troubleshooting**

- **Copilot rewrote, reordered, or reworded existing instructions.** Run `git restore .github/copilot-instructions.md` and send the prompt again. Your additions belong only between the markers.
- **Copilot edited other files**, such as `README.md`. The existing instructions tell agents to update the README, so this can happen. Before you commit, run `git restore <file>` on every changed file except the instructions file.
- **The markers were reworded or turned into a Markdown heading.** Copy them exactly as they appear in the prompt.
- **The Copilot app offers to run Install dependencies.** Skip it. No step needs `npm ci`. The exercise turns off the automatic install, and the command stays in the Run menu only for later use.
- **No result comment after a couple of minutes.**
  - Run `git log -1 --stat` and confirm that the commit includes the file and was pushed.
  - Then select **Actions → Step 1 → Run workflow** and choose your branch.

**Validation**

- **Success criteria**:
  - The file has exactly one begin marker and one end marker, with the begin marker first.
  - The section between them mentions TSDoc and applies the rule to new or changed exported functions.
  - Every original non-blank line is still present.
- **Validation signal**:
  - A push that changes `.github/copilot-instructions.md` runs **Step 1**.
  - Step 1 runs `.github/scripts/check-step-1.sh` against the pushed commit and posts a ✅/❌ checklist on the exercise issue.
  - The check reads only file content. It can't tell which Copilot surface, mode, or agent made the edit.
- **Failure feedback** (one line for each failed check):
  - Markers: "Add `<!-- BEGIN WORKSHOP: TSDoc -->` and `<!-- END WORKSHOP: TSDoc -->` on their own lines, once each, with the begin marker first."
  - TSDoc: "Your workshop section doesn't mention TSDoc."
  - Scope: "State that the rule applies to **new or changed exported** TypeScript **functions**." The message names whichever term is missing.
  - Preservation: "These original lines are missing or changed: … (up to 5). Restore them and keep your additions inside the markers."

**Transition**

- **Actions Trigger**: `push` to any branch with `paths: [.github/copilot-instructions.md]`, plus `workflow_dispatch` for re-checks.
- **Grading-Check**: graded, using the custom script `.github/scripts/check-step-1.sh`. All checks are case-insensitive:
  1. The begin and end markers each appear exactly once, in order.
  2. The section contains `tsdoc`.
  3. The section contains `export`, `function`, `new`, and one of `chang|modif|updat`.
  4. Every non-blank line of the starting file still appears outside the markers. The starting file comes from the repository's root commit, and trailing whitespace is ignored.
- **Learner artifact**: the original instructions, unchanged, plus a delimited workshop TSDoc section.
- **References**: [Adding repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions), [TSDoc](https://tsdoc.org/)

### Step 2: Make quality-check reports evidence-based (~5 min)

**📖 Theory: Agent skills and honest reporting**

An agent skill is a folder that contains a `SKILL.md` file. Its YAML frontmatter (`name`, `description`) tells Copilot when the skill applies, and its Markdown body tells Copilot how to do the work. Tailspin's `quality-checks` skill already covers `npm run test:unit`, `npm run lint`, and `npm run typecheck:all`. Because the frontmatter controls when Copilot picks the skill, you change only the body. A fixed report shape (command, status, evidence, reason) makes results easy to review, and a `blocked` status plus a "never invent results" rule keep Copilot honest when a check couldn't run, for example because dependencies aren't installed.

**⌨️ Activity: Add a report format to the quality-checks skill**

1. In the same session, send this prompt. — _(type: chat prompt)_

   ```prompt
   Update .github/skills/quality-checks/SKILL.md. Do not change the YAML frontmatter, do not remove existing sections, do not change any other file, and do not run any commands. Add a "## Report format" section after "## Quick Reference". It must say that every quality-check report lists each check with: the exact command, a status of passed, failed, or blocked, the evidence (for example the exit code or relevant output lines), and the reason for any failed or blocked check. Add the rule: never invent command results — if a command was not run or could not complete, mark it blocked and explain why.
   ```

1. Review the diff. The `---` frontmatter block at the top should be unchanged, and all existing sections should still be there. — _(type: GitHub UI, plain instruction)_
1. Commit and push. — _(type: terminal)_

   ```bash
   git add .github/skills/quality-checks/SKILL.md
   git commit -m "Add evidence-based report format to quality-checks skill"
   git push -u origin HEAD
   ```

1. Open the exercise issue and wait for the Step 2 result comment. — _(type: GitHub UI)_

**Troubleshooting**

- **Copilot changed `description` or another frontmatter line.** Restore the original block. `git diff` shows exactly which lines changed, and the grader compares the block to the starting version.
- **Copilot tried to run `npm ci` or the checks themselves.** Decline. This step only edits instructions and needs no dependencies.
- **Feedback says a status is missing.** Use the exact words `passed`, `failed`, and `blocked`.
- **"Report section not found."** Use a level-2 or level-3 heading that includes the word "Report."
- **You pushed this change before Step 1 passed.** Once Step 2 appears in the issue, select **Actions → Step 2 → Run workflow**.
- **A Run tests run failed or is still running.** That workflow comes with the Tailspin starter and isn't part of grading. Only the Step 2 result comment counts.

**Validation**

- **Success criteria**:
  - The frontmatter is identical to the starting version.
  - The original headings and the three npm commands are still present.
  - A new report section names the command, all three statuses, evidence, and the reason.
  - That section includes an explicit rule against inventing results.
- **Validation signal**: a push that changes the skill file runs **Step 2**. Step 2 runs `.github/scripts/check-step-2.sh` against the pushed commit and posts a ✅/❌ checklist on the exercise issue. It reads only file content.
- **Failure feedback**:
  - Frontmatter: "Your frontmatter changed. Restore it exactly:" followed by the diff.
  - Preservation: "Missing original heading(s) or command(s): …"
  - Section: "Add a `## Report format` heading (any level-2 or level-3 heading containing 'Report')."
  - Fields: "Your report section is missing: …", followed by any missing terms from `command`, `passed`, `failed`, `blocked`, `evidence`, and `reason`.
  - Honesty: "Add an explicit rule, such as 'Never invent command results; mark checks that didn't run as blocked and explain why.'"

**Transition**

- **Actions Trigger**: `push` to any branch with `paths: [.github/skills/quality-checks/SKILL.md]`, plus `workflow_dispatch`.
- **Grading-Check**: graded, using the custom script `.github/scripts/check-step-2.sh`. All checks are case-insensitive:
  1. The frontmatter block matches the root-commit version exactly, ignoring trailing whitespace.
  2. Every starting heading (`#` through `###`) is still present, along with `npm run test:unit`, `npm run lint`, and `npm run typecheck:all`.
  3. A level-2 or level-3 heading matches `report`.
  4. That section contains `command`, `passed`, `failed`, `blocked`, `evidence`, and `reason`.
  5. One sentence in that section contains a negation (`never|do not|don't|must not`) together with `invent|fabricate|make up|guess`.
- **Learner artifact**: the `quality-checks` skill with its frontmatter intact and an evidence-based report format.
- **References**: [About agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)

### Step 3: Recruit a QA custom agent (~5 min)

**📖 Theory: Custom agents with guardrails**

A custom agent is a Markdown file named `NAME.agent.md` in `.github/agents/`. It starts with YAML frontmatter (`name`, `description`, and optional settings such as `tools`), followed by instructions that define the agent's role and limits. Repository instructions apply to every request, but an agent applies only when someone selects it, which makes it the right place for a role like QA. A good QA agent states its guardrails explicitly: it reports on each requirement with evidence, asks before changing the implementation, and leaves commits and pull requests to people. You select and use the agent in your Copilot surface; the repository only stores its definition.

**⌨️ Activity: Create `.github/agents/qa.agent.md`**

1. In the same session, send this prompt. — _(type: chat prompt)_

   ```prompt
   Create .github/agents/qa.agent.md for a Tailspin Toys QA custom agent. Start the file on line 1 with YAML frontmatter containing name: qa and a one-sentence description. In the body, instruct the agent to: check work against the stated requirements and report each requirement as met or not met with evidence (file paths, line numbers, or command output); use the quality-checks skill's report format when reporting checks; always ask the user before making any implementation changes; and never commit, push, or open pull requests. Do not change any other file or run any commands.
   ```

1. Review the file. — _(type: GitHub UI, plain instruction)_
   - It's at `.github/agents/qa.agent.md`.
   - Its frontmatter starts on line 1.
   - It isn't wrapped in a code fence.
1. Commit and push. — _(type: terminal)_

   ```bash
   git add .github/agents/qa.agent.md
   git commit -m "Add QA custom agent"
   git push -u origin HEAD
   ```

1. Open the exercise issue and wait for the Step 3 result and the review comment. — _(type: GitHub UI)_

> [!TIP]
> Optional and not graded: select the **qa** agent in your Copilot surface and ask it to check whether `.github/copilot-instructions.md` contains the workshop TSDoc section, reporting on each requirement with evidence and without changing any files. GitHub Actions can't detect whether you tried this.

**Troubleshooting**

- **Wrong path or name** (`qa.md`, `.github/agent/`, `QA.agent.md`). Run `git mv <file> .github/agents/qa.agent.md`.
- **Frontmatter not detected.** Line 1 must be `---`, with no blank line before it and no ```` ```markdown ```` fence, and the block must close with `---`.
- **A guardrail check failed.** Write each guardrail as an explicit rule: "Never commit or push…", "Never open pull requests…", "Ask before making implementation changes."
- **The agent doesn't appear in your Copilot surface.** Reload the session. This doesn't affect grading.
- **A Run tests run failed or is still running.** That workflow comes with the Tailspin starter and isn't part of grading. Only the Step 3 result and the review comment count.

**Validation**

- **Success criteria**:
  - The file is at the exact path, its frontmatter starts on line 1, and `name` and `description` aren't empty.
  - The body says to report on each requirement with evidence.
  - The body says to ask before making implementation changes.
  - The body says never to commit and never to open pull requests.
- **Validation signal**:
  - A push that changes the agent file runs **Step 3 # Last step of the exercise**.
  - Step 3 runs `file-exists`, then `.github/scripts/check-step-3.sh`.
  - If both pass, it posts the review and finishes the exercise. It reads only file content, so it can't prove that anyone selected or used the agent.
- **Failure feedback**:
  - Path: "Couldn't find `.github/agents/qa.agent.md`. Check that the folder is `agents` (plural) and the file name ends in `.agent.md`."
  - Frontmatter: "Frontmatter must start on line 1 and include non-empty `name:` and `description:`."
  - Reporting: "Say that the agent reports on each **requirement** with **evidence**."
  - Ask-first: "Add a rule that the agent asks before making implementation changes."
  - No commits: "Add an explicit 'never commit' rule."
  - No PRs: "Add an explicit 'never open pull requests' rule."

**Transition**

- **Actions Trigger**: `push` to any branch with `paths: [.github/agents/qa.agent.md]`, plus `workflow_dispatch`.
- **Grading-Check**: graded. First, `skills/exercise-toolkit/actions/file-exists` checks the path. Then `check-step-3.sh` runs these case-insensitive checks:
  1. Line 1 is `---`, and a closing `---` exists.
  2. `name:` and `description:` have non-empty values.
  3. The body contains `requirement` and `evidence`.
  4. One sentence contains `ask|confirm|permission|approv` together with `chang|implement|edit|modif`.
  5. One sentence contains a negation (`never|do not|don't|must not`) together with `commit`.
  6. One sentence contains a negation together with `pull request|PRs?`.
- **Learner artifact**: `.github/agents/qa.agent.md`.
- **References**: [Creating custom agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents), [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)

## Review recap

This section feeds `.github/steps/x-review.md`.

- **Accomplishments**:
  - Added a delimited TSDoc rule to the repository custom instructions without changing the existing guidance.
  - Gave the `quality-checks` skill an evidence-based report format (command, a passed, failed, or blocked status, evidence, and reasons) and a never-invent-results rule, and kept its frontmatter intact.
  - Created a `qa` agent that reports with evidence, asks before changing code, and never commits or opens pull requests.
  - You're cleared for takeoff.
- **What's next** (optional, not part of this exercise):
  - Ship a Tailspin Toys feature with the Copilot app, using the instructions, skill, and agent you just set up.
  - Learn about Agent Merge for landing work.
  - Learn about MCP servers, which connect Copilot to external tools and data.
  - Try canvases in the Copilot app.

## File map

| File | Purpose |
| --- | --- |
| `.github/exercise-outline.md` | This approved outline, saved verbatim by bootstrap |
| `README.md` | Exercise landing page that replaces the Tailspin starter README. It includes the title "Copilot app Cleared for Takeoff", the welcome block, and a Copy Exercise badge that creates `skills-copilot-app-cleared-for-takeoff`. It also has a short "About Tailspin Toys" section and the license footer. Drop the starter README's description of the nonexistent `bootstrap-issues.yml` workflow. |
| `LICENSE` | The starter's existing MIT license. Its copyright line feeds the README footer, and the holder is decided at publish. |
| `.github/steps/1-step.md` | Step 1: Theory, Activity, branch and **Run tests** note, troubleshooting |
| `.github/steps/2-step.md` | Step 2: Theory, Activity, troubleshooting |
| `.github/steps/3-step.md` | Step 3: Theory, Activity, optional tip, troubleshooting |
| `.github/steps/x-review.md` | Recap and optional next steps |
| `.github/workflows/0-start-exercise.yml` | `Step 0 # Start Exercise`: creates the exercise issue, posts Step 1, and enables Step 1 |
| `.github/workflows/1-step.yml` | `Step 1`: runs `check-step-1.sh` and posts the results. On a pass, it posts Step 2 and swaps which step workflow is enabled. |
| `.github/workflows/2-step.yml` | `Step 2`: the same pattern, with `check-step-2.sh` |
| `.github/workflows/3-step.yml` | `Step 3 # Last step of the exercise`: runs `file-exists` and `check-step-3.sh`, posts the review, and finishes the exercise |
| `.github/scripts/check-step-1.sh` | Content validator. Reads the starting file from the root commit and emits a ✅/❌ Markdown checklist. |
| `.github/scripts/check-step-2.sh` | The same, for the frontmatter, preservation, and report checks |
| `.github/scripts/check-step-3.sh` | The same, for the frontmatter and guardrail checks |
| `.github/github-app.yml` | Starter Copilot app configuration. Bootstrap removes only the `triggers: [session.create]` entry from the **Install dependencies** script. All four Run-menu commands stay. |
| `.github/copilot-instructions.md`, `.github/skills/quality-checks/SKILL.md` | Existing starter files that the learner edits. Bootstrap must **not** modify them. |
| `.github/workflows/run-tests.yml` | Starter CI, left unchanged. It runs on pushes and pull requests to `main` and isn't part of grading. |
| `.github/agents/qa.agent.md` | Created by the learner. It must **not** exist in the starter. |

Every step workflow:

- sets explicit `permissions` (`contents: read`, `actions: write`, `issues: write`),
- includes comments that explain each task,
- checks out with `fetch-depth: 0`,
- skips grading in the template repository itself.

This follows the starter's own Actions guidance. The exercise needs no images.

## Success criteria

- All three graded checks pass, and the review comment appears on the exercise issue.
- Each learner artifact passes content checks, not only existence checks.
- No graded step requires application code, dependency installation, database setup, browser tests, or a pull request or merge.
- The README and Copy Exercise badge use the approved title and the learner copy name `skills-copilot-app-cleared-for-takeoff`.

## Risks and open questions

### Decisions (resolved at Gate 1)

1. **Identity.** The title is "Copilot app Cleared for Takeoff", the repository name is `copilot-app-cleared-for-takeoff`, and the learner copy is `skills-copilot-app-cleared-for-takeoff`. The target owner is `arilivigni`.
2. **Branch policy.** Grading accepts pushes to any branch, and no pull request is needed. The steps note that the starter's **Run tests** workflow, which runs on pushes to `main`, isn't part of grading.
3. **Automatic `npm ci`.** Bootstrap removes only the `session.create` trigger in `.github/github-app.yml`. The Run-menu commands, including **Install dependencies**, stay.
4. **Root README.** The exercise README replaces the Tailspin README and includes a short "About Tailspin Toys" section.

### Open questions

- **Copyright holder**: decide at publish. Nothing else blocks bootstrap.

### Remaining risks

1. **Wording-sensitive grading.** The prompts include the exact terms, such as the markers and the three status words. The checks are case-insensitive and allow rephrasing, the failure feedback names any missing term, and hand edits are fine.
2. **Actions can't prove which Copilot surface, mode, or agent was used.** Grading reads only content, and the steps and README must not claim otherwise.
3. **Preservation baseline.** The checks read the starting files from the root commit, which is the single initial commit in a learner's copy. Bootstrap must use `fetch-depth: 0` and leave both edited starter files untouched.
4. **Workflow gating.** Steps 1–3 must not grade the initial template push. A change pushed before its step is enabled isn't graded, so troubleshooting points learners to **Run workflow** (`workflow_dispatch`).
5. **Stray edits.** The starter instructions tell agents to update the README when they add functionality. The prompts say "do not change any other file," and troubleshooting covers `git restore`.
6. **Noisy CI on `main`.** Pushing to `main` starts the starter's **Run tests** workflow, which runs lint, unit, typecheck, and end-to-end jobs and can fail or take a while. The step notes and troubleshooting say that it isn't graded.
7. **Manual dependency install.** Learners can still run **Install dependencies** from the Run menu. It's harmless but unnecessary, and troubleshooting tells them to skip it.
