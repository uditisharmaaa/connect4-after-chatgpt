import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """
    Initialize a 2D board with all elements as whitespaces.
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """
    Print the game board with column labels and formatted grid.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
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

def get_valid_input(current_player):
    """
    Get valid column input from the player.
    
    Args:
        current_player: The checker symbol of the current player
    
    Returns:
        The column index (0-6) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col

def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column at the lowest available position.
    
    Args:
        board: The 2D list representing the game board
        col: The column index where the checker should be placed
        player_checker: The checker symbol to place
    
    Returns:
        True if the checker was successfully placed, False if the column is full
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    print(f"Column {chr(ord('A') + col)} is full. Please choose another column.")
    return False

def check_win(board, player_checker):
    """
    Check if the current player has won the game.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_draw(board):
    """
    Check if the game is a draw (board is full with no winner).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        
        # Get valid column input from player
        valid_placement = False
        while not valid_placement:
            col = get_valid_input(current_player_checker)
            valid_placement = place_checker(board, col, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
