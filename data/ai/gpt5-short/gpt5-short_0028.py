import os
import random
import sys

# Constants you can tweak
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"
TOKENS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
NUM_PLAYERS = 2  # set between 2 and 5

# --- Utility functions ---

def clear_screen():
    # Requirement: use os.system('clear')
    try:
        os.system('clear')
    except Exception:
        pass

def new_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Rows
    for r in range(ROWS):
        row = "| " + " ".join(board[r]) + " |"
        print(row)
    print("  " + "-".join('-' for _ in range(COLS)))

def get_valid_columns(board):
    # A column is valid if top cell is empty
    return [c for c in range(COLS) if board[0][c] == ' ']

def col_label_to_index(label):
    label = label.upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None

def drop_token(board, col, token):
    # Place token in lowest available row in col; return row index or None if col full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return r
    return None

def check_winner(board, token):
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                if is_four_in_a_row(board, r, c, dr, dc, token):
                    return True
    return False

def is_four_in_a_row(board, r, c, dr, dc, token):
    for k in range(4):
        rr = r + dr * k
        cc = c + dc * k
        if rr < 0 or rr >= ROWS or cc < 0 or cc >= COLS:
            return False
        if board[rr][cc] != token:
            return False
    return True

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def choose_starting_player(players):
    return random.randrange(len(players))

def prompt_move(current_token, valid_cols):
    valid_labels = [COLUMN_LABELS[c] for c in valid_cols]
    prompt = f"Player {current_token}, choose a column ({'/'.join(valid_labels)}) or Q to quit: "
    while True:
        try:
            choice = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return 'Q'
        if not choice:
            continue
        if choice.upper() == 'Q':
            return 'Q'
        idx = col_label_to_index(choice)
        if idx is None:
            print("Invalid column. Use letters A-G.")
            continue
        if idx not in valid_cols:
            print("That column is full. Pick another.")
            continue
        return idx

# --- Main game loop ---

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    players = TOKENS[:NUM_PLAYERS]
    board = new_board()
    current_idx = choose_starting_player(players)

    while True:
        clear_screen()
        print_board(board)
        current_token = players[current_idx]
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("It's a draw! No more valid moves.")
            break

        move = prompt_move(current_token, valid_cols)
        if move == 'Q':
            print("Game quit.")
            break

        row_placed = drop_token(board, move, current_token)
        if row_placed is None:
            # Shouldn't happen due to validation, but safeguard
            print("Column full. Try again.")
            input("Press Enter to continue...")
            continue

        if check_winner(board, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_idx = (current_idx + 1) % len(players)

if __name__ == "__main__":
    main()
