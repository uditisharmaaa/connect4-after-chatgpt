import os
import random
import string

# ------------------- CONSTANTS -------------------
ROWS = 6               # Board rows
COLUMNS = 7            # Board columns (max 26)
NUM_PLAYERS = 2        # Number of players (2-5)
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']

EMPTY_CELL = " "
COLUMN_LABELS = list(string.ascii_uppercase)[:COLUMNS]

# ------------------- FUNCTIONS -------------------

def clear_screen():
    os.system('clear')  # For Unix/Linux terminals

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Top column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_first_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_column(input_str):
    if input_str in COLUMN_LABELS:
        return True
    return False

def is_column_full(board, col_idx):
    return all(row[col_idx] != EMPTY_CELL for row in board)

def place_checker(board, col_idx, player_char):
    # Start from the bottom row, look upward
    for row in reversed(board):
        if row[col_idx] == EMPTY_CELL:
            row[col_idx] = player_char
            return board.index(row), col_idx  # Return position
    return None  # Already full

def input_column(board, current_player):
    while True:
        column_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not column_input:
            print("No input provided. Try again.")
            continue
        if not is_valid_column(column_input):
            print(f"Invalid column '{column_input}'. Use columns {', '.join(COLUMN_LABELS)}.")
            continue
        col_idx = COLUMN_LABELS.index(column_input)
        if is_column_full(board, col_idx):
            print(f"Column {column_input} is full! You lose this turn.")
            return None  # Lose turn if full
        return col_idx

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLUMNS

def check_win(board, player_char):
    # Horizontal, vertical, diagonal checks for 4 in a row
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] != player_char:
                continue
            # Horizontal
            if c + 3 < COLUMNS and all(board[r][c + i] == player_char for i in range(4)):
                return True
            # Vertical
            if r + 3 < ROWS and all(board[r + i][c] == player_char for i in range(4)):
                return True
            # Diagonal down-right
            if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == player_char for i in range(4)):
                return True
            # Diagonal up-right
            if r - 3 >= 0 and c + 3 < COLUMNS and all(board[r - i][c + i] == player_char for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(EMPTY_CELL not in row for row in board)

def main():
    # Initialize board and players
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHARS[:NUM_PLAYERS]

    first_turn = get_first_player(NUM_PLAYERS)
    turn = first_turn

    clear_screen()
    print_board(board)
    print(f"\nPlayer {players[turn]} starts!\n")

    while True:
        current_player = players[turn]

        col_idx = input_column(board, current_player)
        if col_idx is None:  # Column was full; lose the turn
            turn = (turn + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        row_idx, placed_col_idx = place_checker(board, col_idx, current_player)

        clear_screen()
        print_board(board)

        # Win check
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        # Draw check
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
