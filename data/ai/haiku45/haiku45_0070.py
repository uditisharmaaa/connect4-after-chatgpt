import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the board with empty spaces."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board, cols):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * cols + "+")


def get_column_input(cols):
    """Get and validate column input from the player."""
    while True:
        user_input = input("Enter a column (A-" + chr(ord('A') + cols - 1) + "): ").upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if user_input < 'A' or user_input >= chr(ord('A') + cols):
            print("Invalid column. Please enter a letter between A and " + chr(ord('A') + cols - 1) + ".")
            continue
        
        col_index = ord(user_input) - ord('A')
        return col_index


def place_checker(board, col, checker, rows):
    """Place a checker in the specified column. Returns True if successful."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_horizontal_win(board, rows, cols, checker):
    """Check if there is a horizontal win."""
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, rows, cols, checker):
    """Check if there is a vertical win."""
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, rows, cols, checker):
    """Check if there is a diagonal win (both directions)."""
    # Check diagonal from top-left to bottom-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal from top-right to bottom-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, rows, cols, checker):
    """Check if the current player has won."""
    return (check_horizontal_win(board, rows, cols, checker) or
            check_vertical_win(board, rows, cols, checker) or
            check_diagonal_win(board, rows, cols, checker))


def is_board_full(board, rows, cols):
    """Check if the board is full (draw condition)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Choose random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    
    # Game loop
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_player]
        
        print("Player " + checker + ", please enter a column:")
        
        # Get valid column input
        while True:
            col = get_column_input(COLS)
            
            # Try to place checker
            if place_checker(board, col, checker, ROWS):
                break
            else:
                print("Column is full. Please choose another column.")
        
        # Print board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, ROWS, COLS, checker):
            print("Player " + checker + " won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board, ROWS, COLS):
            print("It's a draw!")
            game_over = True
        
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
