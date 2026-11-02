import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # Column labels A-G
    print(header)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_input(column, board):
    if column.isalpha() and column.upper() in [chr(65 + i) for i in range(len(board[0]))]:
        col_index = ord(column.upper()) - 65
        return board[0][col_index] == " "  # Check if the column is not completely filled
    return False

def place_checker(board, column, checker):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

def check_winner(board, player_checkers):
    for checker in player_checkers:
        # Check horizontal, vertical and diagonal wins
        for row in range(len(board)):
            for col in range(len(board[0])):
                if (
                    col + 3 < len(board[0]) and
                    all(board[row][col+i] == checker for i in range(4)) or
                    row + 3 < len(board) and
                    all(board[row+i][col] == checker for i in range(4)) or
                    row + 3 < len(board) and col + 3 < len(board[0]) and
                    all(board[row+i][col+i] == checker for i in range(4)) or
                    row - 3 >= 0 and col + 3 < len(board[0]) and
                    all(board[row-i][col+i] == checker for i in range(4))
                ):
                    return checker
    return None

def is_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def play_game(num_players=2, rows=ROWS, columns=COLUMNS):
    board = initialize_board(rows, columns)
    player_checkers = CHECKERS[:num_players]
    random.shuffle(player_checkers)
    current_player_index = 0

    print_board(board)

    while True:
        current_checker = player_checkers[current_player_index]
        move = input(f"Player {current_checker}, please enter a column: ").strip()

        if not is_valid_input(move, board):
            print("Invalid input. Please try again.")
            continue

        place_checker(board, move, current_checker)
        print_board(board)

        winner = check_winner(board, player_checkers)
        if winner:
            print(f"Player {winner} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

# Set to 2 players and default board size for submission
play_game(num_players=2, rows=ROWS, columns=COLUMNS)
