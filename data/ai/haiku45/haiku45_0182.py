import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """
    Creates and returns a 2D board with all cells initialized to spaces.
    """
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """
    Prints the current state of the board with column labels and borders.
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(" " + chr(ord('A') + col) + " ", end="")
    print()
    
    # Print rows with borders
    for row in range(rows):
        # Top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Row content
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def get_valid_input(cols):
    """
    Prompts the user for a column input and validates it.
    Returns the column index (0-based) if valid.
    """
    while True:
        user_input = input().strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter:")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a column letter (A-" + chr(ord('A') + cols - 1) + "):")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within bounds
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Please enter a column letter (A-" + chr(ord('A') + cols - 1) + "):")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Places a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_win(board, checker):
    """
    Checks if the specified checker has won.
    Returns True if the checker has 4 in a row, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """
    Checks if the board is completely full.
    Returns True if full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Create the board
    board = create_board(ROWS, COLS)
    
    # Select checkers for each player
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        
        # Get player input
        print("Player " + current_checker + ", please enter a column:")
        col = get_valid_input(COLS)
        
        # Try to place the checker
        if not place_checker(board, col, current_checker):
            print("Column is full. Please choose another column:")
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print("Player " + current_checker + " won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("Draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
