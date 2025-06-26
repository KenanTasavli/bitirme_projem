# anaekran.py
# -*- coding: utf-8 -*-
"""
AFAD – Tweet Adres Tespiti • Ana Panel
* ONAYLA  → görev paneli (gorevlerim.py) açılır, ana ekran kapanır
* Tweet onaylanınca _dummy_data listesinden silinir (başkaları görmez)
* Kalan 10 tweet 5-er saniyede bir eklenerek gerçek-zaman hissi verir
"""
import sys, webbrowser, urllib.parse
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap

from gorevlerim import Ui_GorevWindow   # değişmedi

# --------------------------------------------------------------------------- #
# Bursa için 15 tweet — ilk 5’i hemen, kalan 10’u akışta eklenecek
_all_tweets = [
    # --- ilk 5 (başlangıçta gözükecek) ---
    {"city":"Bursa","timestamp":"25.06.2025 14:10",
     "tweet":"Nilüfer FSM Bulvarı'nda apartman çöktü, yardım lazım!",
     "address":"FSM Bulvarı No:125 Nilüfer/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 14:22",
     "tweet":"Yıldırım Namazgah Mah. 3 kişi enkaz altında!",
     "address":"Namazgah Mah. 2. Paşa Sok. Yıldırım/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 14:35",
     "tweet":"Osmangazi Altıparmak Cad. bina ağır hasarlı, yaralılar var!",
     "address":"Altıparmak Cad. No:87 Osmangazi/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 14:41",
     "tweet":"Görükle Kampüsü KYK yurdunda çatlaklar oluştu, tahliye gerekiyor!",
     "address":"Görükle Kampüsü KYK Yurdu Nilüfer/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 14:55",
     "tweet":"Mudanya Halitpaşa’da apartmanda mahsur kalan aile var!",
     "address":"Halitpaşa Mah. Güneş Sk. Mudanya/Bursa"},
    # --- sonraki 10 (5-er saniyede bir akacak) ---
    {"city":"Bursa","timestamp":"25.06.2025 15:01",
     "tweet":"İnegöl Kültürpark civarında ağır hasarlı bina bildirildi!",
     "address":"Kültürpark Cad. No:4 İnegöl/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:05",
     "tweet":"Karacabey Uluabat kıyısında çadır ihtiyacı var!",
     "address":"Uluabat Mh. Yalı Sok. Karacabey/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:09",
     "tweet":"Gemlik Cumhuriyet Mah. bodrum katta ses var, ekip lazım!",
     "address":"Cumhuriyet Mah. Kordon Boyu Gemlik/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:12",
     "tweet":"Nilüfer Beşevler Metrosu yakınında yaralıların olduğu bildirildi!",
     "address":"Beşevler Mh. Kavakdibi Nilüfer/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:18",
     "tweet":"Yıldırım Değirmenönü İlkokulu bahçesinde toplananlar var, battaniye gerek!",
     "address":"Değirmenönü Mh. Okul Sk. Yıldırım/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:25",
     "tweet":"Orhaneli merkezde su hattı patladı, ekip yönlendirilmeli!",
     "address":"Orhaneli Meydan Orhaneli/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:32",
     "tweet":"Osmangazi Dikkaldırım Spor Salonu çatısı çöktü, yaralı var!",
     "address":"Dikkaldırım Mh. Spor Cd. Osmangazi/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:37",
     "tweet":"Hürriyet Mh. pazar yerinde çökme riski bildirildi!",
     "address":"Hürriyet Mh. Pazar Sk. Osmangazi/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:43",
     "tweet":"Nilüfer Odunluk TOKİ’de engelli vatandaş mahsur kaldı!",
     "address":"Odunluk Mh. TOKİ Blok Nilüfer/Bursa"},
    {"city":"Bursa","timestamp":"25.06.2025 15:50",
     "tweet":"İznik Yeşil Cami çevresinde tarihi yapıda hasar var!",
     "address":"Mecidiye Mh. Atatürk Cd. İznik/Bursa"}
]

# önce ilk 5 tweet tabloya gelecek
_dummy_data       = _all_tweets[:5]
_remaining_stream = _all_tweets[5:]

accepted_tasks = []          # onaylanan görevler

# --------------------------------------------------------------------------- #
class Ui_MainWindow(object):
    def __init__(self, city_name=""):
        self.city_name = city_name.strip() or "Şehir Seçilmedi"

    # ------------------------- Arayüz Kurulumu ----------------------------- #
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.resize(1200, 720)

        # ana pencere rengi de koyu mavi olsun; köşelerde siyah kalmaz
        MainWindow.setStyleSheet("background:#1E2D3A;")  

        self.centralwidget = QtWidgets.QWidget(MainWindow, objectName="centralwidget")
        self.centralwidget.setStyleSheet(self._modern_style())

        # Başlık
        self.lbl_title = QtWidgets.QLabel(self.centralwidget)
        self.lbl_title.setGeometry(20, 15, 700, 40)
        self.lbl_title.setText(f"AFAD – Tweet Adres Tespiti  |  Şehir: {self.city_name}")
        self.lbl_title.setStyleSheet("font-size:26px;font-weight:bold;")

        self._create_window_controls()

        # ---------------- Sol Tweet Tablosu -------------------- #
        self.tbl_requests = QtWidgets.QTableWidget(self.centralwidget)
        self.tbl_requests.setGeometry(20, 80, 600, 560)
        self.tbl_requests.setColumnCount(3)
        self.tbl_requests.setHorizontalHeaderLabels(["Zaman", "Tweet", "Adres"])
        self.tbl_requests.horizontalHeader().setStretchLastSection(True)
        self.tbl_requests.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tbl_requests.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbl_requests.verticalHeader().setVisible(False)
        self.tbl_requests.setShowGrid(False)

        # ---------------- Sağ Detay Paneli --------------------- #
        self.frm_detail = QtWidgets.QFrame(self.centralwidget)
        self.frm_detail.setGeometry(650, 80, 520, 560)
        self.frm_detail.setStyleSheet("background:#243546;border-radius:12px;")

        self.lbl_det_header = QtWidgets.QLabel("Detay", self.frm_detail)
        self.lbl_det_header.setGeometry(20, 15, 480, 30)
        self.lbl_det_header.setStyleSheet("font-size:22px;font-weight:bold;")

        self.txt_detail = QtWidgets.QTextEdit(self.frm_detail)
        self.txt_detail.setGeometry(20, 60, 480, 330)
        self.txt_detail.setReadOnly(True)
        self.txt_detail.setStyleSheet("background:#1E2D3A;border-radius:8px;")

        # ONAY & RED
        self.btn_accept = QtWidgets.QPushButton("ONAYLA", self.frm_detail)
        self.btn_accept.setGeometry(60, 410, 160, 50)
        self._style_action_btn(self.btn_accept, "#2E7D32", "#43A047")
        self.btn_accept.clicked.connect(lambda: self._respond(True))

        self.btn_reject = QtWidgets.QPushButton("REDDET", self.frm_detail)
        self.btn_reject.setGeometry(300, 410, 160, 50)
        self._style_action_btn(self.btn_reject, "#C62828", "#E53935")
        self.btn_reject.clicked.connect(lambda: self._respond(False))

        # Haritada göster
        self.btn_map = QtWidgets.QPushButton("HARİTADA GÖSTER", self.frm_detail)
        self.btn_map.setGeometry(150, 480, 220, 50)
        self.btn_map.clicked.connect(self.open_in_maps)

        # Yenile
        self.btn_refresh = QtWidgets.QPushButton("YENİLE", self.centralwidget)
        self.btn_refresh.setGeometry(20, 660, 100, 40)
        self.btn_refresh.clicked.connect(self.populate_table)

        # Logo
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(1060, 610, 120, 120)
        pix = QPixmap(r"D:\Code\Bitirme\gui_deprem\AFAD-Logo-Renkli.png")
        if not pix.isNull():
            self.logo.setPixmap(pix.scaled(120, 120, QtCore.Qt.KeepAspectRatio,
                                            QtCore.Qt.SmoothTransformation))
        self.logo.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # ---------------- Veri & sinyaller --------------------- #
        self.tbl_requests.itemSelectionChanged.connect(self.show_detail)
        self.populate_table()

        # 5 sn’de bir yeni tweet ekle (varsa)
        self.stream_timer = QtCore.QTimer()
        self.stream_timer.timeout.connect(self._push_next_tweet)
        self.stream_timer.start(5000)

        MainWindow.setCentralWidget(self.centralwidget)

    # --------------------------- Stil ------------------------------------- #
    def _modern_style(self):
        return """
        *{border:none;background:transparent;color:#EAF0F6;font-family:Arial;}
        #centralwidget{background:#1E2D3A;}      /* radius = 0 -> köşeler siyah kalmaz */
        QLabel{font-size:18px;}
        QTableWidget{background:#1E2D3A;border-radius:12px;border:2px solid #3D5A80;font-size:16px;}
        QHeaderView::section{background:#3D5A80;padding:6px;font-weight:bold;}
        QTextEdit{font-size:16px;padding:8px;}
        QPushButton{background:#3D5A80;border-radius:10px;padding:8px 12px;font-size:18px;font-weight:bold;}
        QPushButton:hover{background:#537A9C;} QPushButton:pressed{background:#2B445E;}
        """

    def _style_action_btn(self, btn, base, hover):
        btn.setStyleSheet(
            f"QPushButton{{background:{base};border-radius:10px;color:white;font-size:18px;font-weight:bold;}}"
            f"QPushButton:hover{{background:{hover};}}"
            f"QPushButton:pressed{{background:#2B445E;}}"
        )

    # ---------------- Window Kontrolleri ----------------------- #
    def _create_window_controls(self):
        frame = QtWidgets.QFrame(self.centralwidget)
        frame.setGeometry(1100, 20, 80, 30)
        btn_min = QtWidgets.QPushButton("-", frame)
        btn_min.setGeometry(0, 0, 30, 30)
        btn_min.setStyleSheet("background:#FFA500;font-size:20px;border-radius:4px;")
        btn_min.clicked.connect(self.MainWindow.showMinimized)
        btn_close = QtWidgets.QPushButton("X", frame)
        btn_close.setGeometry(40, 0, 30, 30)
        btn_close.setStyleSheet("background:#f44336;font-size:20px;border-radius:4px;")
        btn_close.clicked.connect(self.MainWindow.close)

    # ---------------- Tablo Doldurma --------------------------- #
    def populate_table(self):
        data = [d for d in _dummy_data if d["city"].lower() == self.city_name.lower()]
        self.tbl_requests.setRowCount(len(data))
        for r, d in enumerate(data):
            self.tbl_requests.setItem(r, 0, QtWidgets.QTableWidgetItem(d["timestamp"]))
            self.tbl_requests.setItem(r, 1, QtWidgets.QTableWidgetItem(d["tweet"]))
            self.tbl_requests.setItem(r, 2, QtWidgets.QTableWidgetItem(d["address"]))
        self.tbl_requests.resizeColumnsToContents()
        if data:
            self.tbl_requests.selectRow(len(data) - 1)     # en son eklenen seçili
        else:
            self.txt_detail.clear()

    # ---------------- Yeni tweet akışı ------------------------ #
    def _push_next_tweet(self):
        if not _remaining_stream:
            self.stream_timer.stop()
            return
        next_tw = _remaining_stream.pop(0)
        _dummy_data.append(next_tw)
        self.populate_table()

    # ---------------- Detay Göster ----------------------------- #
    def show_detail(self):
        i = self.tbl_requests.currentRow()
        if i < 0:
            self.txt_detail.clear()
            return
        ts = self.tbl_requests.item(i, 0).text()
        tw = self.tbl_requests.item(i, 1).text()
        ad = self.tbl_requests.item(i, 2).text()
        self.txt_detail.setHtml(
            f"<b>Zaman :</b> {ts}<br><br>"
            f"<b>Tweet :</b><br>{tw}<br><br>"
            f"<b>Adres :</b><br>{ad}"
        )

    # ---------------- Haritada Göster -------------------------- #
    def open_in_maps(self):
        i = self.tbl_requests.currentRow()
        if i < 0: return
        addr = self.tbl_requests.item(i, 2).text()
        webbrowser.open("https://www.google.com/maps/search/?api=1&query=" +
                        urllib.parse.quote_plus(addr))

    # ---------------- ONAY / RED İşlem ------------------------- #
    def _respond(self, accepted: bool):
        i = self.tbl_requests.currentRow()
        if i < 0:
            return

        if not accepted:        # REDDET
            self.tbl_requests.clearSelection()
            return

        # ONAYLA
        task = {
            "timestamp": self.tbl_requests.item(i, 0).text(),
            "tweet"    : self.tbl_requests.item(i, 1).text(),
            "address"  : self.tbl_requests.item(i, 2).text()
        }
        accepted_tasks.append(task)

        # Seçilen tweet'i anlık listelerden kaldır
        global _dummy_data
        _dummy_data = [d for d in _dummy_data if not (
            d["timestamp"] == task["timestamp"] and
            d["tweet"]     == task["tweet"]     and
            d["address"]   == task["address"]
        )]
        self.populate_table()

        # Görev panelini aç
        self.gorevWin = QtWidgets.QMainWindow()
        self.gorevUI  = Ui_GorevWindow(task, accepted_tasks, self.city_name)
        self.gorevUI.setupUi(self.gorevWin)
        self.gorevWin.show()

        # Ana paneli kapat
        self.MainWindow.close()

# ---------------- Test --------------------------------------- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw  = QtWidgets.QMainWindow()
    ui  = Ui_MainWindow("Bursa")
    ui.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())
