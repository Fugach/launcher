from .portablemc import install
import sys, time, subprocess, darkdetect, json
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from pathlib import Path

basedir = ''
PORTABLEMC_DIR = Path(__file__).parent.parent / 'bin' / 'portablemc.exe'
ROOT_DIR = Path(__file__).parent.parent
TEXTURES_DIR = Path(__file__).parent / 'textures'
PROFILES_DIR = Path(__file__).parent.parent.parent / 'profiles.txt'

print('-' * 55)
print('ROOT_DIR         |', ROOT_DIR)
print('TEXTURES_DIR     |', TEXTURES_DIR)
print('PORTABLEMC_DIR   |', PORTABLEMC_DIR)
print('PROFILES_DIR     |', PROFILES_DIR)
print('-' * 55)

if not PROFILES_DIR.is_file():
    with open(PROFILES_DIR, 'w', encoding='utf-8') as file:
        pass
with open(PROFILES_DIR, 'r', encoding='utf-8') as file:
     PROFILES = file.read().splitlines()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Первый запуск")
        self.setFixedSize(QSize(600, 480))

        self.stacked_layout = QStackedLayout()


        first_page = PMG_page(self.stacked_layout)
        second_page = account_page(self.stacked_layout)
        third_page = success_page(self.stacked_layout)

        for widget in [first_page, second_page, third_page]:
            self.stacked_layout.addWidget(widget)
        self.stacked_layout.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(self.stacked_layout)
        self.setCentralWidget(widget)

class PMG_page(QWidget):
    def __init__(self, stacked_layout):
        self.stacked_layout = stacked_layout
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Приветствую вас в DumbMC!")
        title_font = title.font()
        title_font.setPointSize(32)
        title.setFont(title_font)
        title.setAlignment(
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(title)

        main_text = QLabel("Прежде чем начать работу, нужно настроить лаунчер под вас.")
        main_text_font = main_text.font()
        main_text_font.setPointSize(16)
        main_text.setFont(main_text_font)
        main_text.setWordWrap(True)
        main_text.setAlignment(
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(main_text)

        self.button = (
            QPushButton("Погнали"))
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button_font = self.button.font()
        button_font.setPointSize(16)
        self.button.setFont(button_font)
        self.button.clicked.connect(self.download_pmc)
        self.button.pressed.connect(lambda : self.button.setText("и..."))
        self.button.setFixedSize(90, 60)
        self.button.updateGeometry()
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
    def download_pmc(self):
        self.button.setDisabled(True)
        if not PORTABLEMC_DIR.is_file():
            self.button.setText("Скачиваем\nportablemc...")
            self.button.setDisabled(True)
            QApplication.processEvents()
            install()
        else:
            self.stacked_layout.setCurrentIndex(1)
        self.button.clicked.disconnect(self.download_pmc)
        self.button.clicked.connect(lambda : self.stacked_layout.setCurrentIndex(1))
        QApplication.processEvents()
        self.button.setText("Дальше")
        self.button.setDisabled(False)

class account_page(QWidget):
    def __init__(self, stacked_layout):
        super().__init__()
        self.stacked_layout = stacked_layout
        self.button_next = None
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Выберите, как вы будете играть.")
        title_font = title.font()
        title_font.setPointSize(32)
        title.setFont(title_font)
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(title)

        options = QWidget()
        options_layout = QHBoxLayout()

        lic_acc = QPushButton("С лицензией")
        lic_acc.setIconSize(QSize(30, 30))
        lic_acc.clicked.connect(self.get_licence, self.stacked_layout)
        lic_acc_font = lic_acc.font()
        lic_acc_font.setPointSize(16)
        lic_acc.setFont(lic_acc_font)
        options_layout.addWidget(lic_acc)

        offline_acc = QPushButton("Без лицензии")
        offline_acc.setIconSize(QSize(30, 30))
        offline_acc_font = offline_acc.font()
        offline_acc_font.setPointSize(16)
        offline_acc.setFont(offline_acc_font)
        self.nickname = ""
        offline_acc.clicked.connect(self.get_nickname)
        options_layout.addWidget(offline_acc)
        options.setLayout(options_layout)
        self.layout.addWidget(options)
        self.setLayout(self.layout)

    def get_nickname(self):
        def write_nickname():
            with open(PROFILES_DIR, 'r', encoding='utf-8') as file:
                profiles = file.read().splitlines()
                if self.nickname not in profiles:
                    profiles.append(self.nickname)
                    with open(PROFILES_DIR, 'w', encoding='utf-8') as file:
                        file.write('\n'.join(profiles))
                    self.stacked_layout.setCurrentIndex(2)
                # json.dump()
        title = "Никнейм"
        label = "Введи свой никнейм..."
        self.nickname = ''
        while self.nickname == '':
            self.nickname, ok = QInputDialog.getText(
                self, title, label
            )
            wrong_symbols = []
            for symbol in self.nickname:
                if symbol not in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789_":
                    wrong_symbols.append(symbol)
            if not ok:
                break
            if self.nickname == "":
                self.nickname = ''
                error = QMessageBox.critical(self, 'Ошибка', 'Никнейм не может быть пустым!', buttons=QMessageBox.StandardButton.Ok)
            if wrong_symbols != []:
                self.nickname = ''
                wrong_nickname = QMessageBox.critical(self, 'Ошибка',
                                                      f'В никнейме есть недопустимые символы:\n"{", ".join(wrong_symbols)}"\n'
                                                      f'Пожалуйста, учтите, что разрешены только:\n'
                                                      f'1. Латинские буквы(A-Z, a-z)\n'
                                                      f'2. Цифры (0-9)\n'
                                                      f'3. Нижнее подчёркивание (_)', buttons=QMessageBox.StandardButton.Ok)
        if self.nickname != "":
            for btn in self.findChildren(QPushButton):
                if btn == self.button_next:
                    btn.deleteLater()
            print("Player nickname:", self.nickname)
            self.button_next = QPushButton(f"Продолжить с никнеймом\n{self.nickname}")
            button_next_font = self.button_next.font()
            self.button_next.clicked.connect(lambda : write_nickname())
            button_next_font.setPointSize(12)
            self.button_next.setFont(button_next_font)
            self.layout.addWidget(self.button_next)
    def get_licence(self):
        if self.button_next:
            self.button_next.deleteLater()
            self.layout.removeWidget(self.button_next)
        login = subprocess.Popen(
            [PORTABLEMC_DIR, "--main-dir", "%~dp0", "auth", "login", "--output", "machine"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        while login:
            line = login.stdout.readline()
            if "auth_device_code" in line:
                code = line.split()[2]
                break
        info = QLabel("Откройте ваш браузер и перейдите на")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)

        link = QLineEdit("https://www.microsoft.com/link")
        link_font = link.font()
        link_font.setPointSize(16)
        link.setFont(link_font)
        link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        link.setReadOnly(True)

        info2 = QLabel("Войдите в свою учётную запись Microsoft и введите следующий код:")
        info2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info2.setWordWrap(True)

        copyable_code = QLineEdit(code)
        copyable_code_font = copyable_code.font()
        copyable_code_font.setPointSize(16)
        copyable_code.setFont(copyable_code_font)
        copyable_code.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyable_code.setReadOnly(True)

        for widget in [info, link, info2, copyable_code]:
            self.layout.addWidget(widget)

        login.stdin.write("\n")
        login.stdin.flush()
        QApplication.processEvents()
        while login:
            if login.poll() is None:
                pass
                QApplication.processEvents()
            else:
                print("Login successful!")
                break
        for widget in [info, link, info2, copyable_code]:
            widget.deleteLater()
        self.stacked_layout.setCurrentIndex(2)

class success_page(QWidget):
    def __init__(self, stacked_layout):
        super().__init__()
        self.stacked_layout = stacked_layout

def start():

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    # запуск цикла в app
    app.exec()
