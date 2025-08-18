import sqlite3
from es_config import get_default_client
from es_search import temizle

# Elasticsearch'e bağlan
es = get_default_client()
if not es:
    raise SystemExit("Elasticsearch bağlantısı kurulamadı. Lütfen servisi kontrol edin.")

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

# Her soruyu Elasticsearch'e yükle (temizlenmiş alanla birlikte)
for soru_id, metin in sorular:
    try:
        temiz_metin = temizle(metin)
        es.index(index="sorular", id=soru_id, document={
            "soru": metin,
            "soru_cleaned": temiz_metin
        })
    except Exception as e:
        print(f"{soru_id} numaralı soru yüklenemedi:", e)

conn.close()

print("Elasticsearch'e veri aktarma tamamlandı.")
