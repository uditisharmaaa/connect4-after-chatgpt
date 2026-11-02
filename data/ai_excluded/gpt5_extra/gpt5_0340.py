import os
import random
import string

# Constants (edit these for different configurations)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Validations for constants
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS > 26:
    raise ValueError("COLS must be <= 26 (A-Z).")

PLAYERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)


def get_next_open_row(board, col):
    # Return the lowest available row index in the given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def check_win(board, piece):
    rows = len(board)
    cols = len(board[0])
    w = WIN_LENGTH

    # Horizontal
    for r in range(rows):
        for c in range(cols - w + 1):
            if all(board[r][c + i] == piece for i in range(w)):
                return True

    # Vertical
    for r in range(rows - w + 1):
        for c in range(cols):
            if all(board[r + i][c] == piece for i in range(w)):
                return True

    # Diagonal down-right
    for r in range(rows - w + 1):
        for c in range(cols - w + 1):
            if all(board[r + i][c + i] == piece for i in range(w)):
                return True

    # Diagonal up-right
    for r in range(w - 1, rows):
        for c in range(cols - w + 1):
            if all(board[r - i][c + i] == piece for i in range(w)):
                return True

    return False


def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True


def read_valid_column(cols):
    # Keep asking for input until the user provides a single uppercase letter within board range
    while True:
        user_in = input().strip()
        if len(user_in) != 1 or not user_in.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            print("Please enter a column:", end=" ")
            continue
        letter = user_in.upper()
        idx = ord(letter) - ord('A')
        if 0 <= idx < cols:
            return idx
        else:
            print("Invalid column. Please choose a letter from A to {}.".format(chr(ord('A') + cols - 1)))
            print("Please enter a column:", end=" ")


def game():
    board = create_board(ROWS, COLS)

    # Randomly select starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        player_piece = PLAYERS[current_player_idx]
        print(f"Player {player_piece}, please enter a column:", end=" ")

        col = read_valid_column(COLS)

        # If column is full, turn is invalid and the player loses the turn
        row = get_next_open_row(board, col)
        if row is None:
            # Column full: lose the turn, print updated board (no change) for clarity
            clear_screen()
            print_board(board)
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the checker
        drop_piece(board, row, col, player_piece)

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, player_piece):
            print(f"Player {player_piece} won!")
            break

        # Check draw
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    game()
