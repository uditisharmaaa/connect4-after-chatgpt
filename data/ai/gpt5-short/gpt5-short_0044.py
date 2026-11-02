import os
import random
import sys

# =========================
# Configuration constants
# =========================
NUM_ROWS = 6
NUM_COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]  # ['A','B','C','D','E','F','G']

# Players: use the first NUM_PLAYERS from PLAYER_TOKENS
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change to any value from 2 to 5

# =========================
# Utility / UI
# =========================
def clear_screen():
    # Per assignment: use os.system('clear')
    os.system('clear')

def create_board(rows=NUM_ROWS, cols=NUM_COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, current_token=None):
    # Header with column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * NUM_COLS)
    for r in range(NUM_ROWS):
        row_cells = []
        for c in range(NUM_COLS):
            row_cells.append(board[r][c] if board[r][c] != ' ' else ' ')
        print('|' + '|'.join(f' {cell}' for cell in row_cells) + '|')
        print('+' + '---+' * NUM_COLS)
    if current_token:
        print(f"Current player: {current_token}")

def next_player_index(i, total):
    return (i + 1) % total

def top_empty_row_in_column(board, col):
    # Returns the row index where a piece would land in this column, or None if full
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

# =========================
# Input handling
# =========================
def parse_column_input(s):
    if not s or len(s) < 1:
        return None
    ch = s.strip().upper()
    if ch == 'Q' or ch == 'QUIT':
        return 'QUIT'
    if len(ch) != 1:
        return None
    if ch not in COLUMN_LABELS:
        return None
    return COLUMN_LABELS.index(ch)

def get_valid_move(board, token):
    while True:
        raw = input(f"Player {token}, choose a column (A-{COLUMN_LABELS[-1]}) or Q to quit: ").strip()
        parsed = parse_column_input(raw)
        if parsed == 'QUIT':
            return 'QUIT'
        if isinstance(parsed, int):
            col = parsed
            row = top_empty_row_in_column(board, col)
            if row is None:
                print("That column is full. Try another.")
            else:
                return col
        else:
            print("Invalid input. Enter a single column letter (A-G) or Q to quit.")

# =========================
# Game logic
# =========================
def drop_token(board, col, token):
    row = top_empty_row_in_column(board, col)
    if row is None:
        return None
    board[row][col] = token
    return row

def count_in_direction(board, start_row, start_col, dr, dc, token):
    r, c = start_row + dr, start_col + dc
    count = 0
    while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, token):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        # Count both directions from the last placed piece
        total = 1
        total += count_in_direction(board, row, col, dr, dc, token)
        total += count_in_direction(board, row, col, -dr, -dc, token)
        if total >= 4:
            return True
    return False

def is_draw(board):
    # Draw if no spaces in top row (i.e., all columns are full)
    return all(board[0][c] != ' ' for c in range(NUM_COLS))

# =========================
# Main loop
# =========================
def main():
    # Validate configuration
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_TOKENS):
        print("Error: Not enough tokens provided for the number of players.")
        sys.exit(1)

    tokens_in_play = PLAYER_TOKENS[:NUM_PLAYERS]

    board = create_board()
    current_index = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board, tokens_in_play[current_index])
        move = get_valid_move(board, tokens_in_play[current_index])
        if move == 'QUIT':
            print("Game aborted. Goodbye!")
            return

        row = drop_token(board, move, tokens_in_play[current_index])
        # drop_token should always succeed here due to validation
        last_token = tokens_in_play[current_index]

        # Check for win/draw
        if check_win(board, row, move, last_token):
            clear_screen()
            print_board(board, last_token)
            print(f"Player {last_token} wins!")
            break
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_index = next_player_index(current_index, NUM_PLAYERS)

    # End of game
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
