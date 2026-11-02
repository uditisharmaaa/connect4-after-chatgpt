import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYERS]
LETTERS = [chr(i) for i in range(ord('A'), ord('A') + COLS)]

# Helper functions
def init_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    print("  " + "   ".join(LETTERS))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_column_index(column):
    return ord(column) - ord('A') if column in LETTERS else -1

def is_valid_move(board, col_idx):
    return 0 <= col_idx < COLS and board[0][col_idx] == " "

def place_checker(board, col_idx, symbol):
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = symbol
            return True
    return False

def check_win(board, symbol):
    # Check horizontal
    for row in board:
        for c in range(COLS - 3):
            if all(row[c + i] == symbol for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True
    # Check diagonal (top-right to bottom-left)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r + i][c - i] == symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def next_player(current, total):
    return (current + 1) % total

# Main game function
def play_game():
    board = init_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column:")
        column = input().strip().upper()
        col_idx = get_column_index(column)

        if not is_valid_move(board, col_idx):
            print("Invalid move! Try again.")
            continue

        place_checker(board, col_idx, PLAYER_SYMBOLS[current_player])
        print_board(board)

        if check_win(board, PLAYER_SYMBOLS[current_player]):
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        current_player = next_player(current_player, PLAYERS)

# Run the game
if __name__ == "__main__":
    play_game()
