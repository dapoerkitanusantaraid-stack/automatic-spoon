# Project-Server
server/
├── main.py
├── requirements.txt
└── Profile
fastapi
uvicorn
python-telegram-bot==13.15
requests
from fastapi import FastAPI, Request
from telegram import Bot

TOKEN = "8505712679:AAGIkuamaV2WFH-XUBjtcB4y8-6zP9kYHXc"
bot = Bot(8505712679:AAGIkuamaV2WFH-XUBjtcB4y8-6zP9kYHXc)

app = FastAPI(AAE0NgAAyqOXPSn7dag5lqTD3AumVy858Gzj9OXvqn_HKg)

@app.get("/")
def health():
    return {"status": "BOT CORE RUNNING"}

# Telegram webhook
@app.post("/telegram")
async def telegram(req: Request):
    data = await req.json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"].lower()

    if text == "/start":
        bot.send_message(chat_id, "Selamat datang!")
    elif text == "promo":
        bot.send_message(chat_id, "Promo hari ini 🔥")
    elif text == "cs":
        bot.send_message(chat_id, "Admin akan bantu")
    else:
        bot.send_message(chat_id, "Ketik: promo | cs")

    return {"ok": True}

# Endpoint dari Android
@app.post("/broadcast")
async def broadcast(data: dict):
    chat_id = data["chat_id"]
    msg = data["msg"]
    bot.send_message(chat_id, msg)
    return {"sent": True}
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "RAILPACK"
  },
  "deploy": {
    "runtime": "V2",
    "numReplicas": 1,
    "sleepApplication": false,
    "useLegacyStacker": false,
    "multiRegionConfig": {
      "us-west2": {
        "numReplicas": 1
      }
    },
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
