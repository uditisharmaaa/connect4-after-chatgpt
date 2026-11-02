import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """
    Create and initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = []
    for row in range(ROWS):
        board.append([" "] * COLS)
    return board


def print_board(board):
    """
    Print the current state of the board with column labels.
    """
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Print top border of each cell
        print("+" + "---+" * COLS)
        # Print cell contents
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+" + "---+" * COLS)


def is_valid_column(board, col):
    """
    Check if a column is valid and has space for a checker.
    Returns True if valid, False otherwise.
    """
    if col < 0 or col >= COLS:
        return False
    # Check if top row of the column is empty
    return board[0][col] == " "


def get_next_row(board, col):
    """
    Find the next available row in the specified column.
    Returns the row index, or -1 if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def place_checker(board, col, symbol):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = symbol
        return True
    return False


def check_win(board, symbol):
    """
    Check if the specified player has won the game.
    Checks horizontal, vertical, and diagonal wins.
    Returns True if player won, False otherwise.
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical wins
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the game is a draw (board is full with no winner).
    Returns True if draw, False otherwise.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def get_player_input(board, player_symbol):
    """
    Get and validate player input for column selection.
    Returns the column index (0-based).
    """
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column has space
        if not is_valid_column(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize board
    board = create_board()
    
    # Set up players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player input and place checker
        col = get_player_input(board, current_player)
        place_checker(board, col, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Start the game
if __name__ == "__main__":
    play_game()
