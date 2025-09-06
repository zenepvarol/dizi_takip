import sqlite3

conn = sqlite3.connect('dizi_takip.db')
c = conn.cursor()

# Oyuncular tablosuna sütun ekle
try:
    c.execute("ALTER TABLE oyuncular ADD COLUMN dogum_yil INTEGER")
except sqlite3.OperationalError:
    print("dogum_yil zaten var")

try:
    c.execute("ALTER TABLE oyuncular ADD COLUMN foto_url TEXT")
except sqlite3.OperationalError:
    print("foto_url zaten var")

conn.commit()
conn.close()
print("Veritabanı güncellendi")
