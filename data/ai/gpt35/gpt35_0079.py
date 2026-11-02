import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Must be between MIN_PLAYERS and MAX_PLAYERS

CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print top border
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")


def valid_input(user_input):
    if len(user_input) != 1:
        return False
    if user_input not in COLUMN_LABELS:
        return False
    return True


def place_checker(board, col_letter, checker):
    col = COLUMN_LABELS.index(col_letter)
    # Find the lowest empty row in column
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    # Column full -> player loses turn
    return False


def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True


def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal \ check
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal / check
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLUMNS - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    return False


def main():
    board = create_board(ROWS, COLUMNS)
    # Randomly select first player
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        player_checker = CHECKERS[current_idx]

        # Prompt user input until valid or column full (lose turn)
        while True:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            if not valid_input(user_input):
                # Invalid input, ask again
                continue
            # Check if column is full
            if board[0][COLUMN_LABELS.index(user_input)] != " ":
                # Column full, player loses turn – break to switch player
                break
            # Place checker and break if success
            placed = place_checker(board, user_input, player_checker)
            if placed:
                break
            else:
                # Column full (should never get here because checked above), treat as lose turn
                break

        # If we placed a checker, check win or draw
        if user_input in COLUMN_LABELS and board[0][COLUMN_LABELS.index(user_input)] != " ":
            if check_win(board, player_checker):
                clear_screen()
                print_board(board)
                print(f"Player {player_checker} won!")
                return
            if board_full(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                return

        # Change to next player
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
