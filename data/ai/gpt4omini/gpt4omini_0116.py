import os
import random

# Constants for board dimensions and player checkers
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print(" ", "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+---" + "---+".join([""] * COLS) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+".join([""] * COLS) + "---+")

def get_valid_input(player):
    while True:
        choice = input(f"Player {player}, please enter a column (A-{chr(65+COLS-1)}): ").upper()
        if choice in (chr(65 + i) for i in range(COLS)):
            col = ord(choice) - 65
            if board[0][col] == ' ':  # Check if selected column is not full
                return col
            else:
                print("Column is full. Please choose another column.")
        else:
            print("Invalid input. Please enter a valid column label.")

def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

def check_winner(board, player):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Check horizontal
                if c <= COLS - 4 and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check vertical
                if r <= ROWS - 4 and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonal down-right
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonal down-left
                if r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == player for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game loop
board = initialize_board()
current_player = random.choice(PLAYERS)
print_board(board)

while True:
    col = get_valid_input(current_player)
    place_checker(board, col, current_player)
    print_board(board)
    
    if check_winner(board, current_player):
        print(f"Player {current_player} won!")
        break
    if check_draw(board):
        print("The game is a draw!")
        break
    
    # Change player
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
