import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from es_search import benzer_sorulari_bul, load_stopwords, save_stopwords

class SoruAramaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Soru Arama ve Stopwords Yönetimi")
        self.root.configure(bg="#f0f4f8")
        self.stopwords = load_stopwords()

        # Başlık
        title = tk.Label(root, text="Soru Arama ve Stopwords Yönetimi", font=("Arial", 18, "bold"), fg="#2a5298", bg="#f0f4f8")
        title.grid(row=0, column=0, columnspan=4, pady=(15, 10))

        # Soru arama bölümü
        tk.Label(root, text="Soru Girin:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#333").grid(row=1, column=0, sticky="e", padx=5)
        self.soru_entry = tk.Entry(root, width=50, font=("Arial", 11))
        self.soru_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        self.ara_button = tk.Button(root, text="Ara", command=self.soru_ara, width=10, bg="#2a5298", fg="white", font=("Arial", 11, "bold"), activebackground="#1e3c72")
        self.ara_button.grid(row=1, column=3, padx=5)
        
        # Eşik değeri
        tk.Label(root, text="Eşik Değeri:", font=("Arial", 11), bg="#f0f4f8").grid(row=2, column=0, sticky="e", padx=5)
        self.esik_var = tk.DoubleVar(value=0.75)
        self.esik_entry = tk.Entry(root, textvariable=self.esik_var, width=10, font=("Arial", 11))
        self.esik_entry.grid(row=2, column=1, sticky="w", pady=5)
        self.temizle_button = tk.Button(root, text="Sonuçları Temizle", command=self.sonuc_temizle, bg="#e17055", fg="white", font=("Arial", 10, "bold"), activebackground="#d35400")
        self.temizle_button.grid(row=2, column=3, padx=5, pady=5)

        # Sonuçlar
        tk.Label(root, text="Arama Sonuçları:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#2a5298").grid(row=3, column=0, sticky="nw", pady=(10,0), padx=5)
        self.sonuc_text = scrolledtext.ScrolledText(root, width=70, height=10, font=("Consolas", 11), bg="#e3f2fd", fg="#222", borderwidth=2, relief="groove")
        self.sonuc_text.grid(row=4, column=0, columnspan=4, padx=5, pady=(0,10))

        # Stopwords yönetimi
        tk.Label(root, text="Stopwords Listesi:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#2a5298").grid(row=5, column=0, sticky="w", padx=5)
        self.stopwords_search = tk.Entry(root, width=20, font=("Arial", 10))
        self.stopwords_search.grid(row=5, column=1, sticky="w", pady=5)
        self.stopwords_search.bind("<KeyRelease>", self.stopwords_ara)
        self.stopwords_listbox = tk.Listbox(root, width=40, height=10, font=("Arial", 10), bg="#fffbe7", fg="#444", borderwidth=2, relief="ridge", selectbackground="#ffe082")
        self.stopwords_listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.stopwords_guncelle()

        self.ekle_button = tk.Button(root, text="Stopword Ekle", command=self.stopword_ekle, bg="#00b894", fg="white", font=("Arial", 10, "bold"), activebackground="#00b894")
        self.ekle_button.grid(row=6, column=2, sticky="n", padx=5)
        self.sil_button = tk.Button(root, text="Seçili Stopword'ü Sil", command=self.stopword_sil, bg="#d63031", fg="white", font=("Arial", 10, "bold"), activebackground="#b71c1c")
        self.sil_button.grid(row=6, column=3, sticky="n", padx=5)

        # Grid ayarları
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(4, weight=1)

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
        import io, sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        benzer_sorulari_bul(soru, esik=esik)
        sys.stdout = old_stdout
        sonuc = mystdout.getvalue()
        self.sonuc_text.delete(1.0, tk.END)
        self.sonuc_text.insert(tk.END, sonuc)

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
                self.stopwords_guncelle()

    def stopword_sil(self):
        secili = self.stopwords_listbox.curselection()
        if secili:
            silinecek = self.stopwords_listbox.get(secili[0])
            self.stopwords = [sw for sw in self.stopwords if sw.lower() != silinecek.lower()]
            save_stopwords(self.stopwords)
            self.stopwords_guncelle()

if __name__ == "__main__":
    root = tk.Tk()
    app = SoruAramaApp(root)
    root.mainloop()