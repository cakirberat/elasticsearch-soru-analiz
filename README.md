# 🎯 Soru Projesi - Performans İzleme Sistemi

Türkçe soru arama ve performans izleme sistemi. Elasticsearch 8.x kullanarak benzer soruları bulur ve tüm işlemlerin performansını detaylı olarak ölçer.

## ✨ Özellikler

- 🔍 **Akıllı Soru Arama**: Elasticsearch ile benzer soruları bulma
- 🛑 **Stopwords Yönetimi**: Türkçe gereksiz kelimeleri filtreleme
- 📊 **Performans İzleme**: Gerçek zamanlı performans metrikleri
- 🖥️ **GUI Arayüzü**: Kullanıcı dostu grafik arayüz
- ⚡ **Hızlı Arama**: Optimize edilmiş arama algoritmaları
- 📈 **Detaylı Raporlama**: JSON formatında performans raporları
- 🔮 **Performans Tahmini**: Gelecekteki performansı tahmin etme

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- Elasticsearch 8.12.1
- Windows/Linux/macOS

### Kurulum

1. **Projeyi klonlayın**
```bash
git clone https://github.com/kullaniciadi/soru-projesi.git
cd soru-projesi
```

2. **Gerekli paketleri yükleyin**
```bash
pip install -r requirements.txt
```

3. **Elasticsearch'i başlatın**
```bash
# Elasticsearch servisinin çalıştığından emin olun
# Varsayılan: http://localhost:9200
```

## 📖 Kullanım

### 🎯 Ana Kontrol Paneli (Önerilen)
```bash
python main_control.py
```

**Tüm proje bileşenlerini tek yerden yönetin:**
- 🖥️ GUI Uygulaması
- 🔍 Elasticsearch Test
- ⚡ Performans Test
- 🔮 Performans Tahmini
- 📊 Sistem Durumu Kontrolü
- 📋 Gerçek Zamanlı Loglar

### Manuel Kullanım
```bash
# GUI Uygulaması
python gui.py

# Elasticsearch testi
python es_test.py

# Performans testi
python performance_test.py

# Performans tahmini
python performance_analyzer.py
```

### Manuel Kullanım
```python
from es_search import benzer_sorulari_bul

# Soru arama
benzer_sorulari_bul("Python programlama nasıl öğrenilir?", esik=0.75)
```

## 📊 Performans İzleme

Sistem otomatik olarak şu metrikleri toplar:

| Metrik | Açıklama |
|--------|----------|
| ⏱️ **Süre** | İşlem tamamlanma süresi (saniye) |
| 💾 **Bellek** | Kullanılan bellek miktarı (MB) |
| 🔥 **CPU** | İşlemci kullanım oranı (%) |
| 🔢 **Çalıştırma** | İşlem çalıştırma sayısı |

### Performans Özeti Görüntüleme
```python
from performance_monitor import print_performance_summary
print_performance_summary()
```

### Performans Tahmini
```python
from performance_analyzer import PerformanceAnalyzer

analyzer = PerformanceAnalyzer()
predictions = analyzer.interactive_prediction()
```

## 🏗️ Proje Yapısı

```
soru-projesi/
├── 📁 main_control.py           # 🎯 Ana Kontrol Paneli
├── 📁 gui.py                    # Ana GUI uygulaması
├── 📁 es_search.py              # Elasticsearch arama fonksiyonları
├── 📁 es_config.py              # Elasticsearch 8.x yapılandırması
├── 📁 es_test.py                # Elasticsearch test scripti
├── 📁 performance_monitor.py    # Performans izleme sistemi
├── 📁 performance_analyzer.py   # Performans analizi ve tahmin
├── 📁 performance_test.py       # Performans test scripti
├── 📁 requirements.txt          # Gerekli paketler
├── 📁 README.md                 # Bu dosya
└── 📁 stopwords.txt             # Türkçe stopwords listesi
```

## 🔧 Yapılandırma

### Elasticsearch Ayarları
`es_config.py` dosyasında Elasticsearch bağlantı ayarlarını değiştirebilirsiniz:

```python
# Varsayılan ayarlar
HOST = "localhost"
PORT = 9200
USE_SSL = False
TIMEOUT = 30
```

### Stopwords Yönetimi
GUI üzerinden veya dosya düzenleyerek stopwords ekleyebilir/çıkarabilirsiniz:


## 📈 Performans Optimizasyonu

### Önerilen Ayarlar
- **Elasticsearch**: Yerel kurulum kullanın
- **Bellek**: En az 2GB RAM ayırın
- **İndeksleme**: Düzenli indeks bakımı yapın

### Tipik Performans Değerleri
- Stopword Temizleme: `0.001-0.005 saniye`
- Elasticsearch Arama: `0.1-2.0 saniye`
- GUI Yanıt Süresi: `<1 saniye`
