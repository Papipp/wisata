from models import User, Destinasi, Pesanan
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

print("="*60)
print("🚀 SCRIPT TAMBAH DATA - TRAVEL SYSTEM")
print("="*60)

# Menu pilihan
print("\nPilih data yang ingin ditambahkan:")
print("1. Tambah Admin User")
print("2. Tambah Sample User")
print("3. Tambah Destinasi")
print("4. Tambah Sample Booking")
print("5. Tambah Semua Data (22 Destinasi + Sample Users & Bookings)")
print("0. Keluar")

choice = input("\nPilihan (0-5): ")

# 1. TAMBAH ADMIN
if choice == '1':
    print("\n--- TAMBAH ADMIN USER ---")
    username = input("Username admin: ") or "admin"
    email = input("Email admin: ") or "admin@travel.com"
    password = input("Password admin: ") or "admin123"
    phone = input("No. Telepon: ") or "081234567890"
    
    if User.create(username, email, password, phone, 'admin'):
        print(f"✅ Admin '{username}' berhasil dibuat!")
        print(f"   Login: {username} / {password}")
    else:
        print("❌ Gagal membuat admin (username/email mungkin sudah ada)")

# 2. TAMBAH SAMPLE USER
elif choice == '2':
    print("\n--- TAMBAH SAMPLE USER ---")
    users = [
        ('user1', 'user1@email.com', 'user123', '081111111111'),
        ('user2', 'user2@email.com', 'user123', '081222222222'),
        ('budi', 'budi@email.com', 'budi123', '081333333333'),
    ]
    
    for username, email, password, phone in users:
        if User.create(username, email, password, phone):
            print(f"✅ User '{username}' berhasil dibuat")
        else:
            print(f"⚠️  User '{username}' sudah ada, skip...")
    
    print("\n✅ Sample users selesai dibuat!")

# 3. TAMBAH DESTINASI
elif choice == '3':
    print("\n--- TAMBAH DESTINASI ---")
    print("Pilih:")
    print("a. Input manual")
    print("b. Insert 22 destinasi default")
    
    sub = input("Pilihan (a/b): ")
    
    if sub == 'a':
        print("\n--- INPUT DESTINASI MANUAL ---")
        nama = input("Nama destinasi: ")
        deskripsi = input("Deskripsi: ")
        lokasi = input("Lokasi: ")
        harga = float(input("Harga (Rp): "))
        durasi = input("Durasi (contoh: 3 Hari 2 Malam): ")
        image_url = input("URL Gambar: ")
        print("Kategori: Pantai, Gunung, Budaya, Danau, Hutan")
        kategori = input("Kategori: ")
        
        if Destinasi.create(nama, deskripsi, lokasi, harga, durasi, image_url, kategori):
            print(f"✅ Destinasi '{nama}' berhasil ditambahkan!")
        else:
            print("❌ Gagal menambahkan destinasi")
    
    elif sub == 'b':
        print("\n🗺️  Menambahkan 22 destinasi default...")
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
        
        success = 0
        for dest in destinations:
            if Destinasi.create(*dest):
                success += 1
                print(f"✅ {dest[0]}")
        
        print(f"\n✅ Berhasil menambahkan {success} destinasi!")

# 4. TAMBAH SAMPLE BOOKING
elif choice == '4':
    print("\n--- TAMBAH SAMPLE BOOKING ---")
    print("Pastikan sudah ada user dan destinasi!")
    
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    bookings = [
        (2, 1, future_date, 2, 17000000, 'Perjalanan honeymoon'),
        (2, 2, future_date, 4, 6000000, ''),
        (3, 5, future_date, 1, 750000, 'Tertarik dengan sejarah'),
    ]
    
    for id_user, id_dest, date, people, price, msg in bookings:
        id_pesanan = Pesanan.create(id_user, id_dest, date, people, price, msg)
        if id_pesanan:
            print(f"✅ Booking #{id_pesanan} berhasil dibuat")
        else:
            print(f"⚠️  Booking gagal (pastikan user & destinasi ada)")
    
    print("\n✅ Sample bookings selesai dibuat!")

# 5. TAMBAH SEMUA DATA
elif choice == '5':
    print("\n--- TAMBAH SEMUA DATA ---")
    print("Ini akan menambahkan:")
    print("- 1 Admin user")
    print("- 3 Sample users")
    print("- 22 Destinasi")
    print("- 3 Sample bookings")
    
    confirm = input("\nLanjutkan? (y/n): ")
    
    if confirm.lower() == 'y':
        # Admin
        print("\n👤 Membuat admin...")
        if User.create('admin', 'admin@travel.com', 'admin123', '081234567890', 'admin'):
            print("✅ Admin berhasil dibuat")
        else:
            print("⚠️  Admin sudah ada")
        
        # Users
        print("\n👥 Membuat sample users...")
        users = [
            ('user1', 'user1@email.com', 'user123', '081111111111'),
            ('user2', 'user2@email.com', 'user123', '081222222222'),
            ('budi', 'budi@email.com', 'budi123', '081333333333'),
        ]
        for username, email, password, phone in users:
            if User.create(username, email, password, phone):
                print(f"✅ User '{username}' berhasil")
            else:
                print(f"⚠️  User '{username}' sudah ada")
        
        # Destinasi
        print("\n🗺️  Membuat 22 destinasi...")
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
        
        success = 0
        for dest in destinations:
            if Destinasi.create(*dest):
                success += 1
        print(f"✅ {success} destinasi berhasil ditambahkan")
        
        # Bookings
        print("\n📅 Membuat sample bookings...")
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        bookings = [
            (2, 1, future_date, 2, 17000000, 'Perjalanan honeymoon'),
            (2, 2, future_date, 4, 6000000, ''),
            (3, 5, future_date, 1, 750000, 'Tertarik dengan sejarah'),
        ]
        
        for id_user, id_dest, date, people, price, msg in bookings:
            if Pesanan.create(id_user, id_dest, date, people, price, msg):
                print(f"✅ Booking berhasil")
        
        print("\n" + "="*60)
        print("✅ SEMUA DATA BERHASIL DITAMBAHKAN!")
        print("="*60)
        print("\n📝 Login Credentials:")
        print("   Admin: admin / admin123")
        print("   User: user1 / user123")
        print("="*60)

# 0. KELUAR
elif choice == '0':
    print("\n👋 Keluar dari script")

else:
    print("\n❌ Pilihan tidak valid")