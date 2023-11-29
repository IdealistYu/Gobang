import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from itertools import product

class Chess(object):
    BOARD_COLOR = "#CDBA96"
    HEADER_BG = "#313131"
    BTN_FONT = ("consolas", 10, "bold")

    def __init__(self):
        self.row, self.column = 19, 19
        self.mesh = 40
        self.ratio = 0.7
        self.board_color = Chess.BOARD_COLOR
        self.header_bg = Chess.HEADER_BG
        self.btn_font = Chess.BTN_FONT
        self.step = self.mesh / 2
        self.chess_r = self.step * self.ratio
        self.point_r = self.step * 0.2
        self.matrix = [[0 for _ in range(self.column)] for _ in range(self.row)]
        self.is_start = False
        self.is_black = True
        self.last_p = None

        self.root = tk.Tk()
        self.root.title("Gobang")
        self.root.resizable(width=False, height=False)

        self.f_header = tk.Frame(self.root, highlightthickness=0, bg=self.header_bg)
        self.f_header.pack(side=tk.TOP, fill=tk.BOTH, ipadx=0)


        style = ttk.Style()
        style.configure("Square.TButton", padding=0, borderwidth=0, foreground='white')

        self.b_start = ttk.Button(self.f_header, text="Start", command=self.bf_start, style="Square.TButton")
        self.b_restart = ttk.Button(self.f_header, text="Again", command=self.bf_restart, state=tk.DISABLED, style="Square.TButton")
        self.l_info = tk.Label(self.f_header, text="NotStarted", bg=Chess.HEADER_BG, font=("consolas", 18, "bold"), fg="white")
        self.b_regret = ttk.Button(self.f_header, text="Undo", command=self.bf_regret, state=tk.DISABLED, style="Square.TButton")
        self.b_lose = ttk.Button(self.f_header, text="Give in", command=self.bf_lose, state=tk.DISABLED, style="Square.TButton")


        self.b_start.pack(side=tk.LEFT, padx=20)
        self.b_restart.pack(side=tk.LEFT)
        self.l_info.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, pady=10)
        self.b_lose.pack(side=tk.RIGHT, padx=20)
        self.b_regret.pack(side=tk.RIGHT)

        self.c_chess = tk.Canvas(self.root, bg=self.board_color, width=(self.column + 1) * self.mesh,
                               height=(self.row + 1) * self.mesh, highlightthickness=0)
        self.draw_board()
        self.c_chess.bind("<Button-1>", self.cf_board)
        self.c_chess.pack()

        self.root.mainloop()

    def draw_mesh(self, x, y):
        ratio = (1 - self.ratio) * 0.99 + 1
        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
        self.c_chess.create_rectangle(center_y - self.step, center_x - self.step,
                                      center_y + self.step, center_x + self.step,
                                      fill=self.board_color, outline=self.board_color)
        a, b = [0, ratio] if y == 0 else [-ratio, 0] if y == self.row - 1 else [-ratio, ratio]
        c, d = [0, ratio] if x == 0 else [-ratio, 0] if x == self.column - 1 else [-ratio, ratio]
        self.c_chess.create_line(center_y + a * self.step, center_x, center_y + b * self.step, center_x)
        self.c_chess.create_line(center_y, center_x + c * self.step, center_y, center_x + d * self.step)

        if ((x == 3 or x == 9 or x == 15) and (y == 3 or y == 9 or y == 15)):
            self.c_chess.create_oval(center_y - self.point_r, center_x - self.point_r,
                                      center_y + self.point_r, center_x + self.point_r, fill="black")

    def draw_chess(self, x, y, color):
        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
        self.c_chess.create_oval(center_y - self.chess_r, center_x - self.chess_r,
                                  center_y + self.chess_r, center_x + self.chess_r,
                                  fill=color)

    def draw_board(self):
        for (x, y) in product(range(self.row), range(self.column)):
            self.draw_mesh(x, y)

    def center_show(self, text):
        width, height = int(self.c_chess['width']), int(self.c_chess['height'])
        self.c_chess.create_text(int(width / 2), int(height / 2), text=text, font=("consolas", 50, "bold"), fill="black")

    def bf_start(self):
        self.set_btn_state("start")
        self.is_start = True
        self.is_black = True
        self.matrix = [[0 for _ in range(self.column)] for _ in range(self.row)]
        self.draw_board()
        self.l_info.config(text="Black to play chess")

    def bf_restart(self):
        self.bf_start()

    def bf_regret(self):
        if not self.last_p:
            messagebox.showinfo("Hints", "There is no turning back now")
            return
        x, y = self.last_p
        self.draw_mesh(x, y)
        self.matrix[x][y] = 0
        self.last_p = None
        self.trans_identify()

    def bf_lose(self):
        self.set_btn_state("init")
        self.is_start = False
        text = "Black throw in the towel" if self.is_black else "White throw in the towel"
        self.l_info.config(text=text)
        self.center_show("You are too weak!")

    def cf_board(self, e):
        x, y = int((e.y - self.step) / self.mesh), int((e.x - self.step) / self.mesh)
        distance = self.calculate_distance(x, y, e)

        if distance > self.step * 0.95 or self.matrix[x][y] != 0 or not self.is_start:
            return

        self.make_move(x, y)

    def calculate_distance(self, x, y, e):
        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
        return ((center_x - e.y) ** 2 + (center_y - e.x) ** 2) ** 0.5

    def make_move(self, x, y):
        color = "black" if self.is_black else "white"
        tag = 1 if self.is_black else -1

        self.draw_chess(x, y, color)
        self.matrix[x][y] = tag
        self.last_p = [x, y]

        if self.is_win(x, y, tag):
            self.is_start = False
            self.set_btn_state("init")
            text = "Black win!" if self.is_black else "White win!"
            self.center_show(text)

        self.trans_identify()

    def is_win(self, x, y, tag):
        def direction(i, j, di, dj, row, column, matrix):
            temp = []
            while 0 <= i < row and 0 <= j < column:
                i, j = i + di, j + dj
            i, j = i - di, j - dj
            while 0 <= i < row and 0 <= j < column:
                temp.append(matrix[i][j])
                i, j = i - di, j - dj
            return temp

        four_direction = []
        four_direction.append([self.matrix[i][y] for i in range(self.row)])
        four_direction.append([self.matrix[x][j] for j in range(self.column)])
        four_direction.append(direction(x, y, 1, 1, self.row, self.column, self.matrix))
        four_direction.append(direction(x, y, 1, -1, self.row, self.column, self.matrix))

        for v_list in four_direction:
            count = 0
            for v in v_list:
                if v == tag:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    def set_btn_state(self, state):
        state_list = [tk.NORMAL, tk.DISABLED, tk.DISABLED, tk.DISABLED] if state == "init" else [tk.DISABLED, tk.NORMAL, tk.NORMAL, tk.NORMAL]
        self.b_start.config(state=state_list[0])
        self.b_restart.config(state=state_list[1])
        self.b_regret.config(state=state_list[2])
        self.b_lose.config(state=state_list[3])

    def ternary_operator(self, true, false):
        return true if self.is_black else false

    def trans_identify(self):
        self.is_black = not self.is_black
        text = self.ternary_operator("Black to play chess", "White to play chess")
        self.l_info.config(text=text)


if __name__ == '__main__':
    Chess()