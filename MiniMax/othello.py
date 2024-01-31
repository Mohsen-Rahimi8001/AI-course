import tkinter as tk
from tkinter import messagebox
import numpy as np


EMPTY = 0
BLACK = 1
WHITE = 2

class OthelloGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = BLACK

    def initialize_board(self):
        board = np.zeros((8, 8), dtype=np.int8)
        board[3, 3] = WHITE
        board[3, 4] = BLACK
        board[4, 3] = BLACK
        board[4, 4] = WHITE
        return board

    def is_valid_move(self, board, player, row, col):
        if board[row, col] != EMPTY:
            return False
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for d in directions:
            r, c = row + d[0], col + d[1]
            
            if r < 0 or r >= 8 or c < 0 or c >= 8:
                continue

            if board[r, c] == 3 - player:
                
                while True:
                
                    r += d[0]
                    c += d[1]
                
                    if r < 0 or r >= 8 or c < 0 or c >= 8:
                        break
                
                    if board[r, c] == EMPTY:
                        break
                
                    if board[r, c] == player:
                        return True

        return False


    def make_move(self, board, player, row, col):
        if not self.is_valid_move(board, player, row, col):
            return False

        board[row, col] = player
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for d in directions:
        
            r, c = row + d[0], col + d[1]
        
            if r < 0 or r >= 8 or c < 0 or c >= 8:
                continue
        
            if board[r, c] == 3 - player:
        
                path = []
        
                while True:
                    
                    path.append((r, c))
                    
                    r += d[0]
                    c += d[1]
                    
                    if r < 0 or r >= 8 or c < 0 or c >= 8:
                        break

                    if board[r, c] == EMPTY:
                        break

                    if board[r, c] == player:
                        for pos in path:
                            board[pos[0], pos[1]] = player

                        break

        return True


    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(self.board, player, row, col):
                    valid_moves.append((row, col))
        return valid_moves


    def evaluate_board(self, player):
        return np.sum(self.board == player) - np.sum(self.board == 3 - player)


    def minimax(self, baord, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_board(BLACK)

        valid_moves = self.get_valid_moves(BLACK if maximizing_player else WHITE)

        if len(valid_moves) == 0:

            if len(self.get_valid_moves(WHITE if maximizing_player else BLACK)) == 0:
                return self.evaluate_board(BLACK)
            else:
                return -self.minimax(baord, depth - 1, -beta, -alpha, not maximizing_player)

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = self.board.copy()
                self.make_move(new_board, BLACK, move[0], move[1])
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = self.board.copy()
                self.make_move(new_board, WHITE, move[0], move[1])
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


    def find_best_move(self, player, depth):
        valid_moves = self.get_valid_moves(player)
        best_move = None
        best_eval = float('-inf')
        
        for move in valid_moves:
            new_board = self.board.copy()
            self.make_move(new_board, player, move[0], move[1])
            eval = self.minimax(new_board, depth - 1, float('-inf'), float('inf'), False)

            if eval > best_eval:
                best_eval = eval
                best_move = move

        return best_move


class OthelloGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello")
        
        self.game = OthelloGame()
        self.current_player = BLACK

        self.canvas = tk.Canvas(master, width=400, height=400, bg="blue")
        self.canvas.pack()

        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.on_click)

        self.check_turn()

    def check_turn(self):
        if self.current_player == WHITE:
            self.ai_move()

        if self.is_game_over():
            self.end_game()
            return

        self.master.after(100, self.check_turn)

    def is_game_over(self):
        return (len(self.game.get_valid_moves(BLACK)) == 0 and self.current_player == BLACK) or (len(self.game.get_valid_moves(WHITE)) == 0 and self.current_player == WHITE)

    def end_game(self):
        black_count = np.sum(self.game.board == BLACK)
        white_count = np.sum(self.game.board == WHITE)
        if black_count > white_count:
            winner = "Black"
        elif white_count > black_count:
            winner = "White"
        else:
            winner = "Tie"

        messagebox.showinfo("Game Over", f"The game is over! Winner: {winner}")

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                x0, y0 = col * 50, row * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue", tags="square")

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                if self.game.board[row, col] == BLACK:
                    self.draw_piece(row, col, "black")
                elif self.game.board[row, col] == WHITE:
                    self.draw_piece(row, col, "white")

    def draw_piece(self, row, col, color):
        x, y = col * 50 + 25, row * 50 + 25
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, tags="piece")

    def on_click(self, event):
        if self.current_player == BLACK:
            col = event.x // 50
            row = event.y // 50
            if self.game.is_valid_move(self.game.board, BLACK, row, col):
                self.game.make_move(self.game.board, BLACK, row, col)
                self.draw_pieces()
                self.current_player = WHITE
            else:
                print("invalid")

    def ai_move(self):
        depth = 5
        move = self.game.find_best_move(WHITE, depth)
        if not move:
            self.end_game()
            return
            
        self.game.make_move(self.game.board, WHITE, move[0], move[1])
        self.draw_pieces()
        self.current_player = BLACK


if __name__ == "__main__":
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()
