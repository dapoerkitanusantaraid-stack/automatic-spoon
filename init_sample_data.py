import sqlite3
import json
from datetime import datetime, timedelta

def init_sample_data():
    """Initialize database dengan sample data"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Clear existing data
    c.execute('DELETE FROM galeri')
    c.execute('DELETE FROM konten')
    
    # Sample konten data
    sample_konten = [
        {
            'judul': '🎉 Promo Besar-besaran Hari Ini',
            'deskripsi': 'Dapatkan diskon hingga 50% untuk semua produk pilihan kami!',
            'kategori': 'promo',
            'isi': 'Promosi spesial kami menawarkan diskon fantastis untuk pelanggan setia. Jangan lewatkan kesempatan emas ini untuk berbelanja produk favorit Anda dengan harga terbaik. Berlaku hingga akhir bulan ini atau sampai stok habis.',
            'gambar_utama': 'https://via.placeholder.com/600x400?text=Promo+Spesial'
        },
        {
            'judul': '📱 Teknologi Terbaru 2024',
            'deskripsi': 'Pelajari fitur-fitur terbaru dari perangkat pintar kami',
            'kategori': 'artikel',
            'isi': 'Teknologi mobile terus berkembang dengan inovasi yang mengagumkan. Artikel ini membahas tren terbaru, spesifikasi canggih, dan bagaimana teknologi ini akan mengubah cara kita bekerja dan berkomunikasi sehari-hari.',
            'gambar_utama': 'https://via.placeholder.com/600x400?text=Teknologi+Terbaru'
        },
        {
            'judul': '🏆 Produk Unggulan Kami',
            'deskripsi': 'Koleksi produk premium dengan kualitas terbaik di kelasnya',
            'kategori': 'produk',
            'isi': 'Produk unggulan kami telah dipercaya oleh jutaan pengguna di seluruh dunia. Setiap produk melalui quality control ketat untuk memastikan kepuasan pelanggan. Kami menjamin kepuasan 100% atau uang kembali.',
            'gambar_utama': 'https://via.placeholder.com/600x400?text=Produk+Unggulan'
        },
        {
            'judul': '📰 Berita Penting Minggu Ini',
            'deskripsi': 'Update terkini tentang perkembangan industri kami',
            'kategori': 'berita',
            'isi': 'Minggu ini kami memiliki beberapa pengumuman penting yang akan mengubah industri. Ekspansi global kami terus berlanjut dengan pembukaan kantor cabang baru di 5 negara berbeda. Kami berkomitmen untuk terus berinovasi dan memberikan layanan terbaik.',
            'gambar_utama': 'https://via.placeholder.com/600x400?text=Berita+Minggu'
        },
        {
            'judul': '🎊 Event Launching Produk Baru',
            'deskripsi': 'Bergabunglah dengan kami di acara launching eksklusif minggu depan',
            'kategori': 'event',
            'isi': 'Event launching kami akan menampilkan demo produk langsung, sesi tanya jawab dengan para ahli, dan hadiah menarik untuk peserta. Tempat terbatas hanya untuk 500 peserta pertama. Daftar sekarang dan dapatkan goodie bag eksklusif!',
            'gambar_utama': 'https://via.placeholder.com/600x400?text=Event+Launching'
        },
        {
            'judul': '💎 Koleksi Premium Terbatas',
            'deskripsi': 'Edisi terbatas eksklusif hanya untuk member VIP',
            'kategori': 'produk',
            'isi': 'Koleksi premium kami yang terbatas telah dirancang oleh desainer internasional. Setiap item adalah karya seni yang menggabungkan fungsionalitas dengan estetika modern. Hanya 100 unit tersedia di seluruh dunia.',
            'gambar_utama': 'https://via.placeholder.com/600x400?text=Koleksi+Premium'
        }
    ]
    
    # Insert konten
    for i, item in enumerate(sample_konten):
        tanggal = (datetime.now() - timedelta(days=i)).isoformat()
        c.execute('''INSERT INTO konten 
                     (judul, deskripsi, kategori, isi, gambar_utama, tanggal)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (item['judul'], item['deskripsi'], item['kategori'], 
                   item['isi'], item['gambar_utama'], tanggal))
        
        konten_id = c.lastrowid
        
        # Add sample galeri for each konten
        galeri_samples = [
            {'url': f'https://via.placeholder.com/300x300?text=Galeri+{i*3+1}', 'deskripsi': f'Gambar {i*3+1}'},
            {'url': f'https://via.placeholder.com/300x300?text=Galeri+{i*3+2}', 'deskripsi': f'Gambar {i*3+2}'},
            {'url': f'https://via.placeholder.com/300x300?text=Galeri+{i*3+3}', 'deskripsi': f'Gambar {i*3+3}'},
        ]
        
        for galeri in galeri_samples:
            c.execute('''INSERT INTO galeri 
                         (konten_id, url, deskripsi)
                         VALUES (?, ?, ?)''',
                      (konten_id, galeri['url'], galeri['deskripsi']))
    
    conn.commit()
    conn.close()
    print("✅ Sample data berhasil dimuat!")

if __name__ == "__main__":
    init_sample_data()
