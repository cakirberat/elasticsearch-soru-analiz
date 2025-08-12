import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import re
from es_search import benzer_sorulari_bul, load_stopwords, save_stopwords, refresh_stopwords
from performance_monitor import monitor_performance, print_performance_summary, save_performance_metrics
from performance_analyzer import PerformanceAnalyzer
from ml_analyzer import MLAnalyzer

class SoruAramaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Soru Arama ve Stopwords Yönetimi")
        self.root.configure(bg="#f0f4f8")
        self.stopwords = load_stopwords()

        # Başlık
        title = tk.Label(root, text="Soru Arama ve Stopwords Yönetimi", font=("Arial", 18, "bold"), fg="#2a5298", bg="#f0f4f8")
        title.grid(row=0, column=0, columnspan=4, pady=(15, 10))

        # Analiz yöntemi seçimi
        tk.Label(root, text="Analiz Yöntemi:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#333").grid(row=1, column=0, sticky="e", padx=5)
        self.analiz_yontemi = tk.StringVar(value="elasticsearch")
        tk.Radiobutton(root, text="🔍 Elasticsearch", variable=self.analiz_yontemi, value="elasticsearch", 
                      bg="#f0f4f8", font=("Arial", 11), fg="#2a5298").grid(row=1, column=1, sticky="w", padx=5)
        tk.Radiobutton(root, text="🤖 Machine Learning", variable=self.analiz_yontemi, value="machine_learning", 
                      bg="#f0f4f8", font=("Arial", 11), fg="#e74c3c").grid(row=1, column=2, sticky="w", padx=5)
        
        # Soru arama bölümü
        tk.Label(root, text="Soru Girin:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#333").grid(row=2, column=0, sticky="e", padx=5)
        self.soru_entry = tk.Entry(root, width=50, font=("Arial", 11))
        self.soru_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        self.ara_button = tk.Button(root, text="Ara", command=self.soru_ara, width=10, bg="#2a5298", fg="white", font=("Arial", 11, "bold"), activebackground="#1e3c72")
        self.ara_button.grid(row=2, column=3, padx=5)
        
        # Eşik değeri
        tk.Label(root, text="Eşik Değeri:", font=("Arial", 11), bg="#f0f4f8").grid(row=3, column=0, sticky="e", padx=5)
        self.esik_var = tk.DoubleVar(value=0.75)
        self.esik_entry = tk.Entry(root, textvariable=self.esik_var, width=10, font=("Arial", 11))
        self.esik_entry.grid(row=3, column=1, sticky="w", pady=5)
        self.temizle_button = tk.Button(root, text="Sonuçları Temizle", command=self.sonuc_temizle, bg="#e17055", fg="white", font=("Arial", 10, "bold"), activebackground="#d35400")
        self.temizle_button.grid(row=3, column=3, padx=5, pady=5)

        # Sonuçlar
        tk.Label(root, text="Arama Sonuçları:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#2a5298").grid(row=4, column=0, sticky="nw", pady=(10,0), padx=5)
        self.sonuc_text = scrolledtext.ScrolledText(root, width=90, height=18, font=("Consolas", 11), bg="#e3f2fd", fg="#222", borderwidth=2, relief="groove")
        self.sonuc_text.grid(row=5, column=0, columnspan=4, padx=5, pady=(0,10), sticky="nsew")

        # Stopwords yönetimi
        tk.Label(root, text="Stopwords Listesi:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#2a5298").grid(row=6, column=0, sticky="w", padx=5)
        self.stopwords_search = tk.Entry(root, width=20, font=("Arial", 10))
        self.stopwords_search.grid(row=6, column=1, sticky="w", pady=5)
        self.stopwords_search.bind("<KeyRelease>", self.stopwords_ara)
        self.stopwords_listbox = tk.Listbox(root, width=40, height=10, font=("Arial", 10), bg="#fffbe7", fg="#444", borderwidth=2, relief="ridge", selectbackground="#ffe082")
        self.stopwords_listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.stopwords_guncelle()

        self.ekle_button = tk.Button(root, text="Stopword Ekle", command=self.stopword_ekle, bg="#00b894", fg="white", font=("Arial", 10, "bold"), activebackground="#00b894")
        self.ekle_button.grid(row=7, column=2, sticky="n", padx=5)
        self.sil_button = tk.Button(root, text="Seçili Stopword'ü Sil", command=self.stopword_sil, bg="#d63031", fg="white", font=("Arial", 10, "bold"), activebackground="#b71c1c")
        self.sil_button.grid(row=7, column=3, sticky="n", padx=5)

        # Performans butonları
        tk.Label(root, text="Performans:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#2a5298").grid(row=8, column=0, sticky="w", padx=5, pady=(10,0))
        self.performans_ozet_button = tk.Button(root, text="Performans Özeti", command=self.performans_ozeti_goster, bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), activebackground="#8e44ad")
        self.performans_ozet_button.grid(row=8, column=1, sticky="w", padx=5, pady=(10,0))
        self.performans_kaydet_button = tk.Button(root, text="Metrikleri Kaydet", command=self.performans_kaydet, bg="#e67e22", fg="white", font=("Arial", 10, "bold"), activebackground="#d35400")
        self.performans_kaydet_button.grid(row=8, column=2, sticky="w", padx=5, pady=(10,0))
        self.performans_tahmin_button = tk.Button(root, text="Performans Tahmini", command=self.performans_tahmini_goster, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), activebackground="#c0392b")
        self.performans_tahmin_button.grid(row=8, column=3, sticky="w", padx=5, pady=(10,0))

        # Grid ayarları
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(5, weight=1)

    def soru_ara(self):
        soru = self.soru_entry.get()
        if not soru.strip():
            messagebox.showwarning("Uyarı", "Lütfen bir soru girin.")
            return
        try:
            esik = float(self.esik_var.get())
        except ValueError:
            messagebox.showerror("Hata", "Eşik değeri sayı olmalı.")
            return
            
        # Analiz yöntemini kontrol et
        yontem = self.analiz_yontemi.get()
        
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
            
        sys.stdout = old_stdout
        sonuc = mystdout.getvalue()
        self.sonuc_text.delete(1.0, tk.END)
        self.sonuc_text.insert(tk.END, sonuc)
        
    def ml_analiz_yap(self, soru, esik):
        """Machine Learning ile analiz yapar"""
        try:
            # ML analizör oluştur
            analyzer = MLAnalyzer()
            
            # Verileri yükle
            if not analyzer.load_questions_from_db():
                print("❌ Veri yükleme başarısız")
                return
                
            # Soruları temizle
            analyzer.clean_questions()
            
            # Model eğitimi/yükleme
            if not analyzer.load_model():
                print("🔄 Model eğitiliyor...")
                analyzer.train_model()
            else:
                # Yüklenen vektörizer ile mevcut korpustan TF-IDF matrisi oluştur
                analyzer.tfidf_matrix = analyzer.vectorizer.transform(analyzer.cleaned_questions)
                
            # Benzer soruları bul
            print(f"\n🔍 Sorgu: {soru}")
            print(f"📊 Eşik değeri: {esik}")
            print("-" * 50)
            
            similar_questions = analyzer.find_similar_questions_ml(soru, top_k=5, threshold=esik)
            
            if similar_questions:
                print(f"📋 {len(similar_questions)} benzer soru bulundu:")
                print()
                for i, result in enumerate(similar_questions, 1):
                    print(f"{i}. {result['soru']}")
                    yuzde = result.get('yuzde', float(result.get('benzerlik', 0)) * 100.0)
                    print(f"   Benzerlik: %{yuzde:.0f}")
                    print()
            else:
                print("❌ Benzer soru bulunamadı")
                
            # İstatistikler
            stats = analyzer.get_ml_statistics()
            if stats:
                print("📊 ML İstatistikleri:")
                print(f"   Toplam Soru: {stats['toplam_soru']}")
                print(f"   Ortalama Uzunluk: {stats['ortalama_soru_uzunlugu']:.1f} kelime")
                print(f"   Benzersiz Kelime: {stats['benzersiz_kelimeler']}")
                if stats['vektor_boyutu']:
                    print(f"   Vektör Boyutu: {stats['vektor_boyutu']}")
                    
        except Exception as e:
            print(f"❌ ML analizi hatası: {e}")

    def sonuc_temizle(self):
        self.sonuc_text.delete(1.0, tk.END)

    def stopwords_guncelle(self, filtre=None):
        self.stopwords = load_stopwords()
        self.stopwords_listbox.delete(0, tk.END)
        for sw in self.stopwords:
            if not filtre or filtre.lower() in sw.lower():
                self.stopwords_listbox.insert(tk.END, sw)

    def stopwords_ara(self, event):
        filtre = self.stopwords_search.get()
        self.stopwords_guncelle(filtre=filtre)

    def stopword_ekle(self):
        yeni = simpledialog.askstring("Stopword Ekle", "Eklemek istediğiniz kelimeyi girin:")
        if yeni:
            yeni = yeni.strip().lower()
            if yeni and yeni not in [sw.lower() for sw in self.stopwords]:
                self.stopwords.append(yeni)
                save_stopwords(self.stopwords)
                try:
                    refresh_stopwords()
                except Exception:
                    pass
                self.stopwords_guncelle()

    def stopword_sil(self):
        secili = self.stopwords_listbox.curselection()
        if secili:
            silinecek = self.stopwords_listbox.get(secili[0])
            self.stopwords = [sw for sw in self.stopwords if sw.lower() != silinecek.lower()]
            save_stopwords(self.stopwords)
            try:
                refresh_stopwords()
            except Exception:
                pass
            self.stopwords_guncelle()

    def performans_ozeti_goster(self):
        """Performans özetini yeni pencerede gösterir"""
        import io, sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        print_performance_summary()
        sys.stdout = old_stdout
        ozet = mystdout.getvalue()
        
        # Yeni pencere oluştur
        ozet_window = tk.Toplevel(self.root)
        ozet_window.title("Performans Özeti")
        ozet_window.configure(bg="#f0f4f8")
        ozet_window.geometry("600x400")
        
        # Özet metni
        ozet_text = scrolledtext.ScrolledText(ozet_window, width=70, height=20, font=("Consolas", 10), bg="#e3f2fd", fg="#222")
        ozet_text.pack(padx=10, pady=10, fill="both", expand=True)
        ozet_text.insert(tk.END, ozet)
        ozet_text.config(state=tk.DISABLED)

    def performans_kaydet(self):
        """Performans metriklerini dosyaya kaydeder"""
        try:
            save_performance_metrics()
            messagebox.showinfo("Başarılı", "Performans metrikleri 'performance_metrics.json' dosyasına kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Metrikler kaydedilirken hata oluştu: {e}")

    def performans_tahmini_goster(self):
        """Performans tahmin penceresini gösterir"""
        # Yeni pencere oluştur
        tahmin_window = tk.Toplevel(self.root)
        tahmin_window.title("Performans Tahmin Sistemi")
        tahmin_window.configure(bg="#f0f4f8")
        tahmin_window.geometry("800x600")
        
        # Başlık
        title = tk.Label(tahmin_window, text="🎯 Performans Tahmin Sistemi", font=("Arial", 16, "bold"), fg="#2a5298", bg="#f0f4f8")
        title.pack(pady=(15, 10))
        
        # Açıklama
        desc = tk.Label(tahmin_window, text="Mevcut performans verilerine dayanarak gelecekteki performansı tahmin eder", font=("Arial", 10), fg="#666", bg="#f0f4f8")
        desc.pack(pady=(0, 20))
        
        # Veri miktarı girişi
        input_frame = tk.Frame(tahmin_window, bg="#f0f4f8")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Hedef Veri Miktarı:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#333").pack(side=tk.LEFT, padx=(0, 10))
        
        data_count_var = tk.StringVar(value="10000")
        data_count_entry = tk.Entry(input_frame, textvariable=data_count_var, width=15, font=("Arial", 12))
        data_count_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(input_frame, text="(örn: 10000, 50000, 100000)", font=("Arial", 10), bg="#f0f4f8", fg="#666").pack(side=tk.LEFT)
        
        # Sonuç alanı
        result_frame = tk.Frame(tahmin_window, bg="#f0f4f8")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        result_text = scrolledtext.ScrolledText(result_frame, width=80, height=25, font=("Consolas", 10), bg="#e3f2fd", fg="#222")
        result_text.pack(fill=tk.BOTH, expand=True)
        
        def run_prediction():
            """Tahmin işlemini çalıştırır"""
            # 1) Girişi oku ve sayıya çevir (sadece bu kısım ValueError yakalar)
            raw_input = data_count_var.get()
            user_input = re.sub(r"\D", "", raw_input or "")
            if not user_input:
                messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
                return
            try:
                target_count = int(user_input)
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
                return
            if target_count <= 0:
                messagebox.showerror("Hata", "Lütfen pozitif bir sayı girin!")
                return

            # 2) Tahmin işlemini çalıştır (diğer hataları ayrı yakala)
            try:
                # Sonuç alanını temizle
                result_text.delete(1.0, tk.END)

                analyzer = PerformanceAnalyzer()

                # Konsola yazılan unicode çıktılarının kodlama hatasını önlemek için
                import io, sys as _sys
                _old_stdout = _sys.stdout
                _sys.stdout = io.StringIO()
                try:
                    # Mevcut performansı analiz et
                    result_text.insert(tk.END, "🔍 Mevcut Performans Analizi Yapılıyor...\n")
                    result_text.insert(tk.END, "="*60 + "\n\n")
                    analyzer.analyze_current_performance()

                    # Veritabanı bilgilerini al
                    result_text.insert(tk.END, "📊 Veritabanı Analizi\n")
                    result_text.insert(tk.END, "="*60 + "\n")
                    current_data_count = analyzer.get_database_info()
                    if current_data_count:
                        result_text.insert(tk.END, f"💡 Mevcut veritabanında {current_data_count:,} döküman bulunuyor.\n")
                        result_text.insert(tk.END, "   Bu veriler üzerinde yapılan analizler kullanılarak tahmin yapılacak.\n\n")

                    # Performans tahmini yap
                    result_text.insert(tk.END, f"🔮 {target_count:,} Veri İçin Performans Tahmini\n")
                    result_text.insert(tk.END, "="*60 + "\n\n")
                    predictions = analyzer.predict_performance(target_count)

                    # Özet rapor
                    result_text.insert(tk.END, "📋 PERFORMANS TAHMİN ÖZETİ\n")
                    result_text.insert(tk.END, "="*60 + "\n")
                    result_text.insert(tk.END, f"🎯 Hedef Veri Miktarı: {target_count:,}\n\n")

                    total_predicted_time = 0
                    total_predicted_memory = 0
                    for operation_name, pred in predictions.items():
                        total_predicted_time += pred['predicted_duration']
                        total_predicted_memory += pred['predicted_memory']
                        result_text.insert(tk.END, f"🔍 {operation_name.upper()}:\n")
                        result_text.insert(tk.END, f"   ⏱️  Tahmini Süre: {pred['predicted_duration']:.2f} saniye\n")
                        result_text.insert(tk.END, f"   💾 Tahmini Bellek: {pred['predicted_memory']:.2f} MB\n\n")

                    result_text.insert(tk.END, "📊 TOPLAM TAHMİN:\n")
                    result_text.insert(tk.END, f"   ⏱️  Toplam Süre: {total_predicted_time:.2f} saniye\n")
                    result_text.insert(tk.END, f"   ⏱️  Toplam Süre: {total_predicted_time/60:.2f} dakika\n")
                    if total_predicted_time > 3600:
                        result_text.insert(tk.END, f"   ⏱️  Toplam Süre: {total_predicted_time/3600:.2f} saat\n")
                    result_text.insert(tk.END, f"   💾 Toplam Bellek: {total_predicted_memory:.2f} MB\n")

                    # Sonuçları kaydet
                    analyzer.save_prediction_results(target_count, predictions)
                    result_text.insert(tk.END, "\n💾 Tahmin sonuçları JSON dosyasına kaydedildi.\n")
                finally:
                    # stdout'u geri yükle
                    _sys.stdout = _old_stdout

            except Exception as e:
                messagebox.showerror("Hata", f"Tahmin sırasında hata oluştu: {e}")
        
        # Tahmin butonu
        predict_button = tk.Button(tahmin_window, text="🎯 Tahmin Yap", command=run_prediction, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), activebackground="#c0392b")
        predict_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SoruAramaApp(root)
    root.mainloop()