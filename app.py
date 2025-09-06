from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)
DB = 'dizi_takip.db'

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# Ana sayfa
@app.route('/')
def home():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM diziler")
    diziler = c.fetchall()
    c.execute("SELECT * FROM oyuncular")
    oyuncular = c.fetchall()
    conn.close()
    return render_template('home.html', diziler=diziler, oyuncular=oyuncular)

# Admin paneli
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_conn()
    c = conn.cursor()

    # Dizi ekleme
    if request.method == 'POST' and 'dizi_ad' in request.form:
        dizi_ad = request.form['dizi_ad']
        afis_url = request.form['afis_url']
        yil = request.form['yil']
        tur = request.form['tur']
        c.execute("INSERT INTO diziler (dizi_ad, afis_url, yil, tur) VALUES (?, ?, ?, ?)",
                  (dizi_ad, afis_url, yil, tur))
        dizi_id = c.lastrowid

        # Cast ekleme
        oyuncu_ad_list = request.form.getlist('oyuncu_ad[]')
        karakter_ad_list = request.form.getlist('karakter_ad[]')
        karakter_resim_list = request.form.getlist('karakter_resim[]')

        for ad, karakter, karakter_resim in zip(oyuncu_ad_list, karakter_ad_list, karakter_resim_list):
            # Oyuncu var mı kontrol et
            c.execute("SELECT id FROM oyuncular WHERE ad=?", (ad,))
            row = c.fetchone()
            if row:
                oyuncu_id = row['id']
            else:
                c.execute("INSERT INTO oyuncular (ad) VALUES (?)", (ad,))
                oyuncu_id = c.lastrowid

            # Aynı oyuncu aynı diziye birden fazla eklenmesin
            c.execute("SELECT * FROM dizi_oyuncu WHERE dizi_id=? AND oyuncu_id=?", (dizi_id, oyuncu_id))
            if not c.fetchone():
                c.execute("INSERT INTO dizi_oyuncu (dizi_id, oyuncu_id, karakter_ad, karakter_resim) VALUES (?, ?, ?, ?)",
                          (dizi_id, oyuncu_id, karakter, karakter_resim))
        conn.commit()

    # Oyuncu ekleme
    if request.method == 'POST' and 'oyuncu_ad' in request.form:
        ad = request.form['oyuncu_ad']
        dogum_yil = request.form['dogum_yil']
        foto_url = request.form['foto_url']
        c.execute("INSERT INTO oyuncular (ad, dogum_yil, foto_url) VALUES (?, ?, ?)", (ad, dogum_yil, foto_url))
        conn.commit()

    c.execute("SELECT * FROM diziler")
    diziler = c.fetchall()
    c.execute("SELECT * FROM oyuncular")
    oyuncular = c.fetchall()
    conn.close()
    return render_template('admin.html', diziler=diziler, oyuncular=oyuncular)

# Dizi sil
@app.route('/dizi_sil/<int:dizi_id>', methods=['POST'])
def dizi_sil(dizi_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM diziler WHERE id=?", (dizi_id,))
    c.execute("DELETE FROM dizi_oyuncu WHERE dizi_id=?", (dizi_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# Oyuncu sil
@app.route('/oyuncu_sil/<int:oyuncu_id>', methods=['POST'])
def oyuncu_sil(oyuncu_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM oyuncular WHERE id=?", (oyuncu_id,))
    c.execute("DELETE FROM dizi_oyuncu WHERE oyuncu_id=?", (oyuncu_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# Dizi detay sayfası
@app.route('/dizi/<int:dizi_id>')
def dizi_detay(dizi_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM diziler WHERE id=?", (dizi_id,))
    dizi = c.fetchone()
    c.execute("""
        SELECT o.id, o.ad, o.foto_url, do.karakter_ad, do.karakter_resim
        FROM dizi_oyuncu do
        JOIN oyuncular o ON do.oyuncu_id = o.id
        WHERE do.dizi_id=?
    """, (dizi_id,))
    cast = c.fetchall()
    conn.close()
    return render_template('dizi_detay.html', dizi=dizi, cast=cast)

# Oyuncu detay sayfas
@app.route('/oyuncu/<int:oyuncu_id>')
def oyuncu_detay(oyuncu_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM oyuncular WHERE id=?", (oyuncu_id,))
    oyuncu = c.fetchone()
    c.execute("""
        SELECT d.id, d.dizi_ad, d.afis_url
        FROM dizi_oyuncu do
        JOIN diziler d ON do.dizi_id = d.id
        WHERE do.oyuncu_id=?
    """, (oyuncu_id,))
    diziler = c.fetchall()
    conn.close()
    return render_template('oyuncu_detay.html', oyuncu=oyuncu, diziler=diziler)

if __name__ == '__main__':
    app.run(debug=True)
