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


## 📊 Performans İzleme

Sistem otomatik olarak şu metrikleri toplar:

| Metrik | Açıklama |
|--------|----------|
| ⏱️ **Süre** | İşlem tamamlanma süresi (saniye) |
| 💾 **Bellek** | Kullanılan bellek miktarı (MB) |
| 🔥 **CPU** | İşlemci kullanım oranı (%) |
| 🔢 **Çalıştırma** | İşlem çalıştırma sayısı |

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



