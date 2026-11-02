import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"

# Up to 5 players: choose from these in order
PLAYER_SYMBOLS = ("X", "O", "V", "H", "M")

# Set how many players are in this game (2 to 5)
NUM_PLAYERS = 2  # <- change to 3, 4, or 5 if desired

# =========================
# Utility functions
# =========================

def clear_screen():
    # Requirement: use 'clear'
    os.system('clear')

def create_board(rows=ROWS, cols=COLS):
    # Use None for empty cells
    return [[None for _ in range(cols)] for _ in range(rows)]

def print_board(board, players, current_player_idx):
    clear_screen()
    print("Connect 4 - {} players: {}".format(len(players), " ".join(players)))
    print("Current player: {}".format(players[current_player_idx]))
    print()
    # Column labels
    print("  " + " ".join(list(COL_LABELS[:len(board[0])])))
    # Board rows
    for r in range(len(board)):
        row_str = []
        for c in range(len(board[0])):
            row_str.append(board[r][c] if board[r][c] is not None else ".")
        print("{:2}".format(r+1) + " " + " ".join(row_str))
    print()

def get_valid_players(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if num_players > len(PLAYER_SYMBOLS):
        raise ValueError("Not enough player symbols defined.")
    return list(PLAYER_SYMBOLS[:num_players])

def col_from_input(user_input):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    if user_input not in COL_LABELS:
        return None
    return COL_LABELS.index(user_input)

def column_has_space(board, col):
    return board[0][col] is None

def drop_piece(board, col, symbol):
    # Drop from bottom up
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] is None:
            board[r][col] = symbol
            return r, col
    return None  # column full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def has_connect_n(board, r, c, symbol, n=4):
    # Directions: horiz (0,1), vert (1,0), diag1 (1,1), diag2 (1,-1)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    rows, cols = len(board), len(board[0])
    for dr, dc in directions:
        count = 1
        # forward
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc
        # backward
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
            count += 1
            rr -= dr
            cc -= dc
        if count >= n:
            return True
    return False

def is_draw(board):
    # Draw if top row is all filled (no moves left)
    return all(cell is not None for cell in board[0])

def next_player_index(current_idx, total):
    return (current_idx + 1) % total

def get_move_input(players, current_player_idx):
    # Prompt user for a column letter A-G, or Q to quit
    prompt = f"Player {players[current_player_idx]} - choose a column ({COL_LABELS[0]}-{COL_LABELS[COLS-1]}) or Q to quit: "
    try:
        user_input = input(prompt)
    except EOFError:
        return "QUIT", None  # handle Ctrl-D gracefully
    if user_input.strip().upper() == "Q":
        return "QUIT", None
    col = col_from_input(user_input)
    if col is None or col >= COLS:
        return "INVALID", None
    return "OK", col

def game_loop():
    players = get_valid_players(NUM_PLAYERS)
    board = create_board(ROWS, COLS)

    # Pick a random first player
    current_player_idx = random.randrange(len(players))

    while True:
        print_board(board, players, current_player_idx)

        # Get input and validate
        status, col = get_move_input(players, current_player_idx)
        if status == "QUIT":
            print("Game ended by user.")
            return
        if status == "INVALID":
            print("Invalid input. Please enter a single column letter between {} and {}.".format(COL_LABELS[0], COL_LABELS[COLS-1]))
            input("Press Enter to continue...")
            continue
        if not column_has_space(board, col):
            print(f"Column {COL_LABELS[col]} is full. Choose another column.")
            input("Press Enter to continue...")
            continue

        # Place piece
        r, c = drop_piece(board, col, players[current_player_idx])

        # Check for win
        if has_connect_n(board, r, c, players[current_player_idx], n=4):
            print_board(board, players, current_player_idx)
            print(f"Player {players[current_player_idx]} wins! Connect 4 achieved.")
            return

        # Check for draw
        if is_draw(board):
            print_board(board, players, current_player_idx)
            print("It's a draw! No more valid moves.")
            return

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, len(players))

def main():
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")

if __name__ == "__main__":
    main()
