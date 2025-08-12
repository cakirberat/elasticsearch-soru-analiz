#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performans Test Scripti
Bu script, projenin çeşitli fonksiyonlarının performansını test eder.
"""

import time
from performance_monitor import monitor_performance, print_performance_summary, save_performance_metrics
from es_search import benzer_sorulari_bul, temizle, load_stopwords

def test_stopword_temizleme():
    """Stopword temizleme fonksiyonunu test eder"""
    print("🔄 Stopword temizleme testi başlatılıyor...")
    
    test_sorular = [
        "Bu bir test sorusudur ve stopwords temizlenmelidir",
        "Python programlama dili hakkında bilgi verir misiniz?",
        "Elasticsearch nasıl kurulur ve yapılandırılır?",
        "Veritabanı bağlantısı nasıl yapılır?",
        "Web uygulaması geliştirme süreci nasıldır?"
    ]
    
    for i, soru in enumerate(test_sorular, 1):
        print(f"  Test {i}: '{soru}'")
        temizlenmis = temizle(soru)
        print(f"  Sonuç: '{temizlenmis}'")
        print()

def test_elasticsearch_arama():
    """Elasticsearch arama fonksiyonunu test eder"""
    print("🔄 Elasticsearch arama testi başlatılıyor...")
    
    test_sorular = [
        "Python",
        "veritabanı",
        "web uygulaması",
        "programlama",
        "test"
    ]
    
    for i, soru in enumerate(test_sorular, 1):
        print(f"  Test {i}: '{soru}' arama yapılıyor...")
        try:
            benzer_sorulari_bul(soru, esik=0.5)
        except Exception as e:
            print(f"  Hata: {e}")
        print()

def test_stopwords_yukleme():
    """Stopwords yükleme performansını test eder"""
    print("🔄 Stopwords yükleme testi başlatılıyor...")
    
    for i in range(5):
        print(f"  Test {i+1}: Stopwords yükleniyor...")
        stopwords = load_stopwords()
        print(f"  Yüklenen stopwords sayısı: {len(stopwords)}")
        print()

def manuel_performans_testi():
    """Manuel performans testi"""
    print("🚀 Manuel Performans Testi Başlatılıyor...")
    print("="*50)
    
    # Test 1: Stopword temizleme
    print("\n1️⃣ Stopword Temizleme Testi:")
    test_stopword_temizleme()
    
    # Test 2: Stopwords yükleme
    print("\n2️⃣ Stopwords Yükleme Testi:")
    test_stopwords_yukleme()
    
    # Test 3: Elasticsearch arama (eğer Elasticsearch çalışıyorsa)
    print("\n3️⃣ Elasticsearch Arama Testi:")
    test_elasticsearch_arama()
    
    # Performans özeti
    print("\n" + "="*50)
    print("📊 PERFORMANS ÖZETİ:")
    print_performance_summary()
    
    # Metrikleri kaydet
    save_performance_metrics("test_performance_metrics.json")
    print("\n✅ Test tamamlandı! Metrikler 'test_performance_metrics.json' dosyasına kaydedildi.")

if __name__ == "__main__":
    print("🎯 Soru Projesi Performans Testi")
    print("Bu script, projenizin çeşitli fonksiyonlarının performansını ölçer.")
    print()
    
    try:
        manuel_performans_testi()
    except KeyboardInterrupt:
        print("\n❌ Test kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Test sırasında hata oluştu: {e}")
        print_performance_summary()
