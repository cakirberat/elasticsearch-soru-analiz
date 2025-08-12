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

class MainControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Soru Projesi - Ana Kontrol Paneli")
        self.root.configure(bg="#f0f4f8")
        self.root.geometry("900x700")
        
        # Çalışan işlemler
        self.running_processes = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        # Ana başlık
        title = tk.Label(self.root, text="🎯 Soru Projesi - Ana Kontrol Paneli", 
                        font=("Arial", 20, "bold"), fg="#2a5298", bg="#f0f4f8")
        title.pack(pady=(20, 10))
        
        
        # Ana frame
        main_frame = tk.Frame(self.root, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sol panel - Butonlar
        left_panel = tk.Frame(main_frame, bg="#f0f4f8", width=300)
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
            ("🖥️ GUI Uygulaması", self.start_gui, "#2a5298"),
            ("🔍 Elasticsearch Test", self.start_es_test, "#e67e22"),
            ("⚡ Performans Test", self.start_performance_test, "#9b59b6"),
            ("🔮 Performans Tahmini", self.start_performance_analyzer, "#e74c3c")
        ])
        
        # Test ve analiz
        self.create_section(parent, "🧪 Test ve Analiz", [
            ("🔧 Elasticsearch Bağlantı", self.start_es_config, "#27ae60"),
            ("📊 Performans Özeti", self.show_performance_summary, "#8e44ad"),
            ("💾 Metrikleri Kaydet", self.save_metrics, "#f39c12")
        ])
        
        # Sistem durumu
        self.create_section(parent, "📈 Sistem Durumu", [
            ("🔄 Durumu Kontrol Et", self.check_system_status, "#16a085"),
            ("🧹 Tüm İşlemleri Durdur", self.stop_all_processes, "#c0392b")
        ])
        
        # Çıkış
        exit_button = tk.Button(parent, text="❌ Çıkış", command=self.root.quit,
                               bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                               width=25, height=2, activebackground="#c0392b")
        exit_button.pack(pady=(20, 0))
        
    def create_section(self, parent, title, buttons):
        """Bölüm oluşturur"""
        # Bölüm başlığı
        tk.Label(parent, text=title, font=("Arial", 12, "bold"), 
                fg="#333", bg="#f0f4f8").pack(pady=(15, 10), anchor=tk.W)
        
        # Butonlar
        for text, command, color in buttons:
            btn = tk.Button(parent, text=text, command=command,
                           bg=color, fg="white", font=("Arial", 10, "bold"),
                           width=25, height=2, activebackground=color)
            btn.pack(pady=2)
            
    def create_log_area(self, parent):
        """Log alanını oluşturur"""
        # Başlık
        tk.Label(parent, text="📋 Sistem Logları", font=("Arial", 14, "bold"), 
                fg="#2a5298", bg="#f0f4f8").pack(pady=(0, 10))
        
        # Log alanı
        self.log_text = scrolledtext.ScrolledText(parent, width=60, height=25, 
                                                 font=("Consolas", 10), bg="#2c3e50", fg="#ecf0f1")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Kontrol butonları
        control_frame = tk.Frame(parent, bg="#f0f4f8")
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(control_frame, text="🧹 Logları Temizle", command=self.clear_logs,
                 bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(control_frame, text="💾 Logları Kaydet", command=self.save_logs,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
    def log_message(self, message, level="INFO"):
        """Log mesajı ekler"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        
        # Renk kodlaması
        if level == "ERROR":
            self.log_text.tag_add("error", f"{self.log_text.index('end-2c').split('.')[0]}.0", "end-1c")
            self.log_text.tag_config("error", foreground="#e74c3c")
        elif level == "SUCCESS":
            self.log_text.tag_add("success", f"{self.log_text.index('end-2c').split('.')[0]}.0", "end-1c")
            self.log_text.tag_config("success", foreground="#27ae60")
        elif level == "WARNING":
            self.log_text.tag_add("warning", f"{self.log_text.index('end-2c').split('.')[0]}.0", "end-1c")
            self.log_text.tag_config("warning", foreground="#f39c12")
            
    def run_script(self, script_name, display_name):
        """Script çalıştırır"""
        try:
            self.log_message(f"{display_name} başlatılıyor...", "INFO")
            
            # Python script'ini çalıştır
            process = subprocess.Popen([sys.executable, script_name], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     text=True, bufsize=1, universal_newlines=True)
            
            self.running_processes[script_name] = process
            self.log_message(f"{display_name} başarıyla başlatıldı (PID: {process.pid})", "SUCCESS")
            
            # Çıktıyı okumak için thread başlat
            threading.Thread(target=self.monitor_process, args=(process, script_name, display_name), 
                           daemon=True).start()
            
        except Exception as e:
            self.log_message(f"{display_name} başlatılırken hata: {e}", "ERROR")
            
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
        self.run_script("gui.py", "GUI Uygulaması")
        
    def start_es_test(self):
        """Elasticsearch testini başlatır"""
        self.run_script("es_test.py", "Elasticsearch Test")
        
    def start_performance_test(self):
        """Performans testini başlatır"""
        self.run_script("performance_test.py", "Performans Test")
        
    def start_performance_analyzer(self):
        """Performans analizini başlatır"""
        self.run_script("performance_analyzer.py", "Performans Analizi")
        
    def start_es_config(self):
        """Elasticsearch yapılandırmasını başlatır"""
        self.run_script("es_config.py", "Elasticsearch Yapılandırma")
        
    def show_performance_summary(self):
        """Performans özetini gösterir"""
        try:
            from performance_monitor import print_performance_summary
            import io, sys
            
            # Çıktıyı yakala
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            print_performance_summary()
            sys.stdout = old_stdout
            
            summary = mystdout.getvalue()
            
            # Yeni pencerede göster
            summary_window = tk.Toplevel(self.root)
            summary_window.title("Performans Özeti")
            summary_window.configure(bg="#f0f4f8")
            summary_window.geometry("700x500")
            
            text_widget = scrolledtext.ScrolledText(summary_window, width=80, height=25, 
                                                   font=("Consolas", 10), bg="#e3f2fd", fg="#222")
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, summary)
            text_widget.config(state=tk.DISABLED)
            
            self.log_message("Performans özeti gösterildi", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Performans özeti gösterilirken hata: {e}", "ERROR")
            
    def save_metrics(self):
        """Metrikleri kaydeder"""
        try:
            from performance_monitor import save_performance_metrics
            save_performance_metrics()
            self.log_message("Performans metrikleri kaydedildi", "SUCCESS")
        except Exception as e:
            self.log_message(f"Metrikler kaydedilirken hata: {e}", "ERROR")
            
    def check_system_status(self):
        """Sistem durumunu kontrol eder"""
        self.log_message("Sistem durumu kontrol ediliyor...", "INFO")
        
        # Elasticsearch bağlantısı kontrol et
        try:
            from es_config import get_default_client
            es = get_default_client()
            if es:
                info = es.info()
                self.log_message(f"Elasticsearch bağlı - Sürüm: {info['version']['number']}", "SUCCESS")
            else:
                self.log_message("Elasticsearch bağlantısı kurulamadı", "WARNING")
        except Exception as e:
            self.log_message(f"Elasticsearch kontrol hatası: {e}", "ERROR")
            
        # Çalışan işlemleri listele
        if self.running_processes:
            self.log_message(f"Çalışan işlemler: {len(self.running_processes)}", "INFO")
            for script, process in self.running_processes.items():
                self.log_message(f"  - {script} (PID: {process.pid})", "INFO")
        else:
            self.log_message("Çalışan işlem yok", "INFO")
            
    def stop_all_processes(self):
        """Tüm çalışan işlemleri durdurur"""
        if not self.running_processes:
            self.log_message("Durdurulacak işlem yok", "INFO")
            return
            
        self.log_message(f"{len(self.running_processes)} işlem durduruluyor...", "WARNING")
        
        for script_name, process in self.running_processes.items():
            try:
                process.terminate()
                self.log_message(f"{script_name} durduruldu", "SUCCESS")
            except Exception as e:
                self.log_message(f"{script_name} durdurulurken hata: {e}", "ERROR")
                
        self.running_processes.clear()
        
    def clear_logs(self):
        """Logları temizler"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Loglar temizlendi", "INFO")
        
    def save_logs(self):
        """Logları dosyaya kaydeder"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_logs_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))
                
            self.log_message(f"Loglar '{filename}' dosyasına kaydedildi", "SUCCESS")
        except Exception as e:
            self.log_message(f"Loglar kaydedilirken hata: {e}", "ERROR")

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
