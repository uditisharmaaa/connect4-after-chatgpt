import os
import random
import string
import sys

# ========= Configuration (you may change these constants for testing) =========
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
# ============================================================================

# Checkers for up to 5 players, in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    # Clear terminal screen (Linux/Unix as per assignment)
    os.system('clear')

def validate_configuration(rows, cols, num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if cols < 1 or cols > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if rows < 1:
        raise ValueError("ROWS must be at least 1.")

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    # Labels A, B, C, ...
    return list(string.ascii_uppercase[:cols])

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header with column labels
    header = "  " + "   ".join(labels)
    print(header)
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(rows):
        line_cells = []
        for c in range(cols):
            line_cells.append(board[r][c])
        print("| " + " | ".join(line_cells) + " |")
        print("+" + ("---+" * cols))

def read_valid_column_input(cols):
    labels = column_labels(cols)
    valid_set = set(labels)
    while True:
        try:
            user_input = input("Please enter a column: ").strip().upper()
        except EOFError:
            # If input stream closes, exit gracefully
            sys.exit(0)

        if len(user_input) != 1 or user_input not in valid_set:
            print(f"Invalid input. Enter one of: {', '.join(labels)}")
            continue
        return labels.index(user_input)  # return column index

def drop_checker(board, col, checker):
    # Place checker in the lowest available row in this column.
    # Returns row index if placed, or None if column full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def print_game_state(board, current_checker, message=None):
    clear_screen()
    print_board(board)
    if message:
        print(message)
    print(f"Player {current_checker},", end=" ")

def main():
    # Validate configuration
    validate_configuration(ROWS, COLS, NUM_PLAYERS)

    # Prepare game
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS)
    last_message = None

    # Initial display
    print_game_state(board, players[current_player_idx], message=None)

    while True:
        # Prompt current player for a valid column letter
        col = read_valid_column_input(COLS)

        # Try to drop checker
        checker = players[current_player_idx]
        row_placed = drop_checker(board, col, checker)

        if row_placed is None:
            # Column full; player loses the turn
            label = column_labels(COLS)[col]
            last_message = f"Column {label} is full. Turn lost."
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_game_state(board, players[current_player_idx], message=last_message)
            continue

        # After a successful move, check for win
        if check_win(board, checker):
            print_game_state(board, checker, message=None)
            print(f"Player {checker} won!")
            break

        # Check for draw
        if board_full(board):
            print_game_state(board, checker, message=None)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        last_message = None
        print_game_state(board, players[current_player_idx], message=None)

if __name__ == "__main__":
    main()
