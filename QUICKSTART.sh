#!/usr/bin/env bash
# Termux-friendly Quickstart for Project Server (Android / Termux)
# This script provides step-by-step commands and helpers for running the
# project inside Termux on Android. It does NOT require Docker.

set -euo pipefail

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}PROJECT SERVER v2.0 - TERMUX QUICKSTART${NC}"
echo -e "${BLUE}======================================${NC}\n"

echo -e "${YELLOW}📋 PREPARATION (Termux)${NC}\n"

echo "1️⃣  Install Termux packages (run in Termux):"
echo -e "${GREEN}   pkg update && pkg upgrade -y${NC}"
echo -e "${GREEN}   pkg install -y python git clang make openssl-tool libffi libcrypt-dev${NC}\n"

echo "2️⃣  Grant storage permission (required for file access):"
echo -e "${GREEN}   termux-setup-storage${NC}\n"

echo -e "${YELLOW}📦 Python environment${NC}\n"
echo "Recommended: create and activate a virtual environment to keep dependencies isolated."
echo -e "${GREEN}   python -m venv .venv${NC}"
echo -e "${GREEN}   source .venv/bin/activate${NC}\n"

echo "3️⃣  Install Python dependencies"
echo -e "${GREEN}   pip install --upgrade pip setuptools wheel${NC}"
echo -e "${GREEN}   pip install -r requirements.txt${NC}\n"

echo "Notes:"
echo " - Some packages (cryptography, cffi) may need a C compiler (clang) and libffi headers installed via pkg."
echo " - If a package fails to build, try: pkg install build-essential (or install clang and make) then retry."

echo -e "${YELLOW}⚙️  Configure environment${NC}\n"
echo "4️⃣  Copy example .env and edit (use a text editor like nano)"
echo -e "${GREEN}   cp .env.example .env${NC}"
echo -e "${GREEN}   nano .env${NC}\n"

echo "Set at minimum these vars in .env for Termux testing:" 
echo "  - TELEGRAM_TOKEN"
echo "  - TELEGRAM_WEBHOOK_URL (if using webhooks) or leave empty to use polling mode"

echo -e "${YELLOW}▶️  Run the server (development)${NC}\n"
echo "Use this command to start the FastAPI app with Uvicorn on Termux:" 
echo -e "${GREEN}   source .venv/bin/activate && python -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload${NC}\n"

echo "If `uvicorn` is not installed as a module, run:"
echo -e "${GREEN}   pip install uvicorn[standard]${NC}\n"

echo -e "${YELLOW}🔗 Webhook testing (optional)${NC}\n"
echo "If your device is not publicly reachable, use ngrok to expose the local port for webhooks."
echo -e "${GREEN}   pkg install -y wget unzip${NC}"
echo -e "${GREEN}   # download ngrok and run: ngrok http 8000${NC}\n"

echo -e "${YELLOW}📱 Quick verification${NC}\n"
echo "After starting the server, open:"
echo -e "  • Customer UI : http://localhost:8000/index.html"
echo -e "  • Admin UI    : http://localhost:8000/admin-dashboard.html"
echo -e "  • API docs    : http://localhost:8000/docs\n"

echo -e "${YELLOW}🛠️  Useful helper commands${NC}\n"
echo -e "${GREEN}   # activate venv${NC}"
echo -e "   source .venv/bin/activate"
echo -e "${GREEN}   # run tests${NC}"
echo -e "   pytest -q"
echo -e "${GREEN}   # start server (background)${NC}"
echo -e "   nohup python -m uvicorn server.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &"

echo -e "${YELLOW}🧭 Deployment notes (Termux limitations)${NC}\n"
echo " - Docker is not available in Termux; use a VPS or Railway for production deployment."
echo " - Termux is suitable for development/testing on-device, not recommended for production."

echo -e "${YELLOW}📚 References${NC}\n"
echo "  • README.md and DEPLOYMENT.md for full production instructions"
echo "  • Use ngrok to test webhooks from Telegram/Twilio when developing on-device"

echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}✅ Termux Quickstart ready — follow steps above to run on Android.${NC}"
echo -e "${BLUE}======================================${NC}\n"
