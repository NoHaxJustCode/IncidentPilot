#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:-NoHaxJustCode}"
REPO="${2:-IncidentPilot}"

git init
if ! git config user.email >/dev/null; then
  git config user.email "you@example.com"
fi
if ! git config user.name >/dev/null; then
  git config user.name "IncidentPilot"
fi

git add .
git commit -m "Initial IncidentPilot project" || true
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${OWNER}/${REPO}.git"
git push -u origin main
