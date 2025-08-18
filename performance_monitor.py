import time
import functools
import psutil
import os
from datetime import datetime
import json

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.start_time = None
        self.process = psutil.Process()
    
    def start_monitoring(self, operation_name):
        """Bir işlemin performans izlemesini başlatır"""
        self.start_time = time.time()
        initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        initial_cpu = self.process.cpu_percent()
        
        return {
            'start_time': self.start_time,
            'initial_memory': initial_memory,
            'initial_cpu': initial_cpu,
            'operation_name': operation_name
        }
    
    def end_monitoring(self, monitoring_data):
        """Bir işlemin performans izlemesini sonlandırır ve sonuçları kaydeder"""
        end_time = time.time()
        duration = end_time - monitoring_data['start_time']
        
        final_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        final_cpu = self.process.cpu_percent()
        
        memory_used = final_memory - monitoring_data['initial_memory']
        cpu_used = final_cpu - monitoring_data['initial_cpu']
        
        operation_name = monitoring_data['operation_name']
        
        if operation_name not in self.metrics:
            self.metrics[operation_name] = []
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'memory_used_mb': memory_used,
            'cpu_used_percent': cpu_used,
            'total_memory_mb': final_memory
        }
        
        self.metrics[operation_name].append(result)
        return result
    
    def monitor_function(self, operation_name=None):
        """Fonksiyon performansını izlemek için decorator"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                op_name = operation_name or func.__name__
                monitoring_data = self.start_monitoring(op_name)
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    self.end_monitoring(monitoring_data)
            return wrapper
        return decorator
    
    def get_statistics(self, operation_name=None):
        """Belirli bir işlem veya tüm işlemler için istatistikleri döndürür"""
        if operation_name:
            if operation_name not in self.metrics:
                return None
            
            durations = [m['duration_seconds'] for m in self.metrics[operation_name]]
            memories = [m['memory_used_mb'] for m in self.metrics[operation_name]]
            
            return {
                'operation': operation_name,
                'count': len(durations),
                'avg_duration': sum(durations) / len(durations),
                'min_duration': min(durations),
                'max_duration': max(durations),
                'avg_memory': sum(memories) / len(memories),
                'total_duration': sum(durations)
            }
        else:
            stats = {}
            for op_name in self.metrics:
                stats[op_name] = self.get_statistics(op_name)
            return stats
    
    def print_summary(self):
        """Tüm performans metriklerinin özetini yazdırır"""
        print("\n" + "="*60)
        print("PERFORMANS ÖZETİ")
        print("="*60)
        
        if not self.metrics:
            print("\n❌ Henüz hiçbir performans verisi toplanmamış.")
            print("   Performans verisi toplamak için test işlemleri yapın.")
            print("\n" + "="*60)
            return
        
        has_data = False
        for operation_name, measurements in self.metrics.items():
            if measurements:
                has_data = True
                durations = [m['duration_seconds'] for m in measurements]
                memories = [m['memory_used_mb'] for m in measurements]
                
                print(f"\n📊 {operation_name.upper()}:")
                print(f"   Çalıştırma sayısı: {len(measurements)}")
                print(f"   Ortalama süre: {sum(durations)/len(durations):.3f} saniye")
                print(f"   En hızlı: {min(durations):.3f} saniye")
                print(f"   En yavaş: {max(durations):.3f} saniye")
                print(f"   Toplam süre: {sum(durations):.3f} saniye")
                print(f"   Ortalama bellek kullanımı: {sum(memories)/len(memories):.2f} MB")
        
        if not has_data:
            print("\n❌ Hiçbir işlem tamamlanmamış.")
            print("   Performans verisi toplamak için test işlemleri yapın.")
        
        print("\n" + "="*60)
    
    def save_metrics(self, filename="performance_metrics.json"):
        """Metrikleri JSON dosyasına kaydeder"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        print(f"Performans metrikleri {filename} dosyasına kaydedildi.")

# Global performans izleyici
performance_monitor = PerformanceMonitor()

def monitor_performance(operation_name=None):
    """Fonksiyon performansını izlemek için basit decorator"""
    return performance_monitor.monitor_function(operation_name)

def print_performance_summary():
    """Performans özetini yazdırır"""
    performance_monitor.print_summary()

def save_performance_metrics(filename="performance_metrics.json"):
    """Performans metriklerini kaydeder"""
    performance_monitor.save_metrics(filename)
