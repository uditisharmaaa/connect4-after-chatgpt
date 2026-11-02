import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and return a board with all cells initialized to empty spaces."""
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """Print the current state of the board with column labels and borders."""
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")


def get_valid_input(board, current_player_checker):
    """Get and validate user input for column selection."""
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """Place a checker in the specified column at the lowest available row."""
    rows = len(board)
    
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """Check if the given checker has won horizontally."""
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, checker):
    """Check if the given checker has won vertically."""
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, checker):
    """Check if the given checker has won diagonally."""
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonals going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """Check if the given checker has won the game."""
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_win(board, checker))


def is_board_full(board):
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """Main game loop for Connect 4."""
    # Initialize board
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Determine checkers for this game
    players_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Clear screen and print initial board
    os.system('clear')
    print_board(board)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = players_checkers[current_player_index]
        
        # Get valid column input from player
        col_index = get_valid_input(board, current_checker)
        
        # Place checker
        place_checker(board, col_index, current_checker)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
