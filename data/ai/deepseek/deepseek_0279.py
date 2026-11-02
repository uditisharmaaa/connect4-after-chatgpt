import os
import random
from itertools import cycle

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before redrawing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = '   ' + '   '.join([chr(ord('A') + i) for i in range(NUM_COLS)])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * NUM_COLS)
    print(border)
    for row in board:
        row_str = '|' + '|'.join(f' {cell} ' for cell in row) + '|'
        print(row_str)
        print(border)

def get_valid_column(player):
    """Prompt the player for a column and validate the input."""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) != 1:
            print("Please enter a single letter.")
            continue
        col_idx = ord(column) - ord('A')
        if 0 <= col_idx < NUM_COLS:
            return col_idx
        print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")

def place_checker(board, player, column):
    """Place the player's checker in the specified column if possible."""
    for row in reversed(range(NUM_ROWS)):
        if board[row][column] == ' ':
            board[row][column] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won the game."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(NUM_ROWS - 3):
        for col in range(3, NUM_COLS):
            if (board[row][col] == player and 
                board[row+1][col-1] == player and 
                board[row+2][col-2] == player and 
                board[row+3][col-3] == player):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = create_board()
    players_cycle = cycle(PLAYERS)
    current_player = next(players_cycle)  # Start with random player
    print_board(board)
    
    while True:
        column = get_valid_column(current_player)
        if not place_checker(board, current_player, column):
            print(f"Column {chr(ord('A') + column)} is full. Turn lost!")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = next(players_cycle)

if __name__ == "__main__":
    # Randomly choose the first player
    random.shuffle(PLAYERS)
    play_game()
