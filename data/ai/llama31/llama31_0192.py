import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels"""
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print("\n+---+---+---+---+---+---+---+")
    print()

def validate_input(column):
    """Check if user input is valid"""
    if not column.isalpha() or not column.isupper():
        return False
    if ord(column) < ord("A") or ord(column) > ord("G"):
        return False
    return True

def place_checker(board, column, checker):
    """Place a checker in the specified column"""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the specified player has won"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i+1][col] == checker and board[i+2][col] == checker and board[i+3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the board is full"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Create the board
    board = create_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        # Clear the screen
        os.system('clear')
        
        # Print the board
        print_board(board)
        
        # Get the current player's checker
        checker = CHECKERS[current_player]
        
        # Prompt the user for a column
        column = input(f"Player {checker}, please enter a column: ")
        
        # Validate the input
        while not validate_input(column):
            column = input("Invalid input. Please enter a column (A-G): ")
        
        # Convert the column to a zero-based index
        column = ord(column) - ord("A")
        
        # Place the checker
        if not place_checker(board, column, checker):
            print("Column is full. Please try again.")
            input("Press Enter to continue...")
            continue
        
        # Check for a win
        if check_win(board, checker):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        # Check for a draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
