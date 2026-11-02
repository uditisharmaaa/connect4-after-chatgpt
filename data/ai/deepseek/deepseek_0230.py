import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Checkers for players (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear' if os.name == 'posix' else 'cls')
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def get_random_first_player(num_players):
    """Return a random player index (0 to num_players - 1)."""
    return random.randint(0, num_players - 1)

def is_valid_column(column):
    """Check if the input column is valid."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return col_char >= 'A' and col_char < chr(65 + COLS)

def get_empty_row(board, col):
    """Return the first empty row in the given column or -1 if column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible, return True if successful."""
    empty_row = get_empty_row(board, col)
    if empty_row == -1:
        return False
    board[empty_row][col] = checker
    return True

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 1
    left_col = col - 1
    while left_col >= 0 and board[row][left_col] == checker:
        count += 1
        left_col -= 1
    right_col = col + 1
    while right_col < COLS and board[row][right_col] == checker:
        count += 1
        right_col += 1
    if count >= 4:
        return True
    
    # Check vertical
    count = 1
    down_row = row + 1
    while down_row < ROWS and board[down_row][col] == checker:
        count += 1
        down_row += 1
    if count >= 4:
        return True
    
    # Check diagonal down-right
    count = 1
    row_i = row - 1
    col_i = col - 1
    while row_i >= 0 and col_i >= 0 and board[row_i][col_i] == checker:
        count += 1
        row_i -= 1
        col_i -= 1
    row_i = row + 1
    col_i = col + 1
    while row_i < ROWS and col_i < COLS and board[row_i][col_i] == checker:
        count += 1
        row_i += 1
        col_i += 1
    if count >= 4:
        return True
    
    # Check diagonal down-left
    count = 1
    row_i = row - 1
    col_i = col + 1
    while row_i >= 0 and col_i < COLS and board[row_i][col_i] == checker:
        count += 1
        row_i -= 1
        col_i += 1
    row_i = row + 1
    col_i = col - 1
    while row_i < ROWS and col_i >= 0 and board[row_i][col_i] == checker:
        count += 1
        row_i += 1
        col_i -= 1
    if count >= 4:
        return True
    
    return False

def is_board_full(board):
    """Check if the board is full."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = get_random_first_player(NUM_PLAYERS)
    players = [PLAYER_CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    while True:
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")
        
        while True:
            column = input().strip().upper()
            if is_valid_column(column):
                col = ord(column) - ord('A')
                if get_empty_row(board, col) != -1:
                    break
                else:
                    print("Column is full. Please choose another column:")
            else:
                print("Invalid column. Please enter a valid column (A to %s):" % chr(65 + COLS - 1))
        
        if place_checker(board, col, players[current_player]):
            row = get_empty_row(board, col) + 1  # Because get_empty_row returns the first empty row (0-based)
            if check_win(board, row, col, players[current_player]):
                print_board(board)
                print(f"Player {players[current_player]} won!")
                break
            if is_board_full(board):
                print_board(board)
                print("Game ended in a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Failed to place checker. Please try again.")

if __name__ == "__main__":
    main()
