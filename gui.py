import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import re
from es_search import benzer_sorulari_bul, load_stopwords, save_stopwords, refresh_stopwords
from performance_monitor import monitor_performance, print_performance_summary, save_performance_metrics
from performance_analyzer import PerformanceAnalyzer
from ml_analyzer import MLAnalyzer
import threading
import time

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

class SoruAramaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Soru Arama ve Stopwords Yönetimi")
        self.root.configure(bg="#f0f4f8")
        self.root.geometry("1200x800")
        
        # Durum değişkenleri
        self.is_searching = False
        self.search_thread = None
        
        # Stopwords yükle
        self.stopwords = set(load_stopwords())
        
        # UI oluştur
        self.setup_ui()
        
        # Tooltip'leri ekle
        self.add_tooltips()
        
    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        # Ana başlık
        title = tk.Label(self.root, text="🔍 Soru Arama ve Stopwords Yönetimi", 
                        font=("Arial", 20, "bold"), fg="#2a5298", bg="#f0f4f8")
        title.grid(row=0, column=0, columnspan=4, pady=(15, 10))

        # Analiz yöntemi seçimi
        tk.Label(self.root, text="Analiz Yöntemi:", font=("Arial", 12, "bold"), 
                bg="#f0f4f8", fg="#333").grid(row=1, column=0, sticky="e", padx=5)
        
        self.analiz_yontemi = tk.StringVar(value="elasticsearch")
        tk.Radiobutton(self.root, text="🔍 Elasticsearch", variable=self.analiz_yontemi, 
                      value="elasticsearch", bg="#f0f4f8", font=("Arial", 11), 
                      fg="#2a5298").grid(row=1, column=1, sticky="w", padx=5)
        tk.Radiobutton(self.root, text="🤖 Machine Learning", variable=self.analiz_yontemi, 
                      value="machine_learning", bg="#f0f4f8", font=("Arial", 11), 
                      fg="#e74c3c").grid(row=1, column=2, sticky="w", padx=5)
        
        # Soru arama bölümü
        tk.Label(self.root, text="Soru Girin:", font=("Arial", 12, "bold"), 
                bg="#f0f4f8", fg="#333").grid(row=2, column=0, sticky="e", padx=5)
        
        self.soru_entry = tk.Entry(self.root, width=50, font=("Arial", 11))
        self.soru_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        self.soru_entry.bind("<Return>", lambda e: self.soru_ara())  # Enter tuşu ile arama
        
        self.ara_button = tk.Button(self.root, text="🔍 Ara", command=self.soru_ara, 
                                   width=10, bg="#2a5298", fg="white", 
                                   font=("Arial", 11, "bold"), activebackground="#1e3c72",
                                   cursor="hand2")
        self.ara_button.grid(row=2, column=3, padx=5)
        
        # Eşik değeri
        tk.Label(self.root, text="Eşik Değeri:", font=("Arial", 11), 
                bg="#f0f4f8").grid(row=3, column=0, sticky="e", padx=5)
        
        self.esik_var = tk.DoubleVar(value=0.75)
        self.esik_entry = tk.Entry(self.root, textvariable=self.esik_var, 
                                  width=10, font=("Arial", 11))
        self.esik_entry.grid(row=3, column=1, sticky="w", pady=5)
        
        self.temizle_button = tk.Button(self.root, text="🗑️ Temizle", command=self.sonuc_temizle, 
                                       bg="#e17055", fg="white", font=("Arial", 10, "bold"), 
                                       activebackground="#d35400", cursor="hand2")
        self.temizle_button.grid(row=3, column=3, padx=5, pady=5)


        
        # Durum etiketi
        self.status_label = tk.Label(self.root, text="Hazır", font=("Arial", 10), 
                                    fg="#666", bg="#f0f4f8")
        self.status_label.grid(row=5, column=0, columnspan=4, pady=(0, 10))

        # Sonuçlar
        tk.Label(self.root, text="Arama Sonuçları:", font=("Arial", 12, "bold"), 
                bg="#f0f4f8", fg="#2a5298").grid(row=6, column=0, sticky="nw", pady=(10,0), padx=5)
        
        self.sonuc_text = scrolledtext.ScrolledText(self.root, width=90, height=18, 
                                                   font=("Consolas", 11), bg="#e3f2fd", 
                                                   fg="#222", borderwidth=2, relief="groove")
        self.sonuc_text.grid(row=7, column=0, columnspan=4, padx=5, pady=(0,10), sticky="nsew")

        # Stopwords yönetimi
        tk.Label(self.root, text="Stopwords Listesi:", font=("Arial", 12, "bold"), 
                bg="#f0f4f8", fg="#2a5298").grid(row=8, column=0, sticky="w", padx=5)
        
        self.stopwords_search = tk.Entry(self.root, width=20, font=("Arial", 10))
        self.stopwords_search.grid(row=8, column=1, sticky="w", pady=5)
        self.stopwords_search.bind("<KeyRelease>", self.stopwords_ara)
        self.stopwords_search.bind("<Return>", lambda e: self.stopword_ekle())  # Enter ile ekleme
        
        self.stopwords_listbox = tk.Listbox(self.root, width=40, height=10, 
                                           font=("Arial", 10), bg="#fffbe7", fg="#444", 
                                           borderwidth=2, relief="ridge", selectbackground="#ffe082")
        self.stopwords_listbox.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.stopwords_guncelle()

        self.ekle_button = tk.Button(self.root, text="➕ Stopword Ekle", command=self.stopword_ekle, 
                                    bg="#00b894", fg="white", font=("Arial", 10, "bold"), 
                                    activebackground="#00b894", cursor="hand2")
        self.ekle_button.grid(row=9, column=2, sticky="n", padx=5)
        
        self.sil_button = tk.Button(self.root, text="🗑️ Seçili Stopword'ü Sil", command=self.stopword_sil, 
                                   bg="#d63031", fg="white", font=("Arial", 10, "bold"), 
                                   activebackground="#b71c1c", cursor="hand2")
        self.sil_button.grid(row=9, column=3, sticky="n", padx=5)

        # Performans butonları
        tk.Label(self.root, text="Performans:", font=("Arial", 12, "bold"), 
                bg="#f0f4f8", fg="#2a5298").grid(row=10, column=0, sticky="w", padx=5, pady=(10,0))
        
        self.performans_ozet_button = tk.Button(self.root, text="📊 Performans Özeti", 
                                               command=self.performans_ozeti_goster, 
                                               bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), 
                                               activebackground="#8e44ad", cursor="hand2")
        self.performans_ozet_button.grid(row=10, column=1, sticky="w", padx=5, pady=(10,0))
        
        self.performans_kaydet_button = tk.Button(self.root, text="💾 Metrikleri Kaydet", 
                                                 command=self.performans_kaydet, 
                                                 bg="#e67e22", fg="white", font=("Arial", 10, "bold"), 
                                                 activebackground="#d35400", cursor="hand2")
        self.performans_kaydet_button.grid(row=10, column=2, sticky="w", padx=5, pady=(10,0))
        
        self.performans_tahmin_button = tk.Button(self.root, text="🔮 Performans Tahmini", 
                                                 command=self.performans_tahmini_goster, 
                                                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
                                                 activebackground="#c0392b", cursor="hand2")
        self.performans_tahmin_button.grid(row=10, column=3, sticky="w", padx=5, pady=(10,0))

        # Grid ayarları
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_rowconfigure(9, weight=1)
        
    def add_tooltips(self):
        """Butonlara tooltip'ler ekler"""
        Tooltip(self.ara_button, "Seçilen yöntemle soru araması yapar")
        Tooltip(self.temizle_button, "Arama sonuçlarını temizler")
        Tooltip(self.ekle_button, "Yeni stopword ekler")
        Tooltip(self.sil_button, "Seçili stopword'ü siler")
        Tooltip(self.performans_ozet_button, "Sistem performans özetini gösterir")
        Tooltip(self.performans_kaydet_button, "Performans metriklerini kaydeder")
        Tooltip(self.performans_tahmin_button, "Gelecek performans tahminini gösterir")
        
    def update_status(self, message, color="#666"):
        """Durum mesajını günceller"""
        self.status_label.config(text=message, fg=color)
        self.root.update_idletasks()
        


    def soru_ara(self):
        """Soru arama fonksiyonu"""
        if self.is_searching:
            messagebox.showwarning("Uyarı", "Arama zaten devam ediyor. Lütfen bekleyin.")
            return
            
        soru = self.soru_entry.get()
        if not soru.strip():
            messagebox.showwarning("Uyarı", "Lütfen bir soru girin.")
            return
            
        try:
            esik = float(self.esik_var.get())
            if esik < 0 or esik > 1:
                messagebox.showerror("Hata", "Eşik değeri 0 ile 1 arasında olmalı.")
                return
        except ValueError:
            messagebox.showerror("Hata", "Eşik değeri sayı olmalı.")
            return
            
        # Analiz yöntemini kontrol et
        yontem = self.analiz_yontemi.get()
        
        # Arama işlemini thread'de çalıştır
        self.is_searching = True
        self.ara_button.config(state="disabled", text="🔍 Aranıyor...")
        self.search_thread = threading.Thread(target=self._perform_search, args=(soru, esik, yontem))
        self.search_thread.daemon = True
        self.search_thread.start()
        
    def _perform_search(self, soru, esik, yontem):
        """Arama işlemini gerçekleştirir (thread'de çalışır)"""
        try:
            import io, sys
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            
            if yontem == "elasticsearch":
                print("🔍 Elasticsearch ile analiz yapılıyor...")
                benzer_sorulari_bul(soru, esik=esik)
            elif yontem == "machine_learning":
                print("🤖 Machine Learning ile analiz yapılıyor...")
                self.ml_analiz_yap(soru, esik)
            else:
                print("❌ Geçersiz analiz yöntemi")
                return
                
            sys.stdout = old_stdout
            result = mystdout.getvalue()
            
            # Sonucu UI'da göster
            self.root.after(0, lambda: self._show_search_result(result))
            
        except Exception as e:
            error_msg = f"Arama sırasında hata oluştu: {e}"
            self.root.after(0, lambda: self._show_search_error(error_msg))
        finally:
            self.root.after(0, self._finish_search)
            
    def _show_search_result(self, result):
        """Arama sonucunu gösterir"""
        self.sonuc_text.delete(1.0, tk.END)
        self.sonuc_text.insert(tk.END, result)
        self.update_status("Arama tamamlandı", "#27ae60")
        
    def _show_search_error(self, error_msg):
        """Arama hatasını gösterir"""
        messagebox.showerror("Arama Hatası", error_msg)
        self.update_status("Arama hatası", "#e74c3c")
        
    def _finish_search(self):
        """Arama işlemini sonlandırır"""
        self.is_searching = False
        self.ara_button.config(state="normal", text="🔍 Ara")
        self.update_status("Hazır", "#666")

    def ml_analiz_yap(self, soru, esik):
        """ML analizi yapar"""
        try:
            analyzer = MLAnalyzer()
            # Verileri yükle ve modeli hazırla
            if not analyzer.load_questions_from_db():
                print("❌ Veritabanından sorular yüklenemedi")
                return
                
            analyzer.clean_questions()
            
            # Model yükle veya eğit
            if not analyzer.load_model():
                analyzer.train_model()
            
            # Benzer soruları bul
            benzer_sorular = analyzer.find_similar_questions_ml(soru, threshold=esik)
            
            print(f"🤖 ML Analizi Sonuçları (Eşik: {esik}):")
            print("="*60)
            
            if benzer_sorular:
                for i, result in enumerate(benzer_sorular, 1):
                    print(f"{i}. Benzerlik: {result['benzerlik']:.3f} ({result['yuzde']:.1f}%)")
                    print(f"   Soru: {result['soru']}")
                    print("-" * 40)
            else:
                print("❌ Benzer soru bulunamadı.")
                
        except Exception as e:
            print(f"❌ ML analizi hatası: {e}")

    def sonuc_temizle(self):
        """Sonuçları temizler"""
        self.sonuc_text.delete(1.0, tk.END)
        self.update_status("Sonuçlar temizlendi", "#f39c12")

    def stopwords_ara(self, event=None):
        """Stopwords listesinde arama yapar"""
        search_term = self.stopwords_search.get().lower()
        self.stopwords_listbox.delete(0, tk.END)
        
        for stopword in self.stopwords:
            if search_term in stopword.lower():
                self.stopwords_listbox.insert(tk.END, stopword)

    def stopwords_guncelle(self):
        """Stopwords listesini günceller"""
        self.stopwords_listbox.delete(0, tk.END)
        for stopword in sorted(self.stopwords):
            self.stopwords_listbox.insert(tk.END, stopword)

    def stopword_ekle(self):
        """Yeni stopword ekler"""
        new_stopword = self.stopwords_search.get().strip().lower()
        if not new_stopword:
            messagebox.showwarning("Uyarı", "Lütfen bir stopword girin.")
            return
            
        if new_stopword in self.stopwords:
            messagebox.showinfo("Bilgi", "Bu stopword zaten mevcut.")
            return
            
        self.stopwords.add(new_stopword)
        save_stopwords(sorted(self.stopwords))
        # Arama motorunun kullandığı global stopwords listesini yenile
        try:
            refresh_stopwords()
        except Exception:
            pass
        self.stopwords_guncelle()
        self.stopwords_search.delete(0, tk.END)
        self.update_status(f"'{new_stopword}' stopword olarak eklendi", "#27ae60")

    def stopword_sil(self):
        """Seçili stopword'ü siler"""
        selection = self.stopwords_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen silinecek stopword'ü seçin.")
            return
            
        stopword = self.stopwords_listbox.get(selection[0])
        result = messagebox.askyesno("Onay", f"'{stopword}' stopword'ünü silmek istediğinizden emin misiniz?")
        
        if result:
            self.stopwords.remove(stopword)
            save_stopwords(sorted(self.stopwords))
            # Arama motorunun kullandığı global stopwords listesini yenile
            try:
                refresh_stopwords()
            except Exception:
                pass
            self.stopwords_guncelle()
            self.update_status(f"'{stopword}' stopword olarak silindi", "#e74c3c")

    def performans_ozeti_goster(self):
        """Performans özetini gösterir"""
        try:
            import io, sys
            
            # Performans verisi var mı kontrol et
            from performance_monitor import performance_monitor
            if not performance_monitor.metrics:
                messagebox.showinfo("Performans Verisi Yok", 
                    "Henüz hiçbir performans verisi toplanmamış.\n\n"
                    "Performans özeti görmek için önce soru arama yapın.")
                return
            
            # Çıktıyı yakala
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            print_performance_summary()
            sys.stdout = old_stdout
            
            summary = mystdout.getvalue()
            
            # Yeni pencerede göster
            summary_window = tk.Toplevel(self.root)
            summary_window.title("📊 Performans Özeti")
            summary_window.configure(bg="#f0f4f8")
            summary_window.geometry("800x600")
            
            # Başlık
            tk.Label(summary_window, text="📊 Performans Özeti", 
                    font=("Arial", 16, "bold"), fg="#2a5298", bg="#f0f4f8").pack(pady=10)
            
            text_widget = scrolledtext.ScrolledText(summary_window, width=90, height=30, 
                                                   font=("Consolas", 10), bg="#e3f2fd", fg="#222")
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, summary)
            text_widget.config(state=tk.DISABLED)
            
            # Kapat butonu
            tk.Button(summary_window, text="❌ Kapat", command=summary_window.destroy,
                     bg="#e74c3c", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Performans özeti gösterilirken hata oluştu:\n{e}")

    def performans_kaydet(self):
        """Performans metriklerini kaydeder"""
        try:
            # Performans verisi var mı kontrol et
            from performance_monitor import performance_monitor
            if not performance_monitor.metrics:
                messagebox.showinfo("Metrik Verisi Yok", 
                    "Henüz hiçbir performans verisi toplanmamış.\n\n"
                    "Metrikleri kaydetmek için önce soru arama yapın.")
                return
            
            save_performance_metrics()
            messagebox.showinfo("Başarılı", 
                "✅ Performans metrikleri başarıyla kaydedildi!\n\n"
                "📁 Dosya: 'performance_metrics.json'\n"
                "📍 Konum: Proje ana dizini")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Metrikler kaydedilirken hata oluştu:\n{e}")

    def performans_tahmini_goster(self):
        """Performans tahminini gösterir"""
        try:
            # Performans verisi var mı kontrol et
            from performance_monitor import performance_monitor
            if not performance_monitor.metrics:
                messagebox.showinfo("Metrik Verisi Yok", 
                    "Henüz hiçbir performans verisi toplanmamış.\n\n"
                    "Performans tahmini görmek için önce soru arama yapın.")
                return
            
            analyzer = PerformanceAnalyzer()
            predictions = analyzer.predict_future_performance()
            
            # Yeni pencerede göster
            prediction_window = tk.Toplevel(self.root)
            prediction_window.title("🔮 Performans Tahmini")
            prediction_window.configure(bg="#f0f4f8")
            prediction_window.geometry("600x400")
            
            # Başlık
            tk.Label(prediction_window, text="🔮 Performans Tahmini", 
                    font=("Arial", 16, "bold"), fg="#2a5298", bg="#f0f4f8").pack(pady=10)
            
            text_widget = scrolledtext.ScrolledText(prediction_window, width=70, height=20, 
                                                   font=("Consolas", 10), bg="#e3f2fd", fg="#222")
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, predictions)
            text_widget.config(state=tk.DISABLED)
            
            # Kapat butonu
            tk.Button(prediction_window, text="❌ Kapat", command=prediction_window.destroy,
                     bg="#e74c3c", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Performans tahmini gösterilirken hata oluştu:\n{e}")

def main():
    """Ana fonksiyon"""
    root = tk.Tk()
    app = SoruAramaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()