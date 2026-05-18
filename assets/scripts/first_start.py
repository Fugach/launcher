from ..ui.first_start.bg import Color
from .portablemc import install, portablemc
import threading, sys, os.path, random, time
from PIL import Image
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Первый запуск")
        self.setFixedSize(QSize(600, 480))

        self.stacked_layout = QStackedLayout()
        layout_pmc = QVBoxLayout()
        layout_pmc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_acc = QVBoxLayout()


        self.button = QPushButton("Погнали")
        self.button.clicked.connect(self.download_pmc)
        self.button.pressed.connect(lambda : self.button.setText("и..."))
        self.button.released.connect(lambda :  self.button.setText(
            random.choice(["Эй! Может начнём?", "Зачем отпустил? :(", "Нажми уже!!!!!!", "ОШИБКА: КНОПКА НЕ НАЖАТА"]))
            if self.button.isEnabled() else None)
        self.button.setFixedSize(QSize(200, 80))
        layout_pmc.addWidget(self.button)


        page_pmc = QWidget()
        page_pmc.setLayout(layout_pmc)

        page_acc = QWidget()
        page_acc.setLayout(layout_acc)

        for widget in [page_pmc, page_acc]:
            self.stacked_layout.addWidget(widget)
        self.stacked_layout.setCurrentIndex(0)
        widget = QWidget()
        widget.setLayout(self.stacked_layout)
        self.setCentralWidget(widget)
    def download_pmc(self):
        self.button.setText("работаем...")
        install()
        if os.path.exists("bin/portablemc.exe"):
            self.button.setText("Готово!")
            self.button.setDisabled(True)
            QApplication.processEvents()
            time.sleep(1)
            self.stacked_layout.setCurrentIndex(1)
        else:
            self.button.setText("Что-то навернулось... Может стоит попробовать ещё раз?")
            self.button.setDisabled(False)

def start():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # запуск цикла в app
    app.exec()
# def download():
#     install()

def login():
    # запускаем логин в лицензионный акк на фоне
    def worker():
        raw_output = portablemc("auth login --output machine", True, False)
    # raw_output = threading.Thread(target=lambda : portablemc("auth login --output machine", True)).start()
    threading.Thread(target=worker, daemon=True).start()

def get_link_and_code(inp):
    print(inp)
    if "auth_device_code" in str(inp):
        print(str(inp).split())



