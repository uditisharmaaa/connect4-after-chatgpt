import os
import random
import string

# Constants (you can change these for testing)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Use only as many checkers as players
PLAYERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Header with column letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    # Board grid
    sep = "+" + ("---+" * cols)
    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(sep)


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def place_checker(board, col_index, checker):
    # Place in the lowest available row in this column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return None  # Column is full


def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def check_win_from_cell(board, r, c, checker):
    if board[r][c] != checker:
        return False
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # forward direction
        nr, nc = r + dr, c + dc
        while in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
            count += 1
            nr += dr
            nc += dc
        # backward direction
        nr, nc = r - dr, c - dc
        while in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
            count += 1
            nr -= dr
            nc -= dc
        if count >= WIN_LENGTH:
            return True
    return False


def check_win(board, last_move, checker):
    if last_move is None:
        return False
    r, c = last_move
    return check_win_from_cell(board, r, c, checker)


def get_valid_column_input(cols):
    while True:
        user_input = input().strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter (e.g., A).")
            continue
        ch = user_input.upper()
        if ch < 'A' or ch >= chr(ord('A') + cols):
            print("Invalid input. Column out of range.")
            continue
        return ord(ch) - ord('A')


def main():
    # Validate constants
    if COLS > 26:
        raise ValueError("Maximum supported columns is 26.")
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("Number of players must be between 2 and 5.")

    board = create_board(ROWS, COLS)

    # Random starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board
    print_board(board)

    last_move = None
    winner = None

    while True:
        current_checker = PLAYERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        col_index = get_valid_column_input(COLS)

        move = place_checker(board, col_index, current_checker)
        print_board(board)

        if move is None:
            print("Column is full. Turn lost.")
        else:
            last_move = move
            if check_win(board, last_move, current_checker):
                winner = current_checker
                print(f"Player {winner} won!")
                break
            if is_board_full(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End of game


if __name__ == "__main__":
    main()
