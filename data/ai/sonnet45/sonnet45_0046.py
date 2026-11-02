import random
import os

# Global constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board with the specified dimensions."""
    board = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    # Print column labels
    print("  ", end="")
    for col in range(NUM_COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print rows with borders
    for row in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * NUM_COLS + "+")

def is_valid_input(column, board):
    """Check if the column input is valid."""
    # Check if column is a single character
    if len(column) != 1:
        return False
    
    # Check if column is an uppercase letter
    if not column.isupper():
        return False
    
    # Check if column is within board range
    col_index = ord(column) - 65
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, column, checker):
    """Place a checker in the specified column."""
    col_index = ord(column) - 65
    
    # Find the lowest available row
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row][col + 1] == checker and
                board[row][col + 2] == checker and
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == checker and
                board[row + 1][col] == checker and
                board[row + 2][col] == checker and
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row + 1][col + 1] == checker and
                board[row + 2][col + 2] == checker and
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == checker and
                board[row - 1][col + 1] == checker and
                board[row - 2][col + 2] == checker and
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    """Main game loop."""
    # Create the board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get player input
        column = input("Player " + checker + ", please enter a column: ")
        
        # Validate input
        while not is_valid_input(column, board):
            column = input("Player " + checker + ", please enter a column: ")
        
        # Place checker
        place_checker(board, column, checker)
        
        # Clear screen and print board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
main()
