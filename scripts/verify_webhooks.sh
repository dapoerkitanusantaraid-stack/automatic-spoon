#!/usr/bin/env bash
set -euo pipefail

# Verify Telegram webhook status using TELEGRAM_BOT_TOKEN from env
# Usage: export TELEGRAM_BOT_TOKEN=... && ./scripts/verify_webhooks.sh

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "Please export TELEGRAM_BOT_TOKEN before running."
  exit 1
fi

echo "Getting Telegram webhook info..."
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | jq '.' || true

echo "Done. If webhook url is empty, either set a webhook or use polling mode in the bot."