import sqlite3

conn = sqlite3.connect('sorular.db')
cursor = conn.cursor()

# Tüm soruları sil
cursor.execute("DELETE FROM sorular")

# Silinen kayıt sayısını göster
print(f"{cursor.rowcount} adet soru silindi.")

conn.commit()
conn.close()

print("Veritabanındaki tüm sorular başarıyla silindi.") 