import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+---+' * COLS)

def is_valid_column(col):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col_char = col.upper()
    return col_char >= 'A' and col_char <= chr(65 + COLS - 1)

def get_column_index(col):
    """Convert the column letter to a 0-based index."""
    return ord(col.upper()) - ord('A')

def place_checker(board, col_idx, player):
    """Place the player's checker in the specified column if possible."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player
            return True
    return False

def check_win(board, player):
    """Check if the current player has won the game."""
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
    
    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal up-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        clear_screen()
        print_board(board)
        
        print(f"Player {current_player}, please enter a column: ", end='')
        col_input = input().strip()
        
        if not is_valid_column(col_input):
            print("Invalid input! Please enter a valid column letter (A-G).")
            input("Press Enter to continue...")
            continue
        
        col_idx = get_column_index(col_input)
        
        if not place_checker(board, col_idx, current_player):
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...")
        else:
            if check_win(board, current_player):
                clear_screen()
                print_board(board)
                print(f"Player {current_player} won!")
                break
            
            if is_draw(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
