import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))
    
    # Print the board rows
    for row in board:
        print('+---+' * BOARD_COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    print('+---+' * BOARD_COLS)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    if not col.isalpha() or not col.isupper():
        return False
    col_index = ord(col) - ord('A')
    return 0 <= col_index < BOARD_COLS

def get_column_index(col):
    """Convert column letter to index."""
    return ord(col) - ord('A')

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    col_index = get_column_index(col)
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Check if the current player has won the game."""
    # Check horizontally
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertically
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)
    print(f"Player {current_player} starts the game.")
    
    while True:
        col = input(f"Player {current_player}, please enter a column: ").strip()
        
        if not is_valid_column(col):
            print("Invalid input! Please enter a valid column (A-G).")
            continue
        
        col_upper = col.upper()
        if not place_checker(board, col_upper, current_player):
            print("Column is full! Try another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw.")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
