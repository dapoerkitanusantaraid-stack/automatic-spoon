#!/usr/bin/env bash
set -euo pipefail

# set_github_secret.sh - Helper to set a GitHub Actions repository secret
# Usage:
#   GITHUB_REPO=owner/repo SECRET_NAME=NAME SECRET_VALUE=VALUE ./scripts/set_github_secret.sh
# Or interactively it will prompt for values.

if [ -z "${GITHUB_REPO:-}" ]; then
  read -rp "Owner/repo (e.g. user/repo): " GITHUB_REPO
fi

if [ -z "${SECRET_NAME:-}" ]; then
  read -rp "Secret name (e.g. TELEGRAM_BOT_TOKEN): " SECRET_NAME
fi

if [ -z "${SECRET_VALUE:-}" ]; then
  echo "Enter secret value (will not be echoed):"
  read -rs SECRET_VALUE
  echo
fi

# Try using gh CLI first
if command -v gh >/dev/null 2>&1; then
  echo "Attempting to set secret via gh CLI..."
  if printf "%s" "$SECRET_VALUE" | gh secret set "$SECRET_NAME" -R "$GITHUB_REPO"; then
    echo "Secret set via gh CLI."
    exit 0
  else
    echo "gh CLI failed to set secret (likely permissions)."
  fi
fi

cat <<EOF
Could not set repository secret automatically. Please add the secret manually in GitHub web UI:
1. Open: https://github.com/$GITHUB_REPO/settings/secrets/actions
2. Click 'New repository secret'
3. Name: $SECRET_NAME
4. Value: (paste the secret you provided)

If you want an automated upload, provide a GitHub Personal Access Token (PAT) with 'repo' and 'admin:repo_hook' scopes and re-run this script with GH_PAT exported. This script currently only supports gh CLI automatic flow.
EOF

exit 1
