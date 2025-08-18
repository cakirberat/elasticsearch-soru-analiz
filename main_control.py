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
            ("🖥️ GUI Uygulaması", self.start_gui, "#2a5298")
        ])
        
        # Test ve analiz
        self.create_section(parent, "🧪 Test ve Analiz", [
            ("🔧 Elasticsearch Bağlantı", self.start_es_config, "#27ae60"),
            ("🤖 ML Test Sistemi", self.start_ml_test_system, "#e74c3c"),
            ("⚡ Hızlı Performans Testi", self.quick_performance_test, "#e67e22"),
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
        
    def _append_log(self, message, level="INFO"):
        """UI thread içinde log mesajını ekler"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        if level == "ERROR":
            self.log_text.tag_add("error", f"{self.log_text.index('end-2c').split('.')[0]}.0", "end-1c")
            self.log_text.tag_config("error", foreground="#e74c3c")
        elif level == "SUCCESS":
            self.log_text.tag_add("success", f"{self.log_text.index('end-2c').split('.')[0]}.0", "end-1c")
            self.log_text.tag_config("success", foreground="#27ae60")
        elif level == "WARNING":
            self.log_text.tag_add("warning", f"{self.log_text.index('end-2c').split('.')[0]}.0", "end-1c")
            self.log_text.tag_config("warning", foreground="#f39c12")

    def log_message(self, message, level="INFO"):
        """Thread-safe log"""
        if threading.current_thread() is threading.main_thread():
            self._append_log(message, level)
        else:
            self.root.after(0, self._append_log, message, level)
            
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
        
    def start_ml_test(self):
        """ML analiz testini başlatır"""
        self.run_script("ml_analyzer.py", "ML Analiz Test")
        
    def start_ml_test_system(self):
        """ML test sistemini başlatır"""
        self.run_script("ml_test.py", "ML Test Sistemi")
        
    def start_es_config(self):
        """Elasticsearch yapılandırmasını başlatır"""
        self.run_script("es_config.py", "Elasticsearch Yapılandırma")
        
    def quick_performance_test(self):
        """Hızlı performans testi yapar"""
        try:
            self.log_message("Hızlı performans testi başlatılıyor...", "INFO")
            
            # Basit performans testleri
            from performance_monitor import monitor_performance
            import time
            
            @monitor_performance("hizli_test_1")
            def test_function_1():
                time.sleep(0.1)
                return "Test 1 tamamlandı"
            
            @monitor_performance("hizli_test_2")
            def test_function_2():
                time.sleep(0.2)
                return "Test 2 tamamlandı"
            
            @monitor_performance("hizli_test_3")
            def test_function_3():
                time.sleep(0.15)
                return "Test 3 tamamlandı"
            
            # Testleri çalıştır
            test_function_1()
            test_function_2()
            test_function_3()
            
            self.log_message("Hızlı performans testi tamamlandı", "SUCCESS")
            messagebox.showinfo("Başarılı", 
                "Hızlı performans testi tamamlandı!\n\n"
                "Artık 'Performans Özeti' butonunu kullanabilirsiniz.")
                
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
                messagebox.showinfo("Bilgi", 
                    "Henüz hiçbir performans verisi toplanmamış.\n\n"
                    "Performans özeti görmek için önce şu işlemlerden birini yapın:\n"
                    "• Elasticsearch Test\n"
                    "• ML Analiz Test\n"
                    "• Performans Test\n"
                    "• GUI Uygulamasında soru arama yapın")
                return
            
            # Çıktıyı yakala
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            print_performance_summary()
            sys.stdout = old_stdout
            
            summary = mystdout.getvalue()
            
            # Eğer özet boşsa
            if not summary.strip() or summary.strip() == "="*60 + "\nPERFORMANS ÖZETİ\n" + "="*60:
                messagebox.showinfo("Bilgi", 
                    "Performans özeti boş.\n\n"
                    "Performans verisi toplamak için önce test işlemleri yapın.")
                return
            
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
            messagebox.showerror("Hata", f"Performans özeti gösterilirken hata oluştu:\n{e}")
            
    def save_metrics(self):
        """Metrikleri kaydeder"""
        try:
            from performance_monitor import save_performance_metrics, performance_monitor
            
            # Performans verisi var mı kontrol et
            if not performance_monitor.metrics:
                messagebox.showinfo("Bilgi", 
                    "Henüz hiçbir performans verisi toplanmamış.\n\n"
                    "Metrikleri kaydetmek için önce test işlemleri yapın.")
                return
            
            save_performance_metrics()
            self.log_message("Performans metrikleri kaydedildi", "SUCCESS")
            messagebox.showinfo("Başarılı", "Performans metrikleri 'performance_metrics.json' dosyasına kaydedildi.")
        except Exception as e:
            self.log_message(f"Metrikler kaydedilirken hata: {e}", "ERROR")
            messagebox.showerror("Hata", f"Metrikler kaydedilirken hata oluştu:\n{e}")
            
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
