import os
import random
import string
import sys

# -------------------------
# Configuration (constants)
# -------------------------
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2 to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # in order

# -------------------------
# Utility / Validation
# -------------------------
def clear_screen():
    # Requirement: clear the game screen before printing the updated board
    os.system('clear')

def validate_settings(rows, cols, num_players):
    if cols < 1 or cols > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if rows < 1:
        raise ValueError("ROWS must be at least 1.")
    if num_players < 2 or num_players > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if num_players > len(CHECKERS):
        raise ValueError("Not enough checker symbols for the requested number of players.")

# -------------------------
# Board creation & printing
# -------------------------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    return [string.ascii_uppercase[i] for i in range(cols)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Column header
    header = "  " + "   ".join(labels)
    line = "+" + ("---+" * cols)

    print(header)
    print(line)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(line)

# -------------------------
# Game Mechanics
# -------------------------
def get_valid_input(cols):
    labels = column_labels(cols)
    while True:
        user_in = input().strip()
        if len(user_in) != 1:
            print(f"Invalid input. Please enter a single letter between {labels[0]} and {labels[-1]}:")
            continue
        ch = user_in.upper()
        if ch not in labels:
            print(f"Invalid input. Please enter a letter between {labels[0]} and {labels[-1]}:")
            continue
        return labels.index(ch), ch

def drop_checker(board, col, symbol):
    # Returns (success, row_index) where success indicates whether the checker was placed
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True, r
    return False, None

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Directions: (dr, dc) -> right, down, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                        count += 1
                    else:
                        break
                if count == 4:
                    return True
    return False

def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

# -------------------------
# Main Game Loop
# -------------------------
def play_game():
    validate_settings(ROWS, COLS, NUM_PLAYERS)
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly choose starting player index
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    while True:
        current_player = players[current_idx]
        print(f"Player {current_player}, please enter a column:", end=" ")

        # Read and validate column input (keep asking until a valid column letter is entered)
        col_index, col_letter = get_valid_input(COLS)

        # Attempt to drop checker
        placed, _ = drop_checker(board, col_index, current_player)

        # Clear and reprint board after the turn (even if turn was lost due to full column)
        clear_screen()
        print_board(board)

        if not placed:
            # Column full, turn lost
            print(f"Column {col_letter} is full. Player {current_player} loses the turn.")
            # Advance to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            # Continue game without win/draw check (no piece placed)
            continue

        # Check for a win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

def main():
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)

if __name__ == "__main__":
    main()
