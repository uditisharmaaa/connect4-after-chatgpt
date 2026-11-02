# Connect 4 (6x7) for 2–5 players with input validation, random first player, and clear screen

import os
import random
import sys

# -----------------------------
# Configuration constants
# -----------------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"  # Must be length COLS
TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Set between 2 and 5 (inclusive)

EMPTY = '·'  # Visible empty cell character


# -----------------------------
# Utility functions
# -----------------------------
def clear_screen():
    """Clear the console using os.system('clear') as requested."""
    os.system('clear')


def create_board():
    """Create and return an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board, players_in_use):
    """Render the board and legend."""
    legend = "Players: " + "  ".join(f"{i+1}:{tok}" for i, tok in enumerate(players_in_use))
    print(legend)
    print()
    # Column headers
    print("   " + " ".join(COLUMN_LABELS))
    # Board rows
    for r in range(ROWS):
        row_str = [board[r][c] for c in range(COLS)]
        print(f"{ROWS - r:2d} " + " ".join(row_str))
    # Footer with numbers aligned to header
    print("   " + " ".join(COLUMN_LABELS))
    print()


def is_valid_column(choice):
    """Return True if the column label is valid and within A-G, else False."""
    return len(choice) == 1 and choice.upper() in COLUMN_LABELS


def get_col_index(choice):
    """Translate a column label (A-G) into a column index."""
    return COLUMN_LABELS.index(choice.upper())


def get_next_open_row(board, col):
    """Return the index of the lowest open row in the given column, or None if full."""
    for r in range(ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col] == EMPTY:
            return r
    return None


def drop_piece(board, row, col, token):
    """Place a token at (row, col)."""
    board[row][col] = token


def in_bounds(r, c):
    """Check if (r, c) is inside the board."""
    return 0 <= r < ROWS and 0 <= c < COLS


def winning_move(board, token):
    """Check for any 4-in-a-row for the given token."""
    directions = [
        (0, 1),    # horizontal →
        (1, 0),    # vertical ↓
        (1, 1),    # diagonal down-right ↘
        (1, -1),   # diagonal down-left ↙
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                for step in range(1, 4):
                    nr, nc = r + dr * step, c + dc * step
                    if not in_bounds(nr, nc) or board[nr][nc] != token:
                        break
                    count += 1
                if count >= 4:
                    return True
    return False


def is_draw(board):
    """A draw occurs when there are no EMPTY cells left."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == EMPTY:
                return False
    return True


def prompt_move(current_player_token):
    """Prompt the current player for a column letter. Validate input format only."""
    while True:
        raw = input(f"Player {current_player_token}, choose a column ({COLUMN_LABELS}): ").strip()
        if not raw:
            print("Please enter a column letter.")
            continue
        if raw.lower() in ("quit", "exit"):
            print("Exiting game. Goodbye!")
            sys.exit(0)
        if not is_valid_column(raw):
            print(f"Invalid input. Please enter one of {', '.join(COLUMN_LABELS)}.")
            continue
        return raw.upper()


def take_turn(board, token):
    """Handle a single turn for the player with 'token'. Returns True if a move was made."""
    while True:
        choice = prompt_move(token)
        col = get_col_index(choice)
        row = get_next_open_row(board, col)
        if row is None:
            print(f"Column {choice} is full. Choose a different column.")
            continue
        drop_piece(board, row, col, token)
        return True


def validate_config():
    """Validate constants and environment assumptions."""
    if len(COLUMN_LABELS) != COLS:
        raise ValueError("COLUMN_LABELS length must equal COLS.")
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(TOKENS):
        raise ValueError("Not enough tokens provided for the number of players.")
    # Optional: enforce uniqueness of tokens
    if len(set(TOKENS[:NUM_PLAYERS])) != NUM_PLAYERS:
        raise ValueError("Player tokens must be unique.")


# -----------------------------
# Main gameplay loop
# -----------------------------
def main():
    validate_config()
    players = TOKENS[:NUM_PLAYERS]
    board = create_board()

    # Randomize starting player by offsetting the turn order
    start_index = random.randrange(NUM_PLAYERS)
    turn_index = start_index

    clear_screen()
    print("Welcome to Connect 4 (6x7)!")
    print(f"{NUM_PLAYERS} players: " + ", ".join(players))
    print(f"Randomly selected starting player: {players[turn_index]}")
    print("\nType 'quit' or 'exit' anytime to end the game.\n")
    print_board(board, players)

    while True:
        current_token = players[turn_index]
        # Show prompt and apply move
        if take_turn(board, current_token):
            clear_screen()
            print_board(board, players)

            # Check win
            if winning_move(board, current_token):
                print(f"Player {current_token} wins!")
                break

            # Check draw
            if is_draw(board):
                print("It's a draw! No more valid moves.")
                break

            # Next player's turn
            turn_index = (turn_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
