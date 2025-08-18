#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ana Kontrol Paneli - Soru Projesi
Bu dosya, projenin tüm bileşenlerini tek bir menüden çalıştırmanızı sağlar.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
import threading
import time
from datetime import datetime
import json

class Tooltip:
    """Tooltip sınıfı - butonlara açıklayıcı ipuçları ekler"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, 
                        bg="#ffffe0", relief="solid", borderwidth=1,
                        font=("Arial", 9), padx=5, pady=3)
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class MainControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Soru Projesi - Ana Kontrol Paneli")
        self.root.configure(bg="#f0f4f8")
        self.root.geometry("1000x750")
        
        # Çalışan işlemler
        self.running_processes = {}
        
        # Durum değişkenleri
        self.system_status = "🟢 Sistem Hazır"
        self.last_update = datetime.now().strftime("%H:%M:%S")
        
        # Ayarları yükle
        self.load_settings()
        
        self.setup_ui()
        self.update_status()
        
    def cleanup_json_files(self):
        """Eski JSON tahmin dosyalarını temizler (son 14 günden eski olanları ve en yeni 10 dosya dışındakileri siler)."""
        try:
            # Tutma politikası
            retention_days = 14
            max_keep = 10

            # Çalışma dizininde tarihe göre isimlenen dosyaları bul
            files = [f for f in os.listdir('.') if f.startswith('performance_prediction_') and f.endswith('.json')]
            files_full = [
                (f, os.path.getmtime(f))
                for f in files
                if os.path.isfile(f)
            ]

            if not files_full:
                messagebox.showinfo("Bilgi", "Temizlenecek JSON dosyası bulunamadı.")
                return

            # Tarihe göre yeni->eski sırala
            files_full.sort(key=lambda x: x[1], reverse=True)

            # En yeni max_keep dosyayı koru, diğer adayları değerlendir
            to_consider = files_full[max_keep:]

            # Gün eşiği
            cutoff = time.time() - (retention_days * 86400)
            deleted = 0
            for fname, mtime in to_consider:
                if mtime < cutoff:
                    try:
                        os.remove(fname)
                        deleted += 1
                    except Exception as e:
                        self.log_message(f"{fname} silinirken hata: {e}", "ERROR")

            self.log_message(f"JSON temizlik tamamlandı. Silinen dosya: {deleted}", "SUCCESS")
            messagebox.showinfo("Tamamlandı", f"Temizlik tamamlandı. Silinen dosya: {deleted}")

        except Exception as e:
            self.log_message(f"JSON temizlik hatası: {e}", "ERROR")
            messagebox.showerror("Hata", f"JSON dosyaları temizlenirken hata oluştu:\n{e}")

    def load_settings(self):
        """Kullanıcı ayarlarını yükler"""
        try:
            if os.path.exists("user_settings.json"):
                with open("user_settings.json", "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
            else:
                self.settings = {
                    "auto_save_metrics": True,
                    "show_tooltips": True,
                    "max_log_lines": 1000
                }
        except Exception as e:
            self.settings = {
                "auto_save_metrics": True,
                "show_tooltips": True,
                "max_log_lines": 1000
            }
    
    def save_settings(self):
        """Kullanıcı ayarlarını kaydeder"""
        try:
            with open("user_settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log_message(f"Ayarlar kaydedilirken hata: {e}", "ERROR")
        
    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        # Ana başlık
        title = tk.Label(self.root, text="🎯 Soru Projesi - Ana Kontrol Paneli", 
                        font=("Arial", 20, "bold"), fg="#2a5298", bg="#f0f4f8")
        title.pack(pady=(20, 10))
        
        # Durum çubuğu
        self.status_frame = tk.Frame(self.root, bg="#e8f4fd", height=30)
        self.status_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame, text=self.system_status, 
                                   font=("Arial", 10), fg="#2a5298", bg="#e8f4fd")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.update_label = tk.Label(self.status_frame, text=f"Son güncelleme: {self.last_update}", 
                                   font=("Arial", 9), fg="#666", bg="#e8f4fd")
        self.update_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Ana frame
        main_frame = tk.Frame(self.root, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sol panel - Butonlar
        left_panel = tk.Frame(main_frame, bg="#f0f4f8", width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Sağ panel - Log alanı
        right_panel = tk.Frame(main_frame, bg="#f0f4f8")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_buttons(left_panel)
        self.create_log_area(right_panel)
        

        
    def create_buttons(self, parent):
        """Butonları oluşturur"""
        # Başlık
        tk.Label(parent, text="🚀 Hızlı Başlat", font=("Arial", 14, "bold"), 
                fg="#2a5298", bg="#f0f4f8").pack(pady=(0, 15))
        
        # Ana uygulamalar
        self.create_section(parent, "📱 Ana Uygulamalar", [
            ("🖥️ GUI Uygulaması", self.start_gui, "#2a5298", 
             "Ana soru arama uygulamasını başlatır. Elasticsearch ve ML analizi yapabilirsiniz.")
        ])
        
        # Test ve analiz
        self.create_section(parent, "🧪 Test ve Analiz", [
            ("🔧 Elasticsearch Bağlantı", self.start_es_config, "#27ae60",
             "Elasticsearch bağlantısını test eder ve yapılandırır."),
            ("🤖 ML Test Sistemi", self.start_ml_test_system, "#e74c3c",
             "Makine öğrenmesi modellerini test eder ve performansını ölçer."),
            ("⚡ Hızlı Performans Testi", self.quick_performance_test, "#e67e22",
             "Sistem performansını hızlıca test eder ve veri toplar."),
            ("📊 Performans Özeti", self.show_performance_summary, "#8e44ad",
             "Toplanan performans verilerinin detaylı özetini gösterir."),
            ("💾 Metrikleri Kaydet", self.save_metrics, "#f39c12",
             "Performans metriklerini JSON dosyasına kaydeder.")
        ])
        
        # Sistem durumu
        self.create_section(parent, "📈 Sistem Durumu", [
            ("🔄 Durumu Kontrol Et", self.check_system_status, "#16a085",
             "Sistem durumunu kontrol eder ve raporlar."),
            ("🧹 Tüm İşlemleri Durdur", self.stop_all_processes, "#c0392b",
             "Çalışan tüm işlemleri güvenli şekilde durdurur."),
            ("🧽 JSON Dosyalarını Temizle", self.cleanup_json_files, "#7f8c8d",
             "Eski performans tahmin JSON dosyalarını temizler."),
            ("⚙️ Ayarlar", self.show_settings, "#34495e",
             "Program ayarlarını düzenler.")
        ])
        
        # Çıkış
        exit_button = tk.Button(parent, text="❌ Çıkış", command=self.safe_exit,
                               bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                               width=25, height=2, activebackground="#c0392b")
        exit_button.pack(pady=(20, 0))
        
        if self.settings.get("show_tooltips", True):
            Tooltip(exit_button, "Programı güvenli şekilde kapatır ve ayarları kaydeder.")
        
    def create_section(self, parent, title, buttons):
        """Bölüm oluşturur"""
        # Bölüm başlığı
        tk.Label(parent, text=title, font=("Arial", 12, "bold"), 
                fg="#333", bg="#f0f4f8").pack(pady=(15, 10), anchor=tk.W)
        
        # Butonlar
        for text, command, color, tooltip in buttons:
            btn = tk.Button(parent, text=text, command=command,
                           bg=color, fg="white", font=("Arial", 10, "bold"),
                           width=30, height=2, activebackground=color,
                           cursor="hand2")
            btn.pack(pady=2)
            
            if self.settings.get("show_tooltips", True):
                Tooltip(btn, tooltip)
            
    def create_log_area(self, parent):
        """Log alanını oluşturur"""
        # Başlık ve kontroller
        header_frame = tk.Frame(parent, bg="#f0f4f8")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text="📋 Sistem Logları", font=("Arial", 12, "bold"), 
                fg="#2a5298", bg="#f0f4f8").pack(side=tk.LEFT)
        
        # Log kontrolleri
        clear_btn = tk.Button(header_frame, text="🗑️ Temizle", command=self.clear_logs,
                             bg="#e74c3c", fg="white", font=("Arial", 9, "bold"),
                             activebackground="#c0392b")
        clear_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        save_btn = tk.Button(header_frame, text="💾 Kaydet", command=self.save_logs,
                            bg="#27ae60", fg="white", font=("Arial", 9, "bold"),
                            activebackground="#229954")
        save_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Log alanı
        self.log_text = scrolledtext.ScrolledText(parent, width=60, height=25, 
                                                font=("Consolas", 10), bg="#e3f2fd", 
                                                fg="#222", borderwidth=2, relief="groove")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Başlangıç mesajı
        self.log_message("🎯 Soru Projesi Ana Kontrol Paneli başlatıldı", "INFO")
        self.log_message("Sistem hazır, işlemlerinizi başlatabilirsiniz.", "INFO")
        
    def update_status(self):
        """Durum bilgilerini günceller"""
        try:
            # Çalışan işlem sayısı
            running_count = len([p for p in self.running_processes.values() if p.poll() is None])
            
            if running_count == 0:
                self.system_status = "🟢 Sistem Hazır"
            elif running_count == 1:
                self.system_status = "🟡 1 İşlem Çalışıyor"
            else:
                self.system_status = f"🟡 {running_count} İşlem Çalışıyor"
            
            self.status_label.config(text=self.system_status)
            self.last_update = datetime.now().strftime("%H:%M:%S")
            self.update_label.config(text=f"Son güncelleme: {self.last_update}")
            
            # 5 saniyede bir güncelle
            self.root.after(5000, self.update_status)
            
        except Exception as e:
            self.log_message(f"Durum güncellenirken hata: {e}", "ERROR")
    
    def log_message(self, message, level="INFO"):
        """Log mesajı ekler"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Renk kodları
            colors = {
                "INFO": "#2a5298",
                "SUCCESS": "#27ae60", 
                "WARNING": "#f39c12",
                "ERROR": "#e74c3c"
            }
            
            color = colors.get(level, "#333")
            
            # Log mesajını ekle
            log_entry = f"[{timestamp}] {level}: {message}\n"
            self.log_text.insert(tk.END, log_entry)
            
            # Renk uygula
            start = f"{self.log_text.index('end-2c').split('.')[0]}.0"
            end = self.log_text.index('end-1c')
            self.log_text.tag_add(level, start, end)
            self.log_text.tag_config(level, foreground=color)
            
            # Otomatik kaydır
            self.log_text.see(tk.END)
            
            # Maksimum log satırı kontrolü
            lines = int(self.log_text.index('end-1c').split('.')[0])
            if lines > self.settings.get("max_log_lines", 1000):
                # İlk 100 satırı sil
                self.log_text.delete("1.0", "101.0")
                
        except Exception as e:
            print(f"Log mesajı eklenirken hata: {e}")
    
    def clear_logs(self):
        """Log alanını temizler"""
        self.log_text.delete("1.0", tk.END)
        self.log_message("Log alanı temizlendi", "INFO")
    
    def save_logs(self):
        """Logları dosyaya kaydeder"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_logs_{timestamp}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.log_text.get("1.0", tk.END))
            
            self.log_message(f"Loglar '{filename}' dosyasına kaydedildi", "SUCCESS")
            messagebox.showinfo("Başarılı", f"Loglar '{filename}' dosyasına kaydedildi.")
            
        except Exception as e:
            self.log_message(f"Loglar kaydedilirken hata: {e}", "ERROR")
            messagebox.showerror("Hata", f"Loglar kaydedilirken hata oluştu: {e}")
    
    def show_settings(self):
        """Ayarlar penceresini gösterir"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Program Ayarları")
        settings_window.configure(bg="#f0f4f8")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # Başlık
        tk.Label(settings_window, text="⚙️ Program Ayarları", 
                font=("Arial", 16, "bold"), fg="#2a5298", bg="#f0f4f8").pack(pady=20)
        
        # Ayarlar
        settings_frame = tk.Frame(settings_window, bg="#f0f4f8")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tooltip ayarı
        tooltip_var = tk.BooleanVar(value=self.settings.get("show_tooltips", True))
        tk.Checkbutton(settings_frame, text="Tooltip'leri göster", variable=tooltip_var,
                      bg="#f0f4f8", font=("Arial", 11)).pack(anchor=tk.W, pady=5)
        
        # Otomatik kaydetme
        auto_save_var = tk.BooleanVar(value=self.settings.get("auto_save_metrics", True))
        tk.Checkbutton(settings_frame, text="Metrikleri otomatik kaydet", variable=auto_save_var,
                      bg="#f0f4f8", font=("Arial", 11)).pack(anchor=tk.W, pady=5)
        

        
        # Maksimum log satırı
        tk.Label(settings_frame, text="Maksimum log satırı:", 
                font=("Arial", 11), bg="#f0f4f8").pack(anchor=tk.W, pady=(10, 5))
        
        max_log_var = tk.StringVar(value=str(self.settings.get("max_log_lines", 1000)))
        max_log_entry = tk.Entry(settings_frame, textvariable=max_log_var, width=10)
        max_log_entry.pack(anchor=tk.W, pady=5)
        
        # Butonlar
        button_frame = tk.Frame(settings_window, bg="#f0f4f8")
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def save_settings():
            try:
                self.settings["show_tooltips"] = tooltip_var.get()
                self.settings["auto_save_metrics"] = auto_save_var.get()
                self.settings["max_log_lines"] = int(max_log_var.get())
                
                self.save_settings()
                messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")
                settings_window.destroy()
                
            except ValueError:
                messagebox.showerror("Hata", "Maksimum log satırı sayı olmalıdır!")
        
        tk.Button(button_frame, text="💾 Kaydet", command=save_settings,
                 bg="#27ae60", fg="white", font=("Arial", 11, "bold")).pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(button_frame, text="❌ İptal", command=settings_window.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 11, "bold")).pack(side=tk.RIGHT)
    
    def safe_exit(self):
        """Güvenli çıkış"""
        try:
            # Çalışan işlemleri durdur
            self.stop_all_processes()
            
            # Ayarları kaydet
            self.save_settings()
            
            # Otomatik metrik kaydetme
            if self.settings.get("auto_save_metrics", True):
                try:
                    from performance_monitor import save_performance_metrics, performance_monitor
                    if performance_monitor.metrics:
                        save_performance_metrics()
                        self.log_message("Metrikler otomatik olarak kaydedildi", "SUCCESS")
                except Exception as e:
                    self.log_message(f"Otomatik metrik kaydetme hatası: {e}", "WARNING")
            
            self.log_message("Program güvenli şekilde kapatılıyor...", "INFO")
            self.root.quit()
            
        except Exception as e:
            self.log_message(f"Çıkış sırasında hata: {e}", "ERROR")
            self.root.quit()

    def run_script(self, script_name, display_name):
        """Script çalıştırır"""
        try:
            self.log_message(f"{display_name} başlatılıyor...", "INFO")
            
            # Python script'ini çalıştır
            # UTF-8 çıktıyı zorla (Windows'ta emoji ve Unicode sorunlarını önler)
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"

            process = subprocess.Popen(
                [sys.executable, "-u", script_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # stderr'i stdout'a birleştir
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                universal_newlines=True,
                env=env,
            )
            
            self.running_processes[script_name] = process
            self.log_message(f"{display_name} başarıyla başlatıldı (PID: {process.pid})", "SUCCESS")
            
            # Çıktıyı okumak için thread başlat
            threading.Thread(target=self.monitor_process, args=(process, script_name, display_name), 
                           daemon=True).start()
            
        except Exception as e:
            self.log_message(f"{display_name} başlatılırken hata: {e}", "ERROR")
            messagebox.showerror("Hata", f"{display_name} başlatılırken hata oluştu:\n{e}")
            
    def monitor_process(self, process, script_name, display_name):
        """İşlem çıktısını izler"""
        try:
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log_message(f"[{display_name}] {output.strip()}", "INFO")
                    
            # İşlem bittiğinde
            if script_name in self.running_processes:
                del self.running_processes[script_name]
            self.log_message(f"{display_name} tamamlandı", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"{display_name} izlenirken hata: {e}", "ERROR")
            
    def start_gui(self):
        """GUI uygulamasını başlatır"""
        try:
            # GUI'nin zaten çalışıp çalışmadığını kontrol et
            if "GUI Uygulaması" in self.running_processes:
                process = self.running_processes["GUI Uygulaması"]
                if process.poll() is None:
                    messagebox.showinfo("Bilgi", "GUI uygulaması zaten çalışıyor!")
                    return
            
            self.run_script("gui.py", "GUI Uygulaması")
            
        except Exception as e:
            self.log_message(f"GUI başlatılırken hata: {e}", "ERROR")
            messagebox.showerror("Hata", f"GUI uygulaması başlatılırken hata oluştu:\n{e}")
        
    def start_es_test(self):
        """Elasticsearch testini başlatır"""
        self.run_script("es_test.py", "Elasticsearch Test")
        
    def start_performance_test(self):
        """Performans testini başlatır"""
        self.run_script("performance_test.py", "Performans Test")
        
    def start_performance_analyzer(self):
        """Performans analizini başlatır"""
        self.run_script("performance_analyzer.py", "Performans Analizi")
        
    def start_ml_test(self):
        """ML analiz testini başlatır"""
        self.run_script("ml_analyzer.py", "ML Analiz Test")
        
    def start_ml_test_system(self):
        """ML test sistemini başlatır"""
        self.run_script("ml_test.py", "ML Test Sistemi")
        
    def start_es_config(self):
        """Elasticsearch yapılandırmasını başlatır"""
        try:
            # Dosyanın varlığını kontrol et
            if not os.path.exists("es_config.py"):
                messagebox.showerror("Hata", "es_config.py dosyası bulunamadı!")
                return
            
            self.run_script("es_config.py", "Elasticsearch Yapılandırma")
            
        except Exception as e:
            self.log_message(f"Elasticsearch yapılandırma hatası: {e}", "ERROR")
            messagebox.showerror("Hata", f"Elasticsearch yapılandırması başlatılırken hata oluştu:\n{e}")
        
    def quick_performance_test(self):
        """Hızlı performans testi yapar"""
        try:
            self.log_message("Hızlı performans testi başlatılıyor...", "INFO")
            
            # Basit performans testleri
            from performance_monitor import monitor_performance
            import time
            
            @monitor_performance("Hızlı Sistem Testi")
            def test_function_1():
                time.sleep(0.1)
                return "Hızlı sistem testi tamamlandı"
            
            @monitor_performance("Orta Süre Testi")
            def test_function_2():
                time.sleep(0.2)
                return "Orta süre testi tamamlandı"
            
            @monitor_performance("Uzun Süre Testi")
            def test_function_3():
                time.sleep(0.15)
                return "Uzun süre testi tamamlandı"
            
            # Testleri çalıştır
            test_function_1()
            test_function_2()
            test_function_3()
            
            self.log_message("Hızlı performans testi tamamlandı", "SUCCESS")
            messagebox.showinfo("Test Tamamlandı", 
                "✅ Hızlı performans testi başarıyla tamamlandı!\n\n"
                "📊 Artık şunları yapabilirsiniz:\n"
                "• 'Performans Özeti' butonuna basarak sonuçları görün\n"
                "• 'Metrikleri Kaydet' butonuna basarak verileri kaydedin\n"
                "• GUI uygulamasında soru arama yaparak daha fazla veri toplayın\n\n"
                "💡 Bu test sayesinde sistem performansı ölçüldü ve veriler toplandı.")
            
        except Exception as e:
            self.log_message(f"Hızlı performans testi hatası: {e}", "ERROR")
            messagebox.showerror("Hata", f"Hızlı performans testi sırasında hata oluştu:\n{e}")
        
    def show_performance_summary(self):
        """Performans özetini gösterir"""
        try:
            from performance_monitor import print_performance_summary, performance_monitor
            import io, sys
            
            # Önce performans verisi var mı kontrol et
            if not performance_monitor.metrics:
                # Performans verisi yoksa kullanıcıya bilgi ver
                messagebox.showinfo("Performans Verisi Yok", 
                    "Henüz hiçbir işlem yapılmamış.\n\n"
                    "Performans özeti görmek için önce:\n"
                    "1️⃣ 'Hızlı Performans Testi' butonuna basın\n"
                    "2️⃣ Veya 'GUI Uygulaması' açıp soru arama yapın\n"
                    "3️⃣ Veya diğer test butonlarından birini kullanın\n\n"
                    "Bu işlemlerden sonra performans verileri toplanır.")
                return
            
            # Çıktıyı yakala
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            print_performance_summary()
            sys.stdout = old_stdout
            
            summary = mystdout.getvalue()
            
            # Eğer özet boşsa
            if not summary.strip() or summary.strip() == "="*60 + "\nPERFORMANS ÖZETİ\n" + "="*60:
                messagebox.showinfo("Performans Özeti Boş", 
                    "Performans özeti boş görünüyor.\n\n"
                    "Bu durumda:\n"
                    "1️⃣ 'Hızlı Performans Testi' butonuna basın\n"
                    "2️⃣ Veya GUI uygulamasında birkaç soru arama yapın\n"
                    "3️⃣ Sonra tekrar 'Performans Özeti' butonuna basın\n\n"
                    "Bu şekilde performans verileri toplanacak ve özet görüntülenebilecek.")
                return
            
            # Yeni pencerede göster
            summary_window = tk.Toplevel(self.root)
            summary_window.title("📊 Performans Özeti")
            summary_window.configure(bg="#f0f4f8")
            summary_window.geometry("800x600")
            
            # Başlık
            tk.Label(summary_window, text="📊 Performans Özeti", 
                    font=("Arial", 16, "bold"), fg="#2a5298", bg="#f0f4f8").pack(pady=10)
            
            # Açıklama
            tk.Label(summary_window, text="Sistem performans metrikleri aşağıda listelenmiştir:", 
                    font=("Arial", 10), fg="#666", bg="#f0f4f8").pack(pady=(0, 10))
            
            text_widget = scrolledtext.ScrolledText(summary_window, width=90, height=30, 
                                                   font=("Consolas", 10), bg="#e3f2fd", fg="#222")
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, summary)
            text_widget.config(state=tk.DISABLED)
            
            # Kapat butonu
            tk.Button(summary_window, text="❌ Kapat", command=summary_window.destroy,
                     bg="#e74c3c", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
            
            self.log_message("Performans özeti gösterildi", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Performans özeti gösterilirken hata: {e}", "ERROR")
            messagebox.showerror("Hata", f"Performans özeti gösterilirken hata oluştu:\n{e}")
            
    def save_metrics(self):
        """Metrikleri kaydeder"""
        try:
            from performance_monitor import save_performance_metrics, performance_monitor
            
            # Performans verisi var mı kontrol et
            if not performance_monitor.metrics:
                messagebox.showinfo("Metrik Verisi Yok", 
                    "Henüz hiçbir performans verisi toplanmamış.\n\n"
                    "Metrikleri kaydetmek için önce:\n"
                    "1️⃣ 'Hızlı Performans Testi' butonuna basın\n"
                    "2️⃣ Veya GUI uygulamasında soru arama yapın\n"
                    "3️⃣ Veya diğer test butonlarından birini kullanın\n\n"
                    "Bu işlemlerden sonra metrikler kaydedilebilir.")
                return
            
            save_performance_metrics()
            
            self.log_message("Performans metrikleri kaydedildi", "SUCCESS")
            messagebox.showinfo("Metrikler Kaydedildi", 
                "✅ Performans metrikleri başarıyla kaydedildi!\n\n"
                "📁 Dosya: 'performance_metrics.json'\n"
                "📍 Konum: Proje ana dizini\n\n"
                "📊 Kaydedilen veriler:\n"
                "• İşlem süreleri\n"
                "• Bellek kullanımı\n"
                "• CPU kullanımı\n"
                "• Zaman damgaları\n\n"
                "💡 Bu dosyayı gelecekte performans analizi için kullanabilirsiniz.")
        except Exception as e:
            self.log_message(f"Metrikler kaydedilirken hata: {e}", "ERROR")
            messagebox.showerror("Hata", f"Metrikler kaydedilirken hata oluştu:\n{e}")
            
    def check_system_status(self):
        """Sistem durumunu kontrol eder"""
        try:
            self.log_message("Sistem durumu kontrol ediliyor...", "INFO")
            
            # Çalışan işlemleri kontrol et
            running_processes = []
            for name, process in self.running_processes.items():
                if process.poll() is None:
                    running_processes.append(name)
            
            # Sistem durumu raporu
            status_report = f"🖥️ Sistem Durumu Raporu\n"
            status_report += f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            status_report += f"🔄 Çalışan İşlemler: {len(running_processes)}\n"
            
            if running_processes:
                status_report += f"📋 İşlem Listesi:\n"
                for proc in running_processes:
                    status_report += f"  ✅ {proc}\n"
            else:
                status_report += f"💤 Çalışan işlem yok.\n"
            
            # Dosya durumları
            status_report += f"\n📁 Dosya Durumları:\n"
            files_to_check = ["gui.py", "es_config.py", "ml_test.py", "performance_monitor.py"]
            for file in files_to_check:
                if os.path.exists(file):
                    status_report += f"  ✅ {file} - Mevcut\n"
                else:
                    status_report += f"  ❌ {file} - Bulunamadı\n"
            
            # Veritabanı durumu
            status_report += f"\n🗄️ Veritabanı Durumu:\n"
            if os.path.exists("sorular.db"):
                db_size = os.path.getsize("sorular.db") / 1024  # KB
                status_report += f"  ✅ sorular.db - Mevcut ({db_size:.1f} KB)\n"
            else:
                status_report += f"  ❌ sorular.db - Bulunamadı\n"
            
            # Elasticsearch bağlantısı kontrol et
            status_report += f"\n🔍 Elasticsearch Durumu:\n"
            try:
                from es_config import get_default_client
                es = get_default_client()
                if es:
                    info = es.info()
                    status_report += f"  ✅ Bağlı - Sürüm: {info['version']['number']}\n"
                    self.log_message(f"Elasticsearch bağlı - Sürüm: {info['version']['number']}", "SUCCESS")
                else:
                    status_report += f"  ❌ Bağlantı kurulamadı\n"
                    self.log_message("Elasticsearch bağlantısı kurulamadı", "WARNING")
            except Exception as e:
                status_report += f"  ❌ Hata: {str(e)[:50]}...\n"
                self.log_message(f"Elasticsearch kontrol hatası: {e}", "ERROR")
            
            # Yeni pencerede göster
            status_window = tk.Toplevel(self.root)
            status_window.title("🖥️ Sistem Durumu")
            status_window.configure(bg="#f0f4f8")
            status_window.geometry("600x500")
            
            # Başlık
            tk.Label(status_window, text="🖥️ Sistem Durumu Raporu", 
                    font=("Arial", 16, "bold"), fg="#2a5298", bg="#f0f4f8").pack(pady=10)
            
            text_widget = scrolledtext.ScrolledText(status_window, width=70, height=25, 
                                                   font=("Consolas", 10), bg="#e3f2fd", fg="#222")
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, status_report)
            text_widget.config(state=tk.DISABLED)
            
            # Kapat butonu
            tk.Button(status_window, text="❌ Kapat", command=status_window.destroy,
                     bg="#e74c3c", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
            
            self.log_message("Sistem durumu kontrol edildi", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Sistem durumu kontrol edilirken hata: {e}", "ERROR")
            messagebox.showerror("Hata", f"Sistem durumu kontrol edilirken hata oluştu:\n{e}")
            
    def stop_all_processes(self):
        """Tüm çalışan işlemleri durdurur"""
        try:
            if not self.running_processes:
                messagebox.showinfo("Bilgi", "Durdurulacak işlem yok.")
                return
            
            # Onay al
            result = messagebox.askyesno("Onay", 
                f"{len(self.running_processes)} çalışan işlem var.\n\n"
                "Tüm işlemleri durdurmak istediğinizden emin misiniz?")
            
            if not result:
                return
            
            self.log_message(f"{len(self.running_processes)} işlem durduruluyor...", "WARNING")
            
            stopped_count = 0
            for script_name, process in self.running_processes.items():
                try:
                    process.terminate()
                    self.log_message(f"{script_name} durduruldu", "SUCCESS")
                    stopped_count += 1
                except Exception as e:
                    self.log_message(f"{script_name} durdurulurken hata: {e}", "ERROR")
            
            self.running_processes.clear()
            
            messagebox.showinfo("Tamamlandı", 
                f"✅ {stopped_count} işlem başarıyla durduruldu.\n\n"
                "Tüm işlemler güvenli şekilde sonlandırıldı.")
            
        except Exception as e:
            self.log_message(f"İşlemler durdurulurken hata: {e}", "ERROR")
            messagebox.showerror("Hata", f"İşlemler durdurulurken hata oluştu:\n{e}")
        
def main():
    """Ana fonksiyon"""
    root = tk.Tk()
    app = MainControlPanel(root)
    
    # Başlangıç mesajı
    app.log_message("Ana Kontrol Paneli başlatıldı", "SUCCESS")
    app.log_message("Proje bileşenlerini başlatmak için sol paneldeki butonları kullanın", "INFO")
    
    root.mainloop()

if __name__ == "__main__":
    main()
