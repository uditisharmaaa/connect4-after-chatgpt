import os
import random
import string

# Configuration constants
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 players

CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4  # Always 4 to win


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    os.system('clear')


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)
    print("+---" * cols + "+")

    # Rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+---" * cols + "+")


def column_letter_to_index(letter):
    return ord(letter) - ord('A')


def get_valid_column_input(cols, current_checker):
    max_letter = chr(ord('A') + cols - 1)
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or not user_input.isalpha():
            continue
        if 'A' <= user_input <= max_letter:
            return column_letter_to_index(user_input)


def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the specified column.
    # Returns (True, row_index) if placed, or (False, None) if column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r
    return False, None


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc) right, down, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == checker:
                    count += 1
                    if count >= WIN_LENGTH:
                        return True
                    nr += dr
                    nc += dc
    return False


def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Ensure configuration validity
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
    assert 1 <= COLS <= 26, "COLS must be between 1 and 26"

    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]

        # Prompt until valid column letter (format and in-range).
        col_idx = get_valid_column_input(COLS, current_checker)

        placed, _ = drop_checker(board, col_idx, current_checker)
        # If column full, player loses the turn (no re-prompt)
        if placed:
            # Print updated board after successful placement
            print_board(board)

            # Check for win
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if is_draw(board):
                print("It's a draw!")
                break
        else:
            # Column full: still show board (unchanged), then continue to next player
            print_board(board)

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
