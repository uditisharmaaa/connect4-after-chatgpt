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
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print column headers
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    
    # Print top border
    print('+' + '---+' * COLS)
    
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or col < 'A' or col > chr(ord('A') + COLS - 1):
            print(f"Column must be a letter from A to {chr(ord('A') + COLS - 1)}")
            continue
        return ord(col) - ord('A')

def place_checker(board, col, player):
    """Place the player's checker in the lowest available row of the column.
    Returns True if placement was successful, False otherwise."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    global current_player
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        col = get_valid_column()
        
        if not place_checker(board, col, current_player):
            print("Column is full. You lose your turn.")
            
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("Game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
