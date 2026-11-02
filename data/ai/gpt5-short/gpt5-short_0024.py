import os
import random
import string

# ==========================
# Configuration constants
# ==========================
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A','B','C','D','E','F','G']

PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 2  # Change to 2..5 for desired number of players

# ==========================
# Utility functions
# ==========================
def clear_screen():
    # Per requirement, use 'clear'
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print(' +' + '---+' * COLS)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print(' | ' + ' | '.join(row_cells) + ' |')
        print(' +' + '---+' * COLS)

def col_from_label(label):
    label = label.strip().upper()
    if len(label) != 1 or label not in COLUMN_LABELS:
        return None
    return ord(label) - ord('A')

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def drop_piece(board, col, token):
    # Place token in the lowest empty row of the column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return r, col
    return None  # Column full (should be guarded by is_valid_move)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win_from_cell(board, r, c, token):
    # Check 4-in-a-row in 4 directions from the last placed token
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
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
        if count >= 4:
            return True
    return False

def is_draw(board):
    # Draw if top row has no empty spaces
    return all(board[0][c] != ' ' for c in range(COLS))

# ==========================
# Game loop
# ==========================
def play_game():
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(PLAYER_TOKENS):
        raise ValueError("Not enough PLAYER_TOKENS for NUM_PLAYERS.")
    active_tokens = PLAYER_TOKENS[:NUM_PLAYERS]

    board = create_board()
    current_index = random.randrange(NUM_PLAYERS)  # random first player

    while True:
        clear_screen()
        print_board(board)
        current_token = active_tokens[current_index]
        prompt = f"Player {current_index + 1} ({current_token}) - choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): "
        user_in = input(prompt).strip()

        col = col_from_label(user_in)
        if col is None:
            print(f"Invalid input. Enter a single letter {COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}. Press Enter to continue...")
            input()
            continue

        if not is_valid_move(board, col):
            print("That column is full or invalid. Press Enter to continue...")
            input()
            continue

        placed = drop_piece(board, col, current_token)
        r, c = placed

        # Check for win
        if check_win_from_cell(board, r, c, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_index + 1} ({current_token}) wins!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
