import os
import random
import string

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7   # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" " for _ in range(cols)])
    return board


def clear_screen():
    os.system('clear')


def get_column_letters(cols):
    letters = []
    for i in range(cols):
        letters.append(string.ascii_uppercase[i])
    return letters


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    col_letters = get_column_letters(cols)
    # Header
    print("  " + "   ".join(col_letters))
    # Rows
    divider = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(divider)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(divider)


def column_index_from_input(col_input, cols):
    if len(col_input) != 1:
        return None
    if not col_input.isalpha():
        return None
    col_input = col_input.upper()
    idx = ord(col_input) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None


def drop_checker(board, col, symbol):
    # Place in the lowest available row in this column
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r][c + 1] == symbol and
                board[r][c + 2] == symbol and
                board[r][c + 3] == symbol):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == symbol and
                board[r + 1][c] == symbol and
                board[r + 2][c] == symbol and
                board[r + 3][c] == symbol):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r + 1][c + 1] == symbol and
                board[r + 2][c + 2] == symbol and
                board[r + 3][c + 3] == symbol):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r - 1][c + 1] == symbol and
                board[r - 2][c + 2] == symbol and
                board[r - 3][c + 3] == symbol):
                return True

    return False


def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    # Basic validations for constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    print_board(board)

    while True:
        current_symbol = symbols[current_player]
        print(f"Player {current_symbol}, please enter a column:")
        # Get valid input (must be a valid column letter)
        col_idx = None
        while col_idx is None:
            user_input = input().strip().upper()
            col_idx = column_index_from_input(user_input, COLS)
            if col_idx is None:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")

        # Try to drop checker
        placed_row = drop_checker(board, col_idx, current_symbol)
        if placed_row is None:
            # Column full -> turn is invalid and player loses the turn
            print("That column is full. You lose your turn.")
            # Print board again (no change, but for clarity)
            print_board(board)
            # Next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Show updated board
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
