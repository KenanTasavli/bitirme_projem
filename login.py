# -*- coding: utf-8 -*-
"""
AFAD – Kurtarıcı Girişi
• Başarılı oturumdan 1,5 s sonra araekran.py açılır.
"""
import sys, sqlite3
from PyQt5.QtCore    import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from login_yeni_donusturulen import Ui_MainWindow as LoginUI      # giriş arayüzü
from sign_deneme             import Signin_Page                   # kayıt arayüzü
from araekran                import Ui_MainWindow as AraEkranUI   # ara ekran arayüzü

# --------------------------------------------------------------------------- #
def delay_show(window, delay_ms: int = 1500):
    """Pencereyi delay_ms ms sonra gösterir (basit bekleme)."""
    QTimer.singleShot(delay_ms, window.show)

# --------------------------------------------------------------------------- #
class LoginPage(QMainWindow, LoginUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)                       # UI kur

        # Veritabanı
        self.conn   = sqlite3.connect("gui_arayuz.db")
        self.cursor = self.conn.cursor()

        # Sinyaller
        self.btn_login.clicked.connect(self.try_login)
        self.btn_signup.clicked.connect(self.open_signup)

    # ----------------------------- Giriş Kontrol --------------------------- #
    def try_login(self):
        kadi  = self.le_user.text().strip()
        sifre = self.le_pass.text().strip()

        if not kadi or not sifre:
            QMessageBox.warning(self, "Eksik", "Kullanıcı adı / şifre girin.")
            return

        try:
            self.cursor.execute("SELECT 1 FROM users WHERE kullanici_adi=? AND sifre=?",
                                (kadi, sifre))
            if self.cursor.fetchone():                      # başarı
                self.open_araekran_delayed()
            else:
                QMessageBox.warning(self, "Hata",
                                    "Geçersiz kullanıcı adı veya şifre.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", str(e))

    # ------------------- Ara ekranı 1,5 s sonra aç ------------------------- #
    def open_araekran_delayed(self):
        self.ara_win = QMainWindow()
        self.ara_ui  = AraEkranUI()
        self.ara_ui.setupUi(self.ara_win)

        delay_show(self.ara_win, 1500)     # 1,5 s sonra görün
        QTimer.singleShot(1500, self.close)  # aynı anda login kapanır

    # --------------------------- Kayıt Ekranı ------------------------------ #
    def open_signup(self):
        self.signup = Signin_Page()
        delay_show(self.signup, 300)        # küçük gecikme ile aç
        self.close()

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())
