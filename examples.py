"""
Example Integration Scripts
Contoh-contoh penggunaan sistem untuk berbagai use case
"""

# ============== EXAMPLE 1: Send Promo ke Telegram ==============

def send_promo_telegram_example():
    """Mengirim promo ke user Telegram"""
    from server.main import bot, get_konten_by_id
    
    chat_id = 123456789  # Telegram chat ID
    konten_id = 1
    
    konten = get_konten_by_id(konten_id)
    
    message = f"""
    🔥 PROMO SPESIAL! 🔥
    
    {konten['judul']}
    
    {konten['deskripsi']}
    
    ✨ Klik link: https://yourdomain.com/?konten={konten_id}
    
    ⏰ Terbatas waktu! Buruan sebelum kehabisan 🚀
    """
    
    bot.send_message(chat_id, message)
    print(f"✅ Promo sent to Telegram user {chat_id}")


# ============== EXAMPLE 2: Send via WhatsApp ==============

def send_promo_whatsapp_example():
    """Mengirim promo ke WhatsApp"""
    from server.whatsapp_bot import whatsapp_bot
    from server.main import get_konten_by_id
    
    phone = "+62812345678"  # Format +62xxx
    konten = get_konten_by_id(1)
    
    result = whatsapp_bot.send_konten_link(phone, konten)
    
    if result:
        print(f"✅ Promo sent to WhatsApp {phone}")
    else:
        print(f"❌ Failed to send to {phone}")


# ============== EXAMPLE 3: Broadcast ke Multiple Customers ==============

def broadcast_to_customers_example():
    """Broadcast konten ke multiple customers berbeda platform"""
    import sqlite3
    from server.main import get_db, get_konten_by_id
    from server.whatsapp_bot import whatsapp_bot
    from server.main import bot
    
    konten = get_konten_by_id(1)
    
    # Get all customers
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, phone, sumber, metadata FROM customers')
    customers = c.fetchall()
    conn.close()
    
    success_count = 0
    failed_count = 0
    
    for customer in customers:
        customer_dict = dict(customer)
        metadata = customer_dict.get('metadata')
        
        try:
            if customer_dict['sumber'] == 'whatsapp':
                result = whatsapp_bot.send_konten_link(customer_dict['phone'], konten)
                if result:
                    success_count += 1
                else:
                    failed_count += 1
                    
            elif customer_dict['sumber'] == 'telegram':
                import json
                metadata = json.loads(metadata) if metadata else {}
                chat_id = metadata.get('telegram_id')
                if chat_id:
                    message = f"📱 {konten['judul']}\n\n{konten['deskripsi']}\n\n🔗 https://yourdomain.com/?konten={konten['id']}"
                    bot.send_message(chat_id, message)
                    success_count += 1
        except Exception as e:
            print(f"Error sending to {customer_dict['phone']}: {e}")
            failed_count += 1
    
    print(f"\n📊 Broadcast Results:")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {failed_count}")


# ============== EXAMPLE 4: Collect Customer Data ==============

def collect_customer_data_example():
    """Contoh mengumpulkan data customer dari mobile SDK"""
    import requests
    import json
    
    API_BASE = "http://localhost:8000"
    
    # Simulating customer device info
    device_info = {
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
        "platform": "iOS",
        "screenResolution": "390x844",
        "timezone": "Asia/Jakarta",
        "language": "id-ID",
        "device": {
            "platform": "iOS",
            "type": "mobile"
        },
        "browser": "Safari"
    }
    
    customer_data = {
        "nama": "John Doe",
        "email": "john@example.com",
        "phone": "+62812345678",
        "sumber": "web",
        "device_info": device_info,
        "metadata": {
            "sessionId": "session_12345",
            "referrer": "google",
            "campaign": "promo_feb"
        }
    }
    
    # Send to server
    response = requests.post(
        f"{API_BASE}/customer/register",
        json=customer_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Customer registered with ID: {result['customer_id']}")
        return result['customer_id']
    else:
        print(f"❌ Error: {response.text}")
        return None


# ============== EXAMPLE 5: Log Customer Interactions ==============

def log_interactions_example(customer_id: int):
    """Log berbagai interaksi customer"""
    import requests
    
    API_BASE = "http://localhost:8000"
    
    interactions = [
        {"platform": "web", "action": "page_load"},
        {"platform": "web", "action": "view_konten", "konten_id": 1},
        {"platform": "web", "action": "view_galeri", "konten_id": 1},
        {"platform": "web", "action": "click_link", "konten_id": 1},
        {"platform": "web", "action": "share", "konten_id": 1},
        {"platform": "web", "action": "page_unload"},
    ]
    
    for interaction in interactions:
        response = requests.post(
            f"{API_BASE}/customer/{customer_id}/log",
            json=interaction
        )
        
        if response.status_code == 200:
            print(f"✅ Logged: {interaction['action']}")
        else:
            print(f"❌ Failed to log: {interaction['action']}")


# ============== EXAMPLE 6: Get Customer Analytics ==============

def get_analytics_example():
    """Get statistics dan analytics"""
    import requests
    
    API_BASE = "http://localhost:8000"
    
    response = requests.get(f"{API_BASE}/admin/stats")
    
    if response.status_code == 200:
        stats = response.json()
        
        print("\n📊 === ANALYTICS REPORT ===\n")
        print(f"👥 Total Customers: {stats['total_customers']}")
        print(f"📱 Total Interactions: {stats['total_interactions']}")
        
        print("\n📈 Customers by Source:")
        for source in stats['customers_by_source']:
            print(f"  • {source['sumber']}: {source['count']}")
        
        print("\n🔝 Top Platforms:")
        for platform in stats['top_platforms']:
            print(f"  • {platform['platform']}: {platform['count']}")
        
        print("\n🎯 Top Actions:")
        for action in stats['top_actions']:
            print(f"  • {action['action']}: {action['count']}")
    else:
        print(f"❌ Error: {response.text}")


# ============== EXAMPLE 7: Social Media Integration ==============

def send_instagram_dm_example():
    """Send DM ke Instagram user"""
    from server.social_media import social_media
    
    user_id = 12345  # Instagram user ID
    message = "Check out our latest collection! 🎁"
    media_url = "https://example.com/image.jpg"
    
    result = social_media.send_instagram_dm(user_id, message, media_url)
    
    if result['success']:
        print(f"✅ Instagram DM sent: {result['message']}")
    else:
        print(f"❌ Failed: {result['error']}")


# ============== EXAMPLE 8: Create Konten via API ==============

def create_konten_example():
    """Create konten baru dengan API"""
    import requests
    
    API_BASE = "http://localhost:8000"
    
    konten_data = {
        "judul": "Produk Terbaru 2024",
        "deskripsi": "Produk revolusioner dengan fitur-fitur terbaru",
        "kategori": "produk",
        "isi": """
        Ini adalah deskripsi lengkap dari produk kami.
        
        Fitur utama:
        1. Feature A
        2. Feature B
        3. Feature C
        
        Untuk pemesanan, hubungi kami sekarang!
        """,
        "gambar_utama": "https://via.placeholder.com/600x400?text=Produk+Baru",
        "galeri": [
            {"url": "https://via.placeholder.com/400x400?text=Gallery+1", "deskripsi": "View 1"},
            {"url": "https://via.placeholder.com/400x400?text=Gallery+2", "deskripsi": "View 2"},
            {"url": "https://via.placeholder.com/400x400?text=Gallery+3", "deskripsi": "View 3"}
        ]
    }
    
    response = requests.post(
        f"{API_BASE}/konten/create",
        json=konten_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Konten created with ID: {result['konten_id']}")
        return result['konten_id']
    else:
        print(f"❌ Error: {response.text}")
        return None


# ============== EXAMPLE 9: Customer Segmentation ==============

def segment_customers_example():
    """Segment customers berdasarkan behavior"""
    from server.main import get_db
    
    conn = get_db()
    c = conn.cursor()
    
    # Get customers dengan banyak interactions
    c.execute('''
        SELECT c.id, c.nama, COUNT(i.id) as interaction_count
        FROM customers c
        LEFT JOIN customer_interactions i ON c.id = i.customer_id
        GROUP BY c.id
        HAVING interaction_count > 5
        ORDER BY interaction_count DESC
    ''')
    
    high_engagement = [dict(row) for row in c.fetchall()]
    
    print("\n👥 === HIGH ENGAGEMENT CUSTOMERS ===\n")
    for customer in high_engagement:
        print(f"• {customer['nama']} - {customer['interaction_count']} interactions")
    
    conn.close()


# ============== EXAMPLE 10: Email Integration ==============

def send_email_notification_example():
    """Send email notification ke customer"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    def send_email(to_email: str, subject: str, body: str):
        """Send email using SMTP"""
        sender_email = "your-email@example.com"
        sender_password = "your-app-password"
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "html"))
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
                print(f"✅ Email sent to {to_email}")
                return True
        except Exception as e:
            print(f"❌ Email error: {e}")
            return False
    
    # Example: Send promotional email
    email_body = """
    <html>
        <body>
            <h2>🎁 Special Promotion for You!</h2>
            <p>We have a special offer just for you:</p>
            <p><a href="https://yourdomain.com/?konten=1">View Promotion</a></p>
            <p>Limited time only!</p>
        </body>
    </html>
    """
    
    send_email(
        to_email="customer@example.com",
        subject="🎁 Special Promotion Just For You!",
        body=email_body
    )


# ============== RUN ALL EXAMPLES ==============

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📚 PROJECT SERVER - INTEGRATION EXAMPLES")
    print("="*60)
    
    # # Uncomment untuk run examples
    # print("\n1️⃣  Send Promo Telegram")
    # send_promo_telegram_example()
    
    # print("\n2️⃣  Send Promo WhatsApp")
    # send_promo_whatsapp_example()
    
    # print("\n3️⃣  Broadcast ke Multiple Customers")
    # broadcast_to_customers_example()
    
    # print("\n4️⃣  Collect Customer Data")
    # customer_id = collect_customer_data_example()
    
    # print("\n5️⃣  Log Customer Interactions")
    # if customer_id:
    #     log_interactions_example(customer_id)
    
    # print("\n6️⃣  Get Analytics")
    # get_analytics_example()
    
    # print("\n8️⃣  Create Konten")
    # create_konten_example()
    
    # print("\n9️⃣  Segment Customers")
    # segment_customers_example()
    
    print("\n" + "="*60)
    print("✅ Examples ready to use!")
    print("Uncomment functions di main block untuk run")
    print("="*60)
