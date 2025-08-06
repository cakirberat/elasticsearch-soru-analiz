import sqlite3
from elasticsearch import Elasticsearch

# Elasticsearch'e bağlan
es = Elasticsearch("http://localhost:9200")

# Index kontrolü (yeni API ile)
try:
    if not es.indices.exists(index="sorular"):
        es.indices.create(index="sorular")
except Exception as e:
    print("Index kontrolünde hata:", e)

# Veritabanından verileri çek
conn = sqlite3.connect('sorular.db')
cursor = conn.cursor()
cursor.execute("SELECT id, metin FROM sorular")
sorular = cursor.fetchall()

# Her soruyu Elasticsearch'e yükle
for soru_id, metin in sorular:
    try:
        es.index(index="sorular", id=soru_id, document={"soru": metin})
    except Exception as e:
        print(f"{soru_id} numaralı soru yüklenemedi:", e)

conn.close()

print("Elasticsearch'e veri aktarma tamamlandı.")
