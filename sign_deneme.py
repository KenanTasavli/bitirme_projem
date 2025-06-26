from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from sign_up_donusturulen import Ui_MainWindow  # Kayıt sayfasının arayüzü
import sqlite3
import re


class Signin_Page(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.signform = Ui_MainWindow()  # Arayüz formunu yükle
        self.signform.setupUi(self)  # Formu başlat
        self.signform.pushButton_kayit_ol_sayfa.clicked.connect(self.KayitOl)  # Kayıt ol butonuna bağlantı

        # Veritabanı bağlantısı
        self.connection = sqlite3.connect('gui_arayuz.db')
        self.cursor = self.connection.cursor()

        # Tablo yoksa oluştur
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "users" (
                "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                "kullanici_adi" TEXT NOT NULL,
                "sifre" TEXT NOT NULL,
                "email" TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def is_valid_email(self, email):
        """
        Basit bir email doğrulama regex'i
        """
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email)

    def KayitOl(self):
        """
        Kullanıcının girdiği bilgileri veritabanına kaydeder.
        """
        from login import Login_Sayfa

        # Kullanıcıdan bilgileri al
        kadi = self.signform.lineEdit_kullanici_adi_kayit.text()
        email = self.signform.lineEdit_mail.text()
        parola = self.signform.lineEdit_sifre_parola_kayit.text()
        parola_tekrar = self.signform.lineEdit_sifre_tekrar.text()

        # Alan kontrolü
        if not kadi or not email or not parola:
            QMessageBox.warning(self, "Hata!", "Lütfen tüm alanları doldurun!")
            return

        if parola != parola_tekrar:
            QMessageBox.warning(self, "Hata!", "Parolalar eşleşmiyor!")
            return

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Hata!", "Geçersiz email formatı!")
            return

        try:
            # Veritabanına kullanıcı ekle
            self.cursor.execute('''
                INSERT INTO "users" ("kullanici_adi", "email", "sifre")
                VALUES (?, ?, ?)
            ''', (kadi, email, parola))
            self.connection.commit()
            print("Veritabanına kayıt eklendi:", kadi, email)
            QMessageBox.information(self, "Başarılı", "Kayıt işlemi başarılı!")
        except sqlite3.Error as e:
            print("SQLite Hatası:", str(e))
            QMessageBox.critical(self, "Hata!", f"Veritabanı hatası: {str(e)}")
            return

        # Giriş sayfasına geçiş
        self.close()
        self.login_page = Login_Sayfa()
        self.login_page.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Signin_Page()
    window.show()
    sys.exit(app.exec_())
