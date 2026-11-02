import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board"""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the board with column labels"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print board rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    """Check if the column input is valid"""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, col_letter, checker):
    """Place a checker in the specified column"""
    col_index = ord(col_letter) - 65
    
    # Find the lowest empty row in the column
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_index] == " ":
            board[i][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Check if the specified checker has won"""
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if (board[i][j] == checker and 
                board[i][j+1] == checker and 
                board[i][j+2] == checker and 
                board[i][j+3] == checker):
                return True
    
    # Check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if (board[i][j] == checker and 
                board[i+1][j] == checker and 
                board[i+2][j] == checker and 
                board[i+3][j] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if (board[i][j] == checker and 
                board[i+1][j+1] == checker and 
                board[i+2][j+2] == checker and 
                board[i+3][j+3] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for i in range(3, ROWS):
        for j in range(COLS - 3):
            if (board[i][j] == checker and 
                board[i-1][j+1] == checker and 
                board[i-2][j+2] == checker and 
                board[i-3][j+3] == checker):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

def main():
    """Main game function"""
    # Initialize board
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
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {checker}, please enter a column: ")
            
            if is_valid_column(col_input, board):
                valid_input = True
            else:
                print("Invalid input. Please try again.")
        
        # Place checker
        place_checker(board, col_input, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
