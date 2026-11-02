import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    board = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current board state."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(NUM_COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for i in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("| ", end="")
        for j in range(NUM_COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * NUM_COLS + "+")

def is_valid_input(column, board):
    """Check if the input is valid."""
    # Check if column is a single character
    if len(column) != 1:
        return False
    
    # Check if column is a letter
    if not column.isalpha():
        return False
    
    # Convert to uppercase and get column index
    column = column.upper()
    col_index = ord(column) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    # Check if column has space
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, column, checker):
    """Place a checker in the specified column."""
    column = column.upper()
    col_index = ord(column) - 65
    
    # Find the lowest available row
    for i in range(NUM_ROWS - 1, -1, -1):
        if board[i][col_index] == " ":
            board[i][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS - 3):
            if (board[i][j] == checker and 
                board[i][j+1] == checker and 
                board[i][j+2] == checker and 
                board[i][j+3] == checker):
                return True
    
    # Check vertical
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS):
            if (board[i][j] == checker and 
                board[i+1][j] == checker and 
                board[i+2][j] == checker and 
                board[i+3][j] == checker):
                return True
    
    # Check diagonal (down-right)
    for i in range(NUM_ROWS - 3):
        for j in range(NUM_COLS - 3):
            if (board[i][j] == checker and 
                board[i+1][j+1] == checker and 
                board[i+2][j+2] == checker and 
                board[i+3][j+3] == checker):
                return True
    
    # Check diagonal (down-left)
    for i in range(NUM_ROWS - 3):
        for j in range(3, NUM_COLS):
            if (board[i][j] == checker and 
                board[i+1][j-1] == checker and 
                board[i+2][j-2] == checker and 
                board[i+3][j-3] == checker):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for j in range(NUM_COLS):
        if board[0][j] == " ":
            return False
    return True

def main():
    """Main game loop."""
    # Create board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get player input
        valid = False
        while not valid:
            column = input(f"Player {checker}, please enter a column: ")
            
            if is_valid_input(column, board):
                valid = True
            else:
                print("Invalid input. Please try again.")
        
        # Place checker
        place_checker(board, column, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
