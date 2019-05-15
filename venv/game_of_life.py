from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# class RasterWindow(QWindow):
#
#     def render_later(self):
#         self.requestUpdate()
#
#     def render_now(self):
#         if not self.isExposed():
#             return
#         rect = QRect(0, 0, self.width(), self.height())
#         self.backing_store.beginPaint(QRegion(rect))
#         device = self.backing_store.paintDevice()
#         painter = QPainter(device)
#         painter.fillRect(0, 0, self.width(), self.height(), QGradient.NightFade)
#         render(painter)
#         painter.end()
#
#     def render(self, painter):
#         painter.drawText(QRectF(0, 0, self.width(), self.height(), Qt.AlignCenter, "QWindow"))
#
#     def resizeEvent(self, _QResizeEvent):
#         self.backing_store.resize(_QResizeEvent.size())
#
#     def exposeEvent(self, _QExposeEvent):
#         if self.isExposed():
#             self.render_now()
#
#     def event(self, _QEvent):
#         while _QEvent.type() == QEvent.UpdateRequest:
#             continue
#         self.render_now()
#         return True
#
#     def __init__(self):
#         super().__init__()
#         self.backing_store = QBackingStore(self)
#         self.setGeometry(100, 100, 300, 200)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Gra o życie"
        self.top = 100
        self.left = 100
        self.width = 700
        self.height = 700
        self.game = Game(20)
        self.cell_w = self.width / self.game.size
        self.cell_h = self.height / self.game.size
        # Wiatrak
        # self.game.game_board[4][2].toggle_state()
        # self.game.game_board[4][3].toggle_state()
        # self.game.game_board[4][4].toggle_state()
        # Collapse to stable
        # self.game.game_board[6][5].toggle_state()
        # self.game.game_board[6][6].toggle_state()
        # self.game.game_board[7][5].toggle_state()
        # Połamany Szybowiec
        # self.game.game_board[1][3].toggle_state()
        # self.game.game_board[2][4].toggle_state()
        # self.game.game_board[3][3].toggle_state()
        # self.game.game_board[3][4].toggle_state()
        # self.game.game_board[3][5].toggle_state()
        # Szybowiec
        self.game.game_board[1][3].toggle_state()
        self.game.game_board[2][4].toggle_state()
        self.game.game_board[3][2].toggle_state()
        self.game.game_board[3][3].toggle_state()
        self.game.game_board[3][4].toggle_state()
        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawRect(0, 0, self.width, self.height)
        pos_x = 0
        pos_y = 0
        for y in range(0, self.game.size):
            for x in range(0, self.game.size):
                painter.fillRect(pos_x, pos_y, self.cell_w, self.cell_h, self.game.game_board[y][x].state)
                pos_x += self.cell_w
            pos_x = 0
            pos_y += self.cell_h
        pos_x = 0
        pos_y = 0
        for y in range(0, self.game.size):
            for x in range(0, self.game.size):
                painter.drawRect(pos_x, pos_y, self.cell_w, self.cell_h)
                pos_x += self.cell_w
            pos_x = 0
            pos_y += self.cell_h

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.game.update()
            self.update()


class Game:
    def __init__(self, size):
        self.size = size
        self.game_board = list()
        for i in range(0, size):
            row = list()
            for ii in range(0, size):
                row.append(Cell())
            self.game_board.append(row)

    def update(self):
        buffer = Game(self.size)
        for y in range(0, self.size):
            for x in range(0, self.size):
                cnt = 0
                if y - 1 >= 0:
                    cnt += self.game_board[y - 1][x].int_val()
                    if x - 1 >= 0:
                        cnt += self.game_board[y - 1][x - 1].int_val()
                    if x + 1 < self.size:
                        cnt += self.game_board[y - 1][x + 1].int_val()
                if y + 1 < self.size:
                    cnt += self.game_board[y + 1][x].int_val()
                    if x - 1 >= 0:
                        cnt += self.game_board[y + 1][x - 1].int_val()
                    if x + 1 < self.size:
                        cnt += self.game_board[y + 1][x + 1].int_val()
                if x - 1 >= 0:
                    cnt += self.game_board[y][x - 1].int_val()
                if x + 1 < self.size:
                    cnt += self.game_board[y][x + 1].int_val()

                if self.game_board[y][x].state == Qt.white:
                    if cnt == 3:
                        buffer.game_board[y][x].toggle_state()
                else:
                    if cnt == 2 or cnt == 3:
                        buffer.game_board[y][x] = self.game_board[y][x]
        self.game_board = buffer.game_board


class Cell:
    def __init__(self):
        self.state = Qt.white

    def toggle_state(self):
        if self.state == Qt.white:
            self.state = Qt.black
        else:
            self.state = Qt.white

    def int_val(self):
        if self.state == Qt.white:
            return 0
        else:
            return 1


app = QApplication([])
window = Window()
window.show()
app.exec_()
