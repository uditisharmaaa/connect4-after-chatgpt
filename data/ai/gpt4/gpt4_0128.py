import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Functions
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(chr(65 + col) for col in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(col_choice, board):
    return col_choice.isalpha() and \
           len(col_choice) == 1 and \
           'A' <= col_choice.upper() <= chr(65 + len(board[0]) - 1)

def is_column_full(col_index, board):
    return board[0][col_index] != " "

def drop_checker(board, col_index, symbol):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = symbol
            return True
    return False

def check_winner(board, rows, cols, connect_length=4):
    def check_direction(r, c, delta_r, delta_c):
        target = board[r][c]
        count = 0
        while (0 <= r < rows and 0 <= c < cols and board[r][c] == target):
            count += 1
            if count == connect_length:
                return True
            r += delta_r
            c += delta_c
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != " ":
                if check_direction(r, c, 0, 1) or \
                   check_direction(r, c, 1, 0) or \
                   check_direction(r, c, 1, 1) or \
                   check_direction(r, c, 1, -1):
                    return True
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main function
def connect_4():
    # Initialize variables
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Set this constant to initialize player count
    players = PLAYER_SYMBOLS[:num_players]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        col_choice = input("> ").strip().upper()

        if not is_valid_column(col_choice, board):
            print("Invalid column. Please enter a valid column letter.")
            continue

        col_index = ord(col_choice) - 65
        if is_column_full(col_index, board):
            print("Column is full. Please choose another column.")
            continue

        drop_checker(board, col_index, current_player)

        if check_winner(board, ROWS, COLUMNS):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % num_players]

# Run the game
if __name__ == "__main__":
    connect_4()
