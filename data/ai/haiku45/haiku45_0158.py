import os
import random

# Constants for board dimensions and game settings
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and return a 2D board with all cells initialized to spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """Print the board in the required format."""
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(chr(ord('A') + i), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for i in range(rows):
        print("|", end="")
        for j in range(cols):
            print(" " + board[i][j] + " |", end="")
        print()
        print("+---" * cols + "+")


def get_column_input(cols):
    """Get and validate column input from the player."""
    while True:
        user_input = input("Player " + current_player_symbol + ", please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is uppercase
        user_input = user_input.upper()
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board
        if col_index < 0 or col_index >= cols:
            print("Invalid column. Please enter a column between A and " + chr(ord('A') + cols - 1) + ".")
            continue
        
        return col_index


def place_checker(board, col, symbol):
    """Place a checker in the specified column. Return True if successful, False if column is full."""
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_horizontal_win(board, symbol):
    """Check if the given symbol has won horizontally."""
    rows = len(board)
    cols = len(board[0])
    
    for i in range(rows):
        for j in range(cols - WIN_LENGTH + 1):
            if (board[i][j] == symbol and 
                board[i][j + 1] == symbol and 
                board[i][j + 2] == symbol and 
                board[i][j + 3] == symbol):
                return True
    return False


def check_vertical_win(board, symbol):
    """Check if the given symbol has won vertically."""
    rows = len(board)
    cols = len(board[0])
    
    for i in range(rows - WIN_LENGTH + 1):
        for j in range(cols):
            if (board[i][j] == symbol and 
                board[i + 1][j] == symbol and 
                board[i + 2][j] == symbol and 
                board[i + 3][j] == symbol):
                return True
    return False


def check_diagonal_win(board, symbol):
    """Check if the given symbol has won diagonally."""
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal (top-left to bottom-right)
    for i in range(rows - WIN_LENGTH + 1):
        for j in range(cols - WIN_LENGTH + 1):
            if (board[i][j] == symbol and 
                board[i + 1][j + 1] == symbol and 
                board[i + 2][j + 2] == symbol and 
                board[i + 3][j + 3] == symbol):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for i in range(rows - WIN_LENGTH + 1):
        for j in range(WIN_LENGTH - 1, cols):
            if (board[i][j] == symbol and 
                board[i + 1][j - 1] == symbol and 
                board[i + 2][j - 2] == symbol and 
                board[i + 3][j - 3] == symbol):
                return True
    
    return False


def check_win(board, symbol):
    """Check if the given symbol has won the game."""
    if (check_horizontal_win(board, symbol) or
        check_vertical_win(board, symbol) or
        check_diagonal_win(board, symbol)):
        return True
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    cols = len(board[0])
    
    for j in range(cols):
        if board[0][j] == " ":
            return False
    return True


def play_game():
    """Main game loop."""
    global current_player_symbol
    
    # Initialize board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Choose random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player_symbol = PLAYER_SYMBOLS[current_player_index]
        
        # Get valid column input
        valid_move = False
        while not valid_move:
            col = get_column_input(BOARD_COLS)
            valid_move = place_checker(board, col, current_player_symbol)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_symbol):
            print("Player " + current_player_symbol + " won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("Draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Global variable to track current player symbol
current_player_symbol = ""

# Start the game
play_game()
