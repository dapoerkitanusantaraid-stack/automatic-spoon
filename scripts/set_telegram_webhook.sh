#!/usr/bin/env bash
set -euo pipefail

# Set Telegram webhook for the bot
# Usage: TELEGRAM_BOT_TOKEN=... TELEGRAM_WEBHOOK_URL=https://yourdomain.com/telegram/webhook ./scripts/set_telegram_webhook.sh

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  read -rp "TELEGRAM_BOT_TOKEN: " TELEGRAM_BOT_TOKEN
fi

if [ -z "${TELEGRAM_WEBHOOK_URL:-}" ]; then
  read -rp "TELEGRAM_WEBHOOK_URL: " TELEGRAM_WEBHOOK_URL
fi

echo "Setting Telegram webhook to $TELEGRAM_WEBHOOK_URL"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=${TELEGRAM_WEBHOOK_URL}" \
  -d "allowed_updates=['message','callback_query']" | jq '.'

echo "Checking webhook info..."
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | jq '.'

echo "Done."