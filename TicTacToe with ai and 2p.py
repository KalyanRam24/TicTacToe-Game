import tkinter as tk
from tkinter import messagebox
import random

def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def minimax(board, depth, is_maximizing, max_depth):
    winner = check_winner()
    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if all(board[r][c] != " " for r in range(3) for c in range(3)):
        return 0
    if depth >= max_depth:
        return 0  # Approximate evaluation
    
    if is_maximizing:
        best_score = -float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "O"
                    score = minimax(board, depth + 1, False, max_depth)
                    board[r][c] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "X"
                    score = minimax(board, depth + 1, True, max_depth)
                    board[r][c] = " "
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    global turn
    best_score = -float("inf")
    best_move = None
    max_depth = difficulty_levels[difficulty]
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = "O"
                score = minimax(board, 0, False, max_depth)
                board[r][c] = " "
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    if best_move:
        row, col = best_move
        board[row][col] = "O"
        buttons[row][col].config(text="O", fg="red")
        winner = check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            reset_board()
        elif all(board[r][c] != " " for r in range(3) for c in range(3)):
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_board()
        else:
            turn += 1

def click(row, col):
    global turn
    if board[row][col] == " " and not game_over:
        board[row][col] = players[turn % 2]
        buttons[row][col].config(text=players[turn % 2], fg="blue")
        winner = check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            reset_board()
        elif all(board[r][c] != " " for r in range(3) for c in range(3)):
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_board()
        else:
            turn += 1
            if game_mode == "AI" and turn % 2 == 1:
                ai_move()

def reset_board():
    global board, turn, game_over
    board = [[" " for _ in range(3)] for _ in range(3)]
    turn = 0
    game_over = False
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text=" ", fg="black", bg="#f0f0f0")

def set_difficulty(level):
    global difficulty
    difficulty = level
    difficulty_frame.destroy()

def set_game_mode(mode):
    global game_mode
    game_mode = mode
    mode_frame.destroy()
    if game_mode == "AI":
        global difficulty_frame
        difficulty_frame = tk.Frame(root, bg="#2c3e50")
        difficulty_frame.pack(pady=20)
        tk.Label(difficulty_frame, text="Select Difficulty", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack()
        tk.Button(difficulty_frame, text="Easy", font=("Arial", 14), bg="#f1c40f", fg="black", width=15, height=2, command=lambda: set_difficulty("Easy")).pack(pady=5)
        tk.Button(difficulty_frame, text="Medium", font=("Arial", 14), bg="#e67e22", fg="white", width=15, height=2, command=lambda: set_difficulty("Medium")).pack(pady=5)
        tk.Button(difficulty_frame, text="Hard", font=("Arial", 14), bg="#e74c3c", fg="white", width=15, height=2, command=lambda: set_difficulty("Hard")).pack(pady=5)

root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg="#2c3e50")

mode_frame = tk.Frame(root, bg="#2c3e50")
mode_frame.pack(pady=20)

tk.Label(mode_frame, text="Choose Game Mode", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack()
tk.Button(mode_frame, text="Play vs AI", font=("Arial", 14), bg="#3498db", fg="white", width=15, height=2, command=lambda: set_game_mode("AI")).pack(pady=5)
tk.Button(mode_frame, text="Two Players", font=("Arial", 14), bg="#2ecc71", fg="white", width=15, height=2, command=lambda: set_game_mode("2P")).pack(pady=5)

root.wait_window(mode_frame)

difficulty_levels = {"Easy": 1, "Medium": 3, "Hard": 6}
difficulty = "Medium"

players = ["X", "O"]
turn = 0
board = [[" " for _ in range(3)] for _ in range(3)]
game_over = False

frame = tk.Frame(root, bg="#2c3e50")
frame.pack()

buttons = [[tk.Button(frame, text=" ", font=('Arial', 24, "bold"), height=2, width=5, bg="#ecf0f1", fg="black",
                      relief="ridge", command=lambda r=r, c=c: click(r, c)) for c in range(3)] for r in range(3)]

for r in range(3):
    for c in range(3):
        buttons[r][c].grid(row=r, column=c, padx=5, pady=5)

reset_button = tk.Button(root, text="Reset", font=('Arial', 16, "bold"), bg="#e74c3c", fg="white", width=10, height=1, command=reset_board)
reset_button.pack(pady=20)

root.mainloop()
