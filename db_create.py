import sqlite3

# Veritabanı dosyası
DB = 'dizi_takip.db'

conn = sqlite3.connect(DB)
c = conn.cursor()

# Eğer tablolar varsa sil (temiz başlamak için)
c.execute("DROP TABLE IF EXISTS dizi_oyuncu")
c.execute("DROP TABLE IF EXISTS diziler")
c.execute("DROP TABLE IF EXISTS oyuncular")
c.execute("DROP TABLE IF EXISTS kullanici_diziler")

# Diziler tablosu
c.execute('''
CREATE TABLE diziler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dizi_ad TEXT,
    afis_url TEXT,
    yil INTEGER,
    tur TEXT
)
''')

# Oyuncular tablosu
c.execute('''
CREATE TABLE oyuncular (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT,
    dogum_yil INTEGER,
    foto_url TEXT
)
''')

# Diziler ve oyuncuların many-to-many ilişkisi
c.execute('''
CREATE TABLE dizi_oyuncu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dizi_id INTEGER,
    oyuncu_id INTEGER,
    karakter_ad TEXT,
    karakter_resim TEXT,
    FOREIGN KEY (dizi_id) REFERENCES diziler(id),
    FOREIGN KEY (oyuncu_id) REFERENCES oyuncular(id)
)
''')

# Kullanıcıların izlediği diziler tablosu
c.execute('''
CREATE TABLE kullanici_diziler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_id INTEGER,
    dizi_id INTEGER,
    izledi_mi BOOLEAN DEFAULT 0,
    FOREIGN KEY (dizi_id) REFERENCES diziler(id)
)
''')

conn.commit()
conn.close()
print("Veritabanı ve tablolar başarıyla oluşturuldu!")
