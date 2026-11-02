import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]

# Current game state
board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
current_player_index = random.randint(0, NUM_PLAYERS - 1)

def print_board():
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join([chr(ord('A') + i) for i in range(COLUMNS)]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_column(column):
    if len(column) != 1:
        return False
    if not column.isalpha() or not column.isupper():
        return False
    column_index = ord(column) - ord('A')
    if column_index < 0 or column_index >= COLUMNS:
        return False
    return board[0][column_index] == " "

def place_checker(column):
    column_index = ord(column) - ord('A')
    for i in range(ROWS - 1, -1, -1):
        if board[i][column_index] == " ":
            board[i][column_index] = CHECKERS[current_player_index]
            return

def check_for_win():
    def check_direction(x_step, y_step):
        for row in range(ROWS):
            for col in range(COLUMNS):
                checker = board[row][col]
                if checker == " ":
                    continue
                count = 0
                for i in range(4):
                    ni, nj = row + i*x_step, col + i*y_step
                    if ni < 0 or nj < 0 or ni >= ROWS or nj >= COLUMNS:
                        break
                    if board[ni][nj] == checker:
                        count += 1
                if count == 4:
                    return True
        return False

    return (check_direction(0, 1) or  # Horizontal
            check_direction(1, 0) or  # Vertical
            check_direction(1, 1) or  # Diagonal \
            check_direction(1, -1))   # Diagonal /

def is_draw():
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    global current_player_index
    print_board()
    while True:
        checker = CHECKERS[current_player_index]
        print(f"Player {checker}, enter a column:")
        column = input().strip()

        if not is_valid_column(column):
            print("Invalid input. Try again.")
            continue

        place_checker(column)
        print_board()

        if check_for_win():
            print(f"Player {checker} won!")
            break

        if is_draw():
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

play_game()
