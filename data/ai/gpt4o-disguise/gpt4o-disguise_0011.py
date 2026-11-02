import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
CHECKERS = CHECKERS[:PLAYERS]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = "   ".join([chr(ord('A') + i) for i in range(COLS)])
    print("  " + col_labels)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_column_choice():
    while True:
        choice = input("Enter a column: ").upper()
        if len(choice) == 1 and 'A' <= choice <= 'Z' and ord(choice) - ord('A') < COLS:
            return ord(choice) - ord('A')
        print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_winner(board, rows, cols, checker):
    for r in range(rows):
        for c in range(cols):
            if c <= cols - 4 and all(board[r][c+i] == checker for i in range(4)):
                return True
            if r <= rows - 4 and all(board[r+i][c] == checker for i in range(4)):
                return True
            if r <= rows - 4 and c <= cols - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            if r >= 3 and c <= cols - 4 and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect4_game():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player = random.choice(range(PLAYERS))
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        col = get_column_choice()
        
        if not place_checker(board, col, CHECKERS[current_player]):
            continue
        
        if check_winner(board, ROWS, COLS, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

connect4_game()
