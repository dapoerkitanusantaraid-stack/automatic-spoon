"""
API Client untuk Project Server
Gunakan script ini untuk test dan interact dengan API
"""

import requests
import json
from typing import Dict, List, Optional

class ProjectServerAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict:
        """Check apakah server berjalan"""
        try:
            response = self.session.get(f"{self.base_url}/")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_all_konten(self) -> Dict:
        """Get semua konten"""
        try:
            response = self.session.get(f"{self.base_url}/konten")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_konten_detail(self, konten_id: int) -> Dict:
        """Get detail konten saat di-click"""
        try:
            response = self.session.get(f"{self.base_url}/konten/{konten_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_galeri(self, konten_id: int) -> Dict:
        """Get galeri dari konten"""
        try:
            response = self.session.get(f"{self.base_url}/konten/{konten_id}/galeri")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_by_kategori(self, kategori: str) -> Dict:
        """Get konten by kategori"""
        try:
            response = self.session.get(f"{self.base_url}/kategori/{kategori}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def create_konten(self, data: Dict) -> Dict:
        """Create konten baru"""
        try:
            response = self.session.post(
                f"{self.base_url}/konten/create",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def delete_konten(self, konten_id: int) -> Dict:
        """Hapus konten"""
        try:
            response = self.session.delete(f"{self.base_url}/konten/{konten_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def print_result(title: str, data: Dict):
    """Pretty print hasil API"""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print('='*60)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """Demo dan testing API"""
    api = ProjectServerAPI()
    
    print("\n" + "="*60)
    print("🚀 PROJECT SERVER API CLIENT")
    print("="*60)
    
    # 1. Health check
    print_result("1. Health Check", api.health_check())
    
    # 2. Get all konten
    result = api.get_all_konten()
    print_result("2. Semua Konten", result)
    
    if "data" in result and len(result["data"]) > 0:
        first_konten = result["data"][0]
        konten_id = first_konten["id"]
        
        # 3. Get detail konten
        print_result(f"3. Detail Konten ID {konten_id}", api.get_konten_detail(konten_id))
        
        # 4. Get galeri
        print_result(f"4. Galeri Konten ID {konten_id}", api.get_galeri(konten_id))
    
    # 5. Get by kategori
    print_result("5. Konten Kategori 'promo'", api.get_by_kategori("promo"))
    
    # 6. Create konten baru (example)
    new_konten = {
        "judul": "Konten Test dari API Client",
        "deskripsi": "Ini adalah konten yang dibuat melalui API",
        "kategori": "artikel",
        "isi": "Konten lengkap dari API client. Ini adalah testing pembuatan konten baru melalui endpoint API.",
        "gambar_utama": "https://via.placeholder.com/600x400?text=API+Test",
        "galeri": [
            {
                "url": "https://via.placeholder.com/300x300?text=Test+Galeri+1",
                "deskripsi": "Gambar Test 1"
            },
            {
                "url": "https://via.placeholder.com/300x300?text=Test+Galeri+2",
                "deskripsi": "Gambar Test 2"
            }
        ]
    }
    
    result_create = api.create_konten(new_konten)
    print_result("6. Create Konten Baru", result_create)
    
    # 7. Contoh pagination (optional)
    print("\n" + "="*60)
    print("💡 TIPS & CONTOH PENGGUNAAN LANJUTAN")
    print("="*60)
    
    print("""
1. Gunakan di Python script:
   from api_client import ProjectServerAPI
   api = ProjectServerAPI("http://localhost:8000")
   result = api.get_all_konten()

2. Gunakan di curl:
   curl http://localhost:8000/konten

3. Gunakan di JavaScript:
   fetch('http://localhost:8000/konten')
     .then(r => r.json())
     .then(data => console.log(data))

4. Create konten dengan curl:
   curl -X POST http://localhost:8000/konten/create \\
     -H "Content-Type: application/json" \\
     -d '{"judul":"...","deskripsi":"...","kategori":"promo","isi":"...","gambar_utama":"..."}'
    """)


if __name__ == "__main__":
    main()
