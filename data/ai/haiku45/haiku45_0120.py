import os
import random

# Configuration constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board filled with spaces
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the board in a formatted manner with column labels.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(65 + i)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for i in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print row border
        print("+", end="")
        for i in range(cols):
            print("---+", end="")
        print()


def is_valid_input(column_input, cols):
    """
    Validate if the input is a valid column choice.
    
    Args:
        column_input: The user input string
        cols: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_input) != 1:
        return False
    
    if not column_input.isupper():
        return False
    
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def can_place_checker(board, col_index):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The 2D list representing the game board
        col_index: The index of the column (0-based)
    
    Returns:
        True if a checker can be placed, False if column is full
    """
    return board[0][col_index] == " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the game board
        col_index: The index of the column (0-based)
        checker: The checker character to place
    
    Returns:
        The row index where the checker was placed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the placed checker results in a win.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the placed checker
        col: The column index of the placed checker
        checker: The checker character to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    
    # Check right
    j = col + 1
    while j < cols and board[row][j] == checker:
        count += 1
        j += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    
    # Check down
    i = row + 1
    while i < rows and board[i][col] == checker:
        count += 1
        i += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    
    # Check down-right
    i, j = row + 1, col + 1
    while i < rows and j < cols and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    
    # Check down-left
    i, j = row + 1, col - 1
    while i < rows and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_move(board, current_player_index):
    """
    Get a valid move from the current player.
    
    Args:
        board: The 2D list representing the game board
        current_player_index: The index of the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    cols = len(board[0])
    checker = CHECKERS[current_player_index]
    
    while True:
        column_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Validate input format
        if not is_valid_input(column_input, cols):
            print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(65 + cols - 1)))
            continue
        
        col_index = ord(column_input) - ord('A')
        
        # Check if column is full
        if not can_place_checker(board, col_index):
            print("That column is full. Please choose another column.")
            continue
        
        return col_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    game_over = False
    winner = None
    
    while not game_over:
        # Get player move
        checker = CHECKERS[current_player_index]
        col_index = get_player_move(board, current_player_index)
        
        # Place checker on board
        row_index = place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, checker):
            print(f"Player {checker} won!")
            game_over = True
            winner = checker
        
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
