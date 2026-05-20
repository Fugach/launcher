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

        title = QLabel("Приветствую вас в NAME!")
        title_font = title.font()
        title_font.setPointSize(32)
        title.setFont(title_font)
        title.setAlignment(
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignHCenter
        )
        layout_pmc.addWidget(title)
        main_text = QLabel("Прежде чем начать работу, нужно настроить лаунчер под вас.")
        main_text_font = main_text.font()
        main_text_font.setPointSize(16)
        main_text.setFont(main_text_font)
        main_text.setWordWrap(True)
        main_text.setAlignment(
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignHCenter
        )
        layout_pmc.addWidget(main_text)
        self.button = QPushButton("Погнали")
        self.button.clicked.connect(self.download_pmc)
        self.button.pressed.connect(lambda : self.button.setText("и..."))
        self.button.setFixedSize(QSize(200, 80))
        layout_pmc.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)


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
        self.button.setDisabled(True)
        if not os.path.exists("bin/portablemc.exe"):
            dlg = PMC_dialog(self)
            if dlg.exec():
                self.button.setText("Скачиваем portablemc...")
                self.button.setDisabled(True)
                QApplication.processEvents()
                install()
            else:
                self.button.clicked.disconnect(self.download_pmc)
                self.button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
                QApplication.processEvents()
                self.button.setText("Дальше")
                self.button.setDisabled(False)
                return None
        else:
            self.button.setText("Portablemc уже тут, отлично!")
            self.button.clicked.disconnect(self.download_pmc)
            QApplication.processEvents()
            time.sleep(1)
            self.stacked_layout.setCurrentIndex(1)
            return None
        if os.path.exists("bin/portablemc.exe"):
            self.button.setDisabled(True)
            self.button.setText("Готово!")
            self.button.clicked.disconnect(self.download_pmc)
            self.button.clicked.connect(lambda : self.stacked_layout.setCurrentIndex(1))
            QApplication.processEvents()
            time.sleep(1)
            self.button.setText("Дальше")
            self.button.setDisabled(False)
        else:
            self.button.setText("Что-то навернулось... Может стоит попробовать ещё раз?")
            self.button.setDisabled(False)


class PMC_dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Уведомление")
        buttons = (
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Abort
        )
        self.buttonbox = QDialogButtonBox(buttons)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("В папке с лаунчером не обнаружен portablemc, скачать его сейчас?\n"
                         "Он обязателен для запуска майнкрафта.\n"
                         "Скачивание произойдёт на фоне без открытия вашего браузера.\n"
                         "В данный момент этот шаг полностью опционален.\n"
                         "Вы сможете выполнить его после начальной настройки.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonbox)
        self.setLayout(self.layout)
def start():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # запуск цикла в app
    app.exec()
# def download():
#     install()

# def login():
#     # запускаем логин в лицензионный акк на фоне
#     def worker():
#         raw_output = portablemc("auth login --output machine", True, False)
#     # raw_output = threading.Thread(target=lambda : portablemc("auth login --output machine", True)).start()
#     threading.Thread(target=worker, daemon=True).start()
#
# def get_link_and_code(inp):
#     print(inp)
#     if "auth_device_code" in str(inp):
#         print(str(inp).split())



