import os
import random

# Game configuration constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Create and initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the game board in the specified format.
    
    Args:
        board: 2D list representing the game board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(ord('A') + col)}   ", end="")
    print()
    
    # Print board with borders
    rows = len(board)
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


def get_valid_input(cols):
    """
    Get and validate player input for column selection.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        Column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input("Player {}, please enter a column: ".format(current_player_checker)).upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter (A-{}).".format(chr(ord('A') + cols - 1)))
            continue
        
        # Check if input is within board range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Please enter a letter between A and {}.".format(chr(ord('A') + cols - 1)))
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: 2D list representing the game board
        col: Column index (0-based)
        checker: Player's checker symbol
    
    Returns:
        True if checker was placed successfully, False if column is full
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, rows, cols, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: 2D list representing the game board
        rows: Number of rows in the board
        cols: Number of columns in the board
        checker: Player's checker symbol to check for win
    
    Returns:
        True if the checker has 4 in a row, False otherwise
    """
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


def check_draw(board, rows, cols):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: 2D list representing the game board
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if board is full, False otherwise
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        
        # Get valid column input from player
        valid_move = False
        while not valid_move:
            col = get_valid_input(COLS)
            valid_move = place_checker(board, col, current_player_checker)
        
        # Print board after move
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, ROWS, COLS, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board, ROWS, COLS):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
