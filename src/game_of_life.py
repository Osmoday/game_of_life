from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from operator import itemgetter
import threading
import math


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Gra o życie"
        self.top = 100
        self.left = 100
        self.width = 700
        self.height = 700
        self.game = Game()
        self.cell_w = 20
        self.cell_h = 20
        self.loop = 0
        self.kill_loop = False
        self.x_offset = 0
        self.y_offset = 0
        self.offset_step = 40
        self.screen_geometry = QDesktopWidget().screenGeometry()
        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.fillRect(0, 0, self.screen_geometry.width(), self.screen_geometry.height(), Qt.white)
        for i in range(0, int(self.screen_geometry.height()/self.cell_h)):
            painter.drawLine(0, i*self.cell_h, self.screen_geometry.width(), i*self.cell_h)
            for k in range(0, int(self.screen_geometry.width()/self.cell_w)):
                painter.drawLine(k*self.cell_w, self.screen_geometry.height(), k*self.cell_w, 0)
        for cell in self.game.game_board:
            if cell[2]:
                painter.fillRect((cell[1] * self.cell_w)+self.x_offset, (cell[0] * self.cell_h)+self.y_offset, self.cell_w, self.cell_h, Qt.black)
            # else:
            #     painter.fillRect(cell[1] * self.cell_w, cell[0] * self.cell_h, self.cell_w, self.cell_h, Qt.cyan)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            if self.loop == 0 or self.kill_loop:
                self.kill_loop = False
                self.loop = threading.Thread(target=self.game_loop, args=(0.1,))
                self.loop.start()
            else:
                self.kill_loop = True
                self.loop = 0
        elif e.key() == Qt.Key_A:
            self.x_offset += self.offset_step
            self.update()
        elif e.key() == Qt.Key_D:
            self.x_offset -= self.offset_step
            self.update()
        elif e.key() == Qt.Key_S:
            self.y_offset -= self.offset_step
            self.update()
        elif e.key() == Qt.Key_W:
            self.y_offset += self.offset_step
            self.update()

    def mousePressEvent(self, e):
        self.game.create_cell(e.x()-self.x_offset, e.y()-self.y_offset, self.cell_w, self.cell_h, self.game.game_board)
        self.update()

    def wheelEvent(self, e):
        if e.angleDelta().y() < 0:
            self.cell_w = self.cell_w/2
            self.cell_h = self.cell_h/2
            self.offset_step = self.offset_step/2
            self.y_offset /= 2
            self.x_offset /= 2
        else:
            self.cell_h *= 2
            self.cell_w *= 2
            self.offset_step *= 2
            self.y_offset *= 2
            self.x_offset *= 2
        self.update()

    def game_loop(self, tick):
        while not self.kill_loop:
            time.sleep(tick)
        # if self.running == 1:
            self.game.update()
            self.update()


class Game:
    def __init__(self):
        self.game_board = list()

    def create_cell(self, x, y, width, height, board):
        index_x = int(x / width)
        index_y = int(y / height)
        found = False
        for index in range(0, board.__len__()):
            if board[index][0] == index_y and board[index][1] == index_x:
                if not board[index][2]:
                    board[index] = (index_y, index_x, True)
                    found = True
                    break
                else:
                    board[index] = (index_y, index_x, False)
                    return
        if not found:
            board.append((index_y, index_x, True))
        neighbours = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        for index in range(0, board.__len__()):
            for i in range(-1, 2):
                if board[index][0] == index_y+i:
                    if board[index][1] == index_x-1:
                        neighbours[i+1][0] = 1
                    elif board[index][1] == index_x:
                        neighbours[i+1][1] = 1
                    elif board[index][1] == index_x+1:
                        neighbours[i+1][2] = 1
        for i in range(0, neighbours.__len__()):
            for k in range(0, neighbours[i].__len__()):
                if neighbours[i][k] != 1:
                    board.append((index_y+(i-1), index_x+(k-1), False))

    def update(self):
        buffer = list()
        self.game_board.sort(key=itemgetter(0, 1))
        for index in range(0, self.game_board.__len__()):
            living_neighbours = 0
            cell = self.game_board[index]
            index_b = index-1
            index_f = index+1
            if index_b >= 0:
                while True:
                    if index_b < 0:
                        break
                    if self.game_board[index_b][0] == cell[0] or self.game_board[index_b][0] == cell[0]-1:
                        if self.game_board[index_b][2]:
                            if self.game_board[index_b][1] == cell[1]-1 or self.game_board[index_b][1] == cell[1] or self.game_board[index_b][1] == cell[1]+1:
                                living_neighbours += 1
                    else:
                        break
                    index_b -= 1
            if index_f < self.game_board.__len__():
                while True:
                    if index_f == self.game_board.__len__():
                        break
                    if self.game_board[index_f][0] == cell[0] or self.game_board[index_f][0] == cell[0]+1:
                        if self.game_board[index_f][2]:
                            if self.game_board[index_f][1] == cell[1]-1 or self.game_board[index_f][1] == cell[1] or self.game_board[index_f][1] == cell[1]+1:
                                living_neighbours += 1
                    else:
                        break
                    index_f += 1
            if cell[2]:
                if living_neighbours == 2 or living_neighbours == 3:
                    self.create_cell(cell[1], cell[0], 1, 1, buffer)
            else:
                if living_neighbours == 3:
                    self.create_cell(cell[1], cell[0], 1, 1, buffer)
        print(buffer)
        self.game_board = buffer


app = QApplication([])
window = Window()
window.show()
app.exec_()
