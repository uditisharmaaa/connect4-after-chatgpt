import os
import random

ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  "
    for i in range(COLUMNS):
        labels += chr(ord('A') + i) + "   "
    print(labels)
    # Print board rows
    for row in range(ROWS):
        print("+" + "---+" * COLUMNS)
        row_str = "|"
        for col in range(COLUMNS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print("+" + "---+" * COLUMNS)

def is_valid_column(col_letter):
    if len(col_letter) != 1:
        return False
    if not ('A' <= col_letter <= chr(ord('A') + COLUMNS -1)):
        return False
    return True

def column_full(board, col_index):
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    # Place checker starting from bottom
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return None  # Column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, checker):
    # Check horizontally
    total = 1  # count current
    total += check_direction(board, row, col-1, 0, -1, checker)
    total += check_direction(board, row, col+1, 0, 1, checker)
    if total >= WIN_LENGTH:
        return True

    # Check vertically
    total = 1
    total += check_direction(board, row-1, col, -1, 0, checker)
    total += check_direction(board, row+1, col, 1, 0, checker)
    if total >= WIN_LENGTH:
        return True

    # Check diagonal (top-left to bottom-right)
    total = 1
    total += check_direction(board, row-1, col-1, -1, -1, checker)
    total += check_direction(board, row+1, col+1, 1, 1, checker)
    if total >= WIN_LENGTH:
        return True

    # Check diagonal (bottom-left to top-right)
    total = 1
    total += check_direction(board, row+1, col-1, 1, -1, checker)
    total += check_direction(board, row-1, col+1, -1, 1, checker)
    if total >= WIN_LENGTH:
        return True

    return False

def board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player_index]
        print(f"Player {checker}, please enter a column:")
        col_input = input().strip().upper()

        if not is_valid_column(col_input):
            continue  # Invalid input, ask again

        col_index = ord(col_input) - ord('A')
        if column_full(board, col_index):
            # Turn is lost if column full
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        result = place_checker(board, col_index, checker)
        if result is None:
            # Should not happen here because we check full before
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        row_placed, col_placed = result
        print_board(board)

        if check_win(board, row_placed, col_placed, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
