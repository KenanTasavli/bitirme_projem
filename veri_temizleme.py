import os
import pandas as pd
import re

# 1. Temizleme Fonksiyonu (Türkçe karakterlerin kaybolmaması için düzenleme yapıyoruz)
def temizle(tweet):
    if isinstance(tweet, str):  # Sadece metin içeren hücreler üzerinde işlem yap
        # Küçük harfe dönüştürme
        tweet = tweet.lower()
        # URL'leri kaldırma
        tweet = re.sub(r'http\S+', '', tweet)
        # Mentionları (@kullaniciadi) kaldırma
        tweet = re.sub(r'@\w+', '', tweet)
        # Hashtagleri (#etiket) kaldırma
        tweet = re.sub(r'#\w+', '', tweet)
        # Emojileri temizleme (Emoji dışındaki karakterleri temizlemek için)
        tweet = re.sub(r'[^\w\s,.-ıİğĞüÜşŞçÇöÖ]', '', tweet)  # Burada Türkçe karakterler korunuyor
        # Noktalama işaretlerini kaldırma (isteğe bağlı, eğer isteniyorsa)
        tweet = re.sub(r'[^\w\s]', '', tweet)
    
    return tweet

# 2. Klasördeki tüm dosyaları oku ve işle
input_folder = r'D:\Code\Bitirme\deprem_tweetleri'  # Verilerin bulunduğu klasör
output_folder = r'D:\Code\Bitirme\temizlenmis_veri'  # Temiz verilerin kaydedileceği klasör

# Klasördeki tüm dosyaları listele
for filename in os.listdir(input_folder):
    if filename.endswith('.xlsx'):  # Sadece Excel dosyalarını işle
        file_path = os.path.join(input_folder, filename)
        
        # 3. Excel dosyasını okuma
        df = pd.read_excel(file_path)
        
        # 4. Sadece 'data' sütununu seç
        if 'data' in df.columns:  # 'data' sütunu olup olmadığını kontrol et
            # 5. 'data' sütunundaki her bir tweet'i temizle
            df['data'] = df['data'].apply(temizle)  # 'data' sütununu temizle
            
            # 6. Yeni dosyaya kaydetme (sadece 'data' sütununu içerecek)
            output_file = os.path.join(output_folder, filename.replace('.xlsx', '_temizveri.xlsx'))
            df[['data']].to_excel(output_file, index=False)  # Yalnızca 'data' sütununu kaydet
            
            print(f"Temizlenmiş dosya kaydedildi: {output_file}")
        else:
            print(f"'{filename}' dosyasında 'data' sütunu bulunamadı.")
