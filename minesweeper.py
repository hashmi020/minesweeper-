import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, QTime

class Cell(QPushButton):
    def __init__(self, x, y, parent):
        super().__init__()
        self.parent_widget = parent
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.setFixedSize(40, 40)

    def mousePressEvent(self, event):
        if not self.parent_widget.timer_started:
            self.parent_widget.start_timer()
        if event.button() == Qt.LeftButton:
            self.parent_widget.reveal_cell(self.x, self.y)
        elif event.button() == Qt.RightButton:
            self.parent_widget.flag_cell(self.x, self.y)

class Minesweeper(QWidget):
    def __init__(self, rows=8, cols=8, mines=10):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Minesweeper with Timer")
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        # Timer and Reset UI
        self.timer_label = QLabel("Time: 0s")
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self.reset_game)

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.timer_label)
        top_bar.addStretch()
        top_bar.addWidget(self.reset_btn)
        self.vbox.addLayout(top_bar)

        self.grid = QGridLayout()
        self.vbox.addLayout(self.grid)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_elapsed = 0
        self.timer_started = False

        self.reset_game()

    def reset_game(self):
        self.timer.stop()
        self.time_elapsed = 0
        self.timer_label.setText("Time: 0s")
        self.timer_started = False

        # Clear old cells
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Create new cells
        self.cells = [[Cell(x, y, self) for y in range(self.cols)] for x in range(self.rows)]
        for x in range(self.rows):
            for y in range(self.cols):
                self.grid.addWidget(self.cells[x][y], x, y)

        self.place_mines()
        self.calculate_adjacency()

    def start_timer(self):
        self.timer_started = True
        self.timer.start(1000)

    def update_timer(self):
        self.time_elapsed += 1
        self.timer_label.setText(f"Time: {self.time_elapsed}s")

    def place_mines(self):
        positions = [(x, y) for x in range(self.rows) for y in range(self.cols)]
        mine_positions = random.sample(positions, self.total_mines)
        for x, y in mine_positions:
            self.cells[x][y].is_mine = True

    def calculate_adjacency(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.cells[x][y].is_mine:
                    continue
                count = 0
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.rows and 0 <= ny < self.cols:
                            if self.cells[nx][ny].is_mine:
                                count += 1
                self.cells[x][y].adjacent_mines = count

    def reveal_cell(self, x, y):
        cell = self.cells[x][y]
        if cell.is_flagged or cell.is_revealed:
            return
        cell.is_revealed = True
        cell.setEnabled(False)

        if cell.is_mine:
            cell.setText("💣")
            self.timer.stop()
            self.game_over(False)
            return

        if cell.adjacent_mines > 0:
            cell.setText(str(cell.adjacent_mines))
        else:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols:
                        self.reveal_cell(nx, ny)

        if self.check_win():
            self.timer.stop()
            self.game_over(True)

    def flag_cell(self, x, y):
        cell = self.cells[x][y]
        if cell.is_revealed:
            return
        if cell.is_flagged:
            cell.setText("")
        else:
            cell.setText("🚩")
        cell.is_flagged = not cell.is_flagged

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def game_over(self, won):
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.setText("💣")
                cell.setEnabled(False)

        if won:
            QMessageBox.information(self, "Victory!", f"You won in {self.time_elapsed} seconds!")
        else:
            QMessageBox.warning(self, "Game Over", "You clicked on a mine!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Minesweeper()
    game.show()
    sys.exit(app.exec_())
