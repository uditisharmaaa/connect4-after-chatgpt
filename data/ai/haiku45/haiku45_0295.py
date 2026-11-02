import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize a board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the current state of the board to the console.
    
    Args:
        board: The game board (2D list)
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


def is_valid_column(column_letter, cols):
    """
    Check if the column letter is valid.
    
    Args:
        column_letter: The column letter provided by the user
        cols: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_letter) != 1:
        return False
    if not column_letter.isupper():
        return False
    col_index = ord(column_letter) - ord('A')
    return 0 <= col_index < cols


def get_column_index(column_letter):
    """
    Convert a column letter to its index.
    
    Args:
        column_letter: The column letter (e.g., 'A', 'B', etc.)
    
    Returns:
        The column index (0-based)
    """
    return ord(column_letter) - ord('A')


def can_place_checker(board, col_index, rows):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The game board (2D list)
        col_index: The column index (0-based)
        rows: Number of rows in the board
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    return board[0][col_index] == " "


def place_checker(board, col_index, checker, rows):
    """
    Place a checker in the given column.
    
    Args:
        board: The game board (2D list)
        col_index: The column index (0-based)
        checker: The checker symbol (e.g., 'X', 'O')
        rows: Number of rows in the board
    
    Returns:
        True if the checker was placed successfully, False otherwise
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_winner(board, rows, cols, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows in the board
        cols: Number of columns in the board
        checker: The checker symbol to check for a win
    
    Returns:
        True if the checker has won, False otherwise
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


def is_board_full(board, rows, cols):
    """
    Check if the board is completely filled.
    
    Args:
        board: The game board (2D list)
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


def get_player_move(current_player, cols):
    """
    Get a valid move from the current player.
    
    Args:
        current_player: The current player's checker symbol
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        column_letter = input(f"Player {current_player}, please enter a column: ").upper()
        
        if not is_valid_column(column_letter, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = get_column_index(column_letter)
        return col_index


def play_game(rows, cols, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
        num_players: Number of players in the game
    """
    # Initialize the board
    board = initialize_board(rows, cols)
    
    # Select checkers for each player
    player_checkers = CHECKERS[:num_players]
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print the initial board
    print_board(board, cols)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        
        # Get player's move
        col_index = get_player_move(current_checker, cols)
        
        # Check if the column is full
        if not can_place_checker(board, col_index, rows):
            print("This column is full. Please choose another column.")
            continue
        
        # Place the checker
        place_checker(board, col_index, current_checker, rows)
        
        # Print the board
        print_board(board, cols)
        
        # Check for a win
        if check_winner(board, rows, cols, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for a draw
        if is_board_full(board, rows, cols):
            print("It's a draw!")
            break
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % num_players


def main():
    """
    Main entry point of the program.
    """
    play_game(BOARD_ROWS, BOARD_COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
