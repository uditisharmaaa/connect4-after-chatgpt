#!/usr/bin/env python3
import os
import random
import sys

# ----- Constants -----
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"

# Choose between 2 and 5 players; tokens will be taken from left to right
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # change to 3, 4, or 5 for more players

# ----- Utilities -----
def clear_screen():
    os.system('clear')  # as requested

def create_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, players, current_player_idx):
    # Header
    print("Connect 4 — {} players: {}".format(len(players), ' '.join(players)))
    print("Current: {} ({})".format(players[current_player_idx], COL_LABELS))
    print("  " + " ".join(COL_LABELS))
    # Rows
    for r in range(ROWS):
        row_str = [board[r][c] for c in range(COLS)]
        print(str(ROWS - r) + " " + " ".join(row_str))
    print()

def col_from_input(inp):
    """Return column index from user input like 'A'..'G'. Returns None if invalid."""
    inp = inp.strip().upper()
    if len(inp) != 1:
        return None
    if inp not in COL_LABELS:
        return None
    return COL_LABELS.index(inp)

def lowest_empty_row(board, col):
    """Return the lowest available row index in the given column, or None if full."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def apply_move(board, col, token):
    """Place token in column; return (row, col) or None if invalid/full."""
    r = lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = token
    return (r, col)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, r, c, dr, dc, token):
    """Count contiguous tokens including start (r,c) moving in (dr,dc) and (-dr,-dc)."""
    count = 1
    # forward
    rr, cc = r + dr, c + dc
    while in_bounds(rr, cc) and board[rr][cc] == token:
        count += 1
        rr += dr
        cc += dc
    # backward
    rr, cc = r - dr, c - dc
    while in_bounds(rr, cc) and board[rr][cc] == token:
        count += 1
        rr -= dr
        cc -= dc
    return count

def check_win(board, last_move, token):
    """Check if placing token at last_move (r,c) created a connect-4."""
    if last_move is None:
        return False
    r, c = last_move
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        if count_in_direction(board, r, c, dr, dc, token) >= 4:
            return True
    return False

def check_draw(board):
    """Draw if no spaces left in top row."""
    return all(board[0][c] != ' ' for c in range(COLS))

def next_player_idx(current_idx, total_players):
    return (current_idx + 1) % total_players

def get_move_input(board, player_token):
    """Prompt user for a valid column input. Returns column index."""
    while True:
        raw = input(f"Player {player_token}, choose column (A-G): ").strip()
        col = col_from_input(raw)
        if col is None:
            print("Invalid input. Enter a single letter A-G.")
            continue
        if lowest_empty_row(board, col) is None:
            print(f"Column {COL_LABELS[col]} is full. Try another.")
            continue
        return col

# ----- Main Game Loop -----
def main():
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    players = PLAYER_TOKENS[:NUM_PLAYERS]
    board = create_board()

    current_player_idx = random.randrange(NUM_PLAYERS)
    last_move = None

    while True:
        clear_screen()
        print_board(board, players, current_player_idx)

        # Input
        col = get_move_input(board, players[current_player_idx])

        # Apply move
        move = apply_move(board, col, players[current_player_idx])
        if move is None:
            # Shouldn't happen due to validation, but guard anyway
            print("Unexpected error applying move. Try again.")
            input("Press Enter...")
            continue

        last_move = move

        # Check win
        if check_win(board, last_move, players[current_player_idx]):
            clear_screen()
            print_board(board, players, current_player_idx)
            print(f"Player {players[current_player_idx]} wins!")
            break

        # Check draw
        if check_draw(board):
            clear_screen()
            print_board(board, players, current_player_idx)
            print("It's a draw!")
            break

        # Next player
        current_player_idx = next_player_idx(current_player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
