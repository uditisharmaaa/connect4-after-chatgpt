# Connect 4 game for 2–5 players
# Requirements:
# - 6 rows, 7 columns (A-G)
# - Players use tokens: X, O, V, H, M (in that order)
# - Number of players set by constant NUM_PLAYERS (2 to 5)
# - Random first player each game
# - Validate input (column exists and not full)
# - Check wins (4 in a row) and draws
# - Clear screen with os.system('clear')
# - Uses only basic Python

import os
import random

# ----- Constants you can adjust -----
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set between 2 and 5
# ------------------------------------

def clear_screen():
    # As requested, use clear (works on macOS/Linux terminals)
    os.system('clear')

def make_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board, current_token=None):
    clear_screen()
    print("Connect 4 (" + str(ROWS) + " rows x " + str(COLS) + " cols)")
    print("Columns: " + " ".join(COLUMN_LABELS))
    print("")
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += board[r][c] + "|"
        print(line)
    print("-" * (COLS * 2 + 1))
    if current_token is not None:
        print("Player " + current_token + "'s turn.")

def col_from_label(label):
    label = label.strip().upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None

def is_column_full(board, col):
    return board[0][col] != ' '

def drop_piece(board, col, token):
    # Place token in the lowest empty row of the column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return r, col
    return None  # column full

def in_bounds(r, c):
    return r >= 0 and r < ROWS and c >= 0 and c < COLS

def check_winner(board, token):
    # Check all directions for 4 in a row:
    # Right (0,1), Down (1,0), Down-Right (1,1), Down-Left (1,-1)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr = r + dr
                cc = c + dc
                while count < 4 and in_bounds(rr, cc) and board[rr][cc] == token:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False

def check_draw(board):
    # Draw if top row is full
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_player_move(board, token):
    while True:
        user_input = input("Player " + token + ", choose a column (A-G): ").strip()
        if user_input == "":
            print("Please enter a column letter A-G.")
            continue
        col = col_from_label(user_input)
        if col is None:
            print("Invalid column. Use letters A-G.")
            continue
        if is_column_full(board, col):
            print("That column is full. Choose another.")
            continue
        return col

def next_player_index(i, total):
    i += 1
    if i >= total:
        i = 0
    return i

def main():
    # Validate NUM_PLAYERS
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    board = make_board()

    # Pick random first player
    current_index = random.randrange(len(tokens))
    current_token = tokens[current_index]

    # Game loop
    while True:
        print_board(board, current_token)
        col = get_player_move(board, current_token)
        drop_piece(board, col, current_token)

        print_board(board)  # show the move

        if check_winner(board, current_token):
            print("Player " + current_token + " wins!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_index = next_player_index(current_index, len(tokens))
        current_token = tokens[current_index]

if __name__ == "__main__":
    main()
