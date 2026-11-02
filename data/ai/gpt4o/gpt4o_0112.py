import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    header = "  " + "   ".join([chr(i) for i in range(65, 65 + COLS)])  # Column labels A-G
    print(header)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(input_char):
    return len(input_char) == 1 and 'A' <= input_char <= chr(64 + COLS)

def drop_checker(board, col, symbol):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return True
    return False

def check_win(board, symbol):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == symbol for i in range(4)):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True
    
    # Diagonal check (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True

    # Diagonal check (/ direction)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    board = initialize_board(ROWS, COLS)
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_idx]
        print(f"Player {current_symbol}, please enter a column:")
        col_input = input().strip().upper()

        if not is_valid_input(col_input):
            print("Invalid input. Try again.")
            continue

        col = ord(col_input) - 65

        if not drop_checker(board, col, current_symbol):
            print("Column is full. You lose your turn.")
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        print_board(board)

        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

play_game()
