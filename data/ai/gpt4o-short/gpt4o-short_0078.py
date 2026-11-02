import os
import random

# Configuration Constants
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change as required, should be 2 to 5

# Game Variables
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')  # Use 'cls' if on Windows

def print_board():
    clear_screen()
    print("  " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("  " + " ".join(COLUMN_LABELS))

def is_valid_move(column):
    return 0 <= column < COLS and board[0][column] == ' '

def make_move(column, symbol):
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = symbol
            return

def is_winning_move(symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][c] == symbol for c in range(col, col + 4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[r][col] == symbol for r in range(row, row + 4)):
                return True

    # Check ascending diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    # Check descending diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    return False

def is_draw():
    return all(board[0][col] != ' ' for col in range(COLS))

def connect4():
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board()
        current_player_symbol = player_symbols[current_player_index]
        move = input(f"Player {current_player_symbol}, choose a column (A-G): ").strip().upper()
        
        if move in COLUMN_LABELS:
            col_idx = COLUMN_LABELS.index(move)
            if is_valid_move(col_idx):
                make_move(col_idx, current_player_symbol)
                
                if is_winning_move(current_player_symbol):
                    print_board()
                    print(f"Player {current_player_symbol} wins!")
                    break

                if is_draw():
                    print_board()
                    print("It's a draw!")
                    break

                current_player_index = (current_player_index + 1) % NUM_PLAYERS
            else:
                print("Invalid move, try again.")
        else:
            print("Invalid input, try again.")

if __name__ == "__main__":
    connect4()
