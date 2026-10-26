#!/usr/bin/env bash
# Hand-off from Phase I (quick chat) to Phase II (project session).
# Creates an empty exercise repo with the approved name and adds the
# Tailspin Toys app (MIT) as starter code, minus upstream-only automation.
#
# Usage:
#   ./handoff.sh <owner> <approved-repo-name> [parent-dir]
#   ./handoff.sh --dry-run <owner> <approved-repo-name> [parent-dir]   # local only: no GitHub repo, no push
set -euo pipefail

dry_run=false
if [[ "${1:-}" == "--dry-run" ]]; then dry_run=true; shift; fi
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 [--dry-run] <owner> <approved-repo-name> [parent-dir]" >&2
  exit 2
fi

owner=$1
name=$2
parent=${3:-$HOME/src/workshop-demo}
starter=https://github.com/github-samples/tailspin-toys.git

if [[ "$name" == skills-* ]]; then
  echo "Use the name without the skills- prefix; learner copies get it automatically." >&2
  exit 1
fi
if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Repository name must be lowercase and hyphenated: $name" >&2
  exit 1
fi

mkdir -p "$parent"
cd "$parent"
if [[ -e "$name" ]]; then
  echo "$parent/$name already exists. Pick another parent dir or remove it first." >&2
  exit 1
fi

if $dry_run; then
  mkdir "$name" && git -C "$name" init --quiet
else
  gh repo create "$owner/$name" --private --clone
fi
cd "$name"

tmp=$(mktemp -d "${TMPDIR:-/tmp}/tailspin.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
git clone --quiet --depth 1 "$starter" "$tmp/src"

# Drop the upstream issue sources and the self-deleting workflow that seeds
# them (the exercise's Step 0 opens its own issue), the upstream maintainer
# triage workflow and its lock file, and CODEOWNERS that points at the
# upstream team.
rsync -a \
  --exclude '.git/' \
  --exclude '.github/bootstrap-issues/' \
  --exclude '.github/workflows/bootstrap-issues.yml' \
  --exclude '.github/workflows/weekly-workshop-triage.*' \
  --exclude '.github/aw/' \
  --exclude '.github/CODEOWNERS' \
  "$tmp/src/" ./

upstream_sha=$(git -C "$tmp/src" rev-parse --short HEAD)
git add -A
git commit --quiet -m "Add Tailspin Toys starter app (MIT) from github-samples/tailspin-toys@$upstream_sha"
git branch -M main

if $dry_run; then
  echo "Dry run: local repo ready at $PWD (no GitHub repo created, nothing pushed)."
else
  git push --quiet -u origin main
  echo "Ready: https://github.com/$owner/$name"
  echo "Local path: $PWD"
fi
echo "Next: add this folder as a project in the Copilot app, start a New session on main (Interactive, Auto > Balance), and paste Prompt 2."
