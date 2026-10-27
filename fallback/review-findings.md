# Review: Copilot app Cleared for Takeoff (rehearsal)

- **Repository**: `arilivigni/copilot-app-cleared-for-takeoff-rehearsal`. It is private, marked as a template, and `main` is at `a10b8b6`.
- **Local checkout**: `/Users/arilivigni/src/workshop-demo/copilot-app-cleared-for-takeoff-rehearsal`
- **Baseline**: Tailspin starter at `4dc1d5b` (root). Approved scope is in `.github/exercise-outline.md`, with three steps.
- **Review mode**: report only. No repository files, settings, or workflows were changed or run.

## Overall readiness

**Ready for live learner copies. No Blocking or Important findings are supported by the evidence.** Step 0, Step 1 grading and feedback, and step-to-step progression all hold up under static review, the pre-handoff checks, and local runs of the graders against a simulated fresh learner copy. The Nice to improve items below are polish and learner-noise issues. None of them breaks the start, grading, or progression.

### Checks already covered

**Approved scope**

- The exercise has three steps, matching the outline.
- The file layout matches the template contract: `0-start-exercise.yml`, steps `1–3` with matching `N-step.yml`, the final `3-step.yml` with `# Last step of the exercise`, and `x-review.md`.
- The bootstrap left the learner targets untouched. `.github/copilot-instructions.md` and `.github/skills/quality-checks/SKILL.md` are identical between `4dc1d5b` and `a10b8b6`, and `.github/agents/` does not exist.
- `github-app.yml` only drops the automatic `Install dependencies` trigger, as the outline specifies.

**Template parity**

- No placeholders remain.
- The toolkit is pinned to `v0.9.3` (latest), and `refs/tags/v0.9.3` resolves.
- Every step has a Theory section with content and a single activity with a `Having trouble? 🤷` block.
- Every step's final activity ends with the Mona instruction.
- Prompt badges and fences are correct: `prompt` and `bash`, with unmodified badges.
- The Copy Exercise badge is correct (`README.md:30`): `template_owner=arilivigni`, `template_name=copilot-app-cleared-for-takeoff-rehearsal`, `owner=%40me`, `name=skills-copilot-app-cleared-for-takeoff-rehearsal`, `description=Exercise:+Copilot+app+Cleared+for+Takeoff`, and `visibility=private`. That visibility matches the private template (`gh repo view`: `isTemplate: true`, `visibility: PRIVATE`).
- Workflow YAML parses, and `actionlint` reports no problems.

**Step 0 starts cleanly and creates exactly one issue**

- `0-start-exercise.yml` runs `start_exercise` only when `!github.event.repository.is_template` (lines 24–25). In the template, the `a10b8b6` push shows Step 0 as `skipped`.
- toolkit `start-exercise.yml@v0.9.3` does three things:
  - creates one issue, "Exercise: …";
  - replaces README with a "Start exercise" commit made with `GITHUB_TOKEN`, which triggers no further workflows;
  - disables every `.github/workflows/[0-9]*` workflow, including Step 0 itself.
- Step 0 then posts `1-step.md` and the "watching" comment, and enables only `Step 1`.
- Step 0 creates no other issues.

**Step 1 content renders correctly**

- `1-step.md` is posted with `vars` (`login`, `full_repo_name`, at `0-start-exercise.yml:44–46`).
- Rendered locally with Nunjucks (`autoescape: true`), it shows `@mona-learner` and `` `mona-learner/skills-…` `` correctly.
- The `$(git rev-list …)` restore command and the `<!-- … -->` markers inside the prompt fence render literally.
- Steps 2 and 3 and `x-review.md` contain no `{{`, `{%`, or `{#`.

**Progression**

- Steps 1–3 trigger on pushes to `"**"`, filtered by the step's file path, and also on `workflow_dispatch`.
- `find_exercise` skips the template and the copy-creation push to the default branch (for example `1-step.yml:26–28`).
- The next-step or review jobs `need` `check_step_work`, which fails through `contains(steps.*.outcome, 'failure')` when any check fails.
- Each passing step disables itself and enables the next one. Step 3 posts the review and calls `finish-exercise.yml@v0.9.3`.

**Workflow safety**

- Every exercise workflow sets `permissions: {}`. Grading jobs hold only `contents: read` and `issues: write`, with no `actions: write` and no `contents: write`.
- Checkout uses `fetch-depth: 0` and `persist-credentials: false`.
- `find-comment` is scoped by `comment-author: github-actions[bot]` and `body-includes: "watch your progress in the background"`, which matches toolkit `watching-for-progress.md@v0.9.3`. This prevents replacing a learner's comment.
- Learner-controlled text reaches the comment only through JSON-encoded `tips` in a `with:` input, never through `run:`.

**No grade depends on npm, a build, browser tooling, or proof of the Copilot mode used**

- `check-step-1/2/3.sh` use only `git` and `python3`, and Step 3 also uses the toolkit `file-exists` action.
- The steps tell learners to skip `npm ci`. `README.md:15` states that Node.js isn't needed.

**Written policy is not presented as proof of model behavior**

- `1-step.md:54` says "Mona reads only the committed file, so she can't tell which Copilot surface, mode, or agent made the edit".
- `2-step.md` says "Mona reads only the committed file".
- `3-step.md:47` says Mona "can't tell whether anyone selected or used the agent", and the test flight is marked "(not graded)".
- One recap line in `x-review.md` is softer than these. See the Nice to improve section.

**Graders exercised**

I simulated a template copy: `git archive a10b8b6`, a single root commit, and then a "Start exercise" commit. I ran each grader with `GITHUB_OUTPUT` set, and rendered the real `step-results-table.md@v0.9.3` with `js-yaml` 4 `loadAll(vars)[0]` and Nunjucks 3 `autoescape: true`, the same flow as `GrantBirki/comment@v2.1.1`.

| Case | Result |
| --- | --- |
| Untouched starter, Step 1 | ❌ exit 1. `markers`, `tsdoc`, and `scope` fail; `preserved` passes. Tip: "no begin marker found; no end marker found". |
| Untouched starter, Step 2 | ❌ exit 1. `section`, `fields`, and `honesty` fail. Tip: "Report section not found. Add a `## Report format` heading…" |
| Untouched starter, Step 3 | ❌ exit 1. All 7 checks fail. Tip: "Couldn't find `.github/agents/qa.agent.md`…" |
| Prompt-faithful artifacts (Steps 1, 2, 3), with LF and CRLF line endings, plus variants ("modified" wording, `### Reporting results` with a table) | ✅ exit 0, `tips=[]`, no Tips section rendered |
| Step 1 with markers turned into headings, reworded markers, a duplicate begin marker, or end before begin | ❌ `markers` fails, with line-specific tips |
| Step 1 missing "TSDoc" or "changed" | ❌ tip names the missing term |
| Step 1 with one line reworded, or one line deleted and another moved inside the markers | ❌ `preserved` fails, naming the original line numbers and text, with a restore command |
| Step 1 file deleted, or whole file rewritten | ❌ actionable restore tip |
| Step 2 frontmatter `description` changed | ❌ tip shows the expected and actual line 3 |
| Step 2 missing `blocked`, no honesty sentence, report under an `####` heading, `### Lint` removed, or file deleted | ❌ each produces a specific tip |
| Step 3 wrapped in a fence, blank line before `---`, empty description, missing never-PR rule, missing ask-first or evidence | ❌ each produces a specific tip |
| Step 3 at `.github/agent/qa.agent.md` or `.github/agents/qa.md` | ❌ near-miss tip with the exact `git mv` command |

The rendered failure comments show `&lt;!-- … --&gt;` and `&#39;` outside code spans. GitHub displays these as literal `<!-- … -->` and `'`. Code spans contain no escaped characters, because the scripts' `code()` helper avoids them.

## Blocking findings

None.

## Important findings

None.

## Nice to improve

1. **Starter automation adds a red run and extra Actions minutes in fresh private copies.** The starter's `.github/dependabot.yml:11` covers the npm ecosystem.
   - **Evidence**: the template's own first Dependabot run (`40553607687`, on `4dc1d5b`) failed with `private_source_authentication_failure` for `drizzle-kit`. That's because `package-lock.json` resolves 6 packages from internal `ms-feed-*.pkgs.visualstudio.com/1es-public` feeds, for example `package-lock.json:758` and `:1144`.
   - **Why it matters**:
     - A fresh copy will probably show a failed **Dependabot Updates** run in the Actions tab during the first 20 seconds.
     - `README.md:41–45` tells learners to check the Actions tab, and that "If the page shows a failed job, please submit an issue."
     - Dependabot may also open pull requests. These are not issues, and toolkit `find-exercise-issue.yml` filters pull requests out, so grading is unaffected.
     - The starter **Run tests** workflow also runs its full lint, unit, typecheck, and Playwright-container E2E jobs on the copy-creation push. `README.md:39` implies only a few seconds of private-repository Actions minutes per check.
   - **Fix**:
     - Add a README troubleshooting line that the starter's **Dependabot Updates** and **Run tests** runs aren't part of the exercise and can be ignored. Mention Run tests minutes in `README.md:39`.
     - Optionally, as a maintainer decision outside the three-step scope, drop `dependabot.yml` from the template or regenerate the lockfile against `registry.npmjs.org`.
2. **A Step 3 push to the wrong `.github/agent/` folder gets no feedback.**
   - **Evidence**:
     - `.github/workflows/3-step.yml:12–13` only watches `.github/agents/**`. The comment at lines 6–8 says misnamed agent files "still get feedback", but that holds only inside `agents/`.
     - The grader's near-miss hint for an `agent/` folder (`check-step-3.sh:156`) is reachable only through a manual **Run workflow**. I verified that the tip itself is correct.
     - `3-step.md:48` lists `.github/agent/` under "Wrong path or name". Unlike Step 1, Step 3 has no "No result comment" bullet that would point the learner there or to **Run workflow**.
   - **Fix**: add `.github/agent/**` to the Step 3 `paths`, or add a "No result comment after a couple of minutes" bullet to `3-step.md` that names the folder check and **Actions → Step 3 → Run workflow**.
3. **Keyword heuristics have narrow edge cases.** Neither is likely with the provided prompts, and both are verified locally.
   - `check-step-2.sh:38` `NEGATION` doesn't match Markdown emphasis. "`Do **not** invent command results…`" fails `honesty`, although the tip still tells the learner how to fix it.
   - `check-step-3.sh:33–37`, 211, and 213 accept any sentence that contains both a negation and `commit` or `PR`. "`Do not worry about style; the user will commit and open a PR.`" passes `no_commit` and `no_pr`.
   - **Fix**: strip `*` and `_` emphasis before matching. Optionally, require the negation to come before the commit or pull-request term in the same clause.
4. **One recap line in `x-review.md:11` reads as a claim about agent behavior.** "Created a `qa` agent that reports with evidence, asks before changing code, and never commits or opens pull requests." Grading only checked the written definition, and the step text correctly says Mona can't tell whether the agent was used.
   - **Fix**: "Created a `qa` agent whose instructions require evidence-based reports, asking before changing code, and never committing or opening pull requests."
5. **The bootstrap edited starter workflows that the outline marks as unchanged.** `permissions: {}` was added at `.github/workflows/run-tests.yml:11–12` and `.github/workflows/copilot-setup-steps.yml:6–7`, but `.github/exercise-outline.md:291` says `run-tests.yml` is "left unchanged".
   - It's harmless: each job already grants its own `contents: read`, and Run tests passed on `a10b8b6` in the template.
   - **Fix**: record the hardening in the outline's file map, or revert it so the scope matches the outline.

## Suggested validation

1. Create one fresh private learner copy from the template, as the coordinator plans. Confirm the following:
   - exactly one issue, "Exercise: Copilot app Cleared for Takeoff";
   - README replaced by a "Start exercise" commit;
   - Step 1 comment shows the real `@login` and `owner/skills-…` name;
   - **Step 1** is enabled and Steps 0, 2, and 3 are disabled;
   - the Step 1–3 runs triggered by the creation push show `skipped`, not failed. This confirms the `github.event.created` guard.
2. Run Step 1 with a fail-then-pass round from the Copilot app session's non-`main` branch:
   - Push markers turned into a `##` heading. Expect a ❌ comment with the line-specific tip.
   - Fix and push again. Expect ✅, Step 2 posted with a new watching comment, Step 1 disabled, and Step 2 enabled.
   - This also confirms that the `"**"` branch filter and new-branch path filtering work in practice.
3. If time allows, finish Steps 2 and 3 in one copy. Confirm the review comment, the README congratulations commit on `main`, and the closed issue.
4. In the same copy, note whether **Dependabot Updates** fails or opens pull requests, so the presenter can explain it if a learner asks.

## Unverified checks

- **Live GitHub Actions behavior in a learner copy.** None of Steps 0–3 were run.
  - Not verified: `github.event.created` being true on the template-generated push, path-filter evaluation for a newly pushed session branch, toolkit reusable workflows at runtime, and `GrantBirki/comment` and `peter-evans/find-comment` posting, finding, and replacing comments.
  - I reproduced the rendering pipeline locally with `nunjucks` and `js-yaml` versions in the action's dependency ranges, not the action itself.
- **Account and organization constraints for copies.**
  - Access to the private template for anyone other than the owner.
  - Actions being enabled, the allowed-actions policy for third-party actions (`GrantBirki/comment`, `peter-evans/find-comment`, `skills/action-text-variables`), and available private Actions minutes.
  - The template itself allows all actions with read-only default token permissions.
- **Dependabot in template-generated private copies.** Not observed: whether version updates run there, and whether the npm job fails the way it did in the template.
- **Real Copilot app output.** The correct artifacts were hand-written to follow each prompt, not generated by Copilot. Whether Copilot follows the prompts, for example keeping every existing line and not wrapping the agent in a fence, wasn't tested.
  - By design, the graders check only committed file content. They don't prove model behavior, which surface or mode was used, or that the `qa` agent obeys its guardrails, and the steps don't claim they do.
- **Platform specifics.**
  - CRLF line endings pass locally.
  - The `git checkout $(git rev-list --max-parents=0 HEAD) -- …` restore tip wasn't run in PowerShell.
  - Uppercase `QA.agent.md` passed locally only because macOS file systems are case-insensitive. On the Linux runner, `file-exists` and the grader should fail it with the `git mv` hint, but I only reasoned about that.
- **Copyright holder.** It remains an open question for publish (`.github/exercise-outline.md:15`, `:321`). The footer reads "&copy; 2026 GitHub, Inc.", and `LICENSE` reads "Copyright GitHub, Inc." with no year, so there's no year mismatch to report.
