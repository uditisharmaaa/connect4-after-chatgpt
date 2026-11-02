import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print(" ", end="  ")
    for label in COLUMN_LABELS:
        print(label, end="   ")
    print()
    for row in board:
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * COLUMNS + "+")

def get_valid_column(player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        if col_input not in COLUMN_LABELS:
            print(f"Invalid column. Please choose from {', '.join(COLUMN_LABELS)}.")
            continue
        col_index = COLUMN_LABELS.index(col_input)
        return col_index

def place_checker(board, col, checker):
    # Place checker in lowest available row in the chosen column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # Column full
    return -1

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all directions from the placed checker position
    # Horizontal
    total = (check_direction(board, row, col, 0, -1, checker) - 1) + (check_direction(board, row, col, 0, 1, checker))
    if total >= WIN_COUNT:
        return True
    # Vertical
    total = (check_direction(board, row, col, -1, 0, checker) - 1) + (check_direction(board, row, col, 1, 0, checker))
    if total >= WIN_COUNT:
        return True
    # Diagonal /
    total = (check_direction(board, row, col, -1, 1, checker) - 1) + (check_direction(board, row, col, 1, -1, checker))
    if total >= WIN_COUNT:
        return True
    # Diagonal \
    total = (check_direction(board, row, col, -1, -1, checker) - 1) + (check_direction(board, row, col, 1, 1, checker))
    if total >= WIN_COUNT:
        return True
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_index]

        col = get_valid_column(current_checker)
        row = place_checker(board, col, current_checker)
        if row == -1:
            print(f"Column {COLUMN_LABELS[col]} is full. Turn lost.")
            # switch player even if turn is lost
            current_player_index = (current_player_index + 1) % PLAYERS
            input("Press Enter to continue...")
            continue

        if check_win(board, row, col, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
