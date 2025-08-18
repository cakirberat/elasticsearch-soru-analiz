#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merkezi Hata Yönetimi Sistemi
Bu modül, uygulama genelinde hata yönetimini sağlar.
"""

import traceback
import logging
import os
from datetime import datetime
from typing import Optional, Callable, Any
import tkinter as tk
from tkinter import messagebox

class ErrorHandler:
    """Merkezi hata yönetimi sınıfı"""
    
    def __init__(self, log_file="error_log.txt"):
        self.log_file = log_file
        self.error_count = 0
        self.last_error_time = None
        
        # Logging ayarları
        logging.basicConfig(
            filename=log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        
        # Hata türleri ve açıklamaları
        self.error_types = {
            'FileNotFoundError': 'Dosya bulunamadı',
            'PermissionError': 'Dosya erişim izni yok',
            'ConnectionError': 'Bağlantı hatası',
            'TimeoutError': 'Zaman aşımı hatası',
            'ValueError': 'Geçersiz değer hatası',
            'TypeError': 'Veri türü hatası',
            'KeyError': 'Anahtar bulunamadı',
            'IndexError': 'Dizin hatası',
            'ImportError': 'Modül yükleme hatası',
            'ModuleNotFoundError': 'Modül bulunamadı',
            'AttributeError': 'Özellik bulunamadı',
            'NameError': 'Değişken bulunamadı',
            'SyntaxError': 'Sözdizimi hatası',
            'IndentationError': 'Girinti hatası',
            'ZeroDivisionError': 'Sıfıra bölme hatası',
            'OverflowError': 'Taşma hatası',
            'MemoryError': 'Bellek yetersiz',
            'OSError': 'İşletim sistemi hatası',
            'IOError': 'Giriş/çıkış hatası',
            'UnicodeError': 'Karakter kodlama hatası',
            'RecursionError': 'Özyineleme hatası',
            'AssertionError': 'Doğrulama hatası',
            'NotImplementedError': 'Uygulanmamış özellik',
            'RuntimeError': 'Çalışma zamanı hatası',
            'SystemError': 'Sistem hatası',
            'KeyboardInterrupt': 'Kullanıcı kesintisi',
            'Exception': 'Genel hata'
        }
    
    def handle_error(self, error: Exception, context: str = "", show_message: bool = True) -> dict:
        """Hatayı işler ve loglar"""
        try:
            error_info = {
                'timestamp': datetime.now().isoformat(),
                'error_type': type(error).__name__,
                'error_message': str(error),
                'context': context,
                'traceback': traceback.format_exc()
            }
            
            # Hata sayısını artır
            self.error_count += 1
            self.last_error_time = datetime.now()
            
            # Hatayı logla
            logging.error(f"Context: {context} | Error: {error_info['error_type']} | Message: {error_info['error_message']}")
            logging.error(f"Traceback: {error_info['traceback']}")
            
            # Kullanıcıya mesaj göster
            if show_message:
                self._show_error_message(error_info)
            
            return error_info
            
        except Exception as e:
            # Hata yönetimi sırasında hata oluşursa
            print(f"Hata yönetimi sırasında hata: {e}")
            return {'error': 'Hata yönetimi başarısız'}
    
    def _show_error_message(self, error_info: dict):
        """Kullanıcıya hata mesajı gösterir"""
        try:
            error_type = error_info['error_type']
            error_message = error_info['error_message']
            context = error_info['context']
            
            # Hata türüne göre açıklama
            error_description = self.error_types.get(error_type, 'Bilinmeyen hata')
            
            # Kullanıcı dostu mesaj
            user_message = f"❌ {error_description}\n\n"
            user_message += f"📝 Detay: {error_message}\n\n"
            
            if context:
                user_message += f"📍 Konum: {context}\n\n"
            
            user_message += "💡 Bu hata otomatik olarak loglanmıştır.\n"
            user_message += "   Teknik destek için log dosyasını kontrol edin."
            
            # Mesaj kutusu göster
            messagebox.showerror("Hata", user_message)
            
        except Exception as e:
            # GUI hatası durumunda konsola yazdır
            print(f"Hata mesajı gösterilemedi: {e}")
            print(f"Orijinal hata: {error_info}")
    
    def safe_execute(self, func: Callable, *args, context: str = "", 
                    default_return: Any = None, **kwargs) -> Any:
        """Fonksiyonu güvenli şekilde çalıştırır"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle_error(e, context)
            return default_return
    
    def async_safe_execute(self, func: Callable, *args, context: str = "", 
                          default_return: Any = None, **kwargs) -> Any:
        """Asenkron fonksiyonu güvenli şekilde çalıştırır"""
        try:
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return asyncio.run(func(*args, **kwargs))
            else:
                return func(*args, **kwargs)
        except Exception as e:
            self.handle_error(e, context)
            return default_return
    
    def validate_file_path(self, file_path: str, context: str = "") -> bool:
        """Dosya yolunu doğrular"""
        try:
            if not file_path:
                raise ValueError("Dosya yolu boş olamaz")
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
            
            if not os.access(file_path, os.R_OK):
                raise PermissionError(f"Dosya okuma izni yok: {file_path}")
            
            return True
            
        except Exception as e:
            self.handle_error(e, f"{context} - Dosya doğrulama")
            return False
    
    def validate_directory(self, dir_path: str, context: str = "") -> bool:
        """Dizin yolunu doğrular"""
        try:
            if not dir_path:
                raise ValueError("Dizin yolu boş olamaz")
            
            if not os.path.exists(dir_path):
                raise FileNotFoundError(f"Dizin bulunamadı: {dir_path}")
            
            if not os.path.isdir(dir_path):
                raise NotADirectoryError(f"Geçerli bir dizin değil: {dir_path}")
            
            if not os.access(dir_path, os.R_OK | os.W_OK):
                raise PermissionError(f"Dizin erişim izni yok: {dir_path}")
            
            return True
            
        except Exception as e:
            self.handle_error(e, f"{context} - Dizin doğrulama")
            return False
    
    def validate_input(self, value: Any, expected_type: type, context: str = "") -> bool:
        """Giriş değerini doğrular"""
        try:
            if not isinstance(value, expected_type):
                raise TypeError(f"Beklenen tür: {expected_type.__name__}, Alınan: {type(value).__name__}")
            
            return True
            
        except Exception as e:
            self.handle_error(e, f"{context} - Giriş doğrulama")
            return False
    
    def get_error_summary(self) -> dict:
        """Hata özeti döndürür"""
        try:
            return {
                'total_errors': self.error_count,
                'last_error_time': self.last_error_time.isoformat() if self.last_error_time else None,
                'log_file': self.log_file,
                'log_file_exists': os.path.exists(self.log_file),
                'log_file_size': os.path.getsize(self.log_file) if os.path.exists(self.log_file) else 0
            }
        except Exception as e:
            return {'error': f'Hata özeti alınamadı: {e}'}
    
    def clear_error_log(self) -> bool:
        """Hata logunu temizler"""
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
                self.error_count = 0
                self.last_error_time = None
                return True
            return False
        except Exception as e:
            self.handle_error(e, "Log temizleme")
            return False
    
    def get_recent_errors(self, count: int = 10) -> list:
        """Son hataları döndürür"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Son hataları al
            recent_errors = []
            for line in reversed(lines):
                if 'ERROR' in line and len(recent_errors) < count:
                    recent_errors.append(line.strip())
            
            return recent_errors
            
        except Exception as e:
            self.handle_error(e, "Son hataları alma")
            return []

# Global hata yöneticisi
error_handler = ErrorHandler()

def handle_error(error: Exception, context: str = "", show_message: bool = True) -> dict:
    """Global hata işleme fonksiyonu"""
    return error_handler.handle_error(error, context, show_message)

def safe_execute(func: Callable, *args, context: str = "", 
                default_return: Any = None, **kwargs) -> Any:
    """Global güvenli çalıştırma fonksiyonu"""
    return error_handler.safe_execute(func, *args, context=context, 
                                    default_return=default_return, **kwargs)

def validate_file_path(file_path: str, context: str = "") -> bool:
    """Global dosya yolu doğrulama"""
    return error_handler.validate_file_path(file_path, context)

def validate_directory(dir_path: str, context: str = "") -> bool:
    """Global dizin doğrulama"""
    return error_handler.validate_directory(dir_path, context)

def validate_input(value: Any, expected_type: type, context: str = "") -> bool:
    """Global giriş doğrulama"""
    return error_handler.validate_input(value, expected_type, context)

# Decorator'lar
def error_safe(func: Callable) -> Callable:
    """Fonksiyonu hata güvenli hale getiren decorator"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler.handle_error(e, f"Function: {func.__name__}")
            return None
    return wrapper

def input_validator(*validators: Callable) -> Callable:
    """Giriş doğrulama decorator'ı"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                # Girişleri doğrula
                for validator in validators:
                    if not validator(*args, **kwargs):
                        raise ValueError("Giriş doğrulama başarısız")
                
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.handle_error(e, f"Input validation for: {func.__name__}")
                return None
        return wrapper
    return decorator

# Test fonksiyonları
def test_error_handler():
    """Hata yöneticisini test eder"""
    print("🧪 Hata yöneticisi test ediliyor...")
    
    # Dosya bulunamadı hatası
    try:
        with open("nonexistent_file.txt", "r") as f:
            pass
    except Exception as e:
        error_handler.handle_error(e, "Test - Dosya okuma")
    
    # Sıfıra bölme hatası
    try:
        result = 10 / 0
    except Exception as e:
        error_handler.handle_error(e, "Test - Matematik işlemi")
    
    # Tip hatası
    try:
        result = "string" + 123
    except Exception as e:
        error_handler.handle_error(e, "Test - Tip işlemi")
    
    print("✅ Hata yöneticisi testi tamamlandı!")

if __name__ == "__main__":
    test_error_handler()
    print("\n📊 Hata özeti:")
    print(error_handler.get_error_summary())
