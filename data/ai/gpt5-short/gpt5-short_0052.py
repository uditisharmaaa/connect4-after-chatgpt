import os
import random
import sys

# ====== CONFIGURABLE CONSTANTS ======
ROWS = 6
COLS = 7
COLUMN_LABELS = "A B C D E F G".split()  # Must be length COLS
TOKENS = ['X', 'O', 'V', 'H', 'M']       # Up to 5 players max
NUM_PLAYERS = 2                          # Set between 2 and 5
# ====================================

def clear_screen():
    os.system('clear')  # Requirement specifies 'clear'

def make_board(rows=ROWS, cols=COLS):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    print('  ' + '   '.join(COLUMN_LABELS))
    print('+' + '---+' * COLS)
    # Print from top row to bottom (so bottom of board is visually at bottom)
    for r in range(ROWS - 1, -1, -1):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {ch} ' for ch in row_cells) + '|')
        print('+' + '---+' * COLS)

def drop_piece(board, col, token):
    # Place token in the lowest empty row of the given column.
    for r in range(ROWS):
        if board[r][col] == ' ':
            board[r][col] = token
            return r  # Return the row where we placed the piece
    return None  # Column is full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_direction(board, start_r, start_c, dr, dc, token):
    # Count consecutive tokens from (start_r, start_c) in direction (dr, dc), excluding start.
    count = 0
    r, c = start_r + dr, start_c + dc
    while in_bounds(r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, r, c, token):
    # Check all four directions: horizontal, vertical, and two diagonals.
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1  # include the placed piece
        total += count_direction(board, r, c, dr, dc, token)
        total += count_direction(board, r, c, -dr, -dc, token)
        if total >= 4:
            return True
    return False

def is_draw(board):
    # Board is full if top cell of every column is not empty
    for c in range(COLS):
        if board[ROWS - 1][c] == ' ':
            return False
    return True

def parse_move(inp):
    inp = inp.strip().upper()
    if len(inp) != 1:
        return None
    if inp not in COLUMN_LABELS:
        return None
    return COLUMN_LABELS.index(inp)

def get_valid_move(board, token):
    while True:
        user_in = input(f"Player {token}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ")
        col = parse_move(user_in)
        if col is None:
            print("Invalid input. Enter a single letter for the column, e.g., A-G.")
            continue
        if board[ROWS - 1][col] != ' ':
            print("That column is full. Pick another column.")
            continue
        return col

def validate_settings():
    # Ensure NUM_PLAYERS is valid and we have enough tokens/labels
    n = NUM_PLAYERS
    if not (2 <= n <= 5):
        print(f"NUM_PLAYERS={NUM_PLAYERS} is out of range. Using 2.")
        n = 2
    if n > len(TOKENS):
        print("Not enough TOKENS provided for the number of players. Truncating.")
        n = len(TOKENS)
    if COLS != len(COLUMN_LABELS):
        print("Warning: COLS does not match number of COLUMN_LABELS. Adjusting to labels length.")
    return n

def game_loop():
    num_players = validate_settings()
    players = TOKENS[:num_players]
    board = make_board()

    current_index = random.randrange(num_players)
    winner = None

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {' '.join(players)}")
        print(f"Current turn: Player {players[current_index]}")

        col = get_valid_move(board, players[current_index])
        row = drop_piece(board, col, players[current_index])

        # Safety check; row None means column full but we validated already
        if row is None:
            print("Unexpected error: column is full. Try again.")
            input("Press Enter to continue...")
            continue

        # Check for win
        if is_winning_move(board, row, col, players[current_index]):
            winner = players[current_index]
            clear_screen()
            print_board(board)
            print(f"Player {winner} wins! Congratulations!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % num_players

def main():
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
