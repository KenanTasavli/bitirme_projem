import pandas as pd
import json
import re

# JSON dosyasındaki ilçe ve şehir bilgilerini yükleyelim
ilceler_path = r'D:\Code\Bitirme\py\ilceler.json'  # JSON dosyasının yolu
with open(ilceler_path, 'r', encoding='utf-8') as f:
    ilceler_data = json.load(f)

# İl bilgilerini çıkaralım
sehir_list = [item['sehir_adi'].lower() for item in ilceler_data]

# Excel dosyasını yükleyelim
excel_path = r'D:\Code\Bitirme\temizlenmis_veri\yardim_isteyen_tweetler_1439_7Subat_temizveri.xlsx'  # Excel dosyasının yolu
df = pd.read_excel(excel_path)

# NaN değerlerini boş string ile değiştirelim
df['data'] = df['data'].fillna('')

# Tweetlerdeki şehir isimlerini ayıralım ve birleşik kelimeleri düzelterek boşluk ekleyelim
def ayir_birlesik_sehirler_v2(tweet, sehir_list):
    tweet = tweet.lower()

    # Her şehir ismini tweet içinde arayalım
    for sehir in sehir_list:
        if sehir in tweet:
            # Şehir adının birleşik kelimeleri varsa, boşluk ekleyelim
            tweet = re.sub(r'(\b' + re.escape(sehir) + r')(\w)', r'\1 \2', tweet)

    return tweet

# Her tweet için ayırma işlemi uygulayalım
df['sehir_ayrilmis'] = df['data'].apply(lambda tweet: ayir_birlesik_sehirler_v2(str(tweet), sehir_list))

# Yeni Excel dosyasını kaydedelim
output_path = r'D:\Code\Bitirme\temizlenmis_veri\tokendata_fixed_sehir_v2.xlsx'  # Yeni dosya yolu
df.to_excel(output_path, index=False)

output_path  # Yeni Excel dosyasının yolu
