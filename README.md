# 🎯 Soru Projesi - Gelişmiş Soru Arama ve Analiz Sistemi

Bu proje, Türkçe soru arama ve analiz işlemleri için geliştirilmiş kapsamlı bir sistemdir. Elasticsearch ve Makine Öğrenmesi teknolojilerini kullanarak benzer soruları bulma, performans izleme ve analiz özellikleri sunar.


### 📊 Performans ve Analiz
- **Gerçek Zamanlı İzleme**: CPU, bellek ve disk kullanımı takibi
- **Detaylı Raporlama**: Performans verilerinin kapsamlı analizi
- **Gelecek Tahminleri**: Sistem performansının gelecekteki durumu hakkında tahminler
- **Metrik Dışa Aktarma**: Performans verilerinin JSON formatında kaydedilmesi
- **ML Model Test Sistemi**: Kapsamlı makine öğrenmesi test ve analiz araçları

## 🛠️ Kurulum

### Gereksinimler
```bash
Python 3.8+
Elasticsearch 7.x+
```

### Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### Elasticsearch Kurulumu
1. Elasticsearch'i indirin ve kurun
2. `es_config.py` dosyasını çalıştırarak bağlantıyı test edin
3. Gerekirse bağlantı ayarlarını düzenleyin

## 🎮 Kullanım

### Ana Kontrol Paneli
```bash
python main_control.py
```

Ana kontrol paneli şu özellikleri sunar:

#### 📱 Ana Uygulamalar
- **🖥️ GUI Uygulaması**: Ana soru arama arayüzü

#### 🧪 Test ve Analiz
- **🔧 Elasticsearch Bağlantı**: Bağlantı testi ve yapılandırma
- **🤖 ML Test Sistemi**: Makine öğrenmesi modellerini test etme
- **⚡ Hızlı Performans Testi**: Sistem performansını hızlıca test etme
- **📊 Performans Özeti**: Toplanan performans verilerinin özeti
- **💾 Metrikleri Kaydet**: Performans verilerini dosyaya kaydetme

#### 📈 Sistem Durumu
- **🔄 Durumu Kontrol Et**: Sistem durumu raporu
- **🧹 Tüm İşlemleri Durdur**: Çalışan işlemleri güvenli şekilde durdurma
- **⚙️ Ayarlar**: Program ayarlarını düzenleme

### GUI Uygulaması
```bash
python gui.py
```

GUI uygulaması şu özellikleri içerir:

#### 🔍 Soru Arama
- **Elasticsearch Analizi**: Elasticsearch tabanlı benzer soru arama
- **Machine Learning Analizi**: ML tabanlı benzer soru arama (TF-IDF + Cosine Similarity)
- **Eşik Değeri Ayarlama**: Arama hassasiyetini ayarlama (0.01 - 1.0 arası)
- **Gerçek Zamanlı Arama**: Thread tabanlı asenkron arama
- **Akıllı Benzerlik Hesaplama**: Gelişmiş metin analizi ve benzerlik skorlama

#### 📝 Stopwords Yönetimi
- **Stopword Ekleme/Silme**: Türkçe stopwords listesini yönetme
- **Arama ve Filtreleme**: Stopwords listesinde arama yapma
- **Otomatik Kaydetme**: Değişikliklerin otomatik kaydedilmesi

#### 📊 Performans İzleme
- **Performans Özeti**: Sistem performansının detaylı özeti
- **Metrik Kaydetme**: Performans verilerini JSON formatında kaydetme
- **Performans Tahmini**: Gelecekteki performans hakkında tahminler

## 📁 Proje Yapısı

```
soru_projesi/
├── main_control.py          # Ana kontrol paneli
├── gui.py                   # GUI uygulaması
├── es_search.py             # Elasticsearch arama fonksiyonları
├── ml_analyzer.py           # Makine öğrenmesi analizi
├── performance_monitor.py   # Performans izleme sistemi
├── performance_analyzer.py  # Performans analizi ve tahmin
├── error_handler.py         # Merkezi hata yönetimi
├── es_config.py             # Elasticsearch yapılandırması
├── ml_test.py               # ML test sistemi
├── requirements.txt         # Python bağımlılıkları
├── sorular.db               # SQLite veritabanı
├── stopwords.txt            # Türkçe stopwords listesi
└── README.md               # Bu dosya
```

## 🔧 Yapılandırma

### Kullanıcı Ayarları
Program ayarları `user_settings.json` dosyasında saklanır:

```json
{
  "auto_save_metrics": true,
  "show_tooltips": true,
  "max_log_lines": 1000
}
```

### Elasticsearch Yapılandırması
`es_config.py` dosyasında Elasticsearch bağlantı ayarları:

```python
ELASTICSEARCH_HOST = "localhost"
ELASTICSEARCH_PORT = 9200
INDEX_NAME = "sorular"
```

## 📊 Performans İzleme

### Metrikler
Sistem şu performans metriklerini toplar:
- **İşlem Süreleri**: Her operasyonun çalışma süresi
- **Bellek Kullanımı**: RAM kullanım miktarı
- **CPU Kullanımı**: İşlemci kullanım yüzdesi
- **Başarı Oranları**: İşlemlerin başarılı/başarısız oranları

### Raporlama
Performans verileri şu formatlarda raporlanır:
- **Konsol Çıktısı**: Anlık performans özeti
- **JSON Dosyası**: Detaylı metrik verileri
- **Grafik Raporlar**: Görsel performans analizi

## 🛡️ Hata Yönetimi

### Merkezi Hata Sistemi
- **Otomatik Loglama**: Tüm hatalar otomatik olarak loglanır
- **Kullanıcı Dostu Mesajlar**: Teknik detaylar gizlenir
- **Hata Kategorileri**: Hata türlerine göre sınıflandırma
- **Geri Bildirim**: Kullanıcıya anlaşılır hata açıklamaları

### Hata Türleri
- **Dosya İşlemleri**: Dosya okuma/yazma hataları
- **Bağlantı Hataları**: Ağ ve veritabanı bağlantı sorunları
- **Veri Doğrulama**: Giriş verilerinin doğrulanması
- **Sistem Hataları**: İşletim sistemi seviyesi sorunlar


**🎯 Soru Projesi** - Türkçe soru arama ve analiz sisteminin en gelişmiş versiyonu!

## 🔧 Teknik Detaylar

### Makine Öğrenmesi Altyapısı
- **TF-IDF Vectorizer**: Metin vektörize etme
- **Cosine Similarity**: Benzerlik hesaplama
- **N-gram Analizi**: 1-3 gram arası kelime grupları
- **Stopwords Filtreleme**: Türkçe stopwords desteği
- **Model Persistence**: Eğitilmiş modellerin kaydedilmesi

### Performans Optimizasyonları
- **Thread-Safe Operations**: Çoklu işlem desteği
- **Memory Management**: Bellek kullanımı optimizasyonu
- **Caching**: Model ve veri önbellekleme
- **Error Recovery**: Hata durumlarında otomatik kurtarma



