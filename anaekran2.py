# anaekran.py – AFAD Tweet Adres Tespiti
#  • Bursa → data_bursa.json
#  • İstanbul → data_istanbul.json
#  • Diğer tüm iller → data_deprem.json
#  • Hashtag’li kelimeler (#deprem vb.) tümden atılır
#  • Şehir karşılaştırması slugify + unicodedata ile sorunsuz

import sys, json, csv, webbrowser, urllib.parse, pathlib, re, string, unicodedata
from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from gorevlerim import Ui_GorevWindow

ROOT   = pathlib.Path(__file__).resolve().parent          # ...\gui_deprem
PY_DIR = ROOT.parent / "py"
sys.path.append(str(PY_DIR))

# ---------------- Model ---------------------------------------------------
from dataset_bilstm   import LABEL2ID
from train_bilstm_crf import BiLSTM_CRF, vocab
import torch

MODEL_PT = ROOT / "bilstm_crf2.pt"
device   = "cpu"
id2lab   = {v: k for k, v in LABEL2ID.items()}

_model = BiLSTM_CRF(len(vocab), len(LABEL2ID)).to(device)
_model.load_state_dict(torch.load(MODEL_PT, map_location=device))
_model.eval()
# --------------------------------------------------------------------------

# ---------------- Yardımcılar --------------------------------------------
PUNCT_TABLE = str.maketrans("", "", string.punctuation + "’‘”“")

def clean_text(txt: str) -> str:
    txt = re.sub(r"#\S+", " ", txt)            # hashtag'li kelimeyi sil
    txt = txt.translate(PUNCT_TABLE)           # noktalama kaldır
    txt = re.sub(r"\s+", " ", txt)
    return txt.strip()

def slugify(city: str) -> str:
    """Türkçe karakterleri ASCII’ye indirger, boşlukları atar."""
    txt = city.lower()
    txt = unicodedata.normalize("NFD", txt)
    txt = "".join(ch for ch in txt if not unicodedata.combining(ch))
    rep = str.maketrans("çğıöşüâîû", "cgiosuaiu")
    return txt.translate(rep).replace(" ", "")

def city_match(a: str, b: str) -> bool:
    return slugify(a) == slugify(b)

def predict_address(text: str) -> List[str]:
    tokens = re.findall(r"\S+", text)
    ids = torch.tensor([[vocab.get(w.lower(), 1) for w in tokens]],
                       dtype=torch.long, device=device)
    mask = torch.ones_like(ids, dtype=torch.bool, device=device)
    with torch.no_grad():
        pred = _model.decode(ids, mask)[0]

    spans, cur = [], []
    for w, lab_id in zip(tokens, pred):
        lab = id2lab[lab_id]
        if lab == "B-LOC":
            if cur:
                spans.append(" ".join(cur))
                cur = []
            cur.append(w)
        elif lab == "I-LOC" and cur:
            cur.append(w)
        else:
            if cur:
                spans.append(" ".join(cur))
                cur = []
    if cur:
        spans.append(" ".join(cur))
    return spans
# --------------------------------------------------------------------------


# ==============================  GUI  =====================================
class Ui_MainWindow(object):
    def __init__(self, city_name=""):
        self.city_name = city_name.strip() or "Unknown"
        self._load_tweets()                   # _dummy_data & _remaining oluşturulur

    # ---------- Veri Yükle -------------
    def _load_tweets(self):
        slug = slugify(self.city_name)

        if slug in ("bursa", "istanbul"):
            fname = ROOT / f"data_{slug}.json"
        else:
            fname = ROOT / "data_deprem.json"

        if not fname.exists():
            QtWidgets.QMessageBox.warning(
                None, "Veri Bulunamadı",
                f"{fname.name} bulunamadı – boş liste ile devam."
            )
            all_rows = []
        else:
            with open(fname, encoding="utf8") as f:
                all_rows = json.load(f)

        #  ---- YALNIZCA seçilen şehre ait tweet'ler ----
        city_rows = [r for r in all_rows if city_match(r.get("city", ""), self.city_name)]

        # ilk 5 tabloya, kalan akışa
        self._dummy_data = []
        for row in city_rows[:5]:
            row["clean"]   = clean_text(row["tweet"])
            row["address"] = "\n".join(predict_address(row["clean"])) or "— bulunamadı —"
            self._dummy_data.append(row)

        self._remaining     = city_rows[5:]
        self.accepted_tasks = []

    # ---------- Arayüz Kurulumu ----------
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.resize(1200, 720)
        MainWindow.setStyleSheet("background:#1E2D3A;")

        self.centralwidget = QtWidgets.QWidget(MainWindow, objectName="centralwidget")
        self.centralwidget.setStyleSheet(self._modern_style())

        self.lbl_title = QtWidgets.QLabel(
            f"AFAD – Tweet Adres Tespiti  |  Şehir: {self.city_name}", self.centralwidget)
        self.lbl_title.setGeometry(20, 15, 800, 40)
        self.lbl_title.setStyleSheet("font-size:26px;font-weight:bold;")

        self._create_window_controls()

        # -------- tablo --------
        self.tbl = QtWidgets.QTableWidget(self.centralwidget)
        self.tbl.setGeometry(20, 80, 600, 560)
        self.tbl.setColumnCount(3)
        self.tbl.setHorizontalHeaderLabels(["Zaman", "Tweet", "Adres"])
        self.tbl.horizontalHeader().setStretchLastSection(True)
        self.tbl.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tbl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setShowGrid(False)

        # -------- detay paneli ---
        self.frm = QtWidgets.QFrame(self.centralwidget)
        self.frm.setGeometry(650, 80, 520, 560)
        self.frm.setStyleSheet("background:#243546;border-radius:12px;")

        self.lbl_det = QtWidgets.QLabel("Detay", self.frm)
        self.lbl_det.setGeometry(20, 15, 480, 30)
        self.lbl_det.setStyleSheet("font-size:22px;font-weight:bold;")

        self.txt = QtWidgets.QTextEdit(self.frm)
        self.txt.setGeometry(20, 60, 480, 330)
        self.txt.setReadOnly(True)
        self.txt.setStyleSheet("background:#1E2D3A;border-radius:8px;")

        # -------- butonlar --------
        self.btn_ok = QtWidgets.QPushButton("ONAYLA", self.frm)
        self.btn_ok.setGeometry(60, 410, 160, 50)
        self._style_btn(self.btn_ok, "#2E7D32", "#43A047")
        self.btn_ok.clicked.connect(lambda: self._respond(True))

        self.btn_no = QtWidgets.QPushButton("REDDET", self.frm)
        self.btn_no.setGeometry(300, 410, 160, 50)
        self._style_btn(self.btn_no, "#C62828", "#E53935")
        self.btn_no.clicked.connect(lambda: self._respond(False))

        self.btn_map = QtWidgets.QPushButton("HARİTADA GÖSTER", self.frm)
        self.btn_map.setGeometry(150, 480, 220, 50)
        self.btn_map.clicked.connect(self.open_in_maps)

        # yenile
        self.btn_refresh = QtWidgets.QPushButton("YENİLE", self.centralwidget)
        self.btn_refresh.setGeometry(20, 660, 100, 40)
        self.btn_refresh.clicked.connect(self.populate_table)

        # logo
        logo = QtWidgets.QLabel(self.centralwidget)
        logo.setGeometry(1060, 610, 120, 120)
        pix = QPixmap(str(ROOT / "AFAD-Logo-Renkli.png"))
        if not pix.isNull():
            logo.setPixmap(
                pix.scaled(120, 120, QtCore.Qt.KeepAspectRatio,
                           QtCore.Qt.SmoothTransformation))

        # sinyaller
        self.tbl.itemSelectionChanged.connect(self.show_detail)
        self.populate_table()

        # Tweet akışı
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._push_next_tweet)
        self.timer.start(5000)

        MainWindow.setCentralWidget(self.centralwidget)

    # ---------- Stil -------------
    def _modern_style(self):
        return """
        *{border:none;background:transparent;color:#EAF0F6;font-family:Arial;}
        #centralwidget{background:#1E2D3A;}
        QLabel{font-size:18px;}
        QTableWidget{background:#1E2D3A;border-radius:12px;border:2px solid #3D5A80;font-size:16px;}
        QHeaderView::section{background:#3D5A80;padding:6px;font-weight:bold;}
        QTextEdit{font-size:16px;padding:8px;}
        QPushButton{background:#3D5A80;border-radius:10px;padding:8px 12px;font-size:18px;font-weight:bold;}
        QPushButton:hover{background:#537A9C;} QPushButton:pressed{background:#2B445E;}
        """

    def _style_btn(self, btn, base, hover):
        btn.setStyleSheet(
            f"QPushButton{{background:{base};border-radius:10px;color:white;font-size:18px;font-weight:bold;}}"
            f"QPushButton:hover{{background:{hover};}}"
            f"QPushButton:pressed{{background:#2B445E;}}")

    def _create_window_controls(self):
        frame = QtWidgets.QFrame(self.centralwidget)
        frame.setGeometry(1100, 15, 80, 30)
        bmin = QtWidgets.QPushButton("-", frame); bmin.setGeometry(0, 0, 30, 30)
        bmin.setStyleSheet("background:#FFA500;font-size:20px;border-radius:4px;")
        bmin.clicked.connect(self.MainWindow.showMinimized)
        bcls = QtWidgets.QPushButton("X", frame); bcls.setGeometry(40, 0, 30, 30)
        bcls.setStyleSheet("background:#f44336;font-size:20px;border-radius:4px;")
        bcls.clicked.connect(self.MainWindow.close)

    # ---------- Tablo -------------
    def populate_table(self):
        data = [d for d in self._dummy_data if city_match(d["city"], self.city_name)]
        self.tbl.setRowCount(len(data))
        for r, d in enumerate(data):
            self.tbl.setItem(r, 0, QtWidgets.QTableWidgetItem(d["timestamp"]))
            self.tbl.setItem(r, 1, QtWidgets.QTableWidgetItem(d["clean"]))
            self.tbl.setItem(r, 2, QtWidgets.QTableWidgetItem(d["address"]))
        self.tbl.resizeColumnsToContents()
        if data:
            self.tbl.selectRow(len(data) - 1)
        else:
            self.txt.clear()

    # ---------- Akış ---------------
    def _push_next_tweet(self):
        while self._remaining:
            tw = self._remaining.pop(0)
            if not city_match(tw["city"], self.city_name):
                continue
            tw["clean"]   = clean_text(tw["tweet"])
            tw["address"] = "\n".join(predict_address(tw["clean"])) or "— bulunamadı —"
            self._dummy_data.append(tw)
            self.populate_table()
            break
        if not self._remaining:
            self.timer.stop()

    # ---------- Detay --------------
    def show_detail(self):
        i = self.tbl.currentRow()
        if i < 0:
            self.txt.clear()
            return
        ts   = self.tbl.item(i, 0).text()
        clean= self.tbl.item(i, 1).text()
        ad   = self.tbl.item(i, 2).text()
        raw  = self._dummy_data[i]["tweet"]
        self.txt.setHtml(
            f"<b>Zaman :</b> {ts}<br><br>"
            f"<b>Tweet (ham):</b><br>{raw}<br><br>"
            f"<b>Tweet (temiz):</b><br>{clean}<br><br>"
            f"<b>Adres :</b><br>{ad}")

    def open_in_maps(self):
        i = self.tbl.currentRow()
        addr = self.tbl.item(i, 2).text() if i >= 0 else ""
        if addr.strip():
            webbrowser.open(
                "https://www.google.com/maps/search/?api=1&query="
                + urllib.parse.quote_plus(addr))

    # ---------- ONAY / RED ---------
    def _respond(self, accepted: bool):
        i = self.tbl.currentRow()
        if i < 0:
            return
        if not accepted:
            self.tbl.clearSelection()
            return

        task = {
            "timestamp": self.tbl.item(i, 0).text(),
            "tweet"    : self._dummy_data[i]["tweet"],
            "clean"    : self.tbl.item(i, 1).text(),
            "address"  : self.tbl.item(i, 2).text(),
        }
        self.accepted_tasks.append(task)

        del self._dummy_data[i]
        self.populate_table()

        CSV_FILE = ROOT / "kaydedilen_adresler.csv"
        write_head = not CSV_FILE.exists()
        with CSV_FILE.open("a", newline="", encoding="utf8") as f:
            w = csv.writer(f)
            if write_head:
                w.writerow(["timestamp", "tweet", "clean_tweet", "address"])
            w.writerow([task["timestamp"], task["tweet"],
                        task["clean"], task["address"]])

        self.gorevWin = QtWidgets.QMainWindow()
        self.gorevUI  = Ui_GorevWindow(task, self.accepted_tasks, self.city_name)
        self.gorevUI.setupUi(self.gorevWin)
        self.gorevWin.show()
        self.MainWindow.close()

# ----------------- Stand-alone test -----------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw  = QtWidgets.QMainWindow()
    ui  = Ui_MainWindow("Hatay")      # istediğiniz ili yazın
    ui.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())
