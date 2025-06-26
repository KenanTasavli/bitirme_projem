# login_gui.py
# -*- coding: utf-8 -*-
"""
AFAD – Tweet Adres Tespiti • Kurtarıcı Girişi
Renklendirme: koyu mavi (#1E2D3A) arka plan, araekran/anaekran ile uyumlu.
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap

# --------------------------------------------------------------------------- #
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # ---------------- Pencere ----------------------------------------- #
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 760)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(MainWindow, objectName="centralwidget")
        self.vlayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # ---------------- Arka Çerçeve (drop-shadow frame) ---------------- #
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("""
            QFrame{
                background:#1E2D3A;
                border-radius:20px;
            }
        """)
        self.frame.setObjectName("dropShadowFrame")

        # ---------------- AFAD Logo -------------------------------------- #
        self.logo = QtWidgets.QLabel(self.frame)
        self.logo.setGeometry(20, 20, 120, 120)
        pix = QPixmap(r"D:\Code\Bitirme\gui_deprem\AFAD-Logo-Renkli.png")
        if not pix.isNull():
            pix = pix.scaled(120, 120, QtCore.Qt.KeepAspectRatio,
                             QtCore.Qt.SmoothTransformation)
            self.logo.setPixmap(pix)

        # ---------------- Başlık & Alt-başlık ---------------------------- #
        self.label_title = QtWidgets.QLabel("AFAD KURTARICI GİRİŞİ", self.frame)
        self.label_title.setGeometry(0, 160, 640, 60)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("color:#EAF0F6;font:600 32px 'Segoe UI';")

        self.label_desc = QtWidgets.QLabel("Tweet Adres Tespiti Sistemi", self.frame)
        self.label_desc.setGeometry(0, 218, 640, 24)
        self.label_desc.setAlignment(QtCore.Qt.AlignCenter)
        self.label_desc.setStyleSheet("color:#98A6BD;font:16px 'Segoe UI';")

        # ---------------- Giriş Kartı ------------------------------------ #
        self.card = QtWidgets.QFrame(self.frame)
        self.card.setGeometry(160, 270, 320, 430)
        self.card.setStyleSheet("""
            QFrame{background-color:rgba(255,255,255,0.08);border-radius:18px;}
        """)

        # --- kart başlığı
        self.card_title = QtWidgets.QLabel("Giriş Paneli", self.card)
        self.card_title.setGeometry(0, 20, 320, 30)
        self.card_title.setAlignment(QtCore.Qt.AlignCenter)
        self.card_title.setStyleSheet("color:#EAF0F6;font:600 20px 'Segoe UI';")

        # --- kullanıcı adı
        self.le_user = QtWidgets.QLineEdit(self.card)
        self.le_user.setGeometry(60, 90, 200, 40)
        self._stylize_lineedit(self.le_user, "Kullanıcı Adı")

        # --- şifre
        self.le_pass = QtWidgets.QLineEdit(self.card)
        self.le_pass.setGeometry(60, 160, 200, 40)
        self._stylize_lineedit(self.le_pass, "Şifre", echo=QtWidgets.QLineEdit.Password)

        # --- Giriş Yap butonu
        self.btn_login = QtWidgets.QPushButton("Giriş Yap", self.card)
        self.btn_login.setGeometry(60, 230, 200, 45)
        self._stylize_button(self.btn_login)

        # --- Kayıt Ol butonu
        self.btn_signup = QtWidgets.QPushButton("Kayıt Ol", self.card)
        self.btn_signup.setGeometry(60, 300, 200, 45)
        self._stylize_button(self.btn_signup, alt=True)

        # ----------------- Pencere Kontrol Düğmeleri ---------------------- #
        self.btn_close = QtWidgets.QPushButton(self.frame)
        self.btn_close.setGeometry(590, 20, 30, 30)
        self.btn_close.setStyleSheet("background:#f44336;border-radius:15px;")
        self.btn_close.clicked.connect(MainWindow.close)

        self.btn_min = QtWidgets.QPushButton(self.frame)
        self.btn_min.setGeometry(550, 20, 30, 30)
        self.btn_min.setStyleSheet("background:#FFA500;border-radius:15px;")
        self.btn_min.clicked.connect(MainWindow.showMinimized)

        # ---------------- Kaydet Layout ---------------------------------- #
        self.vlayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ------------------------------------------------------------------- #
    def _stylize_lineedit(self, w: QtWidgets.QLineEdit, ph, *, echo=None):
        w.setPlaceholderText(ph)
        if echo: w.setEchoMode(echo)
        w.setStyleSheet("""
            QLineEdit{
                background:transparent;
                border:none;
                border-bottom:2px solid #537A9C;
                color:#EAF0F6;padding-bottom:6px;
            }
            QLineEdit:focus{border-bottom:2px solid #EAF0F6;}
        """)
        w.setFont(QtGui.QFont("Segoe UI", 10))

    def _stylize_button(self, b: QtWidgets.QPushButton, alt=False):
        if alt:
            bg1, bg2 = "#FF557F", "#FFAA7F"
        else:
            bg1, bg2 = "#3D5A80", "#537A9C"
        b.setStyleSheet(f"""
            QPushButton {{
                background:{bg1};
                color:white;border-radius:20px;
            }}
            QPushButton:hover{{background:{bg2};}}
            QPushButton:pressed{{background:#2B445E;}}
        """)
        b.setFont(QtGui.QFont("Segoe UI", 12, weight=QtGui.QFont.Bold))

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw  = QtWidgets.QMainWindow()
    ui  = Ui_MainWindow()
    ui.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())
