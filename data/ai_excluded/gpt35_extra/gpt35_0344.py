import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # support up to 5 players
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    # Print the top border
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)


def valid_column_input(user_input):
    if len(user_input) != 1:
        return False
    if user_input not in COLUMN_LABELS:
        return False
    return True


def get_available_row(board, col):
    # Check from bottom row up to find empty row
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1  # no space


def place_checker(board, col, checker):
    row = get_available_row(board, col)
    if row == -1:
        return False  # column full
    board[row][col] = checker
    return True


def is_winning_line(cells):
    """Helper to check if a line has WIN_COUNT of the same non-empty checker."""
    count = 0
    last = " "
    for cell in cells:
        if cell == last and cell != " ":
            count += 1
            if count >= WIN_COUNT:
                return True
        else:
            last = cell
            count = 1 if cell != " " else 0
    return False


def check_horizontal(board, checker):
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    return False


def check_vertical(board, checker):
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    return False


def check_diagonal(board, checker):
    # Check \ diagonals
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Check / diagonals
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    return False


def check_win(board, checker):
    return check_horizontal(board, checker) or \
           check_vertical(board, checker) or \
           check_diagonal(board, checker)


def check_draw(board):
    # If no empty space anywhere, it's a draw
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS_COUNT]

    current_index = random.randint(0, PLAYERS_COUNT - 1)

    while True:
        print_board(board)
        current_checker = players[current_index]
        prompt = f"Player {current_checker}, please enter a column: "
        user_input = input(prompt).strip().upper()

        if not valid_column_input(user_input):
            # Invalid input, retry without losing turn
            continue

        col = ord(user_input) - ord('A')
        if col < 0 or col >= COLS:
            # Should not happen due to valid_column_input but safe check
            continue

        success = place_checker(board, col, current_checker)
        if not success:
            # Column full, player loses the turn (skip to next player)
            current_index = (current_index + 1) % PLAYERS_COUNT
            continue

        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_index = (current_index + 1) % PLAYERS_COUNT


if __name__ == "__main__":
    main()
