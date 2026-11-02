import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYER_COUNT]
COLUMN_INDICES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(COLUMN_INDICES[:len(board[0])]))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    if column not in COLUMN_INDICES[:len(board[0])]:
        return False
    col_index = COLUMN_INDICES.index(column)
    return board[0][col_index] == " "

def get_lowest_empty_row(column, board):
    col_index = COLUMN_INDICES.index(column)
    for row_index in reversed(range(len(board))):
        if board[row_index][col_index] == " ":
            return row_index
    return None

def place_checker(board, column, checker):
    row_index = get_lowest_empty_row(column, board)
    if row_index is not None:
        col_index = COLUMN_INDICES.index(column)
        board[row_index][col_index] = checker
        return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Check vertical
    for col_index in range(len(board[0])):
        for row_index in range(len(board) - 3):
            if all(board[row_index + offset][col_index] == checker for offset in range(4)):
                return True

    # Check diagonals
    for row_index in range(len(board) - 3):
        for col_index in range(len(board[0]) - 3):
            if all(board[row_index + offset][col_index + offset] == checker for offset in range(4)):
                return True
            if all(board[row_index + 3 - offset][col_index + offset] == checker for offset in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYER_COUNT - 1)

    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        column = input(f"Player {checker}, please enter a column: ").upper()

        if not is_valid_column(column, board):
            print("Invalid input! Please enter a valid column.")
            continue

        if not place_checker(board, column, checker):
            print("Column is full! You lose your turn.")
            current_player = (current_player + 1) % PLAYER_COUNT
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    play_game()
