import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Initialize the board with empty spaces."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLS)])
    return board


def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print board with separators
    for row in range(ROWS):
        # Print top separator
        print("+---" * COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom separator
    print("+---" * COLS + "+")


def get_column_input(board, current_player):
    """Get valid column input from the player."""
    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - 65
        
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please enter another column.")
            continue
        
        return col_index


def place_checker(board, col, current_player):
    """Place a checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[current_player]
            return


def check_horizontal_win(board, current_player):
    """Check if the current player has won horizontally."""
    checker = CHECKERS[current_player]
    
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, current_player):
    """Check if the current player has won vertically."""
    checker = CHECKERS[current_player]
    
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, current_player):
    """Check if the current player has won diagonally."""
    checker = CHECKERS[current_player]
    
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


def check_win(board, current_player):
    """Check if the current player has won."""
    return (check_horizontal_win(board, current_player) or
            check_vertical_win(board, current_player) or
            check_diagonal_win(board, current_player))


def check_draw(board):
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
    
    # Choose random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get player input
        col = get_column_input(board, current_player)
        
        # Place checker
        place_checker(board, col, current_player)
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
