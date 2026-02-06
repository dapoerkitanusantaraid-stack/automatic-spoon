#!/usr/bin/env bash
set -euo pipefail

# Simple deploy script using docker-compose
# Usage: ./scripts/deploy.sh

WORKDIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKDIR"

echo "Building images..."
docker-compose build --pull

echo "Starting containers..."
docker-compose up -d --remove-orphans

echo "Waiting for service to start..."
sleep 5

echo "Health check:"
if curl -sSf http://localhost:8000/ >/dev/null 2>&1; then
  echo "Service is up at http://localhost:8000"
else
  echo "Service did not respond on http://localhost:8000 — check logs"
  docker-compose logs --no-color api | tail -n 200
  exit 1
fi

echo "Done. Use 'docker-compose logs -f api' to follow logs."