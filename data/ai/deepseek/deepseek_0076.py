import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---+' * COLS)

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    col = ord(column.upper()) - ord('A')
    return 0 <= col < COLS

def get_next_open_row(board, col):
    """Find the next available row in the specified column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            return row
    return -1  # Column is full

def drop_checker(board, row, col, checker):
    """Place the checker in the specified position."""
    board[row][col] = checker

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    os.system('clear')
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column: ")
        column = input().strip().upper()
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        
        col = ord(column) - ord('A')
        row = get_next_open_row(board, col)
        
        if row == -1:
            print("Column is full. Please choose another column.")
            continue
        
        drop_checker(board, row, col, current_player)
        os.system('clear')
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
