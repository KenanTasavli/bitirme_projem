import os
import pandas as pd

# Dosya yolunu belirtin
file_path = r"D:\Code\Bitirme\temizlenmis_veri\yardim_isteyen_tweetler_2213_9Subat_temizveri.xlsx"

# Dosyanın varlığını kontrol et
if os.path.exists(file_path):
    print(f"Dosya bulundu: {file_path}")
    
    # Excel dosyasını oku
    df = pd.read_excel(file_path)
    
    # Satır aralığını alalım 
    tweets = df.iloc[4750:4780]  # pandas 0 tabanlı indekse sahip, bu yüzden 4:15 arası 5.-15. satırları kapsar.
    
    # Her bir tweet'i sırayla yazdıralım
    for idx, row in tweets.iterrows():
        print(f"{idx+1}. tweet: {row['data']}")  # 'Tweet' sütunu yerine dosyanızdaki tweet sütun adı neyse onu kullanmalısınız.
else:
    print(f"Dosya bulunamadı: {file_path}")
