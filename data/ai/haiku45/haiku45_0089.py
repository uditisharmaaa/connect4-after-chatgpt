import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()
    
    # Print rows
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()

def is_valid_column(column_letter, board):
    """Check if the column letter is valid and not full."""
    # Check if it's a single letter
    if len(column_letter) != 1:
        return False
    
    # Check if it's uppercase
    if not column_letter.isupper():
        return False
    
    # Check if it's a letter
    if not column_letter.isalpha():
        return False
    
    # Convert to column index
    col_index = ord(column_letter) - ord('A')
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, column_letter, checker):
    """Place a checker in the specified column."""
    col_index = ord(column_letter) - ord('A')
    
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return

def check_horizontal_win(board, checker):
    """Check if there is a horizontal win."""
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_vertical_win(board, checker):
    """Check if there is a vertical win."""
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_diagonal_win(board, checker):
    """Check if there is a diagonal win (both directions)."""
    # Check diagonals going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_win(board, checker))

def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Create the board
    board = create_board()
    
    # Get the checkers for each player
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_checker = player_checkers[current_player_index]
        
        # Get valid input from the player
        while True:
            column_letter = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if is_valid_column(column_letter, board):
                break
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Place the checker
        place_checker(board, column_letter, current_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
