# 📱 Project Server - Dokumentasi Lengkap

## 🎯 Deskripsi Project

Project ini adalah sistem web server yang memungkinkan Anda:
- ✅ Membuat multiple links/konten dengan kategori berbeda
- ✅ Menampilkan detail lengkap saat link di-click
- ✅ Melihat galeri gambar untuk setiap konten
- ✅ Filter konten berdasarkan kategori
- ✅ API backend yang powerful dan mudah diintegrasikan

## 📁 Struktur Folder

```
Project-Server/
├── server/
│   └── main.py              # FastAPI backend server
├── index.html               # Frontend dengan UI modern
├── init_sample_data.py      # Script untuk load sample data
├── requirements.txt         # Dependencies Python
└── README.md               # File dokumentasi
```

## 🚀 Cara Instalasi & Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Server
```bash
cd server
python main.py
```

Server akan berjalan di: **http://localhost:8000**

### 3. Load Sample Data (Optional)
```bash
python init_sample_data.py
```

Ini akan membuat database dengan 6 konten sample.

### 4. Buka Frontend
- Buka file `index.html` di browser atau
- Akses: `file:///path/ke/Project-Server/index.html`

## 📡 API Endpoints

### GET /
Cek status server
```
Response: {"status": "SERVER RUNNING"}
```

### GET /konten
Dapatkan semua konten (list semua link)
```
Response: {
  "total": 6,
  "data": [
    {
      "id": 1,
      "judul": "Judul Konten",
      "deskripsi": "Deskripsi singkat",
      "kategori": "promo",
      "gambar_utama": "url_gambar",
      "tanggal": "2024-02-06T..."
    }
  ]
}
```

### GET /konten/{id}
Dapatkan detail konten lengkap saat di-click
```
Response: {
  "id": 1,
  "judul": "Judul Konten",
  "deskripsi": "Deskripsi",
  "kategori": "promo",
  "isi": "Isi lengkap konten...",
  "gambar_utama": "url",
  "tanggal": "...",
  "galeri": [
    {"id": 1, "url": "image1.jpg", "deskripsi": "..."},
    {"id": 2, "url": "image2.jpg", "deskripsi": "..."}
  ]
}
```

### GET /konten/{id}/galeri
Dapatkan galeri dari konten tertentu
```
Response: {
  "konten_id": 1,
  "total_gambar": 3,
  "galeri": [...]
}
```

### GET /kategori/{kategori}
Filter konten berdasarkan kategori
```
GET /kategori/promo
Response: {
  "kategori": "promo",
  "total": 2,
  "data": [...]
}
```

**Kategori yang tersedia:**
- `promo` - Promosi dan penawaran special
- `artikel` - Artikel dan tutorial
- `produk` - Produk dan katalog
- `berita` - Berita dan update
- `event` - Event dan acara

### POST /konten/create
Membuat konten baru
```json
{
  "judul": "Judul Konten",
  "deskripsi": "Deskripsi singkat",
  "kategori": "promo",
  "isi": "Isi lengkap konten...",
  "gambar_utama": "https://example.com/image.jpg",
  "galeri": [
    {"url": "https://example.com/foto1.jpg", "deskripsi": "Foto 1"},
    {"url": "https://example.com/foto2.jpg", "deskripsi": "Foto 2"}
  ]
}
```

### DELETE /konten/{id}
Menghapus konten
```
Response: {"status": "success", "message": "Konten berhasil dihapus"}
```

## 💡 Contoh Penggunaan

### Membuat Konten Baru via API
```bash
curl -X POST http://localhost:8000/konten/create \
  -H "Content-Type: application/json" \
  -d '{
    "judul": "Produk Terbaru",
    "deskripsi": "Produk revolutionary kami",
    "kategori": "produk",
    "isi": "Penjelasan lengkap tentang produk...",
    "gambar_utama": "https://example.com/product.jpg",
    "galeri": [
      {"url": "https://example.com/p1.jpg", "deskripsi": "View 1"},
      {"url": "https://example.com/p2.jpg", "deskripsi": "View 2"}
    ]
  }'
```

## 🎨 Frontend Features

### 1. **List Konten**
- Grid layout responsive yang menampilkan semua konten
- Card dengan thumbnail gambar
- Badge kategori yang colorful
- Tanggal publikasi

### 2. **Filter by Kategori**
- Dropdown untuk filter berdasarkan kategori
- Update list otomatis saat kategori berubah
- Option "Semua Kategori"

### 3. **Detail Modal**
Ketika link di-click:
- Header dengan judul dan kategori
- Gambar utama yang besar
- Deskripsi singkat
- Isi lengkap konten
- **Galeri lengkap** dengan semua gambar
- Tanggal publikasi

### 4. **Galeri**
- Grid thumbnail yang bisa di-click
- Hover effect dengan zoom
- Buka gambar full size di tab baru

### 5. **Responsive Design**
- Mobile-friendly interface
- Smooth animations
- Modern UI dengan gradient colors

## 🔧 Customization

### Mengubah Warna
Edit di `index.html` bagian `<style>`:
```css
/* Ubah warna utama dari ungu ke biru */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Menjadi: */
background: linear-gradient(135deg, #0066ff 0%, #0033cc 100%);
```

### Menambah Kategori
1. Edit di file `index.html` - bagian `<select id="kategoriFilter">`
2. Tambah option baru:
```html
<option value="nama_kategori">Nama Kategori</option>
```

### Merubah API Base URL
Jika server berjalan di port/host berbeda, edit di `index.html`:
```javascript
const API_BASE = 'http://localhost:8000';
// Ganti dengan:
const API_BASE = 'https://api.example.com';
```

## 📊 Database Schema

### Tabel `konten`
```sql
CREATE TABLE konten (
  id INTEGER PRIMARY KEY,
  judul TEXT,
  deskripsi TEXT,
  kategori TEXT,
  isi TEXT,
  gambar_utama TEXT,
  tanggal TEXT
)
```

### Tabel `galeri`
```sql
CREATE TABLE galeri (
  id INTEGER PRIMARY KEY,
  konten_id INTEGER,
  url TEXT,
  deskripsi TEXT,
  FOREIGN KEY(konten_id) REFERENCES konten(id)
)
```

## 🐛 Troubleshooting

### Error: "Gagal memuat konten"
- Pastikan server berjalan: `python server/main.py`
- Pastikan port 8000 tidak digunakan oleh aplikasi lain
- Check API_BASE URL di index.html sesuai dengan server URL

### Database Error
- Hapus file `data.db` jika ada:
```bash
rm data.db
```
- Jalankan ulang server untuk create database baru
- Jalankan `python init_sample_data.py` untuk load sample data

### CORS Error
Server sudah dikonfigurasi untuk allow CORS dari semua origin. Jika masih error, pastikan menggunakan protokol yang sama (http/https).

## 🌟 Tips & Best Practices

1. **Gambar Format**: Gunakan URL lengkap untuk gambar (https://...)
2. **Deskripsi**: Buat deskripsi singkat tapi menarik (max 200 karakter)
3. **Kategori**: Gunakan standar kategori yang sudah ada
4. **Galeri**: Minimal 1 gambar, maksimal sesuai kebutuhan (recommended max 10)
5. **Isi Konten**: Gunakan line breaks untuk readability

## 📱 Mobile Optimization

Interface sudah fully responsive untuk:
- 📱 Mobile phones (320px+)
- 📱 Tablets (768px+)
- 💻 Desktop (1200px+)

## 🔐 Security Notes

⚠️ **Development Mode Only**
- Server ini untuk development/testing saja
- Untuk production, tambahkan authentication
- Gunakan HTTPS untuk transmisi data sensitif
- Validate input dari user

## 📞 Support

Jika ada pertanyaan atau issue, bisa:
1. Check API endpoints documentation di atas
2. Lihat console browser untuk error messages
3. Check terminal server untuk logs

---

**Made with ❤️ - Happy Coding!**
