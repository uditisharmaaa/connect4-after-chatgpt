import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players
WIN_LENGTH = 4
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for __ in range(rows)]


def print_board(board):
    clear_screen()
    print('  ' + '   '.join(COL_LABELS))
    print('+---' * COLS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLS + '+')


def is_valid_column(col_char):
    return col_char in COL_LABELS


def column_to_index(col_char):
    return ord(col_char) - ord('A')


def place_checker(board, col_idx, checker):
    """
    Places the checker in the lowest available row in column col_idx.
    Returns True if placed successfully, False if the column is full.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return True
    return False


def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def check_winner(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (down-right) check
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (down-left) check
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, COLS):
            if all(board[r + i][c - i] == checker for i in range(WIN_LENGTH)):
                return True

    return False


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS)

    print_board(board)
    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        col_char = input(prompt).strip().upper()

        if not is_valid_column(col_char):
            # Invalid input, ask again (same player turn)
            continue

        col_idx = column_to_index(col_char)
        placed = place_checker(board, col_idx, current_checker)

        if not placed:
            # Column full, turn lost
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            print("Game ended in a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
