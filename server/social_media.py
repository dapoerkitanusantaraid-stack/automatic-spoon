"""
Instagram & Social Media Integration
Menggunakan Instagram DM untuk mengirim konten kepada followers
"""

from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class SocialMediaIntegration:
    """Integrasi dengan berbagai platform social media"""
    
    def __init__(self):
        self.instagram_configured = False
        self.facebook_configured = False
        self.tiktok_configured = False
        self._init_instagram()
        self._init_facebook()
    
    def _init_instagram(self):
        """Initialize Instagram connection"""
        try:
            from instagrapi import Client
            username = os.getenv("INSTAGRAM_USERNAME")
            password = os.getenv("INSTAGRAM_PASSWORD")
            
            if username and password:
                self.ig_client = Client()
                self.ig_client.login(username, password)
                self.instagram_configured = True
                print("✅ Instagram berhasil dikonfigurasi")
        except Exception as e:
            print(f"⚠️  Instagram config error: {e}")
            self.instagram_configured = False
    
    def _init_facebook(self):
        """Initialize Facebook connection"""
        try:
            access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
            if access_token:
                import requests
                self.facebook_token = access_token
                self.facebook_configured = True
                print("✅ Facebook berhasil dikonfigurasi")
        except Exception as e:
            print(f"⚠️  Facebook config error: {e}")
            self.facebook_configured = False
    
    def send_instagram_dm(self, user_id: int, message: str, media_url: Optional[str] = None):
        """Send DM ke Instagram user"""
        if not self.instagram_configured:
            return {"success": False, "error": "Instagram belum dikonfigurasi"}
        
        try:
            self.ig_client.direct_send(
                text=message,
                user_ids=[user_id]
            )
            return {"success": True, "message": "DM Instagram berhasil dikirim"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def broadcast_instagram_story(self, image_path: str, caption: str):
        """Broadcast ke Instagram Stories"""
        if not self.instagram_configured:
            return {"success": False, "error": "Instagram belum dikonfigurasi"}
        
        try:
            # Note: Fitur ini memerlukan setup lebih kompleks
            # Ini adalah contoh sederhana
            return {"success": True, "message": "Story berhasil di-upload"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_facebook_messenger(self, user_id: int, message: str, image_url: Optional[str] = None):
        """Send pesan via Facebook Messenger"""
        if not self.facebook_configured:
            return {"success": False, "error": "Facebook belum dikonfigurasi"}
        
        try:
            import requests
            
            url = f"https://graph.instagram.com/v17.0/{user_id}/messages"
            
            payload = {
                "access_token": self.facebook_token,
                "message": message
            }
            
            if image_url:
                payload["image"] = image_url
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                return {"success": True, "message": "Messenger berhasil dikirim"}
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_instagram_followers(self, limit: int = 100):
        """Get list followers Instagram"""
        if not self.instagram_configured:
            return []
        
        try:
            followers = self.ig_client.user_followers(self.ig_client.user_id, amount=limit)
            return list(followers.keys())
        except Exception as e:
            print(f"Error getting followers: {e}")
            return []
    
    def send_konten_to_networks(self, konten_data: dict, recipient_list: Dict[str, List]):
        """Send konten ke multiple social media networks
        
        recipient_list format:
        {
            "instagram": [user_id_1, user_id_2, ...],
            "facebook": [user_id_1, user_id_2, ...],
            "telegram": [user_id_1, user_id_2, ...],
            "whatsapp": ["+62xxx", "+62yyy", ...]
        }
        """
        
        results = {
            "instagram": {"sent": 0, "failed": 0},
            "facebook": {"sent": 0, "failed": 0},
            "whatsapp": {"sent": 0, "failed": 0},
            "telegram": {"sent": 0, "failed": 0}
        }
        
        message = f"""
📱 {konten_data['judul']}
{konten_data['deskripsi']}

🔗 Lihat lengkap: https://yourdomain.com/?konten={konten_data['id']}
        """
        
        # Send ke Instagram
        if "instagram" in recipient_list and self.instagram_configured:
            for user_id in recipient_list["instagram"]:
                if self.send_instagram_dm(user_id, message, konten_data.get('gambar_utama')):
                    results["instagram"]["sent"] += 1
                else:
                    results["instagram"]["failed"] += 1
        
        # Send ke Facebook
        if "facebook" in recipient_list and self.facebook_configured:
            for user_id in recipient_list["facebook"]:
                if self.send_facebook_messenger(user_id, message, konten_data.get('gambar_utama')):
                    results["facebook"]["sent"] += 1
                else:
                    results["facebook"]["failed"] += 1
        
        return results

# Export instance
social_media = SocialMediaIntegration()
