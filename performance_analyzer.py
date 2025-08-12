#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performans Analizi ve Tahmin Sistemi
Bu modül, mevcut performans verilerine dayanarak gelecekteki performansı tahmin eder.
"""

import json
import math
from datetime import datetime
from performance_monitor import performance_monitor

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics = performance_monitor.metrics
        self.analysis_results = {}
    
    def analyze_current_performance(self):
        """Mevcut performans verilerini analiz eder"""
        print("🔍 Mevcut Performans Analizi Yapılıyor...")
        print("="*60)
        
        analysis = {}
        
        for operation_name, measurements in self.metrics.items():
            if not measurements:
                continue
                
            durations = [m['duration_seconds'] for m in measurements]
            memories = [m['memory_used_mb'] for m in measurements]
            
            # Temel istatistikler
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            total_duration = sum(durations)
            
            # Veri sayısı (varsayılan olarak 1, gerçek veri sayısı bilinmiyorsa)
            data_count = len(measurements)
            
            # Performans karakteristikleri
            performance_per_item = avg_duration / max(data_count, 1)
            
            analysis[operation_name] = {
                'data_count': data_count,
                'avg_duration': avg_duration,
                'min_duration': min_duration,
                'max_duration': max_duration,
                'total_duration': total_duration,
                'avg_memory': sum(memories) / len(memories),
                'performance_per_item': performance_per_item,
                'measurement_count': len(measurements)
            }
            
            print(f"\n📊 {operation_name.upper()}:")
            print(f"   Analiz edilen veri sayısı: {data_count}")
            print(f"   Ortalama süre: {avg_duration:.4f} saniye")
            print(f"   Veri başına süre: {performance_per_item:.6f} saniye")
            print(f"   En hızlı: {min_duration:.4f} saniye")
            print(f"   En yavaş: {max_duration:.4f} saniye")
            print(f"   Toplam süre: {total_duration:.4f} saniye")
            print(f"   Ortalama bellek: {sum(memories)/len(memories):.2f} MB")
        
        self.analysis_results = analysis
        return analysis
    
    def predict_performance(self, target_data_count):
        """Belirli veri miktarı için performans tahmini yapar"""
        print(f"\n🔮 {target_data_count:,} Veri İçin Performans Tahmini")
        print("="*60)
        
        predictions = {}
        
        for operation_name, analysis in self.analysis_results.items():
            # Basit doğrusal tahmin
            predicted_duration = analysis['performance_per_item'] * target_data_count
            
            # Bellek kullanımı tahmini (logaritmik artış)
            memory_factor = math.log(target_data_count + 1, 10)
            predicted_memory = analysis['avg_memory'] * memory_factor
            
            # Güven aralığı (varyans bazlı)
            variance = (analysis['max_duration'] - analysis['min_duration']) / 2
            confidence_min = max(0, predicted_duration - variance)
            confidence_max = predicted_duration + variance
            
            predictions[operation_name] = {
                'predicted_duration': predicted_duration,
                'predicted_memory': predicted_memory,
                'confidence_min': confidence_min,
                'confidence_max': confidence_max,
                'estimated_minutes': predicted_duration / 60,
                'estimated_hours': predicted_duration / 3600
            }
            
            print(f"\n🎯 {operation_name.upper()}:")
            print(f"   Tahmini süre: {predicted_duration:.2f} saniye")
            print(f"   Tahmini süre: {predicted_duration/60:.2f} dakika")
            if predicted_duration > 3600:
                print(f"   Tahmini süre: {predicted_duration/3600:.2f} saat")
            print(f"   Güven aralığı: {confidence_min:.2f} - {confidence_max:.2f} saniye")
            print(f"   Tahmini bellek: {predicted_memory:.2f} MB")
        
        return predictions
    
    def get_database_info(self):
        """Veritabanındaki veri sayısını tahmin eder"""
        print("\n📊 Veritabanı Analizi")
        print("="*60)
        
        # Elasticsearch bağlantısı varsa gerçek veri sayısını al
        try:
            from es_config import get_default_client
            es = get_default_client()
            if es:
                # Tüm indekslerdeki toplam döküman sayısını al
                indices = es.cat.indices(format='json')
                total_docs = 0
                
                print("📁 Mevcut İndeksler:")
                for index in indices:
                    doc_count = int(index['docs.count'])
                    total_docs += doc_count
                    print(f"   - {index['index']}: {doc_count:,} döküman")
                
                print(f"\n📈 Toplam Döküman Sayısı: {total_docs:,}")
                return total_docs
            else:
                print("❌ Elasticsearch bağlantısı kurulamadı")
                return None
                
        except Exception as e:
            print(f"❌ Veritabanı analizi hatası: {e}")
            return None
    
    def interactive_prediction(self):
        """Kullanıcıdan veri miktarı alıp tahmin yapar"""
        print("\n🎯 Performans Tahmin Sistemi")
        print("="*60)
        
        # Mevcut performansı analiz et
        self.analyze_current_performance()
        
        # Veritabanı bilgilerini al
        current_data_count = self.get_database_info()
        
        if current_data_count:
            print(f"\n💡 Mevcut veritabanında {current_data_count:,} döküman bulunuyor.")
            print("   Bu veriler üzerinde yapılan analizler kullanılarak tahmin yapılacak.")
        
        # Kullanıcıdan hedef veri miktarını al
        while True:
            try:
                user_input = input(f"\n🎯 Tahmin yapmak istediğiniz veri miktarını girin (örn: 10000): ")
                
                # Virgül ve nokta karakterlerini temizle
                user_input = user_input.replace(',', '').replace('.', '')
                
                target_count = int(user_input)
                
                if target_count <= 0:
                    print("❌ Lütfen pozitif bir sayı girin!")
                    continue
                
                break
                
            except ValueError:
                print("❌ Lütfen geçerli bir sayı girin!")
                continue
        
        # Performans tahmini yap
        predictions = self.predict_performance(target_count)
        
        # Sonuçları kaydet
        self.save_prediction_results(target_count, predictions)
        
        return predictions
    
    def save_prediction_results(self, target_count, predictions):
        """Tahmin sonuçlarını dosyaya kaydeder"""
        timestamp = datetime.now().isoformat()
        
        results = {
            'timestamp': timestamp,
            'target_data_count': target_count,
            'predictions': predictions,
            'analysis_results': self.analysis_results
        }
        
        filename = f"performance_prediction_{timestamp[:10]}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Tahmin sonuçları '{filename}' dosyasına kaydedildi.")
        except Exception as e:
            print(f"❌ Dosya kaydetme hatası: {e}")
    
    def print_summary_report(self, target_count, predictions):
        """Özet rapor yazdırır"""
        print("\n📋 PERFORMANS TAHMİN ÖZETİ")
        print("="*60)
        print(f"🎯 Hedef Veri Miktarı: {target_count:,}")
        print(f"📅 Tahmin Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        total_predicted_time = 0
        total_predicted_memory = 0
        
        for operation_name, pred in predictions.items():
            total_predicted_time += pred['predicted_duration']
            total_predicted_memory += pred['predicted_memory']
            
            print(f"\n🔍 {operation_name.upper()}:")
            print(f"   ⏱️  Tahmini Süre: {pred['predicted_duration']:.2f} saniye")
            print(f"   💾 Tahmini Bellek: {pred['predicted_memory']:.2f} MB")
        
        print(f"\n📊 TOPLAM TAHMİN:")
        print(f"   ⏱️  Toplam Süre: {total_predicted_time:.2f} saniye")
        print(f"   ⏱️  Toplam Süre: {total_predicted_time/60:.2f} dakika")
        if total_predicted_time > 3600:
            print(f"   ⏱️  Toplam Süre: {total_predicted_time/3600:.2f} saat")
        print(f"   💾 Toplam Bellek: {total_predicted_memory:.2f} MB")

def main():
    """Ana fonksiyon"""
    analyzer = PerformanceAnalyzer()
    
    print("🎯 Performans Analizi ve Tahmin Sistemi")
    print("Bu sistem, mevcut performans verilerine dayanarak gelecekteki performansı tahmin eder.")
    
    # İnteraktif tahmin
    predictions = analyzer.interactive_prediction()
    
    # Özet rapor
    target_count = int(input("\n🎯 Hedef veri miktarını tekrar girin (özet için): ").replace(',', ''))
    analyzer.print_summary_report(target_count, predictions)

if __name__ == "__main__":
    main()
