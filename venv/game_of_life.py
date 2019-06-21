from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from operator import itemgetter


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
                painter.fillRect(pos_x, pos_y, self.cell_w, self.cell_h, Qt.white)
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
        for cell in self.game.game_board:
            if cell[2]:
                painter.fillRect(cell[1] * self.cell_w+1, cell[0] * self.cell_h+1, self.cell_w-1, self.cell_h-1, Qt.black)
            else:
                painter.fillRect(cell[1] * self.cell_w+1, cell[0] * self.cell_h+1, self.cell_w-1, self.cell_h-1, Qt.cyan)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.game.update()
            self.update()

    def mousePressEvent(self, e):
        # time1 = time.process_time_ns()
        # dists = list()
        # cells = list()
        # print(e.x(), e.y())
        # for y in range(0, self.game.size):
        #     for x in range(0, self.game.size):
        #         dist = ((e.x() - self.game.game_board[y][x].center[1]) ** 2) + ((e.y() - self.game.game_board[y][x].center[0]) ** 2)
        #         dists.append(dist)
        #         cells.append(self.game.game_board[y][x])
        # cells[dists.index(min(dists))].toggle_state()
        self.game.create_cell(e.x(), e.y(), self.cell_w, self.cell_h, self.game.game_board)
        self.update()


class Game:
    def __init__(self, size):
        self.size = size
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
        print(self.game_board)
        for index in range(0, self.game_board.__len__()):
            living_neighbours = 0
            cell = self.game_board[index]
            index_b = index-1
            index_f = index+1
            if index_b >= 0:
                while True:
                    print(index_b, "ecksdee")
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
                    print(index_f)
                    if index_f == self.game_board.__len__():
                        break
                    if self.game_board[index_f][0] == cell[0] or self.game_board[index_f][0] == cell[0]+1:
                        if self.game_board[index_f][2]:
                            if self.game_board[index_f][1] == cell[1]-1 or self.game_board[index_f][1] == cell[1] or self.game_board[index_f][1] == cell[1]+1:
                                living_neighbours += 1
                    else:
                        break
                    index_f += 1
            print(living_neighbours)
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
