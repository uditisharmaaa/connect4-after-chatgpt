import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """
    Initialize the board with empty cells (whitespaces).
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the board with column labels and formatting.
    
    Args:
        board: The 2D list representing the board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board rows
    for row in board:
        # Print top border
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()


def get_valid_column(board, cols):
    """
    Get a valid column input from the player.
    
    Args:
        board: The 2D list representing the board
        cols: Number of columns in the board
    
    Returns:
        The column index (0-indexed) where the checker will be placed
    """
    while True:
        user_input = input().strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter (A-{}).".format(chr(65 + cols - 1)))
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter (A-{}).".format(chr(65 + cols - 1)))
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - 65
        
        # Validate column is within range
        if col_index < 0 or col_index >= cols:
            print("Invalid input. Please enter a letter between A and {}.".format(chr(65 + cols - 1)))
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column {} is full. Please choose another column.".format(user_input))
            continue
        
        return col_index


def place_checker(board, col_index, checker, rows, cols):
    """
    Place a checker in the specified column at the lowest available position.
    
    Args:
        board: The 2D list representing the board
        col_index: The column index (0-indexed) where the checker will be placed
        checker: The checker symbol (X, O, V, H, or M)
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if checker was placed successfully, False otherwise
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_win(board, checker, rows, cols):
    """
    Check if the given checker has won (4 in a row).
    
    Args:
        board: The 2D list representing the board
        checker: The checker symbol to check for
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the checker has won, False otherwise
    """
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols):
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
        board: The 2D list representing the board
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    
    return True


def play_game(board, rows, cols, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        board: The 2D list representing the board
        rows: Number of rows in the board
        cols: Number of columns in the board
        num_players: Number of players in the game
    """
    # Select a random starting player
    current_player_index = random.randint(0, num_players - 1)
    current_checker = CHECKERS[current_player_index]
    
    # Print initial board
    print_board(board, cols)
    
    # Game loop
    while True:
        # Get player input
        print(f"Player {current_checker}, please enter a column: ", end="")
        col_index = get_valid_column(board, cols)
        
        # Place checker
        place_checker(board, col_index, current_checker, rows, cols)
        
        # Print updated board
        print_board(board, cols)
        
        # Check for win
        if check_win(board, current_checker, rows, cols):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board, rows, cols):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players
        current_checker = CHECKERS[current_player_index]


def main():
    """
    Main function to initialize and start the game.
    """
    board = initialize_board(ROWS, COLS)
    play_game(board, ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
