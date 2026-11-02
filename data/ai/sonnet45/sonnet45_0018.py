import random
import os

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates and returns a 2D board initialized with empty spaces.
    Board dimensions are determined by ROWS and COLS constants.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    """
    Prints the current state of the board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Print top border of row
        print("+---" * COLS + "+")
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")

def is_valid_column(column_input, board):
    """
    Validates if the column input is valid.
    Returns (is_valid, col_index) tuple.
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return False, -1
    
    # Check if input is an uppercase letter
    if not column_input.isupper() or not column_input.isalpha():
        return False, -1
    
    # Convert letter to column index
    col_index = ord(column_input) - 65
    
    # Check if column index is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False, -1
    
    # Check if column has space (top row must be empty)
    if board[0][col_index] != " ":
        return False, -1
    
    return True, col_index

def place_checker(board, col_index, symbol):
    """
    Places a checker in the specified column.
    The checker falls to the lowest available position.
    Returns the row index where the checker was placed.
    """
    # Start from bottom row and find first empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row
    return -1

def check_win(board, symbol):
    """
    Checks if the specified player symbol has won the game.
    Checks horizontal, vertical, and diagonal directions.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if all cells in the top row are filled.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = create_board()
    
    # Get player symbols based on number of players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_symbol = players[current_player_index]
        
        # Get valid input from current player
        valid_move = False
        while not valid_move:
            column_input = input(f"Player {current_symbol}, please enter a column: ")
            is_valid, col_index = is_valid_column(column_input, board)
            
            if is_valid:
                valid_move = True
            else:
                print("Invalid input. Please try again.")
        
        # Place the checker
        place_checker(board, col_index, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    main()
