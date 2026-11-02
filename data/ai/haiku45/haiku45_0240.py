import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """
    Create a board with the specified number of rows and columns.
    All cells are initialized with whitespace.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the board in the format specified in the assignment.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    header = "  "
    for col in range(cols):
        header += chr(ord('A') + col) + "   "
    print(header)
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        row_str = "|"
        for col in range(cols):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    
    # Print bottom border
    print("+---" * cols + "+")

def get_valid_input(cols):
    """
    Get valid column input from the user.
    Input must be a single uppercase letter corresponding to a valid column.
    """
    while True:
        user_input = input("Player {}, please enter a column: ".format(current_player_symbol)).strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Check if the letter is within the valid range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Column {} is out of range.".format(user_input))
            continue
        
        return col_index

def place_checker(board, col, symbol):
    """
    Place a checker in the specified column.
    Returns True if placement was successful, False if column is full.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    
    # Column is full
    return False

def check_win(board, symbol):
    """
    Check if the specified player has won.
    Returns True if the player has 4 checkers in a row, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_draw(board):
    """
    Check if the board is full (draw condition).
    Returns True if the board is full, False otherwise.
    """
    return all(board[0][col] != ' ' for col in range(len(board[0])))

def is_column_full(board, col):
    """
    Check if a column is completely full.
    Returns True if full, False otherwise.
    """
    return board[0][col] != ' '

def play_game():
    """
    Main game loop.
    """
    global current_player_symbol
    
    # Create the board
    board = create_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    current_player_symbol = SYMBOLS[current_player]
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    while True:
        # Get valid column input
        while True:
            col = get_valid_input(COLS)
            
            # Check if column is full
            if is_column_full(board, col):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place checker
        place_checker(board, col, current_player_symbol)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_symbol):
            print("Player {} won!".format(current_player_symbol))
            break
        
        # Check for draw
        if check_draw(board):
            print("Draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS
        current_player_symbol = SYMBOLS[current_player]

# Global variable to track current player symbol
current_player_symbol = SYMBOLS[0]

if __name__ == "__main__":
    play_game()
