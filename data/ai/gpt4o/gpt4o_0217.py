import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_headers = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_headers)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    return column in range(len(board[0]))

def is_column_full(column, board):
    return board[0][column] != " "

def place_checker(column, checker, board):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col <= COLUMNS - 4 and all(board[row][col+i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and all(board[row+i][col] == checker for i in range(4)):
                return True
            if col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if col >= 3 and row <= ROWS - 4 and all(board[row+i][col-i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    board = create_board(ROWS, COLUMNS)
    num_players = 2
    players = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    while True:
        checker = players[current_player_index]
        print_board(board)

        while True:
            try:
                column_input = input(f"Player {checker}, please enter a column: ").upper()
                column = ord(column_input) - 65
                if not is_valid_column(column, board) or is_column_full(column, board):
                    print("Invalid input, try again.")
                    continue
                break
            except (IndexError, ValueError):
                print("Invalid input, try again.")

        place_checker(column, checker, board)

        if check_winner(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

play_game()
