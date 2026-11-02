import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_COLUMNS_LABELS = [chr(65 + i) for i in range(COLUMNS)]  # ['A', 'B', ..., 'G']

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(BOARD_COLUMNS_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column):
    return column in BOARD_COLUMNS_LABELS

def is_column_full(board, column):
    return board[0][column] != " "

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_for_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                if all(board[row][col+j] == checker for j in range(4) if col+j < COLUMNS):
                    return True
                if all(board[row+i][col] == checker for i in range(4) if row+i < ROWS):
                    return True
                if all(board[row+i][col+j] == checker for i, j in zip(range(4), range(4)) if row+i < ROWS and col+j < COLUMNS):
                    return True
                if all(board[row+i][col-j] == checker for i, j in zip(range(4), range(4)) if row+i < ROWS and col-j >= 0):
                    return True
    return False

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    board = create_board()
    num_players = 2
    player_index = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        current_player_checker = PLAYER_CHECKERS[player_index]
        print(f"Player {current_player_checker}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column.")
            continue

        column_index = BOARD_COLUMNS_LABELS.index(user_input)

        if is_column_full(board, column_index):
            print("Column is full. Turn lost.")
            player_index = (player_index + 1) % num_players
            continue

        if place_checker(board, column_index, current_player_checker):
            print_board(board)

            if check_for_winner(board, current_player_checker):
                print(f"Player {current_player_checker} won!")
                break

            if check_for_draw(board):
                print("The game is a draw!")
                break

            player_index = (player_index + 1) % num_players

if __name__ == "__main__":
    play_game()
