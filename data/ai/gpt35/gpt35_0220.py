import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LETTERS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LETTERS))
    sep = "+---" * COLS + "+"
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)


def get_player_input(player_checker):
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col) != 1:
            print("Invalid input. Enter a single letter corresponding to a column.")
            continue
        if col not in COLUMN_LETTERS:
            print(f"Invalid column. Please enter a letter between {COLUMN_LETTERS[0]} and {COLUMN_LETTERS[-1]}.")
            continue
        return COLUMN_LETTERS.index(col)


def place_checker(board, col, checker):
    """
    Places the checker in the given column if possible.
    Returns True if placed successfully, False if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal right-down check (\)
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal left-down check (/)
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(WIN_COUNT - 1, COLS):
            if all(board[r + i][c - i] == checker for i in range(WIN_COUNT)):
                return True

    return False


def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS_COUNT]

    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        col = get_player_input(current_checker)

        if not place_checker(board, col, current_checker):
            # Column full, player loses turn as per specification
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            print_board(board)
            continue

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT


if __name__ == "__main__":
    main()
