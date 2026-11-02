import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty board with the specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels."""
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+" + "---+" * COLS)

def is_valid_column(col_letter, board):
    """Check if the column input is valid and not full."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if input is a letter
    if not col_letter.isalpha():
        return False
    
    # Convert to uppercase and get column index
    col_letter = col_letter.upper()
    col_index = ord(col_letter) - ord('A')
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != ' ':
        return False
    
    return True

def place_checker(board, col_letter, checker):
    """Place a checker in the specified column and return True if successful."""
    col_index = ord(col_letter.upper()) - ord('A')
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    
    return False

def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Set up players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid input from current player
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {current_checker}, please enter a column: ")
            
            if is_valid_column(col_input, board):
                valid_input = True
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Place the checker
        place_checker(board, col_input.upper(), current_checker)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
