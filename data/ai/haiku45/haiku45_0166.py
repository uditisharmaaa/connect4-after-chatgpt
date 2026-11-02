import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board with dimensions COLUMNS x ROWS."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLUMNS)])
    return board


def print_board(board):
    """Print the board in a formatted manner with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with separators
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    print("+---" * COLUMNS + "+")


def get_column_input(current_player_symbol):
    """Get and validate column input from the current player."""
    while True:
        user_input = input(f"Player {current_player_symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Check if column is within board range
        column = ord(user_input) - ord('A')
        if column < 0 or column >= COLUMNS:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        
        return column


def place_checker(board, column, player_symbol):
    """Place a checker in the given column. Return True if successful, False if column is full."""
    # Find the lowest empty row in the column (start from bottom)
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_symbol
            return True
    
    # Column is full
    print("This column is full. Please try another column.")
    return False


def check_horizontal_win(board, player_symbol):
    """Check if the player has won horizontally."""
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, player_symbol):
    """Check if the player has won vertically."""
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_symbol for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, player_symbol):
    """Check if the player has won diagonally."""
    # Check diagonal going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal going down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, player_symbol):
    """Check if the current player has won."""
    if check_horizontal_win(board, player_symbol):
        return True
    if check_vertical_win(board, player_symbol):
        return True
    if check_diagonal_win(board, player_symbol):
        return True
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def get_player_symbols(num_players):
    """Return the symbols for the given number of players."""
    return PLAYER_SYMBOLS[:num_players]


def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Get player symbols
    player_symbols = get_player_symbols(NUM_PLAYERS)
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        current_player_symbol = player_symbols[current_player_index]
        
        # Get valid column input
        column_valid = False
        while not column_valid:
            column = get_column_input(current_player_symbol)
            column_valid = place_checker(board, column, current_player_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_symbol):
            print(f"Player {current_player_symbol} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
