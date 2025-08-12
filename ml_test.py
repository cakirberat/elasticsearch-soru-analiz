#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Machine Learning Test Scripti
Bu script, ML analiz sisteminin tüm özelliklerini test eder.
"""

from ml_analyzer import MLAnalyzer
from performance_monitor import monitor_performance, print_performance_summary, save_performance_metrics
import time

def test_ml_system():
    """ML sistemini kapsamlı test eder"""
    print("🤖 Machine Learning Test Sistemi")
    print("=" * 60)
    
    # Analizör oluştur
    analyzer = MLAnalyzer()
    
    # 1. Veri yükleme testi
    print("\n📊 1. Veri Yükleme Testi")
    print("-" * 30)
    if analyzer.load_questions_from_db():
        pass
    else:
        print("❌ Veri yükleme başarısız")
        return
        
    # 2. Metin temizleme testi
    print("\n🧹 2. Metin Temizleme Testi")
    print("-" * 30)
    analyzer.clean_questions()
    
    # 3. Model eğitimi testi
    print("\n🎓 3. Model Eğitimi Testi")
    print("-" * 30)
    if analyzer.train_model():
        print("✅ TF-IDF modeli başarıyla eğitildi")
        print(f"📊 Vektör boyutu: {analyzer.tfidf_matrix.shape}")
    else:
        print("❌ Model eğitimi başarısız")
        return
        
    # 4. Benzer soru bulma testi
    print("\n🔍 4. Benzer Soru Bulma Testi")
    print("-" * 30)
    
    test_queries = [
        "Python programlama nasıl öğrenilir?",
        "Veritabanı nedir?",
        "Web geliştirme araçları nelerdir?",
        "Algoritma nedir?",
        "Yapay zeka uygulamaları nelerdir?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        results = analyzer.find_similar_questions_ml(query, top_k=3, threshold=0.3)
        
        if results:
            print(f"   📋 {len(results)} benzer soru bulundu:")
            for j, result in enumerate(results, 1):
                print(f"   {j}. {result['soru'][:60]}...")
                yuzde = result.get('yuzde', float(result.get('benzerlik', 0)) * 100.0)
                print(f"      Benzerlik: %{yuzde:.0f}")
        else:
            print("   ❌ Benzer soru bulunamadı")
            
    # 5. Kümeleme analizi testi
    print("\n📊 5. Kümeleme Analizi Testi")
    print("-" * 30)
    clusters = analyzer.cluster_analysis(n_clusters=3)
    if clusters:
        print(f"✅ {len(clusters)} küme oluşturuldu:")
        for cluster_id, questions in clusters.items():
            print(f"   Küme {cluster_id}: {len(questions)} soru")
            if questions:
                print(f"      Örnek: {questions[0]['soru'][:50]}...")
    else:
        print("❌ Kümeleme analizi başarısız")
        
    # 6. Konu analizi testi
    print("\n📚 6. Konu Analizi Testi")
    print("-" * 30)
    topics = analyzer.topic_analysis(n_topics=3)
    if topics:
        print(f"✅ {len(topics)} konu tespit edildi:")
        for topic in topics:
            print(f"   Konu {topic['konu_id']}: {', '.join(topic['kelimeler'][:5])}...")
    else:
        print("❌ Konu analizi başarısız")
        
    # 7. İstatistikler
    print("\n📈 7. Sistem İstatistikleri")
    print("-" * 30)
    stats = analyzer.get_ml_statistics()
    if stats:
        print(f"   Toplam Soru: {stats['toplam_soru']}")
        print(f"   Ortalama Uzunluk: {stats['ortalama_soru_uzunlugu']:.1f} kelime")
        print(f"   Benzersiz Kelime: {stats['benzersiz_kelimeler']}")
        print(f"   Model Durumu: {stats['model_durumu']}")
        if stats['vektor_boyutu']:
            print(f"   Vektör Boyutu: {stats['vektor_boyutu']}")
            
    print("\n✅ ML test sistemi tamamlandı!")

def test_performance_comparison():
    """Elasticsearch vs ML performans karşılaştırması"""
    print("\n⚡ Performans Karşılaştırması")
    print("=" * 60)
    
    from es_search import benzer_sorulari_bul
    from ml_analyzer import MLAnalyzer
    import time
    
    test_query = "Python programlama nasıl öğrenilir?"
    
    # ML test
    print("\n🤖 Machine Learning Test:")
    start_time = time.time()
    
    analyzer = MLAnalyzer()
    analyzer.load_questions_from_db()
    analyzer.clean_questions()
    analyzer.train_model()
    ml_results = analyzer.find_similar_questions_ml(test_query, top_k=5)
    
    ml_time = time.time() - start_time
    print(f"   ⏱️ Süre: {ml_time:.3f} saniye")
    print(f"   📋 Sonuç: {len(ml_results)} soru")
    
    # Elasticsearch test
    print("\n🔍 Elasticsearch Test:")
    start_time = time.time()
    
    import io, sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    benzer_sorulari_bul(test_query, esik=0.3)
    
    sys.stdout = old_stdout
    es_time = time.time() - start_time
    print(f"   ⏱️ Süre: {es_time:.3f} saniye")
    
    # Karşılaştırma
    print(f"\n📊 Karşılaştırma:")
    print(f"   ML: {ml_time:.3f} saniye")
    print(f"   ES: {es_time:.3f} saniye")
    
    if ml_time < es_time:
        print(f"   🏆 ML {es_time/ml_time:.1f}x daha hızlı")
    else:
        print(f"   🏆 ES {ml_time/es_time:.1f}x daha hızlı")

def main():
    """Ana test fonksiyonu"""
    try:
        # ML sistem testi
        test_ml_system()
        
        # Performans karşılaştırması
        test_performance_comparison()
        
        # Performans özeti
        print("\n📊 Performans Özeti:")
        print("-" * 30)
        print_performance_summary()
        
        # Metrikleri kaydet
        save_performance_metrics("ml_test_metrics.json")
        print("\n💾 Metrikler 'ml_test_metrics.json' dosyasına kaydedildi")
        
    except Exception as e:
        print(f"❌ Test sırasında hata: {e}")

if __name__ == "__main__":
    main()
