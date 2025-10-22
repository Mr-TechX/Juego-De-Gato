import tkinter as tk
from tkinter import messagebox
import time

BG = "#0b0f1a"
NEON_X = "#00fff0"
NEON_O = "#ff4dff"
LINE = "#0aff9d"
CELL_BG = "#071225"
GLOW_COLORS = ["#00fff0", "#00ffd6", "#00ffb8", "#00ff9a"]

FONT_LARGE = ("Helvetica", 18, "bold")
FONT_MED = ("Helvetica", 12, "bold")
CELL_SIZE = 140
BOARD_SIZE = 3
CANVAS_SIZE = CELL_SIZE * BOARD_SIZE

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        root.title("Gato Neon - Contra la Máquina (Minimax)")
        root.configure(bg=BG)

        self.board = [[None]*3 for _ in range(3)]
        self.current = 'X'
        self.player_symbol = 'X'
        self.computer_symbol = 'O'
        self.scores = {'X': 0, 'O': 0, 'Empates': 0}
        self.game_over = False

        self.build_ui()
        self.draw_board_grid()
        self.update_score_labels()
        self.animate_glow()

    def build_ui(self):
        top_frame = tk.Frame(self.root, bg=BG)
        top_frame.pack(padx=12, pady=12, anchor='nw')

        sel_frame = tk.LabelFrame(top_frame, text="Elige tu símbolo", fg="white", bg=BG, font=FONT_MED)
        sel_frame.pack(side='left', padx=10)

        self.sel_var = tk.StringVar(value='X')
        rb_x = tk.Radiobutton(sel_frame, text='X', variable=self.sel_var, value='X', bg=BG, fg=NEON_X,
                              selectcolor=BG, font=FONT_MED, command=self.change_symbol)
        rb_o = tk.Radiobutton(sel_frame, text='O', variable=self.sel_var, value='O', bg=BG, fg=NEON_O,
                              selectcolor=BG, font=FONT_MED, command=self.change_symbol)
        rb_x.pack(side='left', padx=8)
        rb_o.pack(side='left', padx=8)

        btn_frame = tk.Frame(top_frame, bg=BG)
        btn_frame.pack(side='left', padx=20)
        tk.Button(btn_frame, text='Nueva ronda', command=self.new_round, font=FONT_MED).pack(side='left', padx=6)
        tk.Button(btn_frame, text='Reiniciar puntaje', command=self.reset_scores, font=FONT_MED).pack(side='left', padx=6)

        score_frame = tk.Frame(self.root, bg=BG)
        score_frame.pack(padx=12, pady=(0,8), anchor='w')

        self.score_x_label = tk.Label(score_frame, text='X: 0', bg=BG, fg=NEON_X, font=FONT_MED)
        self.score_o_label = tk.Label(score_frame, text='O: 0', bg=BG, fg=NEON_O, font=FONT_MED)
        self.score_emp_label = tk.Label(score_frame, text='Empates: 0', bg=BG, fg='white', font=FONT_MED)
        self.turn_label = tk.Label(score_frame, text='Turno: X', bg=BG, fg='white', font=FONT_MED)

        self.score_x_label.pack(side='left', padx=10)
        self.score_o_label.pack(side='left', padx=10)
        self.score_emp_label.pack(side='left', padx=10)
        self.turn_label.pack(side='left', padx=20)

        self.canvas = tk.Canvas(self.root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=CELL_BG, highlightthickness=0)
        self.canvas.pack(padx=12, pady=8)
        self.canvas.bind('<Button-1>', self.player_move)

    def draw_board_grid(self):
        self.canvas.delete('grid')
        for i in range(1, BOARD_SIZE):
            x = i * CELL_SIZE
            y = i * CELL_SIZE
            self.canvas.create_line(x, 6, x, CANVAS_SIZE-6, fill=LINE, width=3, tags='grid')
            self.canvas.create_line(6, y, CANVAS_SIZE-6, y, fill=LINE, width=3, tags='grid')

    def change_symbol(self):
        self.player_symbol = self.sel_var.get()
        self.computer_symbol = 'O' if self.player_symbol == 'X' else 'X'
        self.current = 'X'
        self.turn_label.config(text=f'Turno: {self.current}')
        self.new_round()

    def player_move(self, event):
        if self.game_over or self.current != self.player_symbol:
            return
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if self.board[row][col] is not None:
            return
        self.make_move(row, col, self.player_symbol)
        if not self.game_over:
            self.root.after(400, self.ai_move)

    def make_move(self, r, c, sym):
        self.board[r][c] = sym
        self.draw_symbol(r, c, sym)
        if self.check_win(sym):
            self.game_over = True
            self.scores[sym] += 1
            self.update_score_labels()
            messagebox.showinfo('Ganador', f'¡Gana {sym}!')
        elif self.check_draw():
            self.game_over = True
            self.scores['Empates'] += 1
            self.update_score_labels()
            messagebox.showinfo('Empate', '¡Es un empate!')
        else:
            self.current = 'O' if self.current == 'X' else 'X'
            self.turn_label.config(text=f'Turno: {self.current}')

    def ai_move(self):
        if self.game_over:
            return
        best_score = -float('inf')
        move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] is None:
                    self.board[r][c] = self.computer_symbol
                    score = self.minimax(False)
                    self.board[r][c] = None
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        if move:
            self.make_move(move[0], move[1], self.computer_symbol)

    def minimax(self, is_maximizing):
        if self.check_win(self.computer_symbol):
            return 1
        elif self.check_win(self.player_symbol):
            return -1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best = -float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] is None:
                        self.board[r][c] = self.computer_symbol
                        score = self.minimax(False)
                        self.board[r][c] = None
                        best = max(best, score)
            return best
        else:
            best = float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] is None:
                        self.board[r][c] = self.player_symbol
                        score = self.minimax(True)
                        self.board[r][c] = None
                        best = min(best, score)
            return best

    def draw_symbol(self, r, c, symbol):
        x1 = c * CELL_SIZE + 10
        y1 = r * CELL_SIZE + 10
        x2 = (c+1) * CELL_SIZE - 10
        y2 = (r+1) * CELL_SIZE - 10
        if symbol == 'X':
            self.canvas.create_line(x1, y1, x2, y2, fill=NEON_X, width=5)
            self.canvas.create_line(x1, y2, x2, y1, fill=NEON_X, width=5)
        else:
            self.canvas.create_oval(x1, y1, x2, y2, outline=NEON_O, width=5)

    def check_win(self, sym):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == sym: return True
            if b[0][i] == b[1][i] == b[2][i] == sym: return True
        if b[0][0] == b[1][1] == b[2][2] == sym: return True
        if b[0][2] == b[1][1] == b[2][0] == sym: return True
        return False

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell is None:
                    return False
        return True

    def update_score_labels(self):
        self.score_x_label.config(text=f"X: {self.scores['X']}")
        self.score_o_label.config(text=f"O: {self.scores['O']}")
        self.score_emp_label.config(text=f"Empates: {self.scores['Empates']}")

    def new_round(self):
        self.board = [[None]*3 for _ in range(3)]
        self.canvas.delete('all')
        self.draw_board_grid()
        self.game_over = False
        self.current = 'X'
        self.turn_label.config(text=f'Turno: {self.current}')
        if self.computer_symbol == 'X':
            self.ai_move()

    def reset_scores(self):
        self.scores = {'X': 0, 'O': 0, 'Empates': 0}
        self.update_score_labels()
        self.new_round()

    def animate_glow(self):
        self.root.after(300, self.animate_glow)

if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeAI(root)
    root.mainloop()

