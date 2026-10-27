# Learner validation evidence (rehearsal)

Rehearsal output, 2026-10-27. Template: `arilivigni/copilot-app-cleared-for-takeoff-rehearsal` (private), bootstrap commit `a10b8b6`, toolkit `v0.9.3`.

| Copy | Purpose | State |
| --- | --- | --- |
| [`skills-copilot-app-cleared-for-takeoff-rehearsal`](https://github.com/arilivigni/skills-copilot-app-cleared-for-takeoff-rehearsal/issues/1) | Live demo | Step 1 failing; pass it on stage |
| [`skills-copilot-app-cleared-for-takeoff-rehearsal-backup`](https://github.com/arilivigni/skills-copilot-app-cleared-for-takeoff-rehearsal-backup/issues/1) | Fallback | Step 1 passed; Step 2 posted |

Step 0 succeeded in both copies and opened exactly one issue.

## Fail ([run](https://github.com/arilivigni/skills-copilot-app-cleared-for-takeoff-rehearsal/actions/runs/40561031194))

Incomplete section pushed to `.github/copilot-instructions.md`:

```markdown
<!-- BEGIN WORKSHOP: TSDoc -->
## Workshop: TSDoc for exported functions

- Add a TSDoc comment with a summary, `@param`, and `@returns` to TypeScript code.
<!-- END WORKSHOP: TSDoc -->
```

Feedback: 3 of 4 checks passed. ❌ "The workshop section applies the rule to new or changed exported functions". Tip: "Your section is missing: new, changed (or modified, updated)."

## Pass ([run](https://github.com/arilivigni/skills-copilot-app-cleared-for-takeoff-rehearsal-backup/actions/runs/40561233568))

On stage, replace the bullet in the live copy with these two lines, then commit to `main`:

```markdown
- Every new or changed exported TypeScript function must have a TSDoc comment (`/** ... */`) directly above it.
- The TSDoc comment includes a one-line summary, an `@param` tag for each parameter, and an `@returns` tag.
```

Result: Step 1 passed, and Step 2 was posted to the issue in about a minute.
