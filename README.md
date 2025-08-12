# 🎯 Soru Projesi - Arama ve Performans Sistemi

 Türkçe soru arama ve performans izleme sistemi. Elasticsearch 8.x veya Machine Learning (TF‑IDF + Cosine) ile benzer soruları bulur; tüm işlemlerin performansını ölçer ve tahmin eder.

## ✨ Özellikler

- 🔍 **Akıllı Soru Arama**: Elasticsearch ile benzer soruları bulma (Türkçe destekli)
- 🤖 **Machine Learning Analizi**: Geliştirilmiş TF‑IDF (1–3 n‑gram, L2, sublinear TF) + Cosine Similarity
- 🛑 **Stopwords Yönetimi**: Türkçe gereksiz kelimeleri filtreleme
- 📊 **Performans İzleme**: Gerçek zamanlı performans metrikleri
- 🖥️ **GUI Arayüzü**: Kullanıcı dostu grafik arayüz
- ⚡ **Hızlı Arama**: Optimize edilmiş arama algoritmaları
- 📈 **Detaylı Raporlama**: JSON formatında performans raporları
- 🔮 **Performans Tahmini**: Gelecekteki performansı tahmin etme
- 🎯 **Çift Analiz Yöntemi**: Elasticsearch veya ML seçimi

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

### Manuel Kullanım (Komut Satırı)
```bash
# GUI Uygulaması (Elasticsearch + ML seçimi)
python gui.py

# Elasticsearch testi
python es_test.py

# ML Analiz testi
python ml_analyzer.py

# Performans testi
python performance_test.py

# Performans tahmini
python performance_analyzer.py
```

### Python API Örnekleri
```python
# Elasticsearch ile arama
from es_search import benzer_sorulari_bul
benzer_sorulari_bul("Python programlama nasıl öğrenilir?", esik=0.75)

# Machine Learning ile arama
from ml_analyzer import MLAnalyzer
analyzer = MLAnalyzer()
analyzer.load_questions_from_db()
analyzer.clean_questions()
analyzer.train_model()
results = analyzer.find_similar_questions_ml("Python programlama nasıl öğrenilir?", top_k=5)
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

GUI’de Performans Tahmini penceresine girilen sayı artık farklı formatlarda kabul edilir (örn: `10.000`, `10,000`, `10000`).

## 🏗️ Proje Yapısı

```
soru-projesi/
├── 📁 main_control.py           # 🎯 Ana Kontrol Paneli
├── 📁 gui.py                    # Ana GUI uygulaması (ES + ML)
├── 📁 es_search.py              # Elasticsearch arama fonksiyonları
│   └── `refresh_stopwords()`    # GUI'den güncellenen stopwords'leri yeniden yükler
├── 📁 es_config.py              # Elasticsearch 8.x yapılandırması
├── 📁 es_test.py                # Elasticsearch test scripti
├── 📁 ml_analyzer.py            # 🤖 Machine Learning analiz modülü
├── 📁 performance_monitor.py    # Performans izleme sistemi
├── 📁 performance_analyzer.py   # Performans analizi ve tahmin
├── 📁 performance_test.py       # Performans test scripti
├── 📁 requirements.txt          # Gerekli paketler
├── 📁 README.md                 # Bu dosya
└── 📁 stopwords.txt             # Türkçe stopwords listesi
```

## 🔧 Yapılandırma

### Elasticsearch Ayarları (es_config.py)
`es_config.py` dosyasında Elasticsearch bağlantı ayarlarını değiştirebilirsiniz:

```python
# Varsayılan ayarlar
HOST = "localhost"
PORT = 9200
USE_SSL = False
TIMEOUT = 30
```

### Stopwords Yönetimi
- GUI üzerinden ekle/sil → anında etkili (ES temizleyici `refresh_stopwords()` ile güncellenir)
- Dosya: `stopwords.txt`

### ML Kalite İyileştirmeleri
- Noktalama temizleme + küçük harf + kök/stopsuz temizlik
- TF‑IDF ayarları: n‑gram(1–3), L2 norm, sublinear TF, max_features=5000
- Model yüklenince mevcut korpusa göre TF‑IDF matrisi yeniden oluşturulur


## 📈 Performans Optimizasyonu

### Önerilen Ayarlar
- **Elasticsearch**: Yerel kurulum kullanın
- **Bellek**: En az 2GB RAM ayırın
- **İndeksleme**: Düzenli indeks bakımı yapın

### Tipik Performans Değerleri
- Stopword Temizleme: `0.001-0.005 saniye`
- Elasticsearch Arama: `0.1-2.0 saniye`
- GUI Yanıt Süresi: `<1 saniye`
