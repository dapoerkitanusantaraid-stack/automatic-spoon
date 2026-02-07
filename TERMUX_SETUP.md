# Termux Setup Guide

Panduan langkah demi langkah untuk menjalankan Project Server pada Android menggunakan Termux.

⚠️ Catatan awal
- Termux cocok untuk pengujian dan development on-device, bukan untuk produksi.
- Pastikan perangkat Anda memiliki ruang penyimpanan dan baterai yang cukup.
- Do not paste secrets into public chat.

1) Install Termux dan packages dasar
```bash
pkg update && pkg upgrade -y
pkg install -y python git clang make openssl-tool libffi libcrypt-dev wget unzip
```

2) Setup storage access
```bash
termux-setup-storage
```

3) Clone repo (jika belum)
```bash
git clone https://github.com/dapoerkitanusantaraid-stack/automatic-spoon.git
cd automatic-spoon
```

4) Buat virtualenv dan aktifkan
```bash
python -m venv .venv
source .venv/bin/activate
```

5) Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```
Jika build fail (mis. `cryptography`) pastikan `clang` dan header tersedia. Jika perlu, jalankan ulang `pip install` setelah install `clang`/`make`.

6) Konfigurasi environment
```bash
cp .env.example .env
nano .env
# Set TELEGRAM_TOKEN dan pengaturan lain sesuai kebutuhan
```

7) Jalankan server (development)
```bash
source .venv/bin/activate
python -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

8) Testing dan webhook
- Gunakan `ngrok` untuk expose port 8000 jika ingin menggunakan webhook dari Telegram/Twilio.
- Untuk webhook Telegram: gunakan skrip `./scripts/set_telegram_webhook.sh` (isi `TELEGRAM_BOT_TOKEN` & `TELEGRAM_WEBHOOK_URL`).

9) Troubleshooting
- Lihat `server.log` jika menjalankan menggunakan `nohup`.
- Periksa `pip` error logs, dan install missing headers/libraries.

10) Security
- Jangan menyimpan secrets di repositori.
- Gunakan Railway / VPS untuk deployment produksi.

---

Skrip otomatis disediakan di `scripts/termux_setup.sh` untuk mempercepat langkah-langkah di atas (interactive).