import os
import random
import string
import sys

# ------------------------ #
#         CONSTANTS        #
# ------------------------ #
NUM_ROWS = 6
NUM_COLS = 7  # max 26 due to column letter labeling
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

BOARD_EMPTY = ' '

assert NUM_PLAYERS >= 2 and NUM_PLAYERS <= 5
assert NUM_COLS <= 26

# ------------------------ #
#        FUNCTIONS         #
# ------------------------ #

def clear_screen():
    os.system('clear')  # For Unix/Linux/Mac

def create_board(rows, cols):
    """Returns a 2D board with given dimensions, filled with spaces."""
    return [[BOARD_EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board in the specified format."""
    rows = len(board)
    cols = len(board[0])
    # Print column letters
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * cols)
    for r in range(rows):
        print('|' + '|'.join(f' {board[r][c]} ' for c in range(cols)) + '|')
        print('+' + '---+' * cols)

def select_first_player(num_players):
    """Returns index [0, num_players-1]"""
    return random.randint(0, num_players - 1)

def get_valid_columns(board):
    """Returns a set of column indices that are NOT full."""
    valid_cols = set()
    for col in range(len(board[0])):
        if board[0][col] == BOARD_EMPTY:
            valid_cols.add(col)
    return valid_cols

def input_column(valid_cols, cols):
    """Prompts the user for a column input and validates it. Returns column index."""
    while True:
        col_input = input().strip().upper()
        if len(col_input) != 1:
            print("Invalid input: Please enter a single capital letter corresponding to the columns.")
            print("Please enter a column:")
            continue
        if col_input not in string.ascii_uppercase[:cols]:
            print("Invalid input: Column is not in the board.")
            print("Please enter a column:")
            continue
        col_index = string.ascii_uppercase.index(col_input)
        if col_index not in valid_cols:
            print("Invalid move: This column is full.")
            print("Please enter a column:")
            continue
        return col_index

def place_checker(board, col, checker):
    """Places the checker in the lowest free position of the column. Returns the (row, col) tuple where placed."""
    for row in reversed(range(len(board))):
        if board[row][col] == BOARD_EMPTY:
            board[row][col] = checker
            return (row, col)
    # Should never get here if checked in advance
    return None

def is_within_board(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

def check_win(board, row, col, checker):
    """Check if placing checker at (row, col) wins the game."""
    rows = len(board)
    cols = len(board[0])
    directions = [  # (row_delta, col_delta)
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Start with current placed checker
        # Check one direction
        r, c = row + dr, col + dc
        while is_within_board(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while is_within_board(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Return True if the board is full (draw), else False."""
    for cell in board[0]:
        if cell == BOARD_EMPTY:
            return False
    return True

def main():
    # Setup
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    player_names = [f"Player {ch}" for ch in player_checkers]
    current_player_idx = select_first_player(NUM_PLAYERS)

    clear_screen()
    print_board(board)
    print(f"{player_names[current_player_idx]}, please enter a column:")

    # Game Loop
    while True:
        current_checker = player_checkers[current_player_idx]
        current_name = player_names[current_player_idx]

        valid_cols = get_valid_columns(board)
        if not valid_cols:
            # Board is full, draw
            print("The game is a draw!")
            break

        # Input
        col = input_column(valid_cols, NUM_COLS)
        # Place checker
        row, col = place_checker(board, col, current_checker)
        # Print
        clear_screen()
        print_board(board)

        # Check Win
        if check_win(board, row, col, current_checker):
            print(f"{current_name} won!")
            break
        # Check Draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        print(f"{player_names[current_player_idx]}, please enter a column:")

if __name__ == '__main__':
    main()
