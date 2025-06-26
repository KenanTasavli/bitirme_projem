import pandas as pd
import json
import re

# JSON dosyasındaki ilçe ve şehir bilgilerini yükleyelim
ilceler_path = r'D:\Code\Bitirme\py\ilceler.json'  # JSON dosyasının yolu
with open(ilceler_path, 'r', encoding='utf-8') as f:
    ilceler_data = json.load(f)

# İl bilgilerini çıkaralım
sehir_list = [item['sehir_adi'].lower() for item in ilceler_data]
mahalle_sokak_list = [item['ilce_adi'].lower() for item in ilceler_data]  # İlçe isimlerini de listeledik

# Excel dosyasını yükleyelim
excel_path = r'D:\Code\Bitirme\temizlenmis_veri\yardim_isteyen_tweetler_0331_8Subat_temizveri.xlsx'  # Excel dosyasının yolu
df = pd.read_excel(excel_path)

# NaN değerlerini boş string ile değiştirelim
df['data'] = df['data'].fillna('')

# Mahalle, Sokak ve Cadde için kısaltmaların düzeltilmesi
def duzenle_mah_sokak(tweet):
    tweet = tweet.lower()

    # Mahalle kısaltması düzeltme
    tweet = tweet.replace(" mh", " mahalle")  # mh -> mahalle
    tweet = tweet.replace(" mah", " mahalle")  # mah -> mahalle
    tweet = tweet.replace(" mh.", " mahalle")  # mh. -> mahalle

    # Sokak kısaltması düzeltme
    tweet = tweet.replace(" sk", " sokak")  # sk -> sokak
    tweet = tweet.replace(" cad", " cadde")  # cad -> cadde
    tweet = tweet.replace(" sk.", " sokak")  # sk. -> sokak
    tweet = tweet.replace(" cad.", " cadde")  # cad. -> cadde

    return tweet

# Kişisel adları ve sokakları ayırma işlemi
def ayir_kisisel_ve_sokak(tweet):
    tweet = tweet.lower()

    # Eğer bir sokak adı kişisel bir adla birleşmişse (örneğin, "İbrahim Karakülah Caddesi")
    # Ad ve sokak adlarını ayıralım
    tweet = re.sub(r'(\b\w+)(\s+)(\b\w+)(\s+)(cadde|sokak)', r'\1 \3 \4 \5', tweet)
    # Örneğin: "ibrahim karakülah caddesi" -> "ibrahim karakülah caddesi" (doğru ayırma)

    return tweet

# Tweetlerdeki birleşik şehir ve ilçe isimlerini ayıralım
def ayir_birlesik_sehir(tweet, sehir_list):
    tweet = tweet.lower()

    # Şehir ismini tweet içinde arayalım
    for sehir in sehir_list:
        if sehir in tweet:
            # Şehir adının birleşik kelimeleri varsa, boşluk ekleyelim
            tweet = re.sub(r'(\b' + re.escape(sehir) + r')(\w)', r'\1 \2', tweet)

    return tweet

# Tweetlerdeki birleşik şehir ve ilçe isimlerini ve fiil + yer adlarını ayıralım
def ayir_birlesik_sehir_v5(tweet, sehir_list, mahalle_sokak_list):
    tweet = tweet.lower()

    # Şehir ve ilçe ismi birleşikse ayıralım
    for sehir in sehir_list:
        if sehir in tweet:
            tweet = re.sub(r'(\b' + re.escape(sehir) + r')(\w)', r'\1 \2', tweet)

    # Mahalle, Sokak ve Cadde için kısaltma düzeltmeleri
    tweet = duzenle_mah_sokak(tweet)  

    # Kişisel adlar ve sokaklar arasındaki boşluk eklemeleri
    tweet = ayir_kisisel_ve_sokak(tweet)

    return tweet

# Her tweet için ayırma işlemi uygulayalım
df['sehir_ayrilmis'] = df['data'].apply(lambda tweet: ayir_birlesik_sehir_v5(str(tweet), sehir_list, mahalle_sokak_list))

# Yeni Excel dosyasını kaydedelim
output_path = r'D:\Code\Bitirme\temizlenmis_veri\tokendata_fixed_sehir_sokak_v7.xlsx'  # Yeni dosya yolu
df.to_excel(output_path, index=False)

output_path  # Yeni Excel dosyasının yolu
