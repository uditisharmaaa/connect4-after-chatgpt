import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = "   ".join([chr(65 + i) for i in range(len(board[0]))])
    print(f"  {col_labels}")
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(col, board):
    if col.isalpha() and len(col) == 1:
        col_idx = ord(col.upper()) - 65
        if 0 <= col_idx < len(board[0]) and board[0][col_idx] == " ":
            return True
    return False

def drop_checker(board, col, checker):
    col_idx = ord(col.upper()) - 65
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return

def check_win(board, checker):
    # Horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True
    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        print(f"Player {players[current_player]}, please enter a column:")
        col = input().strip()
        
        if not is_valid_column(col, board):
            print("Invalid column. Try again.")
            continue
        
        drop_checker(board, col, players[current_player])
        print_board(board)
        
        if check_win(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

main()
