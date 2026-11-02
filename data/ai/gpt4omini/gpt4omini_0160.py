import os
import random

# Constants for the game
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def valid_input(col_input):
    if len(col_input) != 1:
        return False
    if not col_input.isalpha() or not col_input.isupper():
        return False
    col_index = ord(col_input) - 65
    return 0 <= col_index < COLS

def get_column_from_input():
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ")
        if valid_input(user_input):
            return ord(user_input) - 65
        else:
            print("Invalid input. Please enter a valid column (A-G).")

def place_checker(board, col, player_checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_checker
            return True
    return False

def check_win(board, player_checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player_checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player_checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player_checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game logic
if __name__ == "__main__":
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        col = get_column_from_input()
        
        if not place_checker(board, col, current_player):
            print(f"Column {chr(65 + col)} is full. Turn lost.")
        else:
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % len(PLAYERS)
