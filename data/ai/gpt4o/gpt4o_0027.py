import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print("  " + column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_input(board):
    valid_range = [chr(65 + i) for i in range(len(board[0]))]
    while True:
        user_input = input("Please enter a column: ").upper()
        if len(user_input) == 1 and user_input in valid_range:
            if board[0][valid_range.index(user_input)] == " ":
                return valid_range.index(user_input)
            else:
                print(f"Column {user_input} is full. Choose another.")
        else:
            print("Invalid input. Try again.")

def place_checker(board, column, checker):
    for row in range(len(board)-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return board

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if check_horizontal(board, row, col, checker) or \
               check_vertical(board, row, col, checker) or \
               check_diagonal(board, row, col, checker):
                return True
    return False

def check_horizontal(board, row, col, checker):
    if col + 3 < COLUMNS and all(board[row][col + i] == checker for i in range(4)):
        return True
    return False

def check_vertical(board, row, col, checker):
    if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
        return True
    return False

def check_diagonal(board, row, col, checker):
    if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == checker for i in range(4)):
        return True
    if row - 3 >= 0 and col + 3 < COLUMNS and all(board[row - i][col + i] == checker for i in range(4)):
        return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.choice(range(NUM_PLAYERS))
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]} turn.")
        column = get_valid_input(board)
        board = place_checker(board, column, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
