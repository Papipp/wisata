from models import Database
import os
from dotenv import load_dotenv

load_dotenv()

db = Database(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

# Inisialisasi tabel
print("🔧 Membuat tabel...")

db.init_db()

# Buat admin account
print("👤 Membuat admin account...")
db.create_user('admin', 'admin@travel.com', 'admin123', 'Administrator', '081234567890', 'admin')

# Buat sample users
print("👥 Membuat sample users...")
db.create_user('user1', 'user1@email.com', 'user123', 'John Doe', '081111111111')
db.create_user('user2', 'user2@email.com', 'user123', 'Jane Smith', '081222222222')
db.create_user('budi', 'budi@email.com', 'budi123', 'Budi Santoso', '081333333333')

# Data destinasi (22 destinasi)
print("🗺️  Membuat destinasi...")
destinations = [
    ('Raja Ampat', 'Surga tersembunyi di Papua dengan keindahan bawah laut yang menakjubkan. Terkenal dengan keanekaragaman hayati laut terkaya di dunia.', 'Papua Barat', 8500000, '4 Hari 3 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Gunung Bromo', 'Keindahan matahari terbit di gunung berapi yang ikonik. Pemandangan lautan pasir dan kawah yang spektakuler.', 'Jawa Timur', 1500000, '2 Hari 1 Malam', 'https://images.unsplash.com/photo-1583417319070-4a69db38a482', 'Gunung'),
    ('Danau Toba', 'Danau vulkanik terbesar di Asia Tenggara dengan pulau Samosir di tengahnya. Budaya Batak yang kental.', 'Sumatera Utara', 2500000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1598965675045-f2c3f9f5d0f8', 'Danau'),
    ('Tanah Lot', 'Pura ikonik di atas batu karang menghadap laut. Sunset terbaik di Bali dengan pemandangan yang memukau.', 'Bali', 500000, '1 Hari', 'https://images.unsplash.com/photo-1537996194471-e657df975ab4', 'Budaya'),
    ('Candi Borobudur', 'Candi Buddha terbesar di dunia dan situs warisan UNESCO. Arsitektur megah dengan relief yang indah.', 'Jawa Tengah', 750000, '1 Hari', 'https://images.unsplash.com/photo-1598365718914-8f9c80e9e097', 'Budaya'),
    ('Labuan Bajo', 'Gerbang menuju Pulau Komodo dan keindahan alam Flores. Pantai pink dan diving spots yang menawan.', 'NTT', 5500000, '4 Hari 3 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Nusa Penida', 'Pulau eksotis dengan tebing dramatis dan pantai tersembunyi. Kelingking Beach dan Angel Billabong.', 'Bali', 1200000, '2 Hari 1 Malam', 'https://images.unsplash.com/photo-1537996194471-e657df975ab4', 'Pantai'),
    ('Wakatobi', 'Surga diving dengan terumbu karang terbaik di dunia. Visibilitas air laut hingga 50 meter.', 'Sulawesi Tenggara', 7500000, '5 Hari 4 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Kawah Ijen', 'Fenomena blue fire dan danau kawah belerang. Pemandangan unik yang hanya ada di beberapa tempat di dunia.', 'Jawa Timur', 1800000, '2 Hari 1 Malam', 'https://images.unsplash.com/photo-1583417319070-4a69db38a482', 'Gunung'),
    ('Bunaken', 'Taman laut dengan biodiversitas laut yang luar biasa. Spot snorkeling dan diving terbaik di Indonesia.', 'Sulawesi Utara', 3500000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Tanjung Puting', 'Rumah bagi orangutan liar di Kalimantan. Pengalaman melihat satwa liar dalam habitat aslinya.', 'Kalimantan Tengah', 4500000, '4 Hari 3 Malam', 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44', 'Hutan'),
    ('Derawan', 'Pulau dengan ubur-ubur tanpa sengat dan penyu hijau. Air laut yang jernih dan pantai berpasir putih.', 'Kalimantan Timur', 3800000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Taman Nasional Ujung Kulon', 'Habitat badak Jawa yang hampir punah. Hutan hujan tropis dan pantai yang masih alami.', 'Banten', 2800000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44', 'Hutan'),
    ('Belitung', 'Pantai dengan formasi batu granit yang unik. Laskar Pelangi island dengan air laut yang jernih.', 'Bangka Belitung', 3200000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Danau Kelimutu', 'Tiga danau kawah dengan warna yang berbeda. Fenomena alam yang menakjubkan di Flores.', 'NTT', 3500000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1598365718914-8f9c80e9e097', 'Danau'),
    ('Tana Toraja', 'Budaya unik dengan upacara pemakaman tradisional. Rumah adat Tongkonan dan pemandangan alam yang indah.', 'Sulawesi Selatan', 4200000, '4 Hari 3 Malam', 'https://images.unsplash.com/photo-1555400082-e0fddf1e5a8a', 'Budaya'),
    ('Gili Trawangan', 'Pulau tropis tanpa kendaraan bermotor. Kehidupan malam yang meriah dan pantai yang cantik.', 'NTB', 2200000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Gunung Rinjani', 'Pendakian menantang dengan danau Segara Anak. Pemandangan sunrise yang spektakuler dari puncak.', 'NTB', 2800000, '4 Hari 3 Malam', 'https://images.unsplash.com/photo-1583417319070-4a69db38a482', 'Gunung'),
    ('Pantai Pink', 'Pantai dengan pasir berwarna pink yang langka. Salah satu dari tujuh pantai pink di dunia.', 'NTT', 3800000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Pulau Weh', 'Titik paling barat Indonesia dengan snorkeling terbaik. Batu Payung dan kehidupan bawah laut yang indah.', 'Aceh', 3200000, '3 Hari 2 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
    ('Dieng Plateau', 'Dataran tinggi dengan candi dan telaga warna. Sunrise golden dan fenomena kawah Sikidang.', 'Jawa Tengah', 1500000, '2 Hari 1 Malam', 'https://images.unsplash.com/photo-1583417319070-4a69db38a482', 'Gunung'),
    ('Mentawai', 'Surga surfing dengan ombak kelas dunia. Pulau-pulau indah dan budaya suku Mentawai yang unik.', 'Sumatera Barat', 6500000, '5 Hari 4 Malam', 'https://images.unsplash.com/photo-1559827260-dc66d52bef19', 'Pantai'),
]

for dest in destinations:
    db.create_destination(*dest)

# Buat beberapa sample booking
print("📅 Membuat sample bookings...")
from datetime import datetime, timedelta
future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

db.create_booking(2, 1, future_date, 2, 17000000, 'Perjalanan honeymoon')
db.create_booking(2, 2, future_date, 4, 6000000, '')
db.create_booking(3, 5, future_date, 1, 750000, 'Tertarik dengan sejarah')

print("\n✅ Database berhasil diinisialisasi!")
print("="*50)
print("📝 Login Credentials:")
print("   Admin:")
print("   - Username: admin")
print("   - Password: admin123")
print("\n   User:")
print("   - Username: user1 / user2 / budi")
print("   - Password: user123 / budi123")
print("="*50)