# gorevlerim.py
# -*- coding: utf-8 -*-
"""
AFAD • Kurtarıcı Görev Paneli
- Aktif görev detayları
- Haritada Göster, Görevi Tamamla, GERİ (kırmızı) butonu
- Geçmiş görev listesinde çift tıkla konum aç
"""
import sys, webbrowser, urllib.parse
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GorevWindow(object):
    def __init__(self, task_dict: dict, history: list, city_name: str):
        self.task = task_dict          # aktif görev
        self.hist = history            # onaylanan geçmiş
        self.city = city_name          # geri dönülecek şehir

    # --------------------------- UI Kurulumu ----------------------------- #
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.resize(850, 640)
        MainWindow.setStyleSheet(self._style())

        self.central = QtWidgets.QWidget(MainWindow, objectName="central")
        MainWindow.setCentralWidget(self.central)

        # ---- Üst şerit (degrade) --------------------------------------- #
        bar = QtWidgets.QFrame(self.central)
        bar.setGeometry(0, 0, 850, 60)
        bar.setStyleSheet("QFrame{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #3D5A80, stop:1 #537A9C);}")
        lbl = QtWidgets.QLabel("GÖREV PANELİ", bar)
        lbl.setGeometry(0, 0, 850, 60)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.setStyleSheet("color:white;font:600 26px 'Segoe UI';")

        self._window_controls(bar)

        # ---- Aktif Görev Kartı ---------------------------------------- #
        card = QtWidgets.QFrame(self.central)
        card.setGeometry(25, 80, 800, 230)
        card.setStyleSheet("QFrame{background:#243546;border-radius:16px;}")

        self.txt_detail = QtWidgets.QTextEdit(card)
        self.txt_detail.setGeometry(20, 20, 760, 150)
        self.txt_detail.setReadOnly(True)
        self.txt_detail.setStyleSheet("background:#1E2D3A;border-radius:10px;")

        # Butonlar (aralıklı)
        self.btn_map = QtWidgets.QPushButton("HARİTADA GÖSTER", card)
        self.btn_map.setGeometry(140, 185, 180, 35)
        self.btn_map.setStyleSheet(self._btn())
        self.btn_map.clicked.connect(self._open_map)

        self.btn_done = QtWidgets.QPushButton("GÖREVİ TAMAMLA", card)
        self.btn_done.setGeometry(340, 185, 180, 35)
        self.btn_done.setStyleSheet(self._btn("#2E7D32", "#43A047"))
        self.btn_done.clicked.connect(self._mark_done)

        self.btn_back = QtWidgets.QPushButton("GERİ", card)
        self.btn_back.setGeometry(560, 185, 150, 35)
        self.btn_back.setStyleSheet(self._btn("#C62828", "#E53935"))  # kırmızı
        self.btn_back.clicked.connect(self._go_back)

        # ---- Geçmiş Liste --------------------------------------------- #
        lbl_hist = QtWidgets.QLabel("Geçmiş Görevler", self.central)
        lbl_hist.setGeometry(25, 330, 800, 28)
        lbl_hist.setAlignment(QtCore.Qt.AlignCenter)
        lbl_hist.setStyleSheet("font:600 20px 'Segoe UI';")

        self.lst_hist = QtWidgets.QListWidget(self.central)
        self.lst_hist.setGeometry(25, 360, 800, 250)
        self.lst_hist.setStyleSheet("background:#1E2D3A;border-radius:12px;")
        self.lst_hist.itemDoubleClicked.connect(self._map_from_history)

        # Verileri doldur
        self._fill_detail(); self._fill_history()

    # -------------------- Yardımcı Metotlar ------------------------------ #
    def _fill_detail(self):
        d = self.task
        self.txt_detail.setHtml(
            f"<b>Zaman :</b> {d['timestamp']}<br><br>"
            f"<b>Tweet :</b><br>{d['tweet']}<br><br>"
            f"<b>Adres :</b><br>{d['address']}"
        )

    def _fill_history(self):
        self.lst_hist.clear()
        for i, d in enumerate(self.hist[::-1], 1):
            self.lst_hist.addItem(f"{i}. {d['timestamp']}  –  {d['address']}")

    # -------------------- Eylemler --------------------------------------- #
    def _open_map(self):
        url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(self.task['address'])}"
        webbrowser.open(url)

    def _map_from_history(self, item):
        addr = item.text().split("–", 1)[-1].strip()
        webbrowser.open("https://www.google.com/maps/search/?api=1&query=" +
                        urllib.parse.quote_plus(addr))

    def _mark_done(self):
        QtWidgets.QMessageBox.information(self.MainWindow, "Tamamlandı", "Görev tamamlandı!")
        self.btn_done.setEnabled(False)

    def _go_back(self):
        from anaekran import Ui_MainWindow as AnaUI
        self.backWin = QtWidgets.QMainWindow()
        self.backUI  = AnaUI(city_name=self.city)
        self.backUI.setupUi(self.backWin)
        self.backWin.show()
        self.MainWindow.close()

    # -------------------- Stil ------------------------------------------ #
    def _style(self):
        return """*{border:none;background:transparent;color:#EAF0F6;font-family:Arial;}
                  #central{background:#1E2D3A;border:2px solid #3D5A80;border-radius:20px;}"""

    def _btn(self, base="#3D5A80", hov="#537A9C"):
        return f"""QPushButton{{background:{base};border-radius:10px;font-size:16px;font-weight:bold;}}
                   QPushButton:hover{{background:{hov};}}
                   QPushButton:pressed{{background:#2B445E;}}"""

    def _window_controls(self, parent):
        btn_min = QtWidgets.QPushButton("-", parent)
        btn_min.setGeometry(760, 12, 30, 30)
        btn_min.setStyleSheet("background:#FFA500;font-size:20px;border-radius:4px;")
        btn_min.clicked.connect(self.MainWindow.showMinimized)
        btn_close = QtWidgets.QPushButton("X", parent)
        btn_close.setGeometry(800, 12, 30, 30)
        btn_close.setStyleSheet("background:#f44336;font-size:20px;border-radius:4px;")
        btn_close.clicked.connect(self.MainWindow.close)

# ----------------------- Test ------------------------------------------- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    sample = {"timestamp":"Şimdi","tweet":"Örnek tweet","address":"Örnek adres"}
    ui = Ui_GorevWindow(sample, [sample], "Bursa")
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())
