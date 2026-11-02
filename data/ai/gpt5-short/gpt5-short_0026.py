#!/usr/bin/env python3
"""
Connect 4 (console) for an intro CS class.

Features:
- 6 rows x 7 columns board
- Columns labeled A-G
- 2 to 5 players (X, O, V, H, M), set by constants below
- Random first player each game
- Robust input validation
- Win and draw detection
- Clears screen each turn with os.system('clear')
"""

import os
import random

# -------------------------------
# Configuration constants
# -------------------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must be length COLS
EMPTY = "."               # What an empty cell looks like

# Allowed player symbols, in the order they'll be used
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Set the number of players to use (between 2 and 5 inclusive)
NUM_PLAYERS = 2  # Change this to 3, 4, or 5 if you want more players

# -------------------------------
# Utility functions
# -------------------------------

def clear_screen():
    """Clears the console screen using the 'clear' command."""
    os.system('clear')


def create_board(rows=ROWS, cols=COLS):
    """Creates a rows x cols board filled with EMPTY cells."""
    return [[EMPTY for _ in range(cols)] * 1 for _ in range(rows)]


def print_board(board):
    """Prints the board with column labels."""
    print()
    print("  " + " ".join(COLUMN_LABELS))
    for r in range(len(board)):
        print("  " + " ".join(board[r]))
    print()


def get_active_players(num_players):
    """
    Returns a list of active player symbols based on num_players.
    Ensures num_players is valid.
    """
    if not (2 <= num_players <= len(PLAYER_SYMBOLS)):
        raise ValueError(f"NUM_PLAYERS must be between 2 and {len(PLAYER_SYMBOLS)}")
    return PLAYER_SYMBOLS[:num_players]


def col_from_input(s):
    """
    Converts a user input string (e.g., 'A' or 'a') to a column index.
    Returns None if invalid.
    """
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s not in COLUMN_LABELS:
        return None
    return COLUMN_LABELS.index(s)


def drop_piece(board, col, symbol):
    """
    Drops a piece with 'symbol' into column 'col'.
    Returns the row index where the piece lands, or -1 if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):  # start from bottom row
        if board[row][col] == EMPTY:
            board[row][col] = symbol
            return row
    return -1  # column full


def in_bounds(r, c, rows=ROWS, cols=COLS):
    """Checks if (r, c) is within the board boundaries."""
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, last_row, last_col, symbol):
    """
    Checks if placing 'symbol' at (last_row, last_col) creates a 4-in-a-row.
    We only need to check lines that include the last move.
    """
    # Directions to check: (dr, dc)
    directions = [
        (0, 1),   # horizontal (right)
        (1, 0),   # vertical (down)
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    def count_in_direction(r, c, dr, dc):
        """Counts consecutive 'symbol' cells starting from (r, c), moving (dr, dc)."""
        count = 0
        rr, cc = r, c
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc
        return count

    # For each direction, count both ways and see if total >= 4
    for dr, dc in directions:
        total = 1  # include the last placed piece
        total += count_in_direction(last_row - dr, last_col - dc, -dr, -dc)  # backwards
        total += count_in_direction(last_row + dr, last_col + dc, dr, dc)    # forwards
        if total >= 4:
            return True
    return False


def is_draw(board):
    """
    A draw occurs when there are no EMPTY cells in the top row
    (i.e., all columns are full).
    """
    return all(cell != EMPTY for cell in board[0])


def next_player_index(current_index, total_players):
    """Returns the next player's index in a circular fashion."""
    return (current_index + 1) % total_players


def prompt_move(player_symbol):
    """
    Prompts the user for a column letter for the current player.
    Returns a valid column index after validation.
    """
    while True:
        user_input = input(f"Player {player_symbol}, choose a column (A-G): ").strip()
        col = col_from_input(user_input)
        if col is None:
            print("Invalid input. Please enter a single letter A-G.")
            continue
        return col


# -------------------------------
# Main game loop
# -------------------------------

def play_game():
    # Set up game state
    board = create_board(ROWS, COLS)
    players = get_active_players(NUM_PLAYERS)
    total_players = len(players)

    # Randomize first player
    current_idx = random.randrange(total_players)

    while True:
        clear_screen()
        print(f"Connect 4 - {ROWS}x{COLS}")
        print(f"Players: {', '.join(players)}")
        print(f"Current turn: Player {players[current_idx]}")
        print_board(board)

        # Get a valid move
        col = prompt_move(players[current_idx])

        # Try to drop the piece
        row = drop_piece(board, col, players[current_idx])
        if row == -1:
            print("That column is full. Try another column.")
            input("Press Enter to continue...")
            continue

        # Check for a win
        if check_win(board, row, col, players[current_idx]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_idx]} wins! Congratulations!")
            break

        # Check for a draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more valid moves.")
            break

        # Next player's turn
        current_idx = next_player_index(current_idx, total_players)


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
