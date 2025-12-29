import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    """Membuat koneksi database"""
    DATABASE_URL = os.getenv("DB_URL")
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    conn.autocommit = True 
    return conn


class User:
    """Class untuk operasi CRUD User"""
    
    @staticmethod
    def create(username, email, password, phone, role='user'):
        """Membuat user baru"""
        conn = get_db()
        cur = conn.cursor()
        hashed_password = generate_password_hash(password)
        
        cur.execute(
            '''INSERT INTO "user" (username, email, password, phone, role) 
            VALUES (%s, %s, %s, %s, %s)''',
            (username, email, hashed_password, phone, role)
        )
        cur.close()
        conn.close()
        return True
    
    @staticmethod
    def verify(username, password):
        """Verifikasi login user"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM "user" WHERE username = %s', (username,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def get_by_id(id_user):
        """Mengambil user berdasarkan ID"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM "user" WHERE id_user = %s', (id_user,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        return user
    
    @staticmethod
    def get_all():
        """Mengambil semua user"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            'SELECT id_user, username, email, phone, role, created_at FROM "user" ORDER BY created_at DESC'
        )
        users = cur.fetchall()
        
        cur.close()
        conn.close()
        return users
    
    @staticmethod
    def update(id_user, email, phone):
        """Update data user"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            'UPDATE "user" SET email = %s, phone = %s WHERE id_user = %s',
            (email, phone, id_user)
        )
        cur.close()
        conn.close()
        return True


class Destinasi:
    """Class untuk operasi CRUD Destinasi"""
    
    @staticmethod
    def get_all():
        """Mengambil semua destinasi"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM destinasi ORDER BY created_at DESC')
        destinations = cur.fetchall()
        
        cur.close()
        conn.close()
        return destinations
    
    @staticmethod
    def get_by_id(id_destinasi):
        """Mengambil destinasi berdasarkan ID"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM destinasi WHERE id_destinasi = %s', (id_destinasi,))
        destination = cur.fetchone()
        
        cur.close()
        conn.close()
        return destination
    
    @staticmethod
    def create(nama, deskripsi, lokasi, harga, durasi, image_url, kategori):
        """Membuat destinasi baru"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            '''INSERT INTO destinasi (nama, deskripsi, lokasi, harga, durasi, image_url, kategori) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)''',
            (nama, deskripsi, lokasi, harga, durasi, image_url, kategori)
        )
        cur.close()
        conn.close()
        return True
    
    @staticmethod
    def update(id_destinasi, nama, deskripsi, lokasi, harga, durasi, image_url, kategori):
        """Update destinasi"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            '''UPDATE destinasi SET nama = %s, deskripsi = %s, lokasi = %s, 
            harga = %s, durasi = %s, image_url = %s, kategori = %s WHERE id_destinasi = %s''',
            (nama, deskripsi, lokasi, harga, durasi, image_url, kategori, id_destinasi)
        )
        cur.close()
        conn.close()
        return True
    
    @staticmethod
    def delete(id_destinasi):
        """Menghapus destinasi"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('DELETE FROM destinasi WHERE id_destinasi = %s', (id_destinasi,))
        cur.close()
        conn.close()
        return True


class Pesanan:
    """Class untuk operasi CRUD Pesanan (Booking)"""
    
    @staticmethod
    def create(id_user, id_destinasi, tanggal, jumlah_orang, jumlah_harga, pesan):
        """Membuat pesanan baru"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            '''INSERT INTO pesanan (id_user, id_destinasi, tanggal, jumlah_orang, jumlah_harga, pesan) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_pesanan''',
            (id_user, id_destinasi, tanggal, jumlah_orang, jumlah_harga, pesan)
        )
        id_pesanan = cur.fetchone()['id_pesanan']
        cur.close()
        conn.close()
        return id_pesanan
    
    @staticmethod
    def get_by_id(id_pesanan):
        """Mengambil pesanan berdasarkan ID dengan join"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT p.*, d.nama as destination_name, d.lokasi, d.image_url,
            u.username as user_name, u.email as user_email, u.phone as user_phone
            FROM pesanan p
            JOIN destinasi d ON p.id_destinasi = d.id_destinasi
            JOIN "user" u ON p.id_user = u.id_user
            WHERE p.id_pesanan = %s
        ''', (id_pesanan,))
        pesanan = cur.fetchone()
        
        cur.close()
        conn.close()
        return pesanan
    
    @staticmethod
    def get_by_user(id_user):
        """Mengambil semua pesanan user"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT p.*, d.nama as destination_name, d.lokasi, d.image_url
            FROM pesanan p
            JOIN destinasi d ON p.id_destinasi = d.id_destinasi
            WHERE p.id_user = %s
            ORDER BY p.created_at DESC
        ''', (id_user,))
        pesanan_list = cur.fetchall()
        
        cur.close()
        conn.close()
        return pesanan_list
    
    @staticmethod
    def get_all():
        """Mengambil semua pesanan"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT p.*, d.nama as destination_name, d.lokasi,
            u.username as user_name, u.email as user_email
            FROM pesanan p
            JOIN destinasi d ON p.id_destinasi = d.id_destinasi
            JOIN "user" u ON p.id_user = u.id_user
            ORDER BY p.created_at DESC
        ''')
        pesanan_list = cur.fetchall()
        
        cur.close()
        conn.close()
        return pesanan_list
    
    @staticmethod
    def get_recent(limit=10):
        """Mengambil pesanan terbaru"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT p.*, d.nama as destination_name, u.username as user_name
            FROM pesanan p
            JOIN destinasi d ON p.id_destinasi = d.id_destinasi
            JOIN "user" u ON p.id_user = u.id_user
            ORDER BY p.created_at DESC
            LIMIT %s
        ''', (limit,))
        pesanan_list = cur.fetchall()
        
        cur.close()
        conn.close()
        return pesanan_list
    
    @staticmethod
    def update_status(id_pesanan, status):
        """Update status pesanan"""
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            'UPDATE pesanan SET status = %s WHERE id_pesanan = %s',
            (status, id_pesanan)
        )
        cur.close()
        conn.close()
        return True


class Statistics:
    """Class untuk statistik admin dashboard"""
    
    @staticmethod
    def get_admin_stats():
        """Mengambil statistik untuk admin dashboard"""
        conn = get_db()
        cur = conn.cursor()
        
        # Total users
        cur.execute('SELECT COUNT(*) as total FROM "user" WHERE role = %s', ('user',))
        total_users = cur.fetchone()['total']
        
        # Total destinations
        cur.execute('SELECT COUNT(*) as total FROM destinasi')
        total_destinations = cur.fetchone()['total']
        
        # Total bookings
        cur.execute('SELECT COUNT(*) as total FROM pesanan')
        total_bookings = cur.fetchone()['total']
        
        # Pending bookings
        cur.execute('SELECT COUNT(*) as total FROM pesanan WHERE status = %s', ('pending',))
        pending_bookings = cur.fetchone()['total']
        
        # Total revenue
        cur.execute(
            'SELECT SUM(jumlah_harga) as total FROM pesanan WHERE status IN (%s, %s)',
            ('confirmed', 'completed')
        )
        result = cur.fetchone()
        total_revenue = result['total'] if result['total'] else 0
        
        cur.close()
        conn.close()
        
        return {
            'total_users': total_users,
            'total_destinations': total_destinations,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'total_revenue': total_revenue
        }