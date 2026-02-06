"""
WhatsApp Bot Integration menggunakan Twilio
Untuk menggunakan fitur ini, daftar ke Twilio dan dapatkan API credentials
"""

from twilio.rest import Client
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class WhatsAppBot:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
    
    def send_message(self, to_number: str, message: str, media_url: Optional[str] = None):
        """Send pesan WhatsApp"""
        if not self.client:
            print("WhatsApp bot tidak dikonfigurasi")
            return False
        
        try:
            if media_url:
                # Send dengan gambar
                message_obj = self.client.messages.create(
                    from_=f"whatsapp:{self.whatsapp_number}",
                    to=f"whatsapp:{to_number}",
                    body=message,
                    media_url=media_url
                )
            else:
                # Send text only
                message_obj = self.client.messages.create(
                    from_=f"whatsapp:{self.whatsapp_number}",
                    to=f"whatsapp:{to_number}",
                    body=message
                )
            
            print(f"WhatsApp message sent: {message_obj.sid}")
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
    
    def send_konten_link(self, to_number: str, konten_data: dict):
        """Send konten dengan link"""
        message = f"""
📱 *{konten_data['judul']}*

{konten_data['deskripsi']}

🔗 Lihat lengkap: https://yourdomain.com/?konten={konten_data['id']}

Kategori: {konten_data['kategori']}
        """
        
        return self.send_message(
            to_number=to_number,
            message=message,
            media_url=konten_data.get('gambar_utama')
        )
    
    def send_promo(self, to_number: str, promo_data: dict):
        """Send promo spesial"""
        message = f"""
🎉 *PROMO SPESIAL!*

{promo_data['judul']}
{promo_data['deskripsi']}

👉 Klik link: https://yourdomain.com/?konten={promo_data['id']}

⏰ Terbatas waktu! Buruan sebelum kehabisan stock 🔥
        """
        
        return self.send_message(
            to_number=to_number,
            message=message,
            media_url=promo_data.get('gambar_utama')
        )

# Export bot instance
whatsapp_bot = WhatsAppBot()
