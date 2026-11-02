import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Creates and returns an empty board."""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """Prints the board to the console."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    """Checks if the column input is valid."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Check if column is within board range
    col_index = ord(col_letter) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, col_letter, checker):
    """Places a checker in the specified column."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest empty row in the column
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_index] == " ":
            board[i][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Checks if the specified checker has won."""
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - WIN_LENGTH + 1):
            count = 0
            for k in range(WIN_LENGTH):
                if board[i][j + k] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check vertical
    for i in range(ROWS - WIN_LENGTH + 1):
        for j in range(COLS):
            count = 0
            for k in range(WIN_LENGTH):
                if board[i + k][j] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for i in range(ROWS - WIN_LENGTH + 1):
        for j in range(COLS - WIN_LENGTH + 1):
            count = 0
            for k in range(WIN_LENGTH):
                if board[i + k][j + k] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for i in range(WIN_LENGTH - 1, ROWS):
        for j in range(COLS - WIN_LENGTH + 1):
            count = 0
            for k in range(WIN_LENGTH):
                if board[i - k][j + k] == checker:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    return False

def is_board_full(board):
    """Checks if the board is full."""
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

def play_game():
    """Main game function."""
    # Initialize the board
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
        
        # Ask for input
        col_letter = input("Player " + checker + ", please enter a column: ")
        
        # Validate input
        while not is_valid_column(col_letter, board):
            print("Invalid input. Please try again.")
            col_letter = input("Player " + checker + ", please enter a column: ")
        
        # Place the checker
        place_checker(board, col_letter, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS

# Start the game
play_game()
