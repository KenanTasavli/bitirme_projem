from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(644, 728)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Çerçeveyi kaldır
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Arka planı saydam yap

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Arka plan
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("QFrame {\n"
                                           "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(117, 200, 188, 255), stop:1 rgba(255, 240, 152, 255));\n"
                                           "    border-radius: 20px;\n"
                                           "}")
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setObjectName("dropShadowFrame")

        # Başlık
        self.label_title = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_title.setGeometry(QtCore.QRect(0, 70, 661, 81))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(40)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: rgb(58, 155, 200);")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")

        # Alt başlık
        self.label_description = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_description.setGeometry(QtCore.QRect(0, 150, 661, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(13)
        self.label_description.setFont(font)
        self.label_description.setStyleSheet("color: rgb(98, 114, 164);")
        self.label_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_description.setObjectName("label_description")

        # Giriş paneli
        self.label_17 = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_17.setGeometry(QtCore.QRect(150, 190, 321, 451))
        self.label_17.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
                                    "border-radius: 20px;")
        self.label_17.setText("")
        self.label_17.setObjectName("label_17")

        # Kayıt Ol başlığı
        self.label_sign_up = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_sign_up.setGeometry(QtCore.QRect(230, 220, 161, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_sign_up.setFont(font)
        self.label_sign_up.setStyleSheet("color: rgba(255, 255, 255, 210);\n"
                                         "background-color: rgb(85, 170, 127);")
        self.label_sign_up.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sign_up.setObjectName("label_sign_up")

        # Kullanıcı Adı
        self.lineEdit_kullanici_adi_kayit = QtWidgets.QLineEdit(self.dropShadowFrame)
        self.lineEdit_kullanici_adi_kayit.setGeometry(QtCore.QRect(210, 300, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_kullanici_adi_kayit.setFont(font)
        self.lineEdit_kullanici_adi_kayit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                                        "border:none;\n"
                                                        "border-bottom:2px solid rgba(105, 118, 132, 255);\n"
                                                        "color:rgb(0, 0, 0);\n"
                                                        "padding-bottom:7px;")
        self.lineEdit_kullanici_adi_kayit.setPlaceholderText("Kullanıcı Adı")
        self.lineEdit_kullanici_adi_kayit.setObjectName("lineEdit_kullanici_adi_kayit")

        # E-mail
        self.lineEdit_mail = QtWidgets.QLineEdit(self.dropShadowFrame)
        self.lineEdit_mail.setGeometry(QtCore.QRect(210, 360, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_mail.setFont(font)
        self.lineEdit_mail.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                         "border:none;\n"
                                         "border-bottom:2px solid rgba(105, 118, 132, 255);\n"
                                         "color:rgb(0, 0, 0);\n"
                                         "padding-bottom:7px;")
        self.lineEdit_mail.setPlaceholderText("E-mail")
        self.lineEdit_mail.setObjectName("lineEdit_mail")

        # Parola
        self.lineEdit_sifre_parola_kayit = QtWidgets.QLineEdit(self.dropShadowFrame)
        self.lineEdit_sifre_parola_kayit.setGeometry(QtCore.QRect(210, 430, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_sifre_parola_kayit.setFont(font)
        self.lineEdit_sifre_parola_kayit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                                       "border:none;\n"
                                                       "border-bottom:2px solid rgba(105, 118, 132, 255);\n"
                                                       "color:rgb(0, 0, 0);\n"
                                                       "padding-bottom:7px;")
        self.lineEdit_sifre_parola_kayit.setPlaceholderText("Parola")
        self.lineEdit_sifre_parola_kayit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_sifre_parola_kayit.setObjectName("lineEdit_sifre_parola_kayit")

        # Parola Tekrar
        self.lineEdit_sifre_tekrar = QtWidgets.QLineEdit(self.dropShadowFrame)
        self.lineEdit_sifre_tekrar.setGeometry(QtCore.QRect(210, 490, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_sifre_tekrar.setFont(font)
        self.lineEdit_sifre_tekrar.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                                 "border:none;\n"
                                                 "border-bottom:2px solid rgba(105, 118, 132, 255);\n"
                                                 "color:rgb(0, 0, 0);\n"
                                                 "padding-bottom:7px;")
        self.lineEdit_sifre_tekrar.setPlaceholderText("Parola Tekrar")
        self.lineEdit_sifre_tekrar.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_sifre_tekrar.setObjectName("lineEdit_sifre_tekrar")

        # Kayıt Ol Butonu
        self.pushButton_kayit_ol_sayfa = QtWidgets.QPushButton(self.dropShadowFrame)
        self.pushButton_kayit_ol_sayfa.setGeometry(QtCore.QRect(210, 560, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_kayit_ol_sayfa.setFont(font)
        self.pushButton_kayit_ol_sayfa.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 85, 127, 255), stop:1 rgba(255, 170, 127, 255));
                color: white;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 170, 127, 255), stop:1 rgba(255, 85, 127, 255));
            }
        """)
        self.pushButton_kayit_ol_sayfa.setText("Kayıt Ol")
        self.pushButton_kayit_ol_sayfa.setObjectName("pushButton_kayit_ol_sayfa")

        # Kapat Butonu
        self.close_button = QtWidgets.QPushButton(self.dropShadowFrame)
        self.close_button.setGeometry(QtCore.QRect(590, 10, 30, 30))
        self.close_button.setStyleSheet("background-color: red; border-radius: 15px;")
        self.close_button.setObjectName("close_button")
        self.close_button.clicked.connect(MainWindow.close)

        # Simge Durumuna Küçült Butonu
        self.minimize_button = QtWidgets.QPushButton(self.dropShadowFrame)
        self.minimize_button.setGeometry(QtCore.QRect(550, 10, 30, 30))
        self.minimize_button.setStyleSheet("background-color: yellow; border-radius: 15px;")
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.clicked.connect(MainWindow.showMinimized)

        self.verticalLayout.addWidget(self.dropShadowFrame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kayıt Ol"))
        self.label_title.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">AISOFT</span> APP </p></body></html>"))
        self.label_description.setText(_translate("MainWindow", "Artificial Intelligence & Robotics"))
        self.label_sign_up.setText(_translate("MainWindow", "Kayıt Ol"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
