import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_player_input(current_player, board):
    while True:
        try:
            column_letter = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
            column_index = ord(column_letter) - ord('A')
            if column_index < 0 or column_index >= COLS:
                raise ValueError("Column out of range.")
            if board[0][column_index] != " ":
                raise ValueError("Column is full.")
            return column_index
        except ValueError as e:
            print(f"Invalid input: {e}")

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def play_game(num_players=2):
    board = initialize_board()
    print_board(board)
    current_player = random.randint(0, num_players - 1)

    while True:
        column_index = get_player_input(current_player, board)
        place_checker(board, column_index, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    play_game(2)
