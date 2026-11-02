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
    """Print the game board with columns labeled A to G."""
    # Clear the screen
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    print('+---+' * COLS)

def get_valid_column(board):
    """Get a valid column input from the player."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha() or ord(col_input) < 65 or ord(col_input) >= 65 + COLS:
            print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        
        col = ord(col_input) - 65
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won."""
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

def main():
    """Main game loop."""
    global current_player
    
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
