import random
import os

# Constants for game configuration
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """
    Creates and returns an empty game board.
    Board is a 2D list with NUM_ROWS rows and NUM_COLS columns.
    All cells are initialized with empty spaces.
    """
    board = []
    for row in range(NUM_ROWS):
        board.append([' '] * NUM_COLS)
    return board

def print_board(board):
    """
    Prints the current state of the board with column labels.
    Columns are labeled A, B, C, etc.
    """
    # Print column headers
    print("  ", end="")
    for col in range(NUM_COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * NUM_COLS + "+")

def is_valid_column(col_letter, board):
    """
    Checks if the input column letter is valid.
    Returns True if valid, False otherwise.
    Valid means: uppercase letter, within board range, and column not full.
    """
    # Check if input is a single uppercase letter
    if len(col_letter) != 1 or not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    # Check if column is not full (top row has space)
    if board[0][col_index] != ' ':
        return False
    
    return True

def place_checker(board, col_letter, player_symbol):
    """
    Places a checker in the specified column.
    The checker falls to the lowest available row in that column.
    Returns True if successful, False otherwise.
    """
    col_index = ord(col_letter) - 65
    
    # Find the lowest empty row in the column (bottom to top)
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player_symbol
            return True
    
    return False

def check_win(board, player_symbol):
    """
    Checks if the specified player has won the game.
    Returns True if player has 4 in a row (horizontal, vertical, or diagonal).
    """
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical wins
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS):
            if all(board[row + i][col] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_draw(board):
    """
    Checks if the board is full (draw condition).
    Returns True if all cells are filled, False otherwise.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == ' ':
                return False
    return True

def get_player_input(board, player_symbol):
    """
    Gets and validates player input for column selection.
    Keeps asking until valid input is received.
    Returns the valid column letter.
    """
    while True:
        col_letter = input(f"Player {player_symbol}, please enter a column: ")
        
        if is_valid_column(col_letter, board):
            return col_letter
        else:
            print("Invalid input. Please enter a valid column letter.")

def main():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Create empty board
    board = create_board()
    
    # Get player symbols based on number of players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player input
        col_letter = get_player_input(board, current_player)
        
        # Place checker
        place_checker(board, col_letter, current_player)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
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
