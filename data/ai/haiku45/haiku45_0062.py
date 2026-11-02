import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return a board with all cells initialized to empty spaces."""
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """Print the board with column labels and grid formatting."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print board with separators
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def is_valid_column(column_letter, board):
    """Check if the column letter is valid and the column is not full."""
    # Check if it's a valid letter
    if len(column_letter) != 1 or not column_letter.isalpha():
        return False
    
    # Convert to uppercase and check if in range
    column_letter = column_letter.upper()
    col_index = ord(column_letter) - ord('A')
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column is not full (top cell is empty)
    if board[0][col_index] == " ":
        return True
    
    return False


def get_column_index(column_letter):
    """Convert column letter to column index."""
    return ord(column_letter.upper()) - ord('A')


def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available row."""
    # Find the lowest empty row in this column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """Check if there are 4 checkers in a row horizontally."""
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, checker):
    """Check if there are 4 checkers in a row vertically."""
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, checker):
    """Check if there are 4 checkers in a row diagonally."""
    # Check diagonal going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal going down-left
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
    """Check if the board is full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = CHECKERS[current_player_index]
        
        # Get valid input from player
        while True:
            column_input = input(f"Player {current_checker}, please enter a column: ")
            
            if is_valid_column(column_input, board):
                col_index = get_column_index(column_input)
                place_checker(board, col_index, current_checker)
                break
            else:
                print("Invalid input. Please enter a valid column letter (A-" + 
                      chr(ord('A') + COLS - 1) + ").")
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Start the game."""
    play_game()


if __name__ == "__main__":
    main()
