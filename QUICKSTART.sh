#!/usr/bin/env bash

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}PROJECT SERVER v2.0 - QUICKSTART${NC}"
echo -e "${BLUE}======================================${NC}\n"

echo -e "${YELLOW}📋 SETUP (5 MENIT):${NC}\n"

echo "1️⃣  Install dependencies:"
echo -e "${GREEN}   pip install -r requirements.txt${NC}\n"

echo "2️⃣  Setup environment:"
echo -e "${GREEN}   cp .env.example .env${NC}"
echo -e "${GREEN}   # Edit .env dengan Telegram token Anda${NC}\n"

echo "3️⃣  Jalankan server:"
echo -e "${GREEN}   python server/main.py${NC}\n"

echo "4️⃣  (Optional) Load sample data:"
echo -e "${GREEN}   python init_sample_data.py${NC}\n"

echo -e "${YELLOW}🎯 AKSES:${NC}\n"
echo "  👤 Customer: http://localhost:8000/index.html"
echo "  📊 Admin:    http://localhost:8000/admin-dashboard.html"
echo "  🤖 API Docs: http://localhost:8000/docs"
echo "  📱 Telegram: Message /start ke bot Anda\n"

echo -e "${YELLOW}📚 DOKUMENTASI:${NC}\n"
echo "  • README.md        - Project overview"
echo "  • SETUP_GUIDE.md   - Detailed setup & bot config"
echo "  • DOKUMENTASI.md   - API reference"
echo "  • examples.py      - Integration examples\n"

echo -e "${YELLOW}📁 FILE STRUCTURE:${NC}\n"
echo "  server/"
echo "    ├── main.py              # FastAPI + Telegram"
echo "    ├── whatsapp_bot.py      # WhatsApp (Twilio)"
echo "    └── social_media.py      # Instagram/Facebook"
echo "  index.html                 # Customer frontend"
echo "  admin-dashboard.html       # Admin panel"
echo "  sdk.js                     # Mobile tracking SDK"
echo "  requirements.txt           # Dependencies"
echo "  .env.example               # Config template"
echo "  Dockerfile                 # Docker setup"
echo "  docker-compose.yml         # Docker Compose"
echo "  examples.py                # Code examples\n"

echo -e "${YELLOW}🔑 FEATURES:${NC}\n"
echo "  ✅ Multi-platform: Telegram, WhatsApp, Instagram, Facebook, Web"
echo "  ✅ Customer tracking: Collect device info & behavior data"
echo "  ✅ Admin dashboard: Real-time analytics & customer management"
echo "  ✅ Content management: Multiple categories & galleries"
echo "  ✅ Broadcast system: Send to multiple platforms"
echo "  ✅ Mobile SDK: Track web/mobile customer interactions"
echo "  ✅ REST API: Fully documented endpoints\n"

echo -e "${YELLOW}🚀 QUICK COMMANDS:${NC}\n"
echo -e "${GREEN}   ./deploy.sh setup${NC}     # Download & setup"
echo -e "${GREEN}   ./deploy.sh dev${NC}       # Run development"
echo -e "${GREEN}   ./deploy.sh test${NC}      # Test API"
echo -e "${GREEN}   python examples.py${NC}    # Run examples\n"

echo -e "${YELLOW}📞 NEXT STEPS:${NC}\n"
echo "  1. Read SETUP_GUIDE.md for Telegram/WhatsApp setup"
echo "  2. Get Telegram token from @BotFather"
echo "  3. Configure .env with your credentials"
echo "  4. Start server and test with sample data"
echo "  5. Customize frontend & deploy to production\n"

echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}✅ Ready to start! Let's go! 🚀${NC}"
echo -e "${BLUE}======================================${NC}\n"
