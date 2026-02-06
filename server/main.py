from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
from datetime import datetime
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

from server.security import add_security_middleware

app = FastAPI(title="Project Server - Multi Platform", version="2.0")

# Attach security middleware (CORS, rate limiter, security headers)
# Configure via environment variables: ALLOWED_ORIGINS (comma-separated), RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW_SECONDS
allowed = os.getenv("ALLOWED_ORIGINS", "*")
if allowed.strip() == "*":
    origins = ["*"]
else:
    origins = [o.strip() for o in allowed.split(",") if o.strip()]

max_requests = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "200"))
window_seconds = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

add_security_middleware(app, allow_origins=origins, max_requests=max_requests, window_seconds=window_seconds)

# Initialize Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8505712679:AAGIkuamaV2WFH-XUBjtcB4y8-6zP9kYHXc")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ======================== Models ========================
class Gambar(BaseModel):
    id: int
    url: str
    deskripsi: str

class Konten(BaseModel):
    id: int
    judul: str
    deskripsi: str
    kategori: str
    isi: str
    gambar_utama: str
    tanggal: str
    galeri: List[Gambar] = []

class CustomerData(BaseModel):
    """Model untuk data customer dari device mereka"""
    nama: str
    email: Optional[str] = None
    phone: str
    sumber: str  # "telegram", "whatsapp", "instagram", "facebook", "web"
    device_info: Optional[dict] = None  # info tentang device mereka
    metadata: Optional[dict] = None  # data tambahan lainnya

class CustomerInteraction(BaseModel):
    """Model untuk tracking interaksi customer"""
    customer_id: int
    platform: str  # "telegram", "whatsapp", "instagram", etc
    action: str  # "click_link", "view_galeri", "message", etc
    konten_id: Optional[int] = None
    timestamp: Optional[str] = None

# ======================== Database Setup ========================
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Tabel konten
    c.execute('''CREATE TABLE IF NOT EXISTS konten
                 (id INTEGER PRIMARY KEY, 
                  judul TEXT, 
                  deskripsi TEXT,
                  kategori TEXT,
                  isi TEXT,
                  gambar_utama TEXT,
                  tanggal TEXT)''')
    
    # Tabel galeri
    c.execute('''CREATE TABLE IF NOT EXISTS galeri
                 (id INTEGER PRIMARY KEY,
                  konten_id INTEGER,
                  url TEXT,
                  deskripsi TEXT,
                  FOREIGN KEY(konten_id) REFERENCES konten(id))''')
    
    # Tabel customer data (BARU)
    c.execute('''CREATE TABLE IF NOT EXISTS customers
                 (id INTEGER PRIMARY KEY,
                  nama TEXT,
                  email TEXT,
                  phone TEXT UNIQUE,
                  sumber TEXT,
                  device_info TEXT,
                  metadata TEXT,
                  registered_date TEXT,
                  last_activity TEXT)''')
    
    # Tabel interaksi customer (BARU)
    c.execute('''CREATE TABLE IF NOT EXISTS customer_interactions
                 (id INTEGER PRIMARY KEY,
                  customer_id INTEGER,
                  platform TEXT,
                  action TEXT,
                  konten_id INTEGER,
                  timestamp TEXT,
                  FOREIGN KEY(customer_id) REFERENCES customers(id),
                  FOREIGN KEY(konten_id) REFERENCES konten(id))''')
    
    # Tabel social media accounts (BARU)
    c.execute('''CREATE TABLE IF NOT EXISTS social_accounts
                 (id INTEGER PRIMARY KEY,
                  platform TEXT,
                  account_id TEXT,
                  account_username TEXT,
                  access_token TEXT,
                  metadata TEXT,
                  created_date TEXT)''')
    
    conn.commit()
    conn.close()

# ======================== Helper Functions ========================
def get_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_konten_by_id(konten_id: int):
    conn = get_db()
    c = conn.cursor()
    
    # Get konten
    c.execute('SELECT * FROM konten WHERE id = ?', (konten_id,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        return None
    
    konten = dict(row)
    
    # Get galeri
    c.execute('SELECT id, url, deskripsi FROM galeri WHERE konten_id = ?', (konten_id,))
    galeri = [dict(r) for r in c.fetchall()]
    konten['galeri'] = galeri
    
    conn.close()
    return konten

# Customer helper functions (BARU)
def save_customer_data(nama: str, email: str, phone: str, sumber: str, device_info: dict = None, metadata: dict = None):
    """Save atau update customer data"""
    conn = get_db()
    c = conn.cursor()
    
    try:
        # Try update jika sudah exist
        c.execute('SELECT id FROM customers WHERE phone = ?', (phone,))
        existing = c.fetchone()
        
        if existing:
            customer_id = existing['id']
            c.execute('''UPDATE customers 
                         SET nama=?, email=?, device_info=?, metadata=?, last_activity=?
                         WHERE id=?''',
                      (nama, email, json.dumps(device_info) if device_info else None,
                       json.dumps(metadata) if metadata else None, 
                       datetime.now().isoformat(), customer_id))
        else:
            c.execute('''INSERT INTO customers 
                         (nama, email, phone, sumber, device_info, metadata, registered_date, last_activity)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (nama, email, phone, sumber, 
                       json.dumps(device_info) if device_info else None,
                       json.dumps(metadata) if metadata else None,
                       datetime.now().isoformat(), datetime.now().isoformat()))
            customer_id = c.lastrowid
        
        conn.commit()
        return customer_id
    except Exception as e:
        print(f"Error saving customer: {e}")
        return None
    finally:
        conn.close()

def log_customer_interaction(customer_id: int, platform: str, action: str, konten_id: int = None):
    """Log interaksi customer"""
    conn = get_db()
    c = conn.cursor()
    
    try:
        c.execute('''INSERT INTO customer_interactions 
                     (customer_id, platform, action, konten_id, timestamp)
                     VALUES (?, ?, ?, ?, ?)''',
                  (customer_id, platform, action, konten_id, datetime.now().isoformat()))
        conn.commit()
    except Exception as e:
        print(f"Error logging interaction: {e}")
    finally:
        conn.close()

def get_customer_by_phone(phone: str):
    """Get customer data by phone"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM customers WHERE phone = ?', (phone,))
    row = c.fetchone()
    conn.close()
    
    if row:
        customer = dict(row)
        if customer['device_info']:
            customer['device_info'] = json.loads(customer['device_info'])
        if customer['metadata']:
            customer['metadata'] = json.loads(customer['metadata'])
        return customer
    return None

# ======================== Routes ========================

@app.get("/")
def health():
    return {"status": "SERVER RUNNING", "message": "Klik link untuk melihat konten"}

# Get semua konten (list semua link)
@app.get("/konten")
def list_konten():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, judul, deskripsi, kategori, gambar_utama, tanggal FROM konten ORDER BY tanggal DESC')
    konten_list = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {
        "total": len(konten_list),
        "data": konten_list
    }

# Get konten detail saat di-click
@app.get("/konten/{konten_id}")
def get_konten(konten_id: int):
    konten = get_konten_by_id(konten_id)
    
    if not konten:
        raise HTTPException(status_code=404, detail="Konten tidak ditemukan")
    
    return konten

# Get galeri dari konten tertentu
@app.get("/konten/{konten_id}/galeri")
def get_galeri(konten_id: int):
    conn = get_db()
    c = conn.cursor()
    
    # Check konten exists
    c.execute('SELECT id FROM konten WHERE id = ?', (konten_id,))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Konten tidak ditemukan")
    
    # Get galeri
    c.execute('SELECT id, url, deskripsi FROM galeri WHERE konten_id = ? ORDER BY id', (konten_id,))
    galeri = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {
        "konten_id": konten_id,
        "total_gambar": len(galeri),
        "galeri": galeri
    }

# Get berdasarkan kategori
@app.get("/kategori/{kategori}")
def get_by_kategori(kategori: str):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, judul, deskripsi, kategori, gambar_utama, tanggal FROM konten WHERE kategori = ? ORDER BY tanggal DESC', (kategori,))
    konten_list = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {
        "kategori": kategori,
        "total": len(konten_list),
        "data": konten_list
    }

# Create konten baru
@app.post("/konten/create")
def create_konten(data: dict):
    try:
        conn = get_db()
        c = conn.cursor()
        
        tanggal = datetime.now().isoformat()
        
        c.execute('''INSERT INTO konten 
                     (judul, deskripsi, kategori, isi, gambar_utama, tanggal)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (data['judul'], data['deskripsi'], data['kategori'], 
                   data['isi'], data['gambar_utama'], tanggal))
        
        konten_id = c.lastrowid
        
        # Add galeri jika ada
        if 'galeri' in data:
            for gambar in data['galeri']:
                c.execute('''INSERT INTO galeri 
                             (konten_id, url, deskripsi)
                             VALUES (?, ?, ?)''',
                          (konten_id, gambar['url'], gambar.get('deskripsi', '')))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "konten_id": konten_id, "message": "Konten berhasil dibuat"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete konten
@app.delete("/konten/{konten_id}")
def delete_konten(konten_id: int):
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Delete galeri dulu
        c.execute('DELETE FROM galeri WHERE konten_id = ?', (konten_id,))
        # Delete konten
        c.execute('DELETE FROM konten WHERE id = ?', (konten_id,))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Konten berhasil dihapus"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== CUSTOMER DATA ENDPOINTS (BARU) ==============

# Save customer data (dari mobile/SDK)
@app.post("/customer/register")
async def register_customer(data: CustomerData):
    """Save customer data dari perangkat mereka"""
    try:
        customer_id = save_customer_data(
            nama=data.nama,
            email=data.email or "",
            phone=data.phone,
            sumber=data.sumber,
            device_info=data.device_info,
            metadata=data.metadata
        )
        
        if customer_id:
            log_customer_interaction(customer_id, data.sumber, "register")
            return {"status": "success", "customer_id": customer_id, "message": "Data customer berhasil disimpan"}
        else:
            raise HTTPException(status_code=400, detail="Gagal menyimpan data customer")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get semua customers (untuk admin dashboard)
@app.get("/admin/customers")
def get_all_customers():
    """Get semua customer data (admin only)"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, nama, email, phone, sumber, registered_date, last_activity FROM customers ORDER BY registered_date DESC')
    customers = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {
        "total": len(customers),
        "data": customers
    }

# Get customer detail
@app.get("/admin/customers/{customer_id}")
def get_customer_detail(customer_id: int):
    """Get detail customer lengkap"""
    conn = get_db()
    c = conn.cursor()
    
    # Get customer data
    c.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer tidak ditemukan")
    
    customer = dict(row)
    
    # Get interaksi history
    c.execute('''SELECT * FROM customer_interactions 
                 WHERE customer_id = ? 
                 ORDER BY timestamp DESC LIMIT 50''', (customer_id,))
    interactions = [dict(r) for r in c.fetchall()]
    
    customer['interactions'] = interactions
    
    # Parse JSON fields
    if customer['device_info']:
        customer['device_info'] = json.loads(customer['device_info'])
    if customer['metadata']:
        customer['metadata'] = json.loads(customer['metadata'])
    
    conn.close()
    return customer

# Log customer interaction
@app.post("/customer/{customer_id}/log")
async def log_interaction(customer_id: int, data: CustomerInteraction):
    """Log interaksi customer (untuk tracking)"""
    try:
        log_customer_interaction(
            customer_id=customer_id,
            platform=data.platform,
            action=data.action,
            konten_id=data.konten_id
        )
        return {"status": "success", "message": "Interaksi tercatat"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get customer by phone
@app.get("/customer/phone/{phone}")
def get_customer_info(phone: str):
    """Get customer info by phone number"""
    customer = get_customer_by_phone(phone)
    if customer:
        return customer
    raise HTTPException(status_code=404, detail="Customer tidak ditemukan")

# Get customer stats
@app.get("/admin/stats")
def get_stats():
    """Get statistik customers dan interactions"""
    conn = get_db()
    c = conn.cursor()
    
    # Total customers
    c.execute('SELECT COUNT(*) as total FROM customers')
    total_customers = c.fetchone()['total']
    
    # Customers by sumber
    c.execute('SELECT sumber, COUNT(*) as count FROM customers GROUP BY sumber')
    customers_by_source = [dict(row) for row in c.fetchall()]
    
    # Total interactions
    c.execute('SELECT COUNT(*) as total FROM customer_interactions')
    total_interactions = c.fetchone()['total']
    
    # Top platforms
    c.execute('SELECT platform, COUNT(*) as count FROM customer_interactions GROUP BY platform ORDER BY count DESC')
    top_platforms = [dict(row) for row in c.fetchall()]
    
    # Top actions
    c.execute('SELECT action, COUNT(*) as count FROM customer_interactions GROUP BY action ORDER BY count DESC')
    top_actions = [dict(row) for row in c.fetchall()]
    
    conn.close()
    
    return {
        "total_customers": total_customers,
        "customers_by_source": customers_by_source,
        "total_interactions": total_interactions,
        "top_platforms": top_platforms,
        "top_actions": top_actions
    }

# ============== BACKUP SYSTEM ENDPOINTS (SECURE) ==============

@app.post("/backup/request-permission")
async def request_backup_permission(data: dict):
    """
    Request backup permission dari customer
    Customer akan menerima notifikasi untuk approve/deny
    """
    try:
        from server.backup_system import request_backup_permission
        
        result = request_backup_permission(
            customer_id=data.get('customer_id'),
            backup_types=data.get('backup_types', ['photos', 'documents']),
            ip_address=data.get('ip_address', ''),
            device_info=data.get('device_info', {})
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/backup/consent")
async def customer_consent_backup(data: dict):
    """
    Customer APPROVE backup permission
    Hanya customer dengan authenticated session bisa approve
    """
    try:
        from server.backup_system import customer_consent_backup
        
        result = customer_consent_backup(
            customer_id=data.get('customer_id'),
            backup_types=data.get('backup_types', []),
            ip_address=data.get('ip_address', ''),
            device_info=data.get('device_info', {})
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/backup/permission/{customer_id}")
async def get_backup_permission(customer_id: int):
    """Get backup permission status untuk customer"""
    try:
        from server.backup_system import get_backup_permission
        return get_backup_permission(customer_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/backup/create")
async def create_backup(data: dict):
    """
    Create backup untuk customer
    Memerlukan customer authenticated + consent
    """
    try:
        from server.backup_system import create_backup
        
        result = create_backup(
            customer_id=data.get('customer_id'),
            backup_name=data.get('backup_name', f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            backup_types=data.get('backup_types', []),
            sample_files=data.get('files', {}),
            password=data.get('password', ''),
            ip_address=data.get('ip_address', ''),
            device_info=data.get('device_info', {})
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/backup/list/{customer_id}")
async def get_backup_list(customer_id: int):
    """Get semua backup untuk customer (private)"""
    try:
        from server.backup_system import get_backup_list
        backups = get_backup_list(customer_id)
        return {
            "customer_id": customer_id,
            "total": len(backups),
            "backups": backups
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/backup/restore")
async def restore_backup(data: dict):
    """
    Restore backup untuk customer
    Hanya customer sendiri yang bisa restore backup mereka
    """
    try:
        from server.backup_system import restore_backup
        
        result = restore_backup(
            backup_id=data.get('backup_id'),
            customer_id=data.get('customer_id'),
            password=data.get('password'),
            ip_address=data.get('ip_address', ''),
            device_info=data.get('device_info', {})
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/backup/audit/{customer_id}")
async def get_backup_audit_logs(customer_id: int):
    """Get audit logs untuk backup activities customer"""
    try:
        from server.backup_system import get_audit_logs
        
        logs = get_audit_logs(customer_id, limit=100)
        return {
            "customer_id": customer_id,
            "total_logs": len(logs),
            "logs": logs
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/backup/{backup_id}")
async def delete_backup(backup_id: int, customer_id: int):
    """Delete backup untuk customer"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Verify backup belongs to customer
        c.execute('SELECT customer_id FROM backups WHERE id = ?', (backup_id,))
        result = c.fetchone()
        
        if not result or result['customer_id'] != customer_id:
            conn.close()
            raise HTTPException(status_code=403, detail="Backup tidak ditemukan atau bukan milik Anda")
        
        # Delete backup items
        c.execute('DELETE FROM backup_items WHERE backup_id = ?', (backup_id,))
        
        # Delete backup
        c.execute('DELETE FROM backups WHERE id = ?', (backup_id,))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Backup berhasil dihapus"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== TELEGRAM BOT HANDLERS (BARU) ==============

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Webhook untuk Telegram Bot"""
    try:
        json_data = await request.json()
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return {"ok": True}
    except Exception as e:
        print(f"Telegram webhook error: {e}")
        return {"ok": False, "error": str(e)}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handler untuk /start command"""
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    phone = message.contact.phone_number if message.contact else None
    
    # Save customer data
    if phone:
        save_customer_data(
            nama=user_name,
            email=message.from_user.username or "",
            phone=phone,
            sumber="telegram",
            metadata={"telegram_id": chat_id}
        )
    
    # Send welcome message dengan link konten
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, judul FROM konten LIMIT 5')
    konten_list = c.fetchall()
    conn.close()
    
    welcome_text = f"👋 Selamat datang {user_name}!\n\n"
    welcome_text += "📱 Konten terbaru kami:\n"
    
    for konten in konten_list:
        # Deep link ke web dengan konten ID
        link = f"https://yourdomain.com/?konten={konten['id']}"
        welcome_text += f"• <a href='{link}'>{konten['judul']}</a>\n"
    
    welcome_text += "\n💬 Ketik 'promo' untuk melihat promosi terbaru"
    
    bot.send_message(chat_id, welcome_text, parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text.lower() in ['promo', 'produk', 'berita'])
def send_by_category(message):
    """Handler untuk pesan kategori"""
    chat_id = message.chat.id
    category = message.text.lower()
    
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, judul, deskripsi FROM konten WHERE kategori = ? LIMIT 5', (category,))
    konten_list = c.fetchall()
    conn.close()
    
    if konten_list:
        response = f"📌 Konten kategori '{category}':\n\n"
        for konten in konten_list:
            link = f"https://yourdomain.com/?konten={konten['id']}"
            response += f"• <a href='{link}'>{konten['judul']}</a>\n{konten['deskripsi']}\n\n"
    else:
        response = f"❌ Tidak ada konten di kategori '{category}'"
    
    bot.send_message(chat_id, response, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Handler default untuk pesan lain"""
    bot.reply_to(message, "Ketik salah satu: /start, promo, produk, berita")

# ======================== Initialize ========================
if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
