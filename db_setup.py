import sqlite3

# Veritabanı bağlan
conn = sqlite3.connect('dizi_takip.db')
c = conn.cursor()

# Diziler tablosu
c.execute('''
CREATE TABLE IF NOT EXISTS diziler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    afis_url TEXT,
    yil INTEGER,
    tur TEXT
)
''')

# Filmler tablosu
c.execute('''
CREATE TABLE IF NOT EXISTS filmler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    afis_url TEXT,
    yil INTEGER,
    tur TEXT
)
''')

# Oyuncular tablosu
c.execute('''
CREATE TABLE IF NOT EXISTS oyuncular (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    resim_url TEXT
)
''')

# Dizi-oyuncu tablosu (çoklu ilişki)
c.execute('''
CREATE TABLE IF NOT EXISTS dizi_oyuncu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dizi_id INTEGER,
    oyuncu_id INTEGER,
    karakter_ad TEXT,
    karakter_resim TEXT,
    FOREIGN KEY (dizi_id) REFERENCES diziler(id),
    FOREIGN KEY (oyuncu_id) REFERENCES oyuncular(id)
)
''')

# Kullanıcı izleme tablosu
c.execute('''
CREATE TABLE IF NOT EXISTS izlenen_icerikler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_id INTEGER,
    icerik_id INTEGER,
    icerik_turu TEXT,
    izlendi INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()

print("Veritabanı ve tablolar oluşturuldu!")
