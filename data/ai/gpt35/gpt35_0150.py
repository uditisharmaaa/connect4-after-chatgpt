import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
WIN_LEN = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels (A, B, C...)
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    hor_line = "+" + "---+" * len(board[0])
    for r in range(len(board)):
        print(hor_line)
        row_str = "|"
        for c in range(len(board[r])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(hor_line)

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if col_char < 'A' or col_char >= chr(ord('A') + cols):
        return False
    return True

def col_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest empty spot in column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return -1, -1  # Column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, last_row, last_col, checker):
    # Check vertically
    total = check_direction(board, last_row, last_col, 1, 0, checker) + check_direction(board, last_row-1, last_col, -1, 0, checker) - 1
    if total >= WIN_LEN:
        return True

    # Check horizontally
    total = check_direction(board, last_row, last_col, 0, 1, checker) + check_direction(board, last_row, last_col-1, 0, -1, checker) - 1
    if total >= WIN_LEN:
        return True

    # Check diagonal \
    total = check_direction(board, last_row, last_col, 1, 1, checker) + check_direction(board, last_row-1, last_col-1, -1, -1, checker) - 1
    if total >= WIN_LEN:
        return True

    # Check diagonal /
    total = check_direction(board, last_row, last_col, 1, -1, checker) + check_direction(board, last_row-1, last_col+1, -1, 1, checker) - 1
    if total >= WIN_LEN:
        return True

    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS -1)
    while True:
        print_board(board)
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        col_char = input(prompt).strip().upper()

        # Validate input
        while not is_valid_column(col_char, COLS):
            print("Invalid input. Please enter a valid column letter.")
            col_char = input(prompt).strip().upper()
        col = col_index(col_char)
        row, col_placed = place_checker(board, col, current_checker)
        if row == -1:
            # Column full, player loses turn
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        # Check win
        if check_win(board, row, col_placed, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
