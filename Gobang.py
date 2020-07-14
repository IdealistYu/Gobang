from tkinter import *
from tkinter.messagebox import *
  
  
class Chess(object):
  
 def __init__(self):
  self.row, self.column = 19, 19
  self.mesh = 40
  self.ratio = 0.7
  self.board_color = "#CDBA96"
  self.header_bg = "black"
  self.btn_font = ("consolas", 10, "bold")
  self.step = self.mesh / 2
  self.chess_r = self.step * self.ratio
  self.point_r = self.step * 0.2
  self.matrix = [[0 for y in range(self.column)] for x in range(self.row)]
  self.is_start = False
  self.is_black = True
  self.last_p = None
  
  self.root = Tk()
  self.root.title("Gobang By Zhang Haoyu")
  self.root.resizable(width=False, height=False)
  
  self.f_header = Frame(self.root, highlightthickness=0, bg=self.header_bg)
  self.f_header.pack(fill=BOTH, ipadx=10)
  
  self.b_start = Button(self.f_header, text="Start", command=self.bf_start, font=self.btn_font,activebackground='black',bd=5,bg='white',relief=RIDGE)
  self.b_restart = Button(self.f_header, text="Again", command=self.bf_restart, state=DISABLED, font=self.btn_font,activebackground='black',bd=5,bg='white',relief=RIDGE)
  self.l_info = Label(self.f_header, text="NotStarted", bg=self.header_bg, font=("consolas", 18, "bold"), fg="white")
  self.b_regret = Button(self.f_header, text="Undo", command=self.bf_regret, state=DISABLED, font=self.btn_font,activebackground='black',bd=5,bg='white',relief=RIDGE)
  self.b_lose = Button(self.f_header, text="Give in", command=self.bf_lose, state=DISABLED, font=self.btn_font,activebackground='black',bd=5,bg='white',relief=RIDGE)
  
  self.b_start.pack(side=LEFT, padx=20)
  self.b_restart.pack(side=LEFT)
  self.l_info.pack(side=LEFT, expand=YES, fill=BOTH, pady=10)
  self.b_lose.pack(side=RIGHT, padx=20)
  self.b_regret.pack(side=RIGHT)
  
  self.c_chess = Canvas(self.root, bg=self.board_color, width=(self.column + 1) * self.mesh,
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
  [self.draw_mesh(x, y) for y in range(self.column) for x in range(self.row)]
  
 def center_show(self, text):
  width, height = int(self.c_chess['width']), int(self.c_chess['height'])
  self.c_chess.create_text(int(width / 2), int(height / 2), text=text, font=("concolas", 50, "bold"), fill="red")
  
 def bf_start(self):
  self.set_btn_state("start")
  self.is_start = True
  self.is_black = True
  self.matrix = [[0 for y in range(self.column)] for x in range(self.row)]
  self.draw_board()
  self.l_info.config(text="Black to play chess")
  
 def bf_restart(self):
  self.bf_start()
  
 def bf_regret(self):
  if not self.last_p:
   showinfo("Hints", "There is no turning back now")
   return
  x, y = self.last_p
  self.draw_mesh(x, y)
  self.matrix[x][y] = 0
  self.last_p = None
  self.trans_identify()

 def bf_lose(self):
  self.set_btn_state("init")
  self.is_start = False
  text = self.ternary_operator("Black throw in the towel", "White throw in the towel")
  self.l_info.config(text=text)
  self.center_show("You are too weak!")
  
 def cf_board(self, e):
  x, y = int((e.y - self.step) / self.mesh), int((e.x - self.step) / self.mesh)
  center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
  distance = ((center_x - e.y) ** 2 + (center_y - e.x) ** 2) ** 0.5
  if distance > self.step * 0.95 or self.matrix[x][y] != 0 or not self.is_start:
   return
  color = self.ternary_operator("black", "white")
  tag = self.ternary_operator(1, -1)
  self.draw_chess(x, y, color)
  self.matrix[x][y] = tag
  self.last_p = [x, y]
  if self.is_win(x, y, tag):
   self.is_start = False
   self.set_btn_state("init")
   text = self.ternary_operator("Black win!", "White win!")
   self.center_show(text)
   return
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
  state_list = [NORMAL, DISABLED, DISABLED, DISABLED] if state == "init" else [DISABLED, NORMAL, NORMAL, NORMAL]
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