import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    header = "  " + "   ".join([chr(65 + i) for i in range(len(board[0]))])
    print(header)
    
    # Print each row with separators
    separator = "+" + ("---+" * len(board[0]))
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column(col, board):
    """Check if the column is valid and has space."""
    if len(col) != 1:
        return False
    col = col.upper()
    if not col.isalpha() or ord(col) - ord('A') >= len(board[0]):
        return False
    return board[0][ord(col) - ord('A')] == " "

def place_checker(board, col, checker):
    """Place the checker in the specified column."""
    col_idx = ord(col.upper()) - ord('A')
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the current player has won."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    
    # Check vertical
    for row in range(rows - 3):
        for col in range(cols):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    
    # Check diagonal (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    # Initialize game
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    clear_screen()
    print("Welcome to Connect 4!")
    print_board(board)
    
    while True:
        # Get player input
        col = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_column(col, board):
            print("Invalid column. Please choose a valid column (A-G) with space.")
            continue
        
        # Place checker
        if place_checker(board, col, current_player):
            clear_screen()
            print_board(board)
            
            # Check for winner
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            # Check for draw
            if is_draw(board):
                print("The game is a draw!")
                break
            
            # Switch player
            current_player = players[(players.index(current_player) + 1) % len(players)]
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    main()
