import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4

# Players and their checkers (up to 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Game settings - 6x7 board and 2 players as per submission requirements
NUM_PLAYERS = 2


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    # Print the board rows with separators
    row_sep = "+---" * len(board[0]) + "+"
    for row in board:
        print(row_sep)
        print("| " + " | ".join(row) + " |")
    print(row_sep)


def is_valid_column_choice(choice, columns):
    if len(choice) != 1:
        return False
    ch = choice.upper()
    if 'A' <= ch < chr(ord('A') + columns):
        return True
    return False


def get_column_index(choice):
    # Convert column letter to index
    return ord(choice.upper()) - ord('A')


def place_checker(board, col_index, checker):
    """
    Places a checker in the lowest available row in the given column.
    Returns True if placed successfully, False if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            matched = True
            for i in range(WIN_COUNT):
                if board[r + i][c + i] != checker:
                    matched = False
                    break
            if matched:
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            matched = True
            for i in range(WIN_COUNT):
                if board[r - i][c + i] != checker:
                    matched = False
                    break
            if matched:
                return True

    return False


def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True


def get_valid_player_input(player_checker, columns):
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip()
        if not is_valid_column_choice(choice, columns):
            # Invalid input, prompt again
            continue
        col_idx = get_column_index(choice)
        # Check if the column is full before returning
        # We allow the turn to be lost if column is full, so we return the index anyway
        return col_idx


def main():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]

        col_idx = get_valid_player_input(current_checker, COLUMNS)

        placed = place_checker(board, col_idx, current_checker)

        print_board(board)

        if not placed:
            # Column full, turn lost
            # No win or draw check, just next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Check win for current player
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if is_board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
