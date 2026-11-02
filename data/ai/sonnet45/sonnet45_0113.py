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
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(column, board):
    """Check if the column input is valid"""
    # Check if column is a single character
    if len(column) != 1:
        return False
    
    # Check if column is a letter
    if not column.isalpha():
        return False
    
    # Convert to uppercase and check if it's within range
    column = column.upper()
    col_index = ord(column) - 65
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(column, checker, board):
    """Place a checker in the specified column"""
    col_index = ord(column.upper()) - 65
    
    # Find the lowest available row
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
    
    # Check diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if (board[i][j] == checker and 
                board[i+1][j+1] == checker and 
                board[i+2][j+2] == checker and 
                board[i+3][j+3] == checker):
                return True
    
    # Check diagonal (down-left)
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if (board[i][j] == checker and 
                board[i+1][j-1] == checker and 
                board[i+2][j-2] == checker and 
                board[i+3][j-3] == checker):
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
    # Create board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        
        # Get player input
        valid_input = False
        while not valid_input:
            column = input("Player " + checker + ", please enter a column: ")
            
            if is_valid_column(column, board):
                valid_input = True
            else:
                print("Invalid input. Please try again.")
        
        # Place checker
        place_checker(column, checker, board)
        
        # Clear screen and print board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
main()
