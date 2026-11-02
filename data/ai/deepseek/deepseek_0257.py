import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Available checkers based on number of players
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    header = '  '
    for col in range(COLS):
        header += chr(ord('A') + col) + '   '
    print(header.rstrip())
    
    # Print each row with borders
    for row in range(ROWS):
        border = '+' + ('---+' * COLS)
        print(border)
        print('| ' + ' | '.join(board[row]) + ' |')
    
    print('+' + ('---+' * COLS))

def get_valid_column(board):
    """Prompt the player for a valid column input."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or col < 'A' or col > chr(ord('A') + COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + COLS - 1)}.")
            continue
        
        col_index = ord(col) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """Place the checker in the lowest available row in the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last placed checker resulted in a win."""
    # Check horizontal
    count = 1
    # Left side
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Right side
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    if count >= 4:
        return True

    # Check vertical
    count = 1
    # Up side
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Down side (not needed since checkers fall down)
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count = 1
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= 4:
        return True

    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    global current_player
    board = initialize_board()
    current_player = random.choice(CHECKERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        # Get valid column input
        col = get_valid_column(board)
        
        # Place the checker
        row = place_checker(board, col, current_player)
        
        # Check for win
        if check_win(board, row, col, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch players
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
