import os
import random
import sys

# ---------- Configuration Constants ----------
ROWS = 6
COLS = 7
COL_LABELS = tuple("ABCDEFG")  # Must be length COLS
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 tokens as requested
NUM_PLAYERS = 2  # Set between 2 and 5

# ---------- Board Utilities ----------
def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Requirement: use 'clear'. Works on macOS/Linux terminals.
    os.system('clear')

def print_board(board):
    # Print column headers
    print("  " + " ".join(COL_LABELS))
    # Print rows from top to bottom
    for r in range(ROWS):
        row_str = [board[r][c] for c in range(COLS)]
        print(f"{ROWS - r} " + " ".join(row_str))
    # Footer line (optional)
    print()

def col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COL_LABELS:
        return COL_LABELS.index(s)
    return None

def get_next_open_row(board, col):
    # Returns the bottom-most empty row index for the given column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def is_valid_move(board, col):
    if col is None or col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '  # top cell empty means the column has space

def drop_piece(board, row, col, token):
    board[row][col] = token

def board_full(board):
    # If top row has any spaces, board isn't full
    return all(board[0][c] != ' ' for c in range(COLS))

# ---------- Win Checking ----------
def check_win(board, row, col, token):
    # Check 4 in a row including (row, col)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        count = 1  # count the placed piece itself

        # forward direction
        r, c = row + dr, col + dc
        while in_bounds(r, c) and board[r][c] == token:
            count += 1
            r += dr
            c += dc

        # backward direction
        r, c = row - dr, col - dc
        while in_bounds(r, c) and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True
    return False

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

# ---------- Game Flow ----------
def get_active_players(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if num_players > len(PLAYER_TOKENS):
        raise ValueError("Not enough player tokens provided for NUM_PLAYERS.")
    return PLAYER_TOKENS[:num_players]

def prompt_move(current_token):
    while True:
        raw = input(f"Player {current_token}, choose a column (A-G): ").strip()
        if raw == "":
            print("Please enter a column letter A-G.")
            continue
        col = col_from_input(raw)
        if col is None:
            print("Invalid input. Enter a single letter A-G.")
            continue
        return col

def main():
    # Setup
    try:
        players = get_active_players(NUM_PLAYERS)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    board = create_board()
    turn_index = random.randrange(len(players))  # random first player

    # Game loop
    winner = None
    while True:
        clear_screen()
        print_board(board)
        current_token = players[turn_index]
        print(f"Current player: {current_token}")

        # Get a valid move
        col = prompt_move(current_token)
        if not is_valid_move(board, col):
            print("That column is full or invalid. Press Enter to try again.")
            input()
            continue

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_token)

        # Check win
        if check_win(board, row, col, current_token):
            winner = current_token
            clear_screen()
            print_board(board)
            print(f"Player {winner} wins!")
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        turn_index = (turn_index + 1) % len(players)

    print("Game over.")

if __name__ == "__main__":
    main()
