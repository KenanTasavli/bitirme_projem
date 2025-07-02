# Deprem Tweet Adres Tespit Paneli
Türkiye'deki afet durumlarında sosyal medya üzerinden gelen yardım çağrılarını analiz ederek, konum bilgilerini otomatik olarak çıkartan bir masaüstü uygulamadır. Uygulama, Twitter'dan alınan veri setlerini şehir bazlı işler, BiLSTM-CRF modeliyle tweet içinden adresleri bulur ve kullanıcıya kolay arayüz sunar.
---
## 🚀 Özellikler

- ✅ BiLSTM-CRF modeli ile Türkçe tweetlerden konum çıkarımı
- ✅ Şehir bazlı tweet listesi gösterimi
- ✅ Tweet temizleme ve adres tahmini
- ✅ Google Maps ile haritada konum görüntüleme
- ✅ PyQt5 ile modern kullanıcı arayüzü

---
## 🏗️ Proje Yapısı
gui_deprem/
├── anaekran.py # Ana uygulama ekranı (tweet gösterimi)
├── araekran.py # Başlangıç ekranı (şehir seçimi)
├── gorevlerim.py # Onaylanmış adres detayları ekranı
├── data_bursa.json # Bursa şehri için tweet verisi
├── data_istanbul.json # İstanbul şehri için tweet verisi
├── data_deprem.json # Diğer şehirler için genel deprem tweetleri
├── bilstm_crf2.pt # Eğitilmiş BiLSTM-CRF PyTorch modeli
├── dataset_bilstm.py # Veri seti etiket yapısı
├── train_bilstm_crf.py # Model eğitimi kodu (dış kaynak)
└── AFAD-Logo-Renkli.png # Arayüzde kullanılan logo

Uygulamayı çalıştırma
python gui_deprem/araekran.py

📊 Veri Formatı
{
  "city": "Hatay",
  "timestamp": "06.02.2023 15:35",
  "tweet": "Samandağ Karaçay Karakolu yakınında aile çadır bekliyor"
}

🔍 Kullanım
Uygulama başladığında şehir seçimi ekranı açılır.

Şehir seçildikten sonra sistem, o şehir için ilgili veri dosyasını yükler.

Tweetler listelenir. Detay panelinde tweet ham haliyle, temizlenmiş haliyle ve çıkarılan adresle gösterilir.

Tweet onaylanırsa CSV dosyasına eklenir.

Haritada adresi görüntülemek için “HARİTADA GÖSTER” butonuna tıklanabilir.

🧠 Model Bilgisi
Bu projede Türkçe tweetlerde yer alan adres ifadelerini bulmak için BiLSTM-CRF tabanlı bir dizi etiketleme modeli kullanılmıştır. Model, PyTorch ile eğitilmiş ve bilstm_crf2.pt dosyasına kaydedilmiştir.

Etiketleme şeması: B-LOC, I-LOC, O

✍️ Geliştirici
Kenan TAŞAVLI
2025 • Bitirme Projesi • [Bursa Teknik Üniversitesi]

