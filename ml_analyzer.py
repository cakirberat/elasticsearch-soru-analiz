#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Machine Learning Analiz Modülü
Bu modül, Elasticsearch'e alternatif olarak makine öğrenmesi ile soru analizi yapar.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
import joblib
import os
import json
from datetime import datetime
from performance_monitor import monitor_performance
from es_search import load_stopwords, temizle
import re

class MLAnalyzer:
    def __init__(self):
        self.vectorizer = None
        self.questions = []
        self.cleaned_questions = []
        self.tfidf_matrix = None
        self.model_path = "ml_models"
        self.ensure_model_directory()
        # Basit metin normalizasyon paterni (Türkçe karakterler korunur, noktalama temizlenir)
        self._non_word_pattern = re.compile(r"[^\w\sÇĞİÖŞÜçğıöşü]")
        
    def ensure_model_directory(self):
        """Model dizinini oluşturur"""
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
            
    @monitor_performance("ml_veri_yukleme")
    def load_questions_from_db(self):
        """Veritabanından soruları yükler"""
        try:
            import sqlite3
            conn = sqlite3.connect('sorular.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT metin FROM sorular")
            questions = cursor.fetchall()
            
            self.questions = [q[0] for q in questions]
            conn.close()
            
            print(f"✅ {len(self.questions)} soru yüklendi")
            return True
            
        except Exception as e:
            print(f"❌ Veritabanı yükleme hatası: {e}")
            return False
            
    @monitor_performance("ml_metin_temizleme")
    def clean_questions(self):
        """Soruları temizler ve hazırlar"""
        self.cleaned_questions = []
        for question in self.questions:
            basic = self._non_word_pattern.sub(" ", question).lower()
            cleaned = temizle(basic)
            self.cleaned_questions.append(cleaned)
            
        print(f"✅ {len(self.cleaned_questions)} soru temizlendi")
        
    @monitor_performance("ml_model_egitimi")
    def train_model(self):
        """TF-IDF modelini eğitir"""
        if not self.cleaned_questions:
            print("❌ Temizlenmiş sorular bulunamadı")
            return False
            
        # TF-IDF vektörizer oluştur
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            norm="l2",
            lowercase=False,
            token_pattern=r"(?u)\b\w\w+\b",
        )
        
        # TF-IDF matrisini oluştur
        self.tfidf_matrix = self.vectorizer.fit_transform(self.cleaned_questions)
        
        # Modeli kaydet
        model_file = os.path.join(self.model_path, "tfidf_model.pkl")
        joblib.dump(self.vectorizer, model_file)
        
        print(f"✅ TF-IDF modeli eğitildi ve kaydedildi")
        print(f"📊 Vektör boyutu: {self.tfidf_matrix.shape}")
        return True
        
    @monitor_performance("ml_model_yukleme")
    def load_model(self):
        """Kaydedilmiş modeli yükler"""
        model_file = os.path.join(self.model_path, "tfidf_model.pkl")
        
        if os.path.exists(model_file):
            self.vectorizer = joblib.load(model_file)
            # TF-IDF matrisini yeniden oluştur
            if self.cleaned_questions:
                self.tfidf_matrix = self.vectorizer.transform(self.cleaned_questions)
                print("✅ Kaydedilmiş model yüklendi ve TF-IDF matrisi oluşturuldu")
            else:
                print("❌ Temizlenmiş sorular bulunamadı, model yüklenemedi")
                return False
            return True
        else:
            print("❌ Kaydedilmiş model bulunamadı, yeni model eğitilecek")
            return False
            
    @monitor_performance("ml_benzer_soru_bulma")
    def find_similar_questions_ml(self, query, top_k=5, threshold=0.3):
        """Makine öğrenmesi ile benzer soruları bulur"""
        if not self.vectorizer:
            print("❌ Model yüklenmemiş")
            return []
            
        # Sorguyu temizle
        cleaned_query = temizle(self._non_word_pattern.sub(" ", query).lower())
        
        # Sorguyu vektörize et
        query_vector = self.vectorizer.transform([cleaned_query])
        
        # Benzerlik hesapla
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        max_similarity = float(similarities.max()) if similarities.size > 0 else 1.0
        
        # En benzer soruları bul
        similar_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in similar_indices:
            similarity = similarities[idx]
            eff_threshold = max(threshold, 0.05)
            if similarity >= eff_threshold:
                results.append({
                    'soru': self.questions[idx],
                    'benzerlik': float(similarity),
                    'yuzde': float((similarity / max_similarity) * 100.0) if max_similarity > 0 else 0.0,
                    'index': int(idx)
                })
                
        return results
        
    @monitor_performance("ml_kumeleme_analizi")
    def cluster_analysis(self, n_clusters=5):
        """Soruları kümeler halinde analiz eder"""
        if self.tfidf_matrix is None:
            print("❌ TF-IDF matrisi bulunamadı")
            return None
            
        # K-means kümeleme
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(self.tfidf_matrix)
        
        # Küme analizi
        clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append({
                'soru': self.questions[i],
                'index': i
            })
            
        return clusters
        
    @monitor_performance("ml_konu_analizi")
    def topic_analysis(self, n_topics=5):
        """LDA ile konu analizi yapar"""
        if self.tfidf_matrix is None:
            print("❌ TF-IDF matrisi bulunamadı")
            return None
            
        # LDA modeli
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=10
        )
        
        # Konuları öğren
        lda.fit(self.tfidf_matrix)
        
        # Konu kelimelerini al
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[-10:]]
            topics.append({
                'konu_id': topic_idx,
                'kelimeler': top_words
            })
            
        return topics
        
    def get_ml_statistics(self):
        """ML analizi istatistiklerini döndürür"""
        if not self.questions:
            return None
            
        stats = {
            'toplam_soru': len(self.questions),
            'ortalama_soru_uzunlugu': np.mean([len(q.split()) for q in self.questions]),
            'benzersiz_kelimeler': len(set(' '.join(self.cleaned_questions).split())),
            'model_durumu': 'Eğitildi' if self.vectorizer else 'Eğitilmedi',
            'vektor_boyutu': self.tfidf_matrix.shape if self.tfidf_matrix is not None else None
        }
        
        return stats

def main():
    """Ana test fonksiyonu"""
    print("🤖 Machine Learning Analiz Sistemi")
    print("=" * 50)
    
    # Analizör oluştur
    analyzer = MLAnalyzer()
    
    # Verileri yükle
    if not analyzer.load_questions_from_db():
        print("❌ Veri yükleme başarısız")
        return
        
    # Soruları temizle
    analyzer.clean_questions()
    
    # Model eğitimi
    if not analyzer.load_model():
        analyzer.train_model()

        
        
    # Test sorgusu
    test_query = "Python programlama nasıl öğrenilir?"
    print(f"\n🔍 Test Sorgusu: {test_query}")
    
    # Benzer soruları bul
    similar_questions = analyzer.find_similar_questions_ml(test_query, top_k=3)
    
    print("\n📋 Benzer Sorular (ML):")
    for i, result in enumerate(similar_questions, 1):
        print(f"{i}. {result['soru']}")
        print(f"   Benzerlik: {result['benzerlik']:.3f}")
        
    # İstatistikler
    stats = analyzer.get_ml_statistics()
    if stats:
        print(f"\n📊 ML İstatistikleri:")
        print(f"   Toplam Soru: {stats['toplam_soru']}")
        print(f"   Ortalama Uzunluk: {stats['ortalama_soru_uzunlugu']:.1f} kelime")
        print(f"   Benzersiz Kelime: {stats['benzersiz_kelimeler']}")
        
    print("\n✅ ML analizi tamamlandı!")

if __name__ == "__main__":
    main()
