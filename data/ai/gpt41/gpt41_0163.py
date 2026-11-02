import os
import random
import string
import sys

# ------------ CONSTANTS ---------------

NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26  # max allowed, for future extensibility
NUM_PLAYERS = 2  # 2-5 allowed, set here for submission

PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ------------ BOARD HANDLING ---------------

def create_board(rows=NUM_ROWS, cols=NUM_COLS):
    """Initialize the board with empty strings."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels."""
    os.system('clear')
    cols = len(board[0])
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    header = '  ' + '   '.join(col_labels)
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def is_valid_column(col_input, cols):
    """Check if user input is a valid column."""
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    idx = ord(col_input.upper()) - ord('A')
    return 0 <= idx < cols

def get_first_empty_row(board, col_idx):
    """Return the index of the lowest empty row in a column, or None if full."""
    for r in reversed(range(len(board))):
        if board[r][col_idx] == ' ':
            return r
    return None

def is_board_full(board):
    """Return True if the board is full, else False."""
    return all(cell != ' ' for row in board for cell in row)

def place_checker(board, col_idx, checker):
    """Place the player's checker in the lowest available row in column col_idx."""
    row_idx = get_first_empty_row(board, col_idx)
    if row_idx is not None:
        board[row_idx][col_idx] = checker
        return row_idx
    return None

# ------------ GAME LOGIC ---------------

def check_winner(board, last_row, last_col, checker):
    """Check win in all directions after placing at (last_row, last_col)."""
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    rows, cols = len(board), len(board[0])
    for dr, dc in directions:
        count = 1  # start with 1 for last placed checker
        # One direction
        r, c = last_row+dr, last_col+dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Opposite direction
        r, c = last_row-dr, last_col-dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# ------------ PLAYER INPUT ---------------

def get_player_input(board, cols, player_checker):
    """Prompt user for column input and validate."""
    while True:
        entry = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(entry, cols):
            print("Invalid column. Please enter a valid column letter (e.g. A, B, ...).")
            continue
        col_idx = ord(entry) - ord('A')
        if get_first_empty_row(board, col_idx) is None:
            print("Column is full. You lose your turn!")
            return None  # lose turn if full
        return col_idx

# ------------ MAIN GAME FUNCTION ---------------

def main():
    rows, cols = NUM_ROWS, NUM_COLS
    num_players = NUM_PLAYERS
    board = create_board(rows, cols)
    players = PLAYER_CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)
    
    print_board(board)
    print(f"Player {players[current_player]} will go first.")

    moves_played = 0
    while True:
        print_board(board)
        player_checker = players[current_player]
        
        col_idx = get_player_input(board, cols, player_checker)
        if col_idx is None:  # column full, lose turn
            current_player = (current_player + 1) % num_players
            continue
        
        row_idx = place_checker(board, col_idx, player_checker)
        moves_played += 1

        # Check for win
        if check_winner(board, row_idx, col_idx, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
