import os
import re
from elasticsearch import Elasticsearch
from TurkishStemmer import TurkishStemmer
from performance_monitor import monitor_performance
from es_config import get_default_client, test_connection

# Stopwords
STOPWORDS_FILE = "stopwords.txt"

def load_stopwords():
    if not os.path.exists(STOPWORDS_FILE):
        with open(STOPWORDS_FILE, 'w', encoding='utf-8') as f:
            pass  # Dosya yoksa oluştur
    with open(STOPWORDS_FILE, 'r', encoding='utf-8') as f:
        # Tüm stopwords'leri küçük harfe çevirerek yükle
        return [line.strip().lower() for line in f if line.strip()]

def save_stopwords(stopwords):
    # Tüm stopwordsleri küçük harfe çevir ve kaydet
    with open(STOPWORDS_FILE, 'w', encoding='utf-8') as f:
        for word in stopwords:
            f.write(word.strip().lower() + '\n')

stopwords = load_stopwords()
stemmer = TurkishStemmer()
# Noktalama ve özel karakterleri temizlemek için regex (Türkçe karakterleri korur)
_non_word_pattern = re.compile(r"[^\w\sÇĞİÖŞÜçğıöşü]")

def refresh_stopwords():
    """Stopwords listesini dosyadan tekrar yükler (GUI değişikliklerinde güncel kalması için)."""
    global stopwords
    stopwords = load_stopwords()

# Stopwordleri temizle
@monitor_performance("stopword_temizleme")
def temizle(soru):
    global stopwords
    # Metinden noktalama ve özel karakterleri kaldır, küçük harfe çevir
    normalized = _non_word_pattern.sub(" ", str(soru)).lower()
    tokens = normalized.split()

    # Stopwords listesini köklerine indirgenmiş ve küçük harfe çevrilmiş olarak hazırla
    stemmed_stopwords = set(stemmer.stem(sw.lower()) for sw in stopwords)

    # Kelimeleri köklerine indir, stopwords köklerinde olanları çıkar
    filtered_stemmed_tokens = [
        stemmer.stem(token) for token in tokens
        if stemmer.stem(token) not in stemmed_stopwords
    ]

    return " ".join(filtered_stemmed_tokens)

# Elasticsearch arama fonksiyonu
@monitor_performance("elasticsearch_arama")
def benzer_sorulari_bul(soru, esik=0.75):
    # Elasticsearch 8.x için yapılandırılmış istemci kullan
    es = get_default_client()
    if not es:
        print("❌ Elasticsearch bağlantısı kurulamadı. Lütfen servisin çalıştığından emin olun.")
        return
    
    # Sorguyu stopwords ve köklerine göre temizle
    temiz_soru = temizle(soru)

    body = {
        "query": {
            "multi_match": {
                "query": temiz_soru,
                "fields": ["soru_cleaned^2", "soru"]
            }
        }
    }

    try:
        sonuc = es.search(index="sorular", body=body)
        print(f"\n '{soru}' sorusuna benzer sonuçlar:")
        print("-" * 50)

        bulundu = False
        skorlar = [hit["_score"] for hit in sonuc["hits"]["hits"]]
        max_skor = max(skorlar) if skorlar else 1
        for hit in sonuc["hits"]["hits"]:
            skor = hit["_score"]
            if skor >= esik:
                yuzde = (skor / max_skor) * 100 if max_skor else 0
                print(f"• {hit['_source']['soru']}  (Benzerlik: %{yuzde:.0f})")
                bulundu = True

        if not bulundu:
            print("Eşik değeri üzerinde benzer soru bulunamadı.")

    except Exception as e:
        print("Arama hatası:", e)

# Uygulama başlatıcı
if __name__ == "__main__":
    while True:
        print("\n--- Soru Arama ve Stopwords Yönetimi ---")
        print("1. Soru ara")
        print("2. Stopwords listele")
        print("3. Stopwords ekle")
        print("4. Stopwords çıkar")
        print("5. Çıkış")
        secim = input("Seçiminiz: ")
        if secim == "1":
            soru = input("Soru girin: ")
            benzer_sorulari_bul(soru)
        elif secim == "2":
            print("\nStopwords listesi:")
            for i, sw in enumerate(stopwords, 1):
                print(f"{i}. {sw}")
        elif secim == "3":
            yeni = input("Eklemek istediğiniz kelime(ler)i virgülle ayırarak girin: ").split(",")
            yeni = [w.strip() for w in yeni if w.strip() and w.strip() not in stopwords]
            if yeni:
                stopwords.extend(yeni)
                save_stopwords(stopwords)
                print(f"Eklendi: {', '.join(yeni)}")
            else:
                print("Yeni kelime eklenmedi veya zaten mevcut.")
        elif secim == "4":
            sil = input("Çıkarmak istediğiniz kelime(ler)i virgülle ayırarak girin: ").split(",")
            sil = [w.strip() for w in sil if w.strip() in stopwords]
            if sil:
                stopwords = [w for w in stopwords if w not in sil]
                save_stopwords(stopwords)
                print(f"Çıkarıldı: {', '.join(sil)}")
            else:
                print("Belirtilen kelimeler stopwords listesinde yok.")
        elif secim == "5":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")
