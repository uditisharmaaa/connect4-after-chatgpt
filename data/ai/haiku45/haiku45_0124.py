import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with all empty cells (whitespaces).
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * COLS + "+")


def is_valid_input(user_input, board):
    """
    Validate user input.
    Returns True if input is valid, False otherwise.
    Valid input: single uppercase letter within board column range, and column not full.
    """
    # Check if input is a single character
    if len(user_input) != 1:
        return False
    
    # Check if input is a letter
    if not user_input.isalpha():
        return False
    
    # Convert to uppercase and check if it's within range
    col = ord(user_input.upper()) - ord('A')
    if col < 0 or col >= COLS:
        return False
    
    # Check if column is not full (top cell is empty)
    if board[0][col] != " ":
        return False
    
    return True


def get_valid_column(board):
    """
    Prompt the player for a valid column input until a valid input is provided.
    Returns the column index (0-based).
    """
    while True:
        user_input = input("Please enter a column: ").strip()
        if is_valid_input(user_input, board):
            return ord(user_input.upper()) - ord('A')
        print("Invalid input. Please enter a valid column.")


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    Returns True if placement was successful, False if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_winner(board, checker):
    """
    Check if the given checker has won the game.
    A player wins by getting 4 checkers in a row horizontally, vertically, or diagonally.
    Returns True if checker has won, False otherwise.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    Returns True if board is full, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop. Handles the flow of the game.
    """
    # Initialize board
    board = initialize_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column from player
        col = get_valid_column(board)
        
        # Place checker
        place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for winner
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
