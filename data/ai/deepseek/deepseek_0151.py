import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column headers and borders."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + '---+' * COLS)
    
    for row in board:
        # Print each row with borders
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        # Print row border
        print('+' + '---+' * COLS)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col = col.upper()
    return 'A' <= col <= chr(65 + COLS - 1)

def place_checker(board, col, symbol):
    """
    Place the checker in the specified column.
    Returns True if placement was successful, False otherwise.
    """
    col_idx = ord(col.upper()) - ord('A')
    
    # Check if column is full
    if board[0][col_idx] != ' ':
        return False
    
    # Find the lowest empty row in the column
    row_idx = -1
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_idx] == ' ':
            row_idx = i
            break
    
    # Place the checker
    board[row_idx][col_idx] = symbol
    return True

def check_win(board, symbol):
    """Check if the current player has won."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    
    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    
    # Check diagonally (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == symbol for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column: ")
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a column letter from A to " + chr(65 + COLS - 1) + ".")
            continue
        
        if not place_checker(board, col_input, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
