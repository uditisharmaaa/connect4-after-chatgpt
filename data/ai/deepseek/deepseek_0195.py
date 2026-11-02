import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C...)
    headers = '   ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]) + '   '
    border = '+' + ('---+' * BOARD_COLS)
    print(headers)
    print(border)
    
    # Print each row
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        print(row_str)
        print(border)

def get_valid_column(player):
    """Get a valid column from the player."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if not col_input or len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= BOARD_COLS:
            print(f"Column must be between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        
        return col

def place_checker(board, player, col):
    """Place the player's checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won the game."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col = get_valid_column(current_player)
        
        if not place_checker(board, current_player, col):
            print("Column is full. Turn lost.")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
