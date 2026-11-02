import os
import random
import sys

# ----------------------------
# Configuration (adjustable)
# ----------------------------
NUM_ROWS = 6
NUM_COLS = 7          # Max 26
NUM_PLAYERS = 2       # Between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]  # In order

# Constants
WIN_LENGTH = 4
EMPTY_CELL = " "

# ----------------------------
# Utility and Game Functions
# ----------------------------

def clear_screen():
    # Clear the game screen (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def column_labels(num_cols):
    # Labels A.. up to max 26
    labels = []
    for i in range(num_cols):
        labels.append(chr(ord('A') + i))
    return labels

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header with column letters
    header = "  " + "   ".join(labels)
    print(header)
    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def get_player_symbols(num_players):
    return TOKENS[:num_players]

def get_column_input(current_player_symbol, num_cols):
    labels = column_labels(num_cols)
    valid_set = set(labels)
    prompt = f"Player {current_player_symbol}, please enter a column: "
    while True:
        try:
            raw = input(prompt)
        except EOFError:
            # Gracefully end if no input stream
            sys.exit(0)
        if not raw:
            continue
        ch = raw.strip()
        if not ch:
            continue
        ch = ch[0].upper()
        if ch in valid_set:
            return labels.index(ch)
        # Invalid input; ask again (turn not lost)
        print(f"Invalid input. Please enter a letter between {labels[0]} and {labels[-1]}.")

def place_checker(board, col, symbol):
    # Place checker in the lowest available row in the given column.
    # Returns True if placed, False if column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == EMPTY_CELL:
            board[r][col] = symbol
            return True
    return False

def check_direction(board, start_r, start_c, dr, dc, symbol):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    while 0 <= r < rows and 0 <= c < cols:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += dr
        c += dc
    return False

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Horizontal checks for each row
    for r in range(rows):
        if check_direction(board, r, 0, 0, 1, symbol):
            return True

    # Vertical checks for each column
    for c in range(cols):
        if check_direction(board, 0, c, 1, 0, symbol):
            return True

    # Diagonal down-right (\)
    # Start from first row and each column, and each row and first column
    for c in range(cols):
        if check_direction(board, 0, c, 1, 1, symbol):
            return True
    for r in range(1, rows):
        if check_direction(board, r, 0, 1, 1, symbol):
            return True

    # Diagonal up-right (/)
    # Start from last row and each column, and each row and first column
    for c in range(cols):
        if check_direction(board, rows - 1, c, -1, 1, symbol):
            return True
    for r in range(rows - 1):
        if check_direction(board, r, 0, -1, 1, symbol):
            return True

    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY_CELL:
                return False
    return True

def validate_configuration():
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
    assert 1 <= NUM_ROWS, "NUM_ROWS must be positive"
    assert 1 <= NUM_COLS <= 26, "NUM_COLS must be between 1 and 26"

# ----------------------------
# Main Game Loop
# ----------------------------

def main():
    validate_configuration()
    players = get_player_symbols(NUM_PLAYERS)
    board = create_board(NUM_ROWS, NUM_COLS)

    # Choose random starting player index
    current_index = random.randrange(len(players))

    # Show initial empty board
    print_board(board)

    # Game loop
    while True:
        current_symbol = players[current_index]
        print(f"Player {current_symbol}, please enter a column:")
        col = get_column_input(current_symbol, NUM_COLS)

        placed = place_checker(board, col, current_symbol)

        # Print updated (or unchanged, if column full) board
        print_board(board)

        if not placed:
            # Column full: turn is invalid and the player loses the turn
            print(f"Column {column_labels(NUM_COLS)[col]} is full. Player {current_symbol} loses the turn.")
            # Proceed to next player
            current_index = (current_index + 1) % len(players)
            continue

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(players)

if __name__ == "__main__":
    main()
