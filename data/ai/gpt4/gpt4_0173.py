import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def drop_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return True
    return False

def is_valid_move(col):
    return 0 <= col < COLS

def check_winner(board, symbol):
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == symbol for i in range(4)):  # Horizontal
                return True
            if r + 3 < ROWS and all(board[r + i][c] == symbol for i in range(4)):  # Vertical
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == symbol for i in range(4)):  # Diagonal \
                return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == symbol for i in range(4)):  # Diagonal /
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board()
    num_players = 2  # Default to 2 players
    symbols = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        symbol = symbols[current_player]
        print(f"Player {symbol}, please enter a column:")
        col_input = input().strip().upper()

        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Enter a single letter.")
            continue

        col = ord(col_input) - 65

        if not is_valid_move(col) or not drop_checker(board, col, symbol):
            print("Column full or invalid. Try again.")
            continue

        print_board(board)

        if check_winner(board, symbol):
            print(f"Player {symbol} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
