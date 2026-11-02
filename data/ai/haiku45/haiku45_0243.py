import os
import random

# Configuration constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize a board with the given dimensions filled with whitespaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board to the console with proper formatting.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(ord('A') + i)}  ", end="")
    print()
    
    # Print each row with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * cols + "+")


def column_letter_to_index(letter):
    """
    Convert a column letter (A, B, C, etc.) to a 0-based index.
    
    Args:
        letter: A single uppercase letter
    
    Returns:
        The 0-based column index, or -1 if invalid
    """
    if len(letter) != 1 or not letter.isupper() or not letter.isalpha():
        return -1
    
    index = ord(letter) - ord('A')
    return index


def is_valid_move(board, col_index):
    """
    Check if a move to the given column is valid.
    
    Args:
        board: The 2D list representing the game board
        col_index: The 0-based column index
    
    Returns:
        True if the move is valid, False otherwise
    """
    cols = len(board[0])
    rows = len(board)
    
    # Check if column index is within bounds
    if col_index < 0 or col_index >= cols:
        return False
    
    # Check if the top cell of the column is empty
    if board[0][col_index] != " ":
        return False
    
    return True


def get_player_move(board, player_checker, num_cols):
    """
    Get a valid move from the player.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol for the current player
        num_cols: The number of columns on the board
    
    Returns:
        The 0-based column index where the player wants to place their checker
    """
    max_col_letter = chr(ord('A') + num_cols - 1)
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column ({chr(ord('A'))} - {max_col_letter}): ").strip().upper()
        
        col_index = column_letter_to_index(user_input)
        
        if col_index == -1:
            print("Invalid input. Please enter a single uppercase letter.")
            continue
        
        if not is_valid_move(board, col_index):
            print(f"Column {user_input} is either out of bounds or full. Please try again.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the given column (it falls to the lowest available row).
    
    Args:
        board: The 2D list representing the game board
        col_index: The 0-based column index
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1  # Should not happen if is_valid_move was checked


def check_win(board, row, col, checker):
    """
    Check if the player has won after placing a checker at (row, col).
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    def count_consecutive(dr, dc):
        """
        Count consecutive checkers in a given direction.
        
        Args:
            dr: Row direction (-1, 0, or 1)
            dc: Column direction (-1, 0, or 1)
        
        Returns:
            The count of consecutive checkers in that direction
        """
        count = 0
        r, c = row + dr, col + dc
        
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        return count
    
    # Check horizontal
    left = count_consecutive(0, -1)
    right = count_consecutive(0, 1)
    if left + right + 1 >= WIN_LENGTH:
        return True
    
    # Check vertical
    up = count_consecutive(-1, 0)
    down = count_consecutive(1, 0)
    if up + down + 1 >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    top_left = count_consecutive(-1, -1)
    bottom_right = count_consecutive(1, 1)
    if top_left + bottom_right + 1 >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    top_right = count_consecutive(-1, 1)
    bottom_left = count_consecutive(1, -1)
    if top_right + bottom_left + 1 >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Get player checkers
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid move from player
        col_index = get_player_move(board, current_player, BOARD_COLS)
        
        # Place checker
        row_index = place_checker(board, col_index, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
