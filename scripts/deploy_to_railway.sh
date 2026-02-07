#!/usr/bin/env bash
set -euo pipefail

# Helper to deploy this repo to Railway using the Railway CLI
# Prerequisites:
# - Install Railway CLI: https://railway.app/docs/cli
# - Login: `railway login`
# - Link project or create new: `railway init` (follow prompts)
# - Ensure repository has `railway.json` (this repo contains it)

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v railway >/dev/null 2>&1; then
  echo "Railway CLI not found. Install it: https://railway.app/docs/cli"
  exit 1
fi

echo "Logging into Railway..."
railway login || true

echo "If you haven't created/linked a Railway project yet, run:"
echo "  railway init"

echo "Set required environment variables in Railway project. Examples:"
echo "  railway variables set TELEGRAM_BOT_TOKEN=<token>"
echo "  railway variables set ENCRYPTION_PASSWORD=<value>"

echo "You can set variables using the Railway UI as well."

echo "Starting deployment (this will build using railway.json)..."
railway up

echo "Railway deployment finished. Check the Railway dashboard for logs and URL."