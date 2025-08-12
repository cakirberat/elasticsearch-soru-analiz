#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elasticsearch 8.x Yapılandırma Dosyası
Bu dosya, Elasticsearch 8.12.1 sürümü için bağlantı ayarlarını içerir.
"""

from elasticsearch import Elasticsearch
import ssl

def create_elasticsearch_client(host="localhost", port=9200, use_ssl=False, username=None, password=None):
    """
    Elasticsearch 8.x için istemci oluşturur
    
    Args:
        host (str): Elasticsearch sunucu adresi
        port (int): Elasticsearch port numarası
        use_ssl (bool): SSL kullanılıp kullanılmayacağı
        username (str): Kullanıcı adı (eğer authentication varsa)
        password (str): Şifre (eğer authentication varsa)
    
    Returns:
        Elasticsearch: Yapılandırılmış Elasticsearch istemcisi
    """
    
    # Temel URL oluştur
    if use_ssl:
        url = f"https://{host}:{port}"
    else:
        url = f"http://{host}:{port}"
    
    # Bağlantı ayarları
    connection_config = {
        "hosts": [url],
        "verify_certs": False,  # SSL sertifika doğrulamasını devre dışı bırak
        "ssl_show_warn": False,  # SSL uyarılarını gizle
        "timeout": 30,  # 30 saniye timeout
        "max_retries": 3,  # Maksimum 3 deneme
        "retry_on_timeout": True,  # Timeout durumunda tekrar dene
    }
    
    # Eğer kullanıcı adı ve şifre verilmişse ekle
    if username and password:
        connection_config["basic_auth"] = (username, password)
    
    # Elasticsearch 8.x için özel ayarlar
    if use_ssl:
        # SSL bağlantısı için ek ayarlar
        connection_config.update({
            "ssl_context": ssl.create_default_context(),
            "ssl_context.check_hostname": False,
            "ssl_context.verify_mode": ssl.CERT_NONE,
        })
    
    try:
        es = Elasticsearch(**connection_config)
        
        # Bağlantıyı test et
        if es.ping():
            print(f"✅ Elasticsearch bağlantısı başarılı: {url}")
            return es
        else:
            print(f"❌ Elasticsearch bağlantısı başarısız: {url}")
            return None
            
    except Exception as e:
        print(f"❌ Elasticsearch bağlantı hatası: {e}")
        return None

def get_default_client():
    """
    Varsayılan Elasticsearch istemcisini döndürür
    """
    return create_elasticsearch_client()

def test_connection():
    """
    Elasticsearch bağlantısını test eder
    """
    print("🔍 Elasticsearch bağlantısı test ediliyor...")
    
    # HTTP bağlantısı dene
    print("1️⃣ HTTP bağlantısı deneniyor...")
    es_http = create_elasticsearch_client(use_ssl=False)
    
    if es_http:
        print("✅ HTTP bağlantısı başarılı!")
        return es_http
    
    # HTTPS bağlantısı dene
    print("2️⃣ HTTPS bağlantısı deneniyor...")
    es_https = create_elasticsearch_client(use_ssl=True)
    
    if es_https:
        print("✅ HTTPS bağlantısı başarılı!")
        return es_https
    
    print("❌ Hiçbir bağlantı yöntemi başarılı olmadı.")
    print("💡 Elasticsearch servisinin çalıştığından emin olun.")
    return None

if __name__ == "__main__":
    # Bağlantı testi
    client = test_connection()
    
    if client:
        # Cluster bilgilerini al
        info = client.info()
        print(f"\n📊 Elasticsearch Bilgileri:")
        print(f"   Sürüm: {info['version']['number']}")
        print(f"   Cluster: {info['cluster_name']}")
        print(f"   Node: {info['name']}")
        
        # İndeksleri listele
        indices = client.cat.indices(format='json')
        print(f"\n📁 Mevcut İndeksler:")
        for index in indices:
            print(f"   - {index['index']} (döküman sayısı: {index['docs.count']})")
