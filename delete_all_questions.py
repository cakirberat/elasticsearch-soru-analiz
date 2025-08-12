import sqlite3

conn = sqlite3.connect('sorular.db')
cursor = conn.cursor()

# Tüm soruları sil
cursor.execute("DELETE FROM sorular")

# AUTOINCREMENT sayacını sıfırla
cursor.execute("DELETE FROM sqlite_sequence WHERE name='sorular'")

# Silinen kayıt sayısını göster (DELETE sonrası SQLite’da rowcount bazen -1 döner, ama yine de yazalım)
print(f"{cursor.rowcount} adet soru silindi.")

conn.commit()
conn.close()

print("Veritabanındaki tüm sorular başarıyla silindi ve id sayacı sıfırlandı.")
