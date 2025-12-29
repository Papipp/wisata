import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from models import User, Destinasi, Pesanan, Statistics
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Decorator untuk mengecek login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator untuk mengecek admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Akses ditolak. Hanya admin yang dapat mengakses halaman ini', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    # Admin tidak boleh akses halaman index
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    destinations = Destinasi.get_all()
    return render_template('index.html', destinations=destinations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Jika sudah login, redirect
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone', '')
        
        if User.create(username, email, password, phone):
            flash('Registrasi berhasil! Silakan login', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username atau email sudah terdaftar', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Jika sudah login, redirect
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.verify(username, password)
        if user:
            session['user_id'] = user['id_user']
            session['username'] = user['username']
            session['role'] = user['role']
            
            flash(f'Selamat datang, {user["username"]}!', 'success')
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Username atau password salah', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout', 'info')
    return redirect(url_for('login'))

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    # Admin tidak boleh akses user dashboard
    if session.get('role') == 'admin':
        flash('Akses ditolak', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    bookings = Pesanan.get_by_user(session['user_id'])
    return render_template('user_dashboard.html', bookings=bookings)

@app.route('/user/profile')
@login_required
def user_profile():
    # Admin tidak boleh akses user profile
    if session.get('role') == 'admin':
        flash('Akses ditolak', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    user = User.get_by_id(session['user_id'])
    return render_template('user_profile.html', user=user)

@app.route('/user/profile/update', methods=['POST'])
@login_required
def update_profile():
    if session.get('role') == 'admin':
        flash('Akses ditolak', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    email = request.form['email']
    phone = request.form.get('phone', '')
    
    if User.update(session['user_id'], email, phone):
        flash('Profil berhasil diperbarui', 'success')
    else:
        flash('Gagal memperbarui profil', 'danger')
    
    return redirect(url_for('user_profile'))

@app.route('/destinations')
def destinations():
    # Admin tidak boleh akses halaman destinations publik
    if session.get('role') == 'admin':
        return redirect(url_for('admin_destinations'))
    
    all_destinations = Destinasi.get_all()
    return render_template('destinations.html', destinations=all_destinations)

@app.route('/destination/<int:id>')
def destination_detail(id):
    # Admin tidak boleh akses detail destinasi publik
    if session.get('role') == 'admin':
        flash('Akses ditolak', 'danger')
        return redirect(url_for('admin_destinations'))
    
    destination = Destinasi.get_by_id(id)
    if not destination:
        flash('Destinasi tidak ditemukan', 'danger')
        return redirect(url_for('destinations'))
    return render_template('destination_detail.html', destination=destination)

@app.route('/booking/<int:destination_id>', methods=['GET', 'POST'])
@login_required
def booking(destination_id):
    # Hanya user yang bisa booking
    if session.get('role') != 'user':
        flash('Akses ditolak. Hanya user yang dapat melakukan booking', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        jumlah_orang = int(request.form['jumlah_orang'])
        pesan = request.form.get('pesan', '')
        
        destination = Destinasi.get_by_id(destination_id)
        if not destination:
            flash('Destinasi tidak ditemukan', 'danger')
            return redirect(url_for('destinations'))
        
        jumlah_harga = destination['harga'] * jumlah_orang
        
        id_pesanan = Pesanan.create(
            session['user_id'],
            destination_id,
            tanggal,
            jumlah_orang,
            jumlah_harga,
            pesan
        )
        
        if id_pesanan:
            flash('Booking berhasil dibuat!', 'success')
            return redirect(url_for('booking_detail', id=id_pesanan))
        else:
            flash('Gagal membuat booking', 'danger')
    
    destination = Destinasi.get_by_id(destination_id)
    if not destination:
        flash('Destinasi tidak ditemukan', 'danger')
        return redirect(url_for('destinations'))
    
    return render_template('booking_form.html', destination=destination, now=datetime.utcnow(), timedelta=timedelta)

@app.route('/booking/detail/<int:id>')
@login_required
def booking_detail(id):
    if session.get('role') == 'admin':
        flash('Akses ditolak', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    booking = Pesanan.get_by_id(id)
    if not booking or booking['id_user'] != session['user_id']:
        flash('Booking tidak ditemukan', 'danger')
        return redirect(url_for('user_dashboard'))
    return render_template('booking_detail.html', booking=booking)

@app.route('/booking/cancel/<int:id>', methods=['POST'])
@login_required
def cancel_booking(id):
    if session.get('role') == 'admin':
        flash('Akses ditolak', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    booking = Pesanan.get_by_id(id)
    if booking and booking['id_user'] == session['user_id']:
        if Pesanan.update_status(id, 'cancelled'):
            flash('Booking berhasil dibatalkan', 'success')
        else:
            flash('Gagal membatalkan booking', 'danger')
    else:
        flash('Booking tidak ditemukan', 'danger')
    
    return redirect(url_for('user_dashboard'))

# ============= ADMIN ROUTES =============

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    stats = Statistics.get_admin_stats()
    recent_bookings = Pesanan.get_recent(10)
    return render_template('admin_dashboard.html', stats=stats, bookings=recent_bookings)

@app.route('/admin/destinations')
@admin_required
def admin_destinations():
    destinations = Destinasi.get_all()
    return render_template('admin_destinations.html', destinations=destinations)

@app.route('/admin/destination/add', methods=['GET', 'POST'])
@admin_required
def add_destination():
    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']
        lokasi = request.form['lokasi']
        harga = float(request.form['harga'])
        durasi = request.form['durasi']
        image_url = request.form['image_url']
        kategori = request.form['kategori']
        
        if Destinasi.create(nama, deskripsi, lokasi, harga, durasi, image_url, kategori):
            flash('Destinasi berhasil ditambahkan', 'success')
            return redirect(url_for('admin_destinations'))
        else:
            flash('Gagal menambahkan destinasi', 'danger')
    
    return render_template('admin_destination_form.html', destination=None)

@app.route('/admin/destination/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_destination(id):
    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']
        lokasi = request.form['lokasi']
        harga = float(request.form['harga'])
        durasi = request.form['durasi']
        image_url = request.form['image_url']
        kategori = request.form['kategori']
        
        if Destinasi.update(id, nama, deskripsi, lokasi, harga, durasi, image_url, kategori):
            flash('Destinasi berhasil diperbarui', 'success')
            return redirect(url_for('admin_destinations'))
        else:
            flash('Gagal memperbarui destinasi', 'danger')
    
    destination = Destinasi.get_by_id(id)
    if not destination:
        flash('Destinasi tidak ditemukan', 'danger')
        return redirect(url_for('admin_destinations'))
    
    return render_template('admin_destination_form.html', destination=destination)

@app.route('/admin/destination/delete/<int:id>', methods=['POST'])
@admin_required
def delete_destination(id):
    if Destinasi.delete(id):
        flash('Destinasi berhasil dihapus', 'success')
    else:
        flash('Gagal menghapus destinasi', 'danger')
    
    return redirect(url_for('admin_destinations'))

@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    bookings = Pesanan.get_all()
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/admin/booking/update-status/<int:id>', methods=['POST'])
@admin_required
def update_booking_status(id):
    status = request.form['status']
    
    if Pesanan.update_status(id, status):
        flash('Status booking berhasil diperbarui', 'success')
    else:
        flash('Gagal memperbarui status booking', 'danger')
    
    return redirect(url_for('admin_bookings'))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.get_all()
    return render_template('admin_users.html', users=users)

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)