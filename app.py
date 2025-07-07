from flask import Flask, render_template, request, redirect, flash, url_for, session, send_from_directory
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'secret'

# Fungsi koneksi langsung ke PostgreSQL
def get_db_connection():
    import urllib.parse as up
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set.")
    return psycopg2.connect(db_url)

# Halaman Utama
@app.route('/')
def home():
    return render_template('index.html')

# Halaman Materi
@app.route('/materi')
def materi():
    return "Ini Halaman Materi"

# Halaman Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                    (name, email, password))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/')
    
    return render_template('register.html')

# Halaman Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and user[2] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash("Login berhasil!", "success")
            return redirect(url_for('home'))  # ✅ diarahkan ke index.html
        else:
            flash("Login gagal! Periksa kembali username atau password Anda.", "error")

    return render_template('login.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route("/mapel")
def mapel():
    mapel = [
        {"nama": "Matematika", "deskripsi": "Materi dan latihan matematika", "gambar": "/static/matematika.png"},
        {"nama": "Fisika", "deskripsi": "Konsep, rumus, dan soal Fisika", "gambar": "/static/fisika.png"},
        {"nama": "Kimia", "deskripsi": "Materi dan percobaan Kimia", "gambar": "/static/kimia.png"},
        {"nama": "Biologi", "deskripsi": "Struktur sel, genetika, ekosistem", "gambar": "/static/biologi.png"},
        {"nama": "Bahasa Indonesia", "deskripsi": "Teks naratif, eksposisi, dan lainnya", "gambar": "/static/bind.png"},
        {"nama": "Bahasa Inggris", "deskripsi": "Grammar, reading, dan vocab", "gambar": "/static/bing.png"},
    ]
    return render_template("mapel.html", mapel=mapel)

@app.route("/rangkuman")
def rangkuman():
    pdf_list = [
        {"judul": "Rangkuman Bahasa Indonesia Materi Bab Kritik Dan esai ", "nama_file": "Bahasa Indonesia Materi Bab Kritik Dan esai.pdf"},
        {"judul": "Bahasa Inggris Bab Complex Sentenses", "nama_file": "Bahasa Inggris Bab Complex Sentenses.pdf"},
        {"judul": "E Modul Job Application Letter", "nama_file": "E Modul Job Application Letter.pdf"},
        {"judul": "Ikatan Kimia Dan Struktur Molekul", "nama_file": "Ikatan Kimia Dan Struktur Molekul.pdf"},
        {"judul": "Kimia Materi Struktur Atom", "nama_file": "Kimia Materi Struktur Atom.pdf"},
        {"judul": "Materi Bangun Ruang Dan Bangun Datar", "nama_file": "Materi Bangun Ruang Dan Bangun Datar.pdf"},
        {"judul": "Materi Belajar Pembelahan Sel", "nama_file": "Materi Belajar Pembelahan Sel.pdf"},
        {"judul": "Rangkuman Listrik Statis", "nama_file": "Rangkuman Listrik Statis.pdf"},
        {"judul": "Rangkuman Matematika Peminatan", "nama_file": "Rangkuman Matematika Peminatan.pdf"},
        {"judul": "Rangkuman Medan Magnet", "nama_file": "Rangkuman Medan Magnet.pdf"},
        {"judul": "Rangkuman Sistem Pencernaan", "nama_file": "Rangkuman Sistem Pencernaan.pdf"},
        {"judul": "Rangkuman Sistem Peredaran Darah", "nama_file": "Rangkuman Sistem Peredaran Darah.pdf"},
    ]
    return render_template("rangkuman.html", pdfs=pdf_list)

@app.route("/pdf/<path:filename>")
def download_pdf(filename):
    return send_from_directory("pdf", filename)

# Jalankan server Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
