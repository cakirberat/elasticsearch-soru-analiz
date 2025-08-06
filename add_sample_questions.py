import sqlite3

conn = sqlite3.connect('sorular.db')
cursor = conn.cursor()

sorular = [
    # Farklı sorular
    ("Türkiye'nin başkenti neresidir?",),
    ("Python programlama dili hangi yıl ortaya çıkmıştır?",),
    ("Dünya'nın en büyük okyanusu hangisidir?",),
    ("En küçük asal sayı kaçtır?",),
    ("Güneş sistemindeki en küçük gezegen hangisidir?",),
    # Birbirine benzeyen sorular
    ("Türkiye'nin başkenti hangi şehirdir?",),
    ("Türkiye'nin başkenti neresidir?",),
    ("Türkiye'nin başkenti Ankara mıdır?",),
    ("Python hangi yılda ortaya çıkmıştır?",),
    ("Python programlama dili hangi yılda çıkmıştır?",),
    ("Python dili hangi yıl ortaya çıktı?",),
    ("Güneş sisteminin en büyük gezegeni hangisidir?",),
    ("Güneş sistemindeki en büyük gezegen nedir?",),
    ("Türkiye'nin hangi denizlere kıyısı vardır?",),
    ("Türkiye'nin kıyısı olduğu denizler arasında hangisi yer almaz?",),
]

cursor.executemany("INSERT INTO sorular (metin) VALUES (?)", sorular)
conn.commit()
conn.close()

print("Örnek sorular başarıyla eklendi.")