import os
import random
import string
import sys

# ==================== CONSTANTS ====================
ROWS = 6
COLUMNS = 7  # Max 26 columns allowed (A-Z)
PLAYER_COUNT = 2  # Must be between 2 and 5
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# ==================== BOARD SETUP ====================
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')
    cols = len(board[0])

    # Print column headers
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)

    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

# ==================== USER INPUT & VALIDATION ====================
def get_column_input(current_player, cols):
    valid_inputs = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if user_input in valid_inputs:
            return valid_inputs.index(user_input)
        else:
            print(f"Invalid input! Please enter a column label from {valid_inputs[0]} to {valid_inputs[-1]}.")

# ==================== GAME LOGIC ====================
def place_checker(board, column, token):
    # Place token in lowest empty space in column, if possible
    for row_idx in range(ROWS-1, -1, -1): # start bottom up
        if board[row_idx][column] == ' ':
            board[row_idx][column] = token
            return row_idx
    return -1  # This means the column is full

def is_full_column(board, column):
    return all(row[column] != ' ' for row in board)

def board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

# Win/Drawing logic
def check_win(board, row, column, token):
    # Direction vectors: (delta_row, delta_col)
    directions = [
        (0, 1),    # Horizontal →
        (1, 0),    # Vertical ↓
        (1, 1),    # Diagonal ↘
        (1, -1)    # Diagonal ↙
    ]
    for dr, dc in directions:
        count = 1  # Token at (row, column)
        # Check in both directions for each vector
        for delta in [1, -1]:
            r, c = row, column
            while True:
                r += dr * delta
                c += dc * delta
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == token:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

# ==================== MAIN GAME FUNCTION ====================
def main():
    # Setup
    if PLAYER_COUNT < 2 or PLAYER_COUNT > 5:
        print("PLAYER_COUNT must be between 2 and 5.")
        sys.exit(1)
    if COLUMNS > 26 or COLUMNS < 4 or ROWS < 4:
        print("Board must have 4-26 columns (up to A-Z) and at least 4 rows.")
        sys.exit(1)

    board = create_board(ROWS, COLUMNS)
    tokens = PLAYER_TOKENS[:PLAYER_COUNT]

    # Randomly choose first player
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)
    print_board(board)
    print(f"Player {tokens[current_player_idx]} starts!")

    while True:
        token = tokens[current_player_idx]
        # Get move
        col = get_column_input(token, COLUMNS)
        if is_full_column(board, col):
            print(f"Column {string.ascii_uppercase[col]} is full! You lose your turn.")
        else:
            row = place_checker(board, col, token)
            print_board(board)
            if check_win(board, row, col, token):
                print(f"Player {token} won!")
                break
            elif board_full(board):
                print("It's a draw!")
                break

        # Next player
        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
