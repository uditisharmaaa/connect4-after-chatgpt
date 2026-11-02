#!/usr/bin/env python3
import os
import random
import sys

# ---------- Configuration ----------
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

# Supported player tokens, in turn order. Use the first N.
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Number of players (2 to 5). Must be <= len(PLAYER_TOKENS).
NUM_PLAYERS = 2
# -----------------------------------

def clear_screen():
    # Clears terminal; 'clear' (Unix) as requested. Fall back to 'cls' if needed.
    # You can simplify to just os.system('clear') if your environment is Unix.
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Header with column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLS)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {ch} ' for ch in row_cells) + '|')
        print('+' + '---+' * COLS)

def is_valid_column_label(label):
    return label.upper() in COLUMN_LABELS

def column_full(board, col_index):
    return board[0][col_index] != ' '

def drop_piece(board, col_index, token):
    """
    Drops a piece in the given column. Returns the (row, col) where it lands.
    Assumes the column has space.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = token
            return r, col_index
    # Should not happen because we check column_full before calling
    raise RuntimeError("Tried to drop a piece into a full column.")

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, token):
    """
    Count contiguous tokens matching `token` starting from (start_r, start_c)
    moving in direction (dr, dc), not including the starting cell.
    """
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, last_r, last_c, token):
    """
    Check if placing token at (last_r, last_c) creates a connect 4.
    We check four directions: horizontal, vertical, diag-down-right, diag-up-right.
    """
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        total = 1  # include the last placed piece
        total += count_in_direction(board, last_r, last_c, dr, dc, token)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, token)
        if total >= 4:
            return True
    return False

def is_draw(board):
    # Draw if no spaces remain in the top row (i.e., all columns full)
    return all(board[0][c] != ' ' for c in range(COLS))

def prompt_move(current_token):
    """
    Prompt the user for a move. Returns a column index or None if the user wants to quit.
    Accepts:
      - Single letter A-G (case-insensitive)
      - 'Q' to quit
    """
    while True:
        raw = input(f"Player {current_token}, choose a column (A-{COLUMN_LABELS[-1]}) or Q to quit: ").strip()
        if not raw:
            print("Empty input. Try again.")
            continue
        if raw.lower() == 'q':
            return None
        if not is_valid_column_label(raw):
            print(f"Invalid column '{raw}'. Please enter a letter between A and {COLUMN_LABELS[-1]}.")
            continue
        col_index = COLUMN_LABELS.index(raw.upper())
        return col_index

def setup_players():
    if not (2 <= NUM_PLAYERS <= min(5, len(PLAYER_TOKENS))):
        print(f"NUM_PLAYERS must be between 2 and {min(5, len(PLAYER_TOKENS))}.")
        sys.exit(1)
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    # Randomly choose starting player by rotating the list
    start_idx = random.randrange(NUM_PLAYERS)
    players = players[start_idx:] + players[:start_idx]
    return players

def main():
    random.seed()
    board = create_board(ROWS, COLS)
    players = setup_players()

    winner = None
    turn_index = 0

    while True:
        clear_screen()
        print_board(board)
        current_token = players[turn_index % len(players)]

        col = prompt_move(current_token)
        if col is None:
            print("Game ended by user.")
            break

        if column_full(board, col):
            print(f"Column {COLUMN_LABELS[col]} is full. Press Enter to choose another column.")
            input()
            continue

        r, c = drop_piece(board, col, current_token)

        if is_winning_move(board, r, c, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins! Congratulations!")
            winner = current_token
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more valid moves.")
            break

        turn_index += 1

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
