import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

# fungsi untuk menghubungkan ke datbase
def get_db():
    DATABASE_URL = os.getenv("DB_URL")
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    conn.autocommit = True 
    return conn

class User:
    @staticmethod
    def create(username, email, password, phone, role='user'):
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
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM "user" WHERE id_user = %s', (id_user,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        return user
    
    @staticmethod
    def get_all():
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            'SELECT id_user, username, email, phone, role, created_at FROM "user" ORDER BY created_at ASC'
        )
        users = cur.fetchall()
        
        cur.close()
        conn.close()
        return users
    
    @staticmethod
    def update(id_user, email, phone):
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
    @staticmethod
    def get_all():
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM destinasi ORDER BY created_at ASC')
        destinations = cur.fetchall()
        
        cur.close()
        conn.close()
        return destinations
    
    @staticmethod
    def get_by_id(id_destinasi):
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM destinasi WHERE id_destinasi = %s', (id_destinasi,))
        destination = cur.fetchone()
        
        cur.close()
        conn.close()
        return destination
    
    @staticmethod
    def create(nama, deskripsi, lokasi, harga, durasi, image_url, kategori):
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
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('DELETE FROM destinasi WHERE id_destinasi = %s', (id_destinasi,))
        cur.close()
        conn.close()
        return True


class Pesanan:
    @staticmethod
    def create(id_user, id_destinasi, tanggal, jumlah_orang, jumlah_harga, pesan):
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
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT p.*, d.nama as destination_name, d.lokasi, d.image_url
            FROM pesanan p
            JOIN destinasi d ON p.id_destinasi = d.id_destinasi
            WHERE p.id_user = %s
            ORDER BY p.created_at ASC
        ''', (id_user,))
        pesanan_list = cur.fetchall()
        
        cur.close()
        conn.close()
        return pesanan_list
    
    @staticmethod
    def get_all():
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT p.*, d.nama as destination_name, d.lokasi,
            u.username as user_name, u.email as user_email
            FROM pesanan p
            JOIN destinasi d ON p.id_destinasi = d.id_destinasi
            JOIN "user" u ON p.id_user = u.id_user
            ORDER BY p.created_at ASC
        ''')
        pesanan_list = cur.fetchall()
        
        cur.close()
        conn.close()
        return pesanan_list
    
    @staticmethod
    def get_recent(limit=10):
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT p.*, d.nama as destination_name, u.username as user_name
            FROM pesanan p
            JOIN destinasi d ON p.id_destinasi = d.id_destinasi
            JOIN "user" u ON p.id_user = u.id_user
            ORDER BY p.created_at ASC
            LIMIT %s
        ''', (limit,))
        pesanan_list = cur.fetchall()
        
        cur.close()
        conn.close()
        return pesanan_list
    
    @staticmethod
    def update_status(id_pesanan, status):
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute(
            'UPDATE pesanan SET status = %s WHERE id_pesanan = %s',
            (status, id_pesanan)
        )
        cur.close()
        conn.close()
        return True


# Statistik untuk dashboard admin
class Statistics:
    @staticmethod
    def get_admin_stats():
        conn = get_db()
        cur = conn.cursor()
        
        # data daftar user
        cur.execute('SELECT COUNT(*) as total FROM "user" WHERE role = %s', ('user',))
        total_users = cur.fetchone()['total']
        
        # data jumlah destinasi
        cur.execute('SELECT COUNT(*) as total FROM destinasi')
        total_destinations = cur.fetchone()['total']
        
        # data jumlah booking
        cur.execute('SELECT COUNT(*) as total FROM pesanan')
        total_bookings = cur.fetchone()['total']
        
        # status booking
        cur.execute('SELECT COUNT(*) as total FROM pesanan WHERE status = %s', ('pending',))
        pending_bookings = cur.fetchone()['total']
        
        return {
            'total_users': total_users,
            'total_destinations': total_destinations,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
        }