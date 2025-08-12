#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elasticsearch 8.x Test Scripti
Bu script, Elasticsearch 8.12.1 bağlantısını ve temel işlemleri test eder.
"""

from es_config import test_connection, create_elasticsearch_client, get_default_client
from performance_monitor import monitor_performance, print_performance_summary, save_performance_metrics

@monitor_performance("elasticsearch_test")
def test_basic_operations():
    """Temel Elasticsearch işlemlerini test eder"""
    print("🔍 Elasticsearch temel işlemleri test ediliyor...")
    
    # Bağlantı testi
    es = test_connection()
    if not es:
        print("❌ Bağlantı kurulamadı, test durduruluyor.")
        return False
    
    try:
        # 1. Cluster bilgilerini al
        print("\n1️⃣ Cluster bilgileri alınıyor...")
        info = es.info()
        print(f"   Sürüm: {info['version']['number']}")
        print(f"   Cluster: {info['version']['build_flavor']}")
        print(f"   Lucene: {info['version']['lucene_version']}")
        
        # 2. İndeksleri listele
        print("\n2️⃣ Mevcut indeksler listeleniyor...")
        indices = es.cat.indices(format='json')
        if indices:
            for index in indices:
                print(f"   - {index['index']} (döküman: {index['docs.count']})")
        else:
            print("   Hiç indeks bulunamadı.")
        
        # 3. Test indeksi oluştur
        print("\n3️⃣ Test indeksi oluşturuluyor...")
        test_index = "test_sorular"
        
        # İndeks varsa sil
        if es.indices.exists(index=test_index):
            es.indices.delete(index=test_index)
            print(f"   Eski {test_index} indeksi silindi.")
        
        # Yeni indeks oluştur
        mapping = {
            "mappings": {
                "properties": {
                    "soru": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "kategori": {
                        "type": "keyword"
                    },
                    "tarih": {
                        "type": "date"
                    }
                }
            }
        }
        
        es.indices.create(index=test_index, body=mapping)
        print(f"   {test_index} indeksi oluşturuldu.")
        
        # 4. Test dökümanı ekle
        print("\n4️⃣ Test dökümanı ekleniyor...")
        test_doc = {
            "soru": "Python programlama dili nasıl öğrenilir?",
            "kategori": "programlama",
            "tarih": "2024-01-01"
        }
        
        result = es.index(index=test_index, body=test_doc)
        print(f"   Döküman eklendi. ID: {result['_id']}")
        
        # 5. Arama testi
        print("\n5️⃣ Arama testi yapılıyor...")
        search_body = {
            "query": {
                "match": {
                    "soru": "Python"
                }
            }
        }
        
        search_result = es.search(index=test_index, body=search_body)
        hits = search_result['hits']['hits']
        print(f"   {len(hits)} sonuç bulundu.")
        
        for hit in hits:
            print(f"   - {hit['_source']['soru']} (skor: {hit['_score']:.2f})")
        
        # 6. Test indeksini temizle
        print("\n6️⃣ Test indeksi temizleniyor...")
        es.indices.delete(index=test_index)
        print(f"   {test_index} indeksi silindi.")
        
        print("\n✅ Tüm testler başarıyla tamamlandı!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test sırasında hata oluştu: {e}")
        return False

def test_performance():
    """Performans testleri"""
    print("\n🚀 Performans testleri başlatılıyor...")
    
    es = get_default_client()
    if not es:
        print("❌ Bağlantı kurulamadı.")
        return
    
    # Bağlantı hızı testi
    import time
    
    print("📊 Bağlantı hızı test ediliyor...")
    start_time = time.time()
    
    for i in range(10):
        es.ping()
    
    end_time = time.time()
    avg_time = (end_time - start_time) / 10
    print(f"   Ortalama ping süresi: {avg_time:.3f} saniye")

def main():
    """Ana test fonksiyonu"""
    print("🎯 Elasticsearch 8.x Test Scripti")
    print("="*50)
    
    # Performans izleme başlat
    print("📊 Performans izleme aktif...")
    
    # Temel işlemleri test et
    success = test_basic_operations()
    
    if success:
        # Performans testleri
        test_performance()
        
        # Performans özeti
        print("\n" + "="*50)
        print("📊 PERFORMANS ÖZETİ:")
        print_performance_summary()
        
        # Metrikleri kaydet
        save_performance_metrics("es_test_metrics.json")
        print("\n✅ Test tamamlandı! Metrikler 'es_test_metrics.json' dosyasına kaydedildi.")
    else:
        print("\n❌ Test başarısız oldu. Lütfen Elasticsearch servisini kontrol edin.")

if __name__ == "__main__":
    main()
