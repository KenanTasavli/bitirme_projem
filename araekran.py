# -*- coding: utf-8 -*-
"""
araekran.py – AFAD Tweet Adres Tespiti • Görev Seçim Ekranı
• “Görev Bul” tıklandığında anaekran 1,5 s gecikmeyle açılır.
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtGui  import QPixmap
from anaekran     import Ui_MainWindow as AnaEkranUI

# ---------------- Basit gecikmeli gösterici ------------------------------- #
def delay_show(window, delay_ms: int = 1500):
    QTimer.singleShot(delay_ms, window.show)

# ---------------- İl listesi (kısaltılmadı) ------------------------------- #
TURKEY_CITIES = [
    "Adana","Adıyaman","Afyonkarahisar","Ağrı","Aksaray","Amasya","Ankara","Antalya",
    "Ardahan","Artvin","Aydın","Balıkesir","Bartın","Batman","Bayburt","Bilecik",
    "Bingöl","Bitlis","Bolu","Burdur","Bursa","Çanakkale","Çankırı","Çorum","Denizli",
    "Diyarbakır","Düzce","Edirne","Elazığ","Erzincan","Erzurum","Eskişehir","Gaziantep",
    "Giresun","Gümüşhane","Hakkâri","Hatay","Iğdır","Isparta","İstanbul","İzmir",
    "Kahramanmaraş","Karabük","Karaman","Kars","Kastamonu","Kayseri","Kırıkkale",
    "Kırklareli","Kırşehir","Kilis","Kocaeli","Konya","Kütahya","Malatya","Manisa",
    "Mardin","Mersin","Muğla","Muş","Nevşehir","Niğde","Ordu","Osmaniye","Rize",
    "Sakarya","Samsun","Siirt","Sinop","Sivas","Şanlıurfa","Şırnak","Tekirdağ",
    "Tokat","Trabzon","Tunceli","Uşak","Van","Yalova","Yozgat","Zonguldak"
]

# --------------------------------------------------------------------------- #
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.resize(960, 680)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setStyleSheet(self._modern_style())

        self.centralwidget = QtWidgets.QWidget(MainWindow, objectName="centralwidget")

        # Başlık
        self.lbl_title = QtWidgets.QLabel("AFAD – Tweet Adres Tespiti | Görev Seçim",
                                          self.centralwidget)
        self.lbl_title.setGeometry(0, 20, 960, 40)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setStyleSheet("font-size:28px;font-weight:bold;")

        # Şehir seçimi
        self.lbl_city = QtWidgets.QLabel("Görev Şehri", self.centralwidget)
        self.lbl_city.setGeometry(70, 130, 200, 32)

        self.cmb_city = QtWidgets.QComboBox(self.centralwidget)
        self.cmb_city.setGeometry(300, 125, 300, 50)
        self.cmb_city.addItems(TURKEY_CITIES)
        self.cmb_city.setEditable(True)
        self.cmb_city.completer().setFilterMode(QtCore.Qt.MatchContains)

        # Başlangıç zamanı
        self.lbl_start = QtWidgets.QLabel("Operasyon Başlangıcı", self.centralwidget)
        self.lbl_start.setGeometry(70, 230, 200, 32)

        self.dt_start = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dt_start.setGeometry(300, 225, 300, 50)
        self.dt_start.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        self.dt_start.setCalendarPopup(True)
        now = QDateTime.currentDateTime()
        self.dt_start.setDateTime(now)
        self.dt_start.setMinimumDateTime(now)

        # Model (RO)
        self.lbl_model = QtWidgets.QLabel("Model", self.centralwidget)
        self.lbl_model.setGeometry(70, 330, 200, 32)

        self.le_model = QtWidgets.QLineEdit(self.centralwidget)
        self.le_model.setGeometry(300, 325, 300, 50)
        self.le_model.setText("Tweet Adres Tespiti")
        self.le_model.setReadOnly(True)

        # Görev Bul
        self.btn_start = QtWidgets.QPushButton("Görev Bul", self.centralwidget)
        self.btn_start.setGeometry(380, 440, 200, 60)
        self.btn_start.clicked.connect(self.launch_dashboard)

        # Logo
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(20, 490, 250, 250)
        pix = QPixmap(r"D:\Code\Bitirme\gui_deprem\AFAD-Logo-Renkli.png")
        if not pix.isNull():
            pix = pix.scaled(250, 250, QtCore.Qt.KeepAspectRatio,
                             QtCore.Qt.SmoothTransformation)
            self.logo.setPixmap(pix)

        self._create_window_controls()
        MainWindow.setCentralWidget(self.centralwidget)

    # ---------------- Görev Bul ------------------------------------------- #
    def launch_dashboard(self):
        city = self.cmb_city.currentText().strip()
        if not city:
            QtWidgets.QMessageBox.warning(self.MainWindow, "Eksik Bilgi",
                                          "Lütfen görev yapacağınız şehri seçin.")
            return
        self.dash = QtWidgets.QMainWindow()
        self.dash_ui = AnaEkranUI(city_name=city)
        self.dash_ui.setupUi(self.dash)

        delay_show(self.dash, 1500)   # 1,5 s sonra anaekran görünür
        QTimer.singleShot(1500, self.MainWindow.close)  # bu pencere kapanır

    # ---------------- Stil & Kontrol düğmeleri ---------------------------- #
    def _modern_style(self):
        return """
        *{border:none;background:transparent;color:#EAF0F6;font-family:Arial;font-size:18px;}
        #centralwidget{background:#1E2D3A;border-radius:20px;border:2px solid #3D5A80;}
        QLabel{font-weight:bold;font-size:20px;}
        QComboBox,QDateTimeEdit,QLineEdit{
            padding:10px;background:#3D5A80;border-radius:10px;border:2px solid #537A9C;}
        QComboBox:hover,QDateTimeEdit:hover{border-color:#3D5A80;}
        QPushButton{
            padding:15px;background:#3D5A80;font-size:22px;font-weight:bold;border-radius:12px;}
        QPushButton:hover{background:#537A9C;} QPushButton:pressed{background:#2B445E;}
        """

    def _create_window_controls(self):
        frame = QtWidgets.QFrame(self.centralwidget)
        frame.setGeometry(820, 15, 120, 40)
        btn_min = QtWidgets.QPushButton("-", frame)
        btn_min.setGeometry(0, 0, 50, 40)
        btn_min.setStyleSheet("background:#FFA500;font-size:22px;border-radius:6px;")
        btn_min.clicked.connect(self.MainWindow.showMinimized)
        btn_close = QtWidgets.QPushButton("X", frame)
        btn_close.setGeometry(60, 0, 50, 40)
        btn_close.setStyleSheet("background:#f44336;font-size:22px;border-radius:6px;")
        btn_close.clicked.connect(self.MainWindow.close)

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(w)
    w.show()
    sys.exit(app.exec_())
