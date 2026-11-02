import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def drop_checker(board, col, player_symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player_symbol
            return True
    return False

def is_valid_column(column_input):
    return len(column_input) == 1 and column_input.isalpha() and 'A' <= column_input <= chr(65 + COLS - 1)

def check_win(board, player_symbol):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == player_symbol for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == player_symbol for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == player_symbol for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_symbol = PLAYER_SYMBOLS[current_player_idx]
        user_input = input(f"Player {player_symbol}, please enter a column: ").upper()

        if not is_valid_column(user_input):
            continue

        col = ord(user_input) - 65

        if not drop_checker(board, col, player_symbol):
            continue

        print_board(board)

        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
