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
    """Print the game board with column labels and borders."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    for row in range(ROWS):
        # Print row with cell contents
        print('|' + '|'.join([f' {board[row][col]} ' for col in range(COLS)]) + '|')
        # Print row border
        print('+' + ('---+' * COLS))

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    return 'A' <= col <= chr(65 + COLS - 1)

def get_first_empty_row(board, col):
    """Get the first empty row in the specified column."""
    col_index = ord(col) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            return row
    return -1

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    col_index = ord(col) - 65
    row = get_first_empty_row(board, col)
    if row != -1:
        board[row][col_index] = player
        return True
    return False

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col + 1] == player and 
                board[row][col + 2] == player and 
                board[row][col + 3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row + 1][col] == player and 
                board[row + 2][col] == player and 
                board[row + 3][col] == player):
                return True
    
    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row + 1][col + 1] == player and 
                board[row + 2][col + 2] == player and 
                board[row + 3][col + 3] == player):
                return True
    
    # Check diagonal down-left
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == player and 
                board[row + 1][col - 1] == player and 
                board[row + 2][col - 2] == player and 
                board[row + 3][col - 3] == player):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))
    
    while True:
        print_board(board)
        player_symbol = PLAYERS[current_player]
        
        # Handle input
        while True:
            col = input(f"Player {player_symbol}, please enter a column: ").upper()
            if is_valid_column(col):
                if get_first_empty_row(board, col) != -1:
                    break
                else:
                    print("Column is full. Try another column.")
            else:
                print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
        
        # Place checker and check for win/draw
        if place_checker(board, col, player_symbol):
            if check_win(board, player_symbol):
                print_board(board)
                print(f"Player {player_symbol} won!")
                return
            if check_draw(board):
                print_board(board)
                print("Game ended in a draw!")
                return
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
