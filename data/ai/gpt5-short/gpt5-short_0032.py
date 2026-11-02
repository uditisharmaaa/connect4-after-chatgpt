import os
import random

# ====== Configuration Constants ======
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5 inclusive
# =====================================

def clear_screen():
    # As requested, use 'clear'
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board, current_player_symbol=None):
    clear_screen()
    print("Connect 4 - {} rows x {} cols (A-G)".format(ROWS, COLS))
    if current_player_symbol:
        print(f"Current player: {current_player_symbol}")
    print("  " + " ".join(COLUMN_LABELS))
    for r in range(ROWS):
        row_str = [board[r][c] for c in range(COLS)]
        print(str(ROWS - r) + " " + " ".join(row_str))
    print()

def get_valid_column(prompt):
    while True:
        choice = input(prompt).strip().upper()
        if len(choice) != 1 or choice not in COLUMN_LABELS:
            print("Invalid input. Enter a single column letter A-G.")
            continue
        return COLUMN_LABELS.index(choice)

def drop_piece(board, col, symbol):
    # Place piece in the lowest available row in the given column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return None  # Column full

def is_within(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    count = 0
    r, c = start_r, start_c
    while is_within(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, r, c, symbol):
    # Check all 4 directions by counting both ways
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = (
            count_in_direction(board, r, c, dr, dc, symbol) +
            count_in_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def validate_config():
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        raise ValueError("Not enough player symbols for NUM_PLAYERS.")

def main():
    validate_config()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_index = random.randrange(NUM_PLAYERS)

    board = create_board()
    print_board(board, players[current_index])

    while True:
        symbol = players[current_index]
        # Get a valid, non-full column
        while True:
            col = get_valid_column(f"Player {symbol}, choose column (A-G): ")
            if board[0][col] != ' ':
                print("That column is full. Choose another.")
                continue
            break

        # Drop the piece
        pos = drop_piece(board, col, symbol)
        if pos is None:
            # Shouldn't reach here due to pre-check, but safe-guard anyway
            print("Unexpected: column full. Try again.")
            continue

        r, c = pos
        print_board(board, symbol)

        # Check for win
        if check_win(board, r, c, symbol):
            print(f"Player {symbol} wins!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % NUM_PLAYERS
        print_board(board, players[current_index])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
