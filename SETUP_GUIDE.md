# 📱 Project Server v2.0 - Multi-Platform Bot & Customer Data Collection

Sistem server yang lengkap untuk mengelola konten dan tracking customer data dengan integrasi **Telegram**, **WhatsApp**, **Instagram**, **Facebook**, dan **Web**.

## ✨ Fitur Utama

### 🤖 Multi-Platform Support
- ✅ **Telegram Bot** - Interaksi via Telegram dengan /start command, kategori filter
- ✅ **WhatsApp Bot** - Kirim pesan dan galeri via WhatsApp (Twilio)
- ✅ **Instagram Integration** - DM Instagram dan Story Updates
- ✅ **Facebook Messenger** - Integrasi dengan Facebook Pages
- ✅ **Web Platform** - Dashboard responsive untuk semua devices

### 👥 Customer Data Collection
- ✅ Kumpulkan data customer dari semua platform
- ✅ Track device info (OS, browser, screen resolution, timezone)
- ✅ Monitor user interactions (view, click, share)
- ✅ Store customer metadata dan preferences
- ✅ Analytics real-time tentang customer behavior

### 📊 Admin Dashboard
- ✅ View semua customer data
- ✅ Monitoring interactions & analytics
- ✅ Send broadcast ke multiple platforms
- ✅ Statistics & charts
- ✅ Search & filter customers

### 🎯 Konten Management
- ✅ Create, Read, Update, Delete konten
- ✅ Multiple kategori support
- ✅ Galeri images per konten
- ✅ Filter by kategori
- ✅ Share ke social media

## 🏗️ Struktur Project

```
Project-Server/
├── server/
│   ├── main.py                 # FastAPI backend + Telegram handler
│   ├── whatsapp_bot.py         # WhatsApp integration (Twilio)
│   └── social_media.py         # Instagram/Facebook integration
├── index.html                  # Frontend customer
├── admin-dashboard.html        # Admin dashboard
├── sdk.js                       # Mobile SDK untuk tracking
├── init_sample_data.py         # Sample data loader
├── api_client.py               # API testing
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
└── DOKUMENTASI.md              # Docs lengkap
```

## 🚀 Quick Start

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Environment

```bash
cp .env.example .env
# Edit .env dengan credentials Anda
```

### 3️⃣ Database & Sample Data

```bash
python init_sample_data.py
```

### 4️⃣ Jalankan Server

```bash
cd server
python main.py
```

Server akan berjalan di: **http://localhost:8000**

### 5️⃣ Akses Dashboard

- **User Frontend**: `http://localhost:8000/index.html`
- **Admin Dashboard**: `http://localhost:8000/admin-dashboard.html`
- **Telegram Bot**: Message `/start` ke bot Anda
- **WhatsApp Bot**: Setup webhook di Twilio config

## 📡 API Endpoints

### Konten Management
```
GET     /konten              - Get semua konten
GET     /konten/{id}         - Get detail konten
GET     /konten/{id}/galeri  - Get galeri
GET     /kategori/{kategori} - Filter by kategori
POST    /konten/create       - Create konten baru
DELETE  /konten/{id}         - Delete konten
```

### Customer Management
```
POST    /customer/register           - Register/save customer data
GET     /customer/phone/{phone}      - Get customer by phone
GET     /admin/customers             - Get semua customers
GET     /admin/customers/{id}        - Get customer detail
POST    /customer/{id}/log           - Log interaction
GET     /admin/stats                 - Get statistics
```

### Telegram Bot
```
POST    /telegram/webhook    - Webhook untuk Telegram updates
```

## 🤖 Telegram Bot Setup

### 1. Dapatkan Bot Token
- Chat ke [@BotFather](https://t.me/botfather) di Telegram
- Execute `/newbot` command
- Follow instruksi dan dapatkan token

### 2. Configure Token di `.env`
```
TELEGRAM_BOT_TOKEN=your_token_from_botfather
```

### 3. Webhook Setup
```bash
# Set webhook (ganti dengan domain Anda)
curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook \
  -d url=https://yourdomain.com/telegram/webhook
```

### 4. Bot Commands
- `/start` - Tampilkan sambutan dan link konten
- `promo` - Tampilkan konten kategori promo
- `produk` - Tampilkan konten kategori produk
- `berita` - Tampilkan konten kategori berita

## 📲 WhatsApp Bot Setup

### 1. Register Twilio Account
- Buka https://www.twilio.com
- Sign up dan dapatkan trial credits
- Verify WhatsApp number

### 2. Configure Credentials
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=+1234567890
```

### 3. Send WhatsApp Message
```python
from server.whatsapp_bot import whatsapp_bot

whatsapp_bot.send_konten_link(
    to_number="+62812345678",
    konten_data=konten
)
```

## 📷 Instagram Integration

### 1. Get Credentials
```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### 2. Use in Code
```python
from server.social_media import social_media

social_media.send_instagram_dm(
    user_id=12345,
    message="Check this out!",
    media_url="image.jpg"
)
```

## 📱 Mobile SDK Usage

### 1. Include SDK di Web
```html
<script src="https://yourdomain.com/sdk.js"></script>
<script>
  ProjectServerSDK.init({
    apiBase: 'https://api.yourdomain.com',
    trackingEnabled: true
  });
</script>
```

### 2. Register Customer
```javascript
ProjectServerSDK.registerCustomer({
  nama: 'John Doe',
  email: 'john@example.com',
  phone: '+62812345678'
});
```

### 3. Track Interactions
```javascript
// Track when user views content
ProjectServerSDK.trackKontenView(kontenId);

// Track when user views gallery
ProjectServerSDK.trackGaleriView(kontenId);

// Log custom action
ProjectServerSDK.logInteraction('custom_action', kontenId);
```

### 4. Get Customer Info
```javascript
const info = ProjectServerSDK.getCustomerInfo();
console.log(info.customerId, info.deviceInfo);
```

## 📊 Admin Dashboard Features

### 1. Overview Stats
- Total customers
- Total interactions
- Top platform
- Avg interactions per customer

### 2. Customer Management
- List semua customers
- Search by nama/email/phone
- View customer detail
- See customer activity history

### 3. Analytics
- Customers by source (Telegram, WhatsApp, Instagram, Web)
- Top platforms
- Top actions
- Interactive charts

### 4. Broadcast
- Send message ke multiple customers
- Filter by platform
- Track delivery status

## 🔌 Integration Examples

### Send Promo via WhatsApp

```python
@app.post("/send-promo-whatsapp/{konten_id}")
async def send_promo_whatsapp(konten_id: int, phone: str):
    konten = get_konten_by_id(konten_id)
    from server.whatsapp_bot import whatsapp_bot
    
    result = whatsapp_bot.send_konten_link(phone, konten)
    return {"status": result}
```

### Send Promo ke Telegram

```python
@app.post("/send-konten-telegram/{konten_id}/{chat_id}")
async def send_konten_telegram(konten_id: int, chat_id: int):
    konten = get_konten_by_id(konten_id)
    
    message = f"""
    📱 {konten['judul']}
    {konten['deskripsi']}
    
    🔗 https://yourdomain.com/?konten={konten_id}
    """
    
    bot.send_message(chat_id, message)
    return {"status": "sent"}
```

### Broadcast to All Customers

```python
@app.post("/broadcast-all")
async def broadcast_all(konten_id: int):
    konten = get_konten_by_id(konten_id)
    
    # Get all customers
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT phone, sourse FROM customers")
    customers = c.fetchall()
    conn.close()
    
    from server.whatsapp_bot import whatsapp_bot
    
    for customer in customers:
        if customer['sourse'] == 'whatsapp':
            whatsapp_bot.send_konten_link(customer['phone'], konten)
        # Add more platform handlers...
    
    return {"status": "broadcast sent"}
```

## 🗄️ Database Schema

### Customers Table
```sql
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  nama TEXT,
  email TEXT,
  phone TEXT UNIQUE,
  sumber TEXT,           -- 'telegram', 'whatsapp', 'instagram', 'web'
  device_info TEXT,      -- JSON with device info
  metadata TEXT,         -- JSON with additional data
  registered_date TEXT,
  last_activity TEXT
)
```

### Customer Interactions
```sql
CREATE TABLE customer_interactions (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  platform TEXT,         -- 'telegram', 'whatsapp', 'instagram', 'web'
  action TEXT,           -- 'click_link', 'view_galeri', 'share', etc
  konten_id INTEGER,
  timestamp TEXT
)
```

### Social Accounts
```sql
CREATE TABLE social_accounts (
  id INTEGER PRIMARY KEY,
  platform TEXT,
  account_id TEXT,
  account_username TEXT,
  access_token TEXT,
  metadata TEXT,
  created_date TEXT
)
```

## 🔐 Security Checklist

⚠️ **Development Only!** Untuk production:

- [ ] Use environment variables untuk semua secrets
- [ ] Add authentication untuk admin dashboard
- [ ] Rate limiting pada API endpoints
- [ ] Input validation & sanitization
- [ ] HTTPS everywhere
- [ ] Database encryption
- [ ] API key management
- [ ] CORS configuration

## 📱 Supported Devices & Browsers

- ✅ iOS Safari
- ✅ Android Chrome
- ✅ Desktop browsers
- ✅ Modern browsers (Chrome, Firefox, Safari, Edge)

## 🐛 Troubleshooting

### Telegram Bot tidak merespons
- Pastikan token di `.env` correct
- Verifikasi webhook URL di Telegram
- Check `bot.py` logs

### WhatsApp pesan tidak terkirim
- Verify Twilio credentials
- Check Twilio phone number aktif
- Pastikan phone number format: `+62xxx`

### Customer data tidak tersimpan
- Check database: `sqlite3 data.db`
- Verify SDK initialization
- Check browser console untuk errors

### Admin dashboard tidak loading
- Ensure server running: `python server/main.py`
- Check API_BASE URL di dashboard
- Verify CORS enabled

## 📚 Documentation Files

- **DOKUMENTASI.md** - Complete API reference
- **api_client.py** - Example usage
- **sdk.js** - Mobile SDK documentation
- **README.md** - This file

## 💡 Tips & Best Practices

1. **Backup Database**: Regular backup dari `data.db`
2. **Monitor Logs**: Check server logs untuk errors
3. **Test Integrations**: Gunakan `api_client.py` untuk testing
4. **Environment Variables**: Never commit `.env` dengan credentials
5. **Rate Limiting**: Add rate limiting untuk production
6. **Analytics**: Use admin dashboard untuk monitor customer behavior

## 🌟 Next Steps

1. ✅ Setup Telegram bot dengan token
2. ✅ Configure WhatsApp via Twilio
3. ✅ Get Instagram & Facebook tokens
4. ✅ Deploy ke server (Railway, Heroku, AWS, etc)
5. ✅ Setup domain & SSL
6. ✅ Configure webhook URLs
7. ✅ Start collecting customer data!

## 📞 Support Resources

- Telegram BotFather: https://t.me/botfather
- Twilio Docs: https://www.twilio.com/docs/whatsapp
- FastAPI: https://fastapi.tiangolo.com
- SQLite: https://www.sqlite.org

---

**Version**: 2.0
**Last Updated**: February 6, 2026
**Status**: Production Ready ✅

Made with ❤️ for growing your business!
