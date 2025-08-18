#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performans İzleme Sistemi
Bu modül, uygulama performansını izler ve metrikleri toplar.
"""

import time
import psutil
import json
import os
from datetime import datetime
from functools import wraps
import threading

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()
        
    def monitor_performance(self, operation_name):
        """Performans izleme decorator'ı"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                start_cpu = psutil.cpu_percent()
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                except Exception as e:
                    success = False
                    raise e
                finally:
                    end_time = time.time()
                    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                    end_cpu = psutil.cpu_percent()
                    
                    duration = end_time - start_time
                    memory_used = end_memory - start_memory
                    cpu_used = (start_cpu + end_cpu) / 2
                    
                    measurement = {
                        'timestamp': datetime.now().isoformat(),
                        'duration_seconds': duration,
                        'memory_used_mb': memory_used,
                        'cpu_percent': cpu_used,
                        'success': success,
                        'function_name': func.__name__,
                        'args_count': len(args),
                        'kwargs_count': len(kwargs)
                    }
                    
                    with self.lock:
                        if operation_name not in self.metrics:
                            self.metrics[operation_name] = []
                        self.metrics[operation_name].append(measurement)
                
                return result
            return wrapper
        return decorator
    
    def get_operation_stats(self, operation_name):
        """Belirli bir operasyon için istatistikleri döndürür"""
        if operation_name not in self.metrics or not self.metrics[operation_name]:
            return None
            
        measurements = self.metrics[operation_name]
        durations = [m['duration_seconds'] for m in measurements]
        memories = [m['memory_used_mb'] for m in measurements]
        cpus = [m['cpu_percent'] for m in measurements]
        
        return {
            'operation_name': operation_name,
            'total_runs': len(measurements),
            'successful_runs': len([m for m in measurements if m['success']]),
            'failed_runs': len([m for m in measurements if not m['success']]),
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'total_duration': sum(durations),
            'avg_memory': sum(memories) / len(memories),
            'max_memory': max(memories),
            'avg_cpu': sum(cpus) / len(cpus),
            'max_cpu': max(cpus),
            'last_run': measurements[-1]['timestamp'] if measurements else None
        }
    
    def get_all_stats(self):
        """Tüm operasyonlar için istatistikleri döndürür"""
        stats = {}
        for operation_name in self.metrics:
            stats[operation_name] = self.get_operation_stats(operation_name)
        return stats
    
    def clear_metrics(self, operation_name=None):
        """Metrikleri temizler"""
        with self.lock:
            if operation_name:
                if operation_name in self.metrics:
                    del self.metrics[operation_name]
            else:
                self.metrics.clear()
    
    def export_metrics(self, filename=None):
        """Metrikleri dosyaya aktarır"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_metrics_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'export_timestamp': datetime.now().isoformat(),
                    'total_operations': len(self.metrics),
                    'total_measurements': sum(len(measurements) for measurements in self.metrics.values()),
                    'metrics': self.metrics,
                    'summary_stats': self.get_all_stats()
                }, f, indent=2, ensure_ascii=False)
            
            return filename
        except Exception as e:
            raise Exception(f"Metrikler dışa aktarılırken hata: {e}")
    
    def import_metrics(self, filename):
        """Metrikleri dosyadan içe aktarır"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'metrics' in data:
                with self.lock:
                    self.metrics.update(data['metrics'])
                return True
            else:
                raise Exception("Geçersiz metrik dosyası formatı")
                
        except Exception as e:
            raise Exception(f"Metrikler içe aktarılırken hata: {e}")
    
    def get_system_info(self):
        """Sistem bilgilerini döndürür"""
        try:
            return {
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': psutil.virtual_memory().total / 1024 / 1024 / 1024,
                'memory_available_gb': psutil.virtual_memory().available / 1024 / 1024 / 1024,
                'disk_usage_percent': psutil.disk_usage('/').percent,
                'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                'platform': os.name,
                'current_time': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f"Sistem bilgileri alınamadı: {e}"}

# Global performans monitör instance'ı
performance_monitor = PerformanceMonitor()

def monitor_performance(operation_name):
    """Performans izleme decorator'ı (global fonksiyon)"""
    return performance_monitor.monitor_performance(operation_name)

def print_performance_summary():
    """Tüm performans metriklerinin özetini yazdırır"""
    try:
        print("\n" + "="*60)
        print("📊 PERFORMANS ÖZETİ")
        print("="*60)
        
        if not performance_monitor.metrics:
            print("\n❌ Henüz hiçbir performans verisi toplanmamış.")
            print("   Performans verisi toplamak için:")
            print("   1️⃣ 'Hızlı Performans Testi' butonuna basın")
            print("   2️⃣ Veya GUI uygulamasında soru arama yapın")
            print("   3️⃣ Veya diğer test butonlarından birini kullanın")
            print("\n" + "="*60)
            return
        
        # Sistem bilgileri
        system_info = performance_monitor.get_system_info()
        print(f"\n🖥️ Sistem Bilgileri:")
        print(f"   CPU Çekirdek Sayısı: {system_info.get('cpu_count', 'Bilinmiyor')}")
        print(f"   Toplam RAM: {system_info.get('memory_total_gb', 0):.1f} GB")
        print(f"   Kullanılabilir RAM: {system_info.get('memory_available_gb', 0):.1f} GB")
        print(f"   Disk Kullanımı: %{system_info.get('disk_usage_percent', 0):.1f}")
        
        # Genel istatistikler
        total_operations = len(performance_monitor.metrics)
        total_measurements = sum(len(measurements) for measurements in performance_monitor.metrics.values())
        total_duration = sum(
            sum(m['duration_seconds'] for m in measurements)
            for measurements in performance_monitor.metrics.values()
        )
        
        print(f"\n📈 Genel İstatistikler:")
        print(f"   Toplam Operasyon: {total_operations}")
        print(f"   Toplam Ölçüm: {total_measurements}")
        print(f"   Toplam Çalışma Süresi: {total_duration:.2f} saniye")
        print(f"   Ortalama Operasyon Başına: {total_duration/total_operations:.2f} saniye")
        
        # Her operasyon için detaylı istatistikler
        has_data = False
        for operation_name, measurements in performance_monitor.metrics.items():
            if measurements:
                has_data = True
                durations = [m['duration_seconds'] for m in measurements]
                memories = [m['memory_used_mb'] for m in measurements]
                cpus = [m['cpu_percent'] for m in measurements]
                successful = [m for m in measurements if m['success']]
                failed = [m for m in measurements if not m['success']]
                
                print(f"\n📊 {operation_name}:")
                print(f"   🔄 Çalıştırma sayısı: {len(measurements)}")
                print(f"   ✅ Başarılı: {len(successful)}")
                print(f"   ❌ Başarısız: {len(failed)}")
                print(f"   ⏱️  Ortalama süre: {sum(durations)/len(durations):.3f} saniye")
                print(f"   🏃 En hızlı: {min(durations):.3f} saniye")
                print(f"   🐌 En yavaş: {max(durations):.3f} saniye")
                print(f"   ⏰ Toplam süre: {sum(durations):.3f} saniye")
                print(f"   💾 Ortalama bellek kullanımı: {sum(memories)/len(memories):.2f} MB")
                print(f"   🧠 Maksimum bellek kullanımı: {max(memories):.2f} MB")
                print(f"   🔥 Ortalama CPU kullanımı: {sum(cpus)/len(cpus):.1f}%")
                print(f"   🔥 Maksimum CPU kullanımı: {max(cpus):.1f}%")
                
                # Son çalıştırma bilgisi
                if measurements:
                    last_run = measurements[-1]
                    print(f"   🕐 Son çalıştırma: {last_run['timestamp'][:19]}")
                    print(f"   📊 Son çalıştırma durumu: {'✅ Başarılı' if last_run['success'] else '❌ Başarısız'}")
        
        if not has_data:
            print("\n❌ Hiçbir işlem tamamlanmamış.")
            print("   Performans verisi toplamak için:")
            print("   1️⃣ 'Hızlı Performans Testi' butonuna basın")
            print("   2️⃣ Veya GUI uygulamasında soru arama yapın")
            print("   3️⃣ Veya diğer test butonlarından birini kullanın")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Performans özeti yazdırılırken hata: {e}")
        print("="*60)

def save_performance_metrics(filename="performance_metrics.json"):
    """Performans metriklerini JSON dosyasına kaydeder"""
    try:
        if not performance_monitor.metrics:
            raise Exception("Kaydedilecek performans verisi bulunamadı")
        
        # Metrikleri dışa aktar
        exported_file = performance_monitor.export_metrics(filename)
        
        print(f"✅ Performans metrikleri başarıyla kaydedildi: {exported_file}")
        return exported_file
        
    except Exception as e:
        print(f"❌ Performans metrikleri kaydedilirken hata: {e}")
        raise

def load_performance_metrics(filename="performance_metrics.json"):
    """Performans metriklerini JSON dosyasından yükler"""
    try:
        if not os.path.exists(filename):
            raise Exception(f"Dosya bulunamadı: {filename}")
        
        # Metrikleri içe aktar
        performance_monitor.import_metrics(filename)
        
        print(f"✅ Performans metrikleri başarıyla yüklendi: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Performans metrikleri yüklenirken hata: {e}")
        raise

def clear_all_metrics():
    """Tüm performans metriklerini temizler"""
    try:
        performance_monitor.clear_metrics()
        print("✅ Tüm performans metrikleri temizlendi")
    except Exception as e:
        print(f"❌ Metrikler temizlenirken hata: {e}")
        raise

def get_performance_report():
    """Detaylı performans raporu oluşturur"""
    try:
        if not performance_monitor.metrics:
            return "Henüz hiçbir performans verisi toplanmamış."
        
        report = []
        report.append("📊 DETAYLI PERFORMANS RAPORU")
        report.append("="*50)
        
        # Sistem bilgileri
        system_info = performance_monitor.get_system_info()
        report.append(f"\n🖥️ Sistem Bilgileri:")
        report.append(f"   CPU: {system_info.get('cpu_count', 'Bilinmiyor')} çekirdek")
        report.append(f"   RAM: {system_info.get('memory_total_gb', 0):.1f} GB")
        report.append(f"   Disk: %{system_info.get('disk_usage_percent', 0):.1f} kullanımda")
        
        # Operasyon istatistikleri
        stats = performance_monitor.get_all_stats()
        for operation_name, stat in stats.items():
            if stat:
                report.append(f"\n📈 {operation_name}:")
                report.append(f"   Çalıştırma: {stat['total_runs']} kez")
                report.append(f"   Başarı Oranı: %{(stat['successful_runs']/stat['total_runs']*100):.1f}")
                report.append(f"   Ortalama Süre: {stat['avg_duration']:.3f} saniye")
                report.append(f"   Toplam Süre: {stat['total_duration']:.3f} saniye")
                report.append(f"   Ortalama Bellek: {stat['avg_memory']:.2f} MB")
                report.append(f"   Son Çalıştırma: {stat['last_run'][:19] if stat['last_run'] else 'Bilinmiyor'}")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Rapor oluşturulurken hata: {e}"

# Test fonksiyonları
def run_performance_test():
    """Performans testi çalıştırır"""
    @monitor_performance("test_operation")
    def test_function():
        time.sleep(0.1)
        return "Test tamamlandı"
    
    print("🧪 Performans testi başlatılıyor...")
    for i in range(3):
        test_function()
    print("✅ Performans testi tamamlandı!")

if __name__ == "__main__":
    # Test çalıştır
    run_performance_test()
    print_performance_summary()
