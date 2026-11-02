import os
import random
import sys
import time

# -----------------------------
# Configuration (change if desired; submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7       # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5
PLAYER_SYMBOLS_ORDERED = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4, per assignment
# -----------------------------

def clear_screen():
    # Clear Linux/Unix terminal screen
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    header_letters = []
    for c in range(cols):
        header_letters.append(chr(ord('A') + c))
    print("  " + "   ".join(header_letters))
    # Top border
    print("+" + "---+" * cols)
    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)

def is_valid_column_letter(ch, cols):
    if len(ch) != 1 or not ch.isalpha():
        return False
    ch = ch.upper()
    if ch < 'A' or ch > chr(ord('A') + cols - 1):
        return False
    return True

def column_index_from_letter(ch):
    return ord(ch.upper()) - ord('A')

def drop_piece(board, col, symbol):
    """
    Drop a piece into column col.
    Returns the row index where the piece was placed, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row, place at the lowest empty space
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
        count = 0
        for c in range(cols):
            if board[r][c] == symbol:
                count += 1
                if count >= WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == symbol:
                count += 1
                if count >= WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal down-right
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            # Check 3 more steps down-right
            ok = True
            for k in range(1, WIN_LENGTH):
                rr = r + k
                cc = c + k
                if rr >= rows or cc >= cols or board[rr][cc] != symbol:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal up-right
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            ok = True
            for k in range(1, WIN_LENGTH):
                rr = r - k
                cc = c + k
                if rr < 0 or cc >= cols or board[rr][cc] != symbol:
                    ok = False
                    break
            if ok:
                return True

    return False

def check_draw(board):
    # Draw if no empty spaces left
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_active_symbols(num_players):
    if num_players < 2 or num_players > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    return PLAYER_SYMBOLS_ORDERED[:num_players]

def prompt_for_column(cols, current_symbol):
    """
    Prompt the current player until they provide a syntactically valid input (A..).
    Returns the validated column index (0-based).
    Note: If the player later picks a full column, they lose their turn (no re-prompt).
    """
    while True:
        try:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
        except EOFError:
            print("\nInput closed. Exiting game.")
            sys.exit(0)
        if is_valid_column_letter(user_input, cols):
            return column_index_from_letter(user_input)
        # Invalid input: keep asking
        print("Invalid input. Please enter a valid column letter within the board (e.g., A, B, C...).")

def main():
    # Validate configuration
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26 (inclusive).")
        return
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        return
    symbols = get_active_symbols(NUM_PLAYERS)

    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_idx = random.randrange(len(symbols))

    # Initial screen
    clear_screen()
    print_board(board)

    winner = None
    while True:
        current_symbol = symbols[current_idx]
        # Ask for input (must be valid letter)
        col = prompt_for_column(COLS, current_symbol)

        # Try to place
        placed_row = drop_piece(board, col, current_symbol)
        if placed_row is None:
            # Column full -> player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_symbol} loses the turn.")
            time.sleep(1.2)
            # Next player
            current_idx = (current_idx + 1) % len(symbols)
            continue

        # After placing, check for win
        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            winner = current_symbol
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        clear_screen()
        print_board(board)
        current_idx = (current_idx + 1) % len(symbols)

if __name__ == "__main__":
    main()
