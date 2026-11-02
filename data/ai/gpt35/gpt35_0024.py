import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
MAX_COLUMNS = 26  # max allowed columns

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(columns)]
    print(" ", end=" ")
    for label in labels:
        print(f" {label} ", end=" ")
    print()
    # Print horizontal separator line
    line = "+" + "---+" * columns
    for r in range(rows):
        print(line)
        print("|", end="")
        for c in range(columns):
            print(f" {board[r][c]} |", end="")
        print()
    print(line)

def valid_column_input(input_str, columns):
    if len(input_str) != 1:
        return False
    letter = input_str.upper()
    if letter < 'A' or letter >= chr(ord('A') + columns):
        return False
    return True

def column_index(column_letter):
    return ord(column_letter.upper()) - ord('A')

def place_checker(board, col, checker):
    rows = len(board)
    # Start from bottom, find first empty row in column
    for row in range(rows-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return -1, -1  # column full

def check_win(board, row, col, checker):
    rows = len(board)
    columns = len(board[0])

    def count_dir(r_step, c_step):
        count = 1  # include current cell
        # Check forward
        r, c = row + r_step, col + c_step
        while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        # Check backward
        r, c = row - r_step, col - c_step
        while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
            count += 1
            r -= r_step
            c -= c_step
        return count

    # Horizontal
    if count_dir(0, 1) >= WIN_COUNT:
        return True
    # Vertical
    if count_dir(1, 0) >= WIN_COUNT:
        return True
    # Diagonal down-right / up-left
    if count_dir(1, 1) >= WIN_COUNT:
        return True
    # Diagonal down-left / up-right
    if count_dir(1, -1) >= WIN_COUNT:
        return True

    return False

def board_full(board):
    # if any cell in top row is empty, board not full (since checkers fall down)
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def main():
    # Validate constants (according to assignment)
    rows = ROWS
    columns = COLUMNS
    players = PLAYERS
    if columns > MAX_COLUMNS:
        raise ValueError(f"Columns cannot exceed {MAX_COLUMNS}")

    checker_list = CHECKERS[:players]

    board = create_board(rows, columns)

    # Choose starting player randomly by index in checker_list
    current_player_idx = random.randint(0, players - 1)

    print_board(board)

    while True:
        current_checker = checker_list[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        # Input loop (validate input)
        while True:
            user_input = input(prompt).strip()
            if not valid_column_input(user_input, columns):
                # Invalid input: ask again
                continue
            col_idx = column_index(user_input)
            # Try to place checker (check if column full)
            r, c = place_checker(board, col_idx, current_checker)
            if r == -1:
                # Column full -> lose turn (break input loop)
                # Per assignment: player loses turn on full column, no retry
                # So just break here and go to next player
                break
            else:
                # Successfully placed checker
                break

        print_board(board)

        # If placed successfully check for win
        if r != -1:
            if check_win(board, r, c, current_checker):
                print(f"Player {current_checker} won!")
                return

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % players

if __name__ == "__main__":
    main()
