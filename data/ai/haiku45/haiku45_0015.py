import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(width, height):
    """
    Initialize the game board with empty spaces.
    
    Args:
        width: Number of columns
        height: Number of rows
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(width)] for _ in range(height)]
    return board


def print_board(board):
    """
    Print the current game board with column labels and formatting.
    
    Args:
        board: The game board (2D list)
    """
    os.system('clear')
    width = len(board[0])
    height = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(width):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * width + "+")
    
    # Print each row
    for row in range(height):
        print("|", end="")
        for col in range(width):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * width + "+")


def get_valid_input(width):
    """
    Get valid column input from the user.
    
    Args:
        width: Number of columns in the board
    
    Returns:
        Column index (0 to width-1)
    """
    while True:
        user_input = input("Player {}, please enter a column: ".format(current_player_checker)).strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within bounds
        if col_index < 0 or col_index >= width:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + width - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col: Column index
        checker: The checker symbol ('X', 'O', etc.)
    
    Returns:
        True if checker was placed successfully, False if column is full
    """
    height = len(board)
    
    # Find the lowest empty row in the column
    for row in range(height - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("Column is full. Try another column.")
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won the game.
    
    Args:
        board: The game board (2D list)
        checker: The checker symbol to check for
    
    Returns:
        True if the checker has won, False otherwise
    """
    height = len(board)
    width = len(board[0])
    
    # Check horizontal
    for row in range(height):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(width):
        for row in range(height - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, width):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the game is a draw (board is full).
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(board[0][col] != " " for col in range(len(board[0])))


def play_game():
    """
    Main game loop for Connect 4.
    """
    global current_player_checker
    
    # Initialize the board
    board = initialize_board(BOARD_WIDTH, BOARD_HEIGHT)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        current_player_checker = CHECKERS[current_player]
        
        # Get valid input from the player
        while True:
            col = get_valid_input(BOARD_WIDTH)
            if place_checker(board, col, current_player_checker):
                break
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    current_player_checker = ""
    main()
