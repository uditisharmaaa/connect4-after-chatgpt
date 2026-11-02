import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+" + "---+" * COLS)
    
    # Print each row with borders
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        print("+" + "---+" * COLS)


def is_valid_column(col_letter, board):
    """Check if the column input is valid and not full."""
    # Check if it's a single uppercase letter
    if len(col_letter) != 1 or not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full (top row has space)
    if board[0][col_index] != " ":
        return False
    
    return True


def place_checker(board, col_letter, checker):
    """Place a checker in the specified column. Returns True if successful."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
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
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def get_player_input(player_checker):
    """Get valid input from the player."""
    return input(f"Player {player_checker}, please enter a column: ")


def main():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        valid_move = False
        while not valid_move:
            col_input = get_player_input(checker)
            
            if is_valid_column(col_input, board):
                place_checker(board, col_input, checker)
                valid_move = True
            else:
                print("Invalid input. Please try again.")
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
