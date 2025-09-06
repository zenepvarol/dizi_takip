from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('dizi_takip.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ana sayfa (kullanıcı)
@app.route('/')
def home():
    conn = get_db_connection()
    c = conn.cursor()
    # Tüm dizileri al
    c.execute("SELECT * FROM diziler")
    diziler = c.fetchall()
    diziler_list = []
    for d in diziler:
        c.execute("""SELECT o.ad as oyuncu_ad, do.karakter_ad, do.karakter_resim
                     FROM dizi_oyuncu do
                     JOIN oyuncular o ON do.oyuncu_id = o.id
                     WHERE do.dizi_id=?""", (d['id'],))
        cast = c.fetchall()
        diziler_list.append(dict(dizi_ad=d['ad'], afis_url=d['afis_url'], yil=d['yil'], tur=d['tur'], cast=cast, id=d['id']))
    conn.close()
    return render_template('home.html', diziler=diziler_list)

# Admin paneli
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    conn = get_db_connection()
    c = conn.cursor()
    if request.method == 'POST':
        ad = request.form['ad']
        afis_url = request.form.get('afis_url', '')
        yil = request.form.get('yil', '')
        tur = request.form.get('tur', '')

        oyuncu_ad_list = request.form.getlist('oyuncu_ad[]')
        karakter_ad_list = request.form.getlist('karakter_ad[]')
        karakter_resim_list = request.form.getlist('karakter_resim[]')

        # Diziyi ekle
        c.execute("INSERT INTO diziler (ad, afis_url, yil, tur) VALUES (?, ?, ?, ?)", (ad, afis_url, yil, tur))
        dizi_id = c.lastrowid

        # Cast ekle
        for i in range(len(oyuncu_ad_list)):
            oyuncu_ad = oyuncu_ad_list[i]
            karakter_ad = karakter_ad_list[i]
            karakter_resim = karakter_resim_list[i] if i < len(karakter_resim_list) else ''

            # Oyuncuyu ekle yoksa
            c.execute("SELECT id FROM oyuncular WHERE ad=?", (oyuncu_ad,))
            oyuncu = c.fetchone()
            if oyuncu:
                oyuncu_id = oyuncu[0]
            else:
                c.execute("INSERT INTO oyuncular (ad) VALUES (?)", (oyuncu_ad,))
                oyuncu_id = c.lastrowid

            # dizi_oyuncu tablosuna ekle
            c.execute("""INSERT INTO dizi_oyuncu (dizi_id, oyuncu_id, karakter_ad, karakter_resim)
                         VALUES (?, ?, ?, ?)""", (dizi_id, oyuncu_id, karakter_ad, karakter_resim))
        conn.commit()

    # GET isteği
    c.execute("SELECT * FROM diziler")
    diziler = c.fetchall()
    diziler_list = []
    for d in diziler:
        c.execute("""SELECT o.ad as oyuncu_ad, do.karakter_ad, do.karakter_resim
                     FROM dizi_oyuncu do
                     JOIN oyuncular o ON do.oyuncu_id = o.id
                     WHERE do.dizi_id=?""", (d['id'],))
        cast = c.fetchall()
        diziler_list.append(dict(dizi_ad=d['ad'], afis_url=d['afis_url'], yil=d['yil'], tur=d['tur'], cast=cast, id=d['id']))

    c.execute("SELECT * FROM oyuncular")
    oyuncular = c.fetchall()
    conn.close()
    return render_template('admin.html', diziler=diziler_list, oyuncular=oyuncular)

# Dizi sil
@app.route('/dizi_sil/<int:dizi_id>')
def dizi_sil(dizi_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM dizi_oyuncu WHERE dizi_id=?", (dizi_id,))
    c.execute("DELETE FROM diziler WHERE id=?", (dizi_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# Oyuncu sil
@app.route('/oyuncu_sil/<int:oyuncu_id>')
def oyuncu_sil(oyuncu_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM dizi_oyuncu WHERE oyuncu_id=?", (oyuncu_id,))
    c.execute("DELETE FROM oyuncular WHERE id=?", (oyuncu_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# Oyuncu detay sayfası
@app.route('/oyuncu/<int:oyuncu_id>')
def oyuncu_detay(oyuncu_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM oyuncular WHERE id=?", (oyuncu_id,))
    oyuncu = c.fetchone()

    c.execute("""SELECT d.ad as dizi_ad, d.afis_url, do.karakter_ad, do.karakter_resim
                 FROM dizi_oyuncu do
                 JOIN diziler d ON do.dizi_id = d.id
                 WHERE do.oyuncu_id=?""", (oyuncu_id,))
    diziler = c.fetchall()
    conn.close()
    return render_template('oyuncu_detay.html', oyuncu=oyuncu, diziler=diziler)

if __name__ == '__main__':
    app.run(debug=True)
