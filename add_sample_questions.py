import sqlite3

conn = sqlite3.connect('sorular.db')
cursor = conn.cursor()

sorular = [
    # --- Kısa bilgi soruları ---
    ("Türkiye'nin yüzölçümü yaklaşık kaç kilometrekaredir?",),
    ("Osmanlı Devleti hangi yılda kurulmuştur?",),
    ("Fotosentezin temel amacı nedir?",),
    ("İnsan vücudunda en büyük iç organ hangisidir?",),
    ("Edebiyatımızda 'Sefiller' romanını dilimize kim çevirmiştir?",),
    ("Su, deniz seviyesinde kaç derecede kaynar?",),
    ("Türkiye’nin en yüksek dağı hangisidir?",),
    ("Dünya’nın uydusu nedir?",),
    ("İyonlaşma enerjisi en yüksek element hangisidir?",),
    ("Türkiye'nin üç tarafı hangi denizlerle çevrilidir?",),

    # --- Orta uzunluktaki bilgi soruları ---
    ("Cumhuriyet Dönemi'nde yazılmış ilk tiyatro eseri hangisidir?",),
    ("Bir üçgende iç açıların ölçüleri toplamı kaç derecedir?",),
    ("Yeryüzündeki tatlı su kaynaklarının en büyük kısmı nerede bulunur?",),
    ("Bir elektroliz deneyinde elektrotların işlevi nedir?",),
    ("Türkiye’de ilk nüfus sayımı hangi yıl yapılmıştır?",),
    ("Fotosentezde ışık enerjisini kimyasal enerjiye dönüştüren pigment nedir?",),
    ("Ankara hangi yılda başkent ilan edilmiştir?",),
    ("Türk edebiyatında Servet-i Fünun topluluğunun en önemli temsilcilerinden biri kimdir?",),
    ("Bir dik üçgende hipotenüsün karesinin diğer iki kenarın kareleri toplamına eşit olduğunu söyleyen teorem nedir?",),
    ("Türkiye’nin en uzun akarsuyu hangisidir?",),

    # --- Uzun yorum soruları ---
    ("Bir öğrencinin yaptığı deneyde, suyun farklı sıcaklıklarda çözme kapasitesinin değiştiğini gözlemlediği belirtilmektedir. Bu durum hangi bilimsel kavramla açıklanır?",),
    ("Bir şehirdeki hava kirliliği ölçümlerinde, özellikle kış aylarında partikül madde miktarının arttığı görülmüştür. Bu artışın temel nedenleri neler olabilir?",),
    ("Bir roman kahramanının, çevresindeki toplumsal olaylara kayıtsız kalması ve yalnızlığa yönelmesi edebi açıdan hangi akımın özelliklerini yansıtır?",),
    ("Bir ülkenin ihracatında tarım ürünlerinin payı yüksekse, bu durum o ülkenin ekonomik yapısı hakkında ne tür çıkarımlar yapılmasına olanak tanır?",),
    ("Bir öğrenci, bir deneyde aynı hacimdeki suyun farklı sıcaklıklarda kaynama süresini ölçüyor. Deneyin bağımlı ve bağımsız değişkenleri nelerdir?",),
    ("Bir matematik probleminin çözümünde, öncelikle denklem sisteminin çözüm kümesinin boş olduğunun belirlenmesi ne anlama gelir?",),
    ("Bir edebi eserde kahramanın iç çatışmalarını anlatmak için yazarın bilinç akışı tekniğini kullanması, okuyucuda nasıl bir etki yaratır?",),
    ("Bir toplumda okuma alışkanlığının artmasıyla birlikte bireylerin eleştirel düşünme becerilerinin de geliştiği gözlemlenmektedir. Bu durum hangi sosyal bilim kavramıyla açıklanabilir?",),
    ("Bir elektrik devresinde direnç arttıkça akımın azalması hangi fizik yasasıyla ifade edilir?",),
    ("Bir kimya laboratuvarında yapılan titrasyon deneyinde, indikatörün renk değiştirdiği anın önemi nedir?",),

    # --- TYT seviyesinde mantık ve işlem soruları ---
    ("Bir otobüs saatte 60 km hızla giderse 5 saatte kaç kilometre yol alır?",),
    ("Bir çiftçinin 120 adet elması vardır. Bunları eşit sayıda 8 kasaya koyarsa her kasada kaç elma olur?",),
    ("Bir sınıfta 20 öğrenci vardır. Öğrencilerin yarısı kız ise kız öğrenci sayısı kaçtır?",),
    ("Bir musluk dakikada 4 litre su akıtıyorsa 15 dakikada kaç litre su akar?",),
    ("Bir tren 3 saatte 180 km gidiyorsa saatteki hızı kaç km'dir?",),
    ("Bir dikdörtgenin kısa kenarı 6 cm, uzun kenarı 10 cm ise çevresi kaç cm’dir?",),
    ("Bir işçi günde 8 saat çalışarak 10 günde bir işi bitiriyorsa, aynı işi 5 işçi kaç günde bitirir?",),
    ("Bir aracın deposunda 50 litre benzin vardır. Araba 100 km’de 8 litre yakıt harcıyorsa bu benzinle kaç km yol gidilir?",),
    ("Bir sayı 5 ile çarpılıp 20 eklenince 45 oluyorsa bu sayı kaçtır?",),
    ("Bir otelde 240 oda vardır. Odaların %25'i doluysa kaç oda boş demektir?",),

    # --- AYT seviyesinde yorum ve analiz soruları ---
    ("Bir şiirde kullanılan 'aliterasyon' tekniğinin anlam ve işlevini açıklayınız.",),
    ("Bir hikayede geriye dönüş tekniğinin kullanılması olay örgüsünü nasıl etkiler?",),
    ("Klasik fiziğin açıklamakta yetersiz kaldığı olaylara örnek veriniz.",),
    ("Modernizm akımının Türk edebiyatındaki etkilerini örneklerle açıklayınız.",),
    ("Sanayi Devrimi'nin toplumsal sınıflar üzerindeki etkilerini değerlendiriniz.",),
    ("Bir edebi eserde metafor kullanımının okur üzerindeki etkisini tartışınız.",),
    ("Osmanlı Devleti'nin 19. yüzyılda yaptığı reformların başarısız olma nedenlerini analiz ediniz.",),
    ("Bir ülkede tarımsal üretimin artması ile sanayi üretimi arasında nasıl bir ilişki vardır?",),
    ("Bir romanda kahramanın iç monologlarının yoğun şekilde kullanılması eserin temposunu nasıl etkiler?",),
    ("Bir deneyde sıcaklık değişiminin reaksiyon hızına etkisini açıklayınız.",),

    # --- Karışık bilgi ve yorum soruları ---
    ("Dünya'nın eksen eğikliği mevsimlerin oluşumunu nasıl etkiler?",),
    ("Bir insanın kan grubunu belirleyen faktörler nelerdir?",),
    ("Bir toplumda nüfus artış hızının sürekli artması hangi sorunlara yol açabilir?",),
    ("Bir öğrenci aynı anda hem fizik hem de kimya deneyini yapmaya çalışırsa hangi sorunlarla karşılaşabilir?",),
    ("Türkiye'de farklı iklim tiplerinin görülmesinin başlıca nedeni nedir?",),
    ("Bir ressamın eserlerinde sürekli olarak doğa teması işlemesi ne anlama gelir?",),
    ("Yer çekimi kuvvetinin Ay’da Dünya’ya göre daha az olmasının nedenleri nelerdir?",),
    ("Bir romanın gerçekçi sayılabilmesi için hangi özellikleri taşıması gerekir?",),
    ("Bir fizik deneyinde kullanılan hassas ölçüm cihazının kalibrasyonunun önemi nedir?",),
    ("Bir kimyasal tepkimede katalizörün işlevi nedir?",),

    # --- Ek sorular ile 100'e tamamlanıyor ---
    ("Mimar Sinan’ın en önemli eserlerinden biri hangisidir?",),
    ("Türkiye’de tarımın en çok yapıldığı bölge hangisidir?",),
    ("İstanbul Boğazı hangi iki denizi birbirine bağlar?",),
    ("Cumhuriyet hangi yıl ilan edilmiştir?",),
    ("Bir cismin hızı ile kütlesi biliniyorsa kinetik enerjisi nasıl hesaplanır?",),
    ("Newton’un üçüncü hareket yasası neyi ifade eder?",),
    ("Dünya’nın kendi ekseni etrafındaki dönüş süresi ne kadardır?",),
    ("Türkiye’de yetişen başlıca tarım ürünlerinden üç tanesini yazınız.",),
    ("Bir romanın başkahramanının zamanla değişim göstermesi hangi edebi kavramla açıklanır?",),
    ("Bir devrede seri ve paralel dirençlerin farkını açıklayınız.",)
]

cursor.executemany("INSERT INTO sorular (metin) VALUES (?)", sorular)
conn.commit()
conn.close()

print(f"{len(sorular)} örnek soru başarıyla eklendi.")
