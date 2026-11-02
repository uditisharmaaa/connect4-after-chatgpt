import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_headers = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # A, B, C...
    print(column_headers)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def get_valid_columns(board):
    return [chr(65 + i) for i in range(len(board[0])) if board[0][i] == " "]

def drop_checker(board, column, player_mark):
    col_index = ord(column) - 65
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_mark
            return

def is_winner(board, player_mark):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player_mark for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == player_mark for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player_mark for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == player_mark for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_player_input(valid_columns):
    while True:
        column = input("Please enter a column: ").strip().upper()
        if column in valid_columns:
            return column
        print("Invalid input. Try again.")

def play_game():
    # Initialize board
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_MARKS[:2]  # Set to 2 players for submission, can be adjusted to MAX_PLAYERS
    random.shuffle(players)
    current_player_index = 0

    while True:
        print_board(board)
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print("The game is a draw!")
            break

        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")

        column = get_player_input(valid_columns)
        drop_checker(board, column, current_player)

        if is_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(players)

if __name__ == "__main__":
    play_game()
