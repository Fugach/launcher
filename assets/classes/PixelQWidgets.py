import sys, os
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
# ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()
#  #######   #      #  #         #          ######   #      #  ########  ########
#  #      #  #      #  #         #         #         #      #     #         #
#  #      #  #      #  #         #         #         #      #     #         #
#  #######   #      #  #         #          ######   ########     #         #
#  #      #  #      #  #         #                #  #      #     #         #
#  #      #  #      #  #         #                #  #      #     #         #
#  #######    ######   ########  ########   ######   #      #  ########     #
# ()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()


# Отключаем HiDPI-масштабирование, иначе Qt начнёт дробно скейлить и "мылить" пиксели
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"

if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)  # .exe
else:
    basedir = os.path.dirname(os.path.abspath(__file__))  # .py
textures_dir = os.path.abspath(os.path.join(os.path.join(basedir, ".."), "textures"))
print("ASSETS DIRECTORY:", textures_dir)

class PixelQPushButton(QPushButton):
    def __init__(self, text : str, border_size=1, parent=None):
        super().__init__(text, parent)
        self.border = border_size

        self.pixmaps = {
            "base": QPixmap(os.path.join(os.path.join(textures_dir, "PixelQPushButton"), "base.png")),
            "hover": QPixmap(os.path.join(os.path.join(textures_dir, "PixelQPushButton"), "hover.png")),
            "pressed": QPixmap(os.path.join(os.path.join(textures_dir, "PixelQPushButton"), "pressed.png"))
        }

        self.state = "base"
        self.setMouseTracking(True)
        self.setStyleSheet("background: transparent; border: none;")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.setMinimumSize(2 * border_size + 1, 2 * border_size + 1)

    def _set_state(self, new_state):
        if new_state != self.state:
            self.state = new_state
            self.update()

    def enterEvent(self, event):
        self._set_state("hover")
        super().enterEvent(event)
    def leaveEvent(self, event):
        self._set_state("base")
        super().leaveEvent(event)
    def mousePressEvent(self, event):
        self._set_state("pressed")
        super().mousePressEvent(event)
    def mouseReleaseEvent(self, event):
        self._set_state("hover" if self.underMouse() else "base")
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

        pm = self.pixmaps[self.state]
        if pm.isNull():
            raise FileNotFoundError(f'Не нашёл "{self.state}". Он ТОЧНО есть?')

        w, h = pm.width(), pm.height() # ширина и высота исходной текстуры кнопки
        dw, dh = self.width(), self.height() # ширина и высота запрашиваемой кнопки
        b = self.border # b это граница, решил сократить название из-за приколов ниже

        if dw <= 2 * b:
            dw = 2 * b + 1
        if dh <= 2 * b:
            dh = 2 * b + 1

        regions = [
            (QRect(0, 0, b, b), QRect(0, 0, b, b)), # левый верхний угол
            (QRect(b, 0, w - 2 * b, b), QRect(b, 0, dw - 2 * b, b)), # верх
            (QRect(w - b, 0, b, b), QRect(dw - b, 0, b, b)), # правый верхний угол
            (QRect(0, b, b, h - 2 * b), QRect(0, b, b, dh - 2 * b)), # лево
            (QRect(b, b, w - 2 * b, h - 2 * b), QRect(b, b, dw - 2 * b, dh - 2 * b)), # центр
            (QRect(w - b, b, b, h - 2 * b), QRect(dw - b, b, b, dh - 2 * b)), # право
            (QRect(0, h - b, b, b), QRect(0, dh - b, b, b)), # левый нижний угол
            (QRect(b, h - b, w - 2 * b, b), QRect(b, dh - b, dw - 2 * b, b)), # низ
            (QRect(w - b, h - b, b, b), QRect(dw - b, dh - b, b, b)) # правый нижний угол
        ]

        # 🟩 ТЕКСТУРА РИСУЕТСЯ БЕЗ СДВИГА (остаётся на месте)
        for src, dst in regions:
            painter.drawPixmap(dst, pm, src)

        # 🔽 СДВИГ НА 1 ПИКСЕЛЬ ВНИЗ ПРИ НАЖАТИИ (ТОЛЬКО ДЛЯ ТЕКСТА)
        if self.text():
            offset = QPoint(0, 1) if self.state == "pressed" else QPoint(0, 0)
            painter.setPen(self.palette().color(QPalette.WindowText))
            painter.drawText(self.rect().translated(offset), Qt.AlignmentFlag.AlignCenter, self.text())

    def sizeHint(self):
        # Если размер уже задан (через setFixedSize), возвращаем его.
        # self.size() до первого лейаута = 0x0, поэтому ставим проверку > 1
        if self.width() > 1:
            return self.size()

        # Иначе возвращаем безопасный дефолт (или размер базовой текстуры)
        pm = self.pixmaps["base"]
        return pm.size() if not pm.isNull() else QSize(90, 60)