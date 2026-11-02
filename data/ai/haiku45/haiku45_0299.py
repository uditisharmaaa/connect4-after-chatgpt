import os
import random

# Configuration constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, columns):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows (int): Number of rows in the board
        columns (int): Number of columns in the board
    
    Returns:
        list: A 2D list representing the game board
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board, columns):
    """
    Print the game board with column labels and formatting.
    
    Args:
        board (list): The 2D game board
        columns (int): Number of columns in the board
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(columns):
        print(f"{chr(65 + i)}   ", end="")
    print()
    
    # Print board with borders
    for row in board:
        # Top border
        print("+---" * columns + "+")
        # Row content
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Bottom border
    print("+---" * columns + "+")


def is_valid_column(column_input, columns):
    """
    Validate if the column input is valid.
    
    Args:
        column_input (str): The user input for column
        columns (int): Number of columns in the board
    
    Returns:
        tuple: (is_valid, column_index) where is_valid is bool and column_index is int or None
    """
    if len(column_input) != 1:
        return False, None
    
    if not column_input.isalpha():
        return False, None
    
    column_index = ord(column_input.upper()) - 65
    
    if column_index < 0 or column_index >= columns:
        return False, None
    
    return True, column_index


def can_place_checker(board, column, rows):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board (list): The 2D game board
        column (int): The column index
        rows (int): Number of rows in the board
    
    Returns:
        bool: True if checker can be placed, False otherwise
    """
    return board[0][column] == " "


def place_checker(board, column, checker, rows):
    """
    Place a checker in the given column at the lowest available position.
    
    Args:
        board (list): The 2D game board
        column (int): The column index
        checker (str): The checker symbol to place
        rows (int): Number of rows in the board
    
    Returns:
        int: The row index where the checker was placed
    """
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row
    
    return -1


def check_direction(board, row, col, checker, rows, columns, delta_row, delta_col):
    """
    Check if there are 4 consecutive checkers in a given direction.
    
    Args:
        board (list): The 2D game board
        row (int): Starting row index
        col (int): Starting column index
        checker (str): The checker symbol to look for
        rows (int): Number of rows in the board
        columns (int): Number of columns in the board
        delta_row (int): Direction offset for rows
        delta_col (int): Direction offset for columns
    
    Returns:
        bool: True if 4 consecutive checkers found in this direction
    """
    count = 1  # Count the current checker
    
    # Check in positive direction
    r, c = row + delta_row, col + delta_col
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    
    # Check in negative direction
    r, c = row - delta_row, col - delta_col
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
        count += 1
        r -= delta_row
        c -= delta_col
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker, rows, columns):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board (list): The 2D game board
        row (int): Row index of the last placed checker
        col (int): Column index of the last placed checker
        checker (str): The checker symbol that was placed
        rows (int): Number of rows in the board
        columns (int): Number of columns in the board
    
    Returns:
        bool: True if the player won, False otherwise
    """
    # Check horizontal
    if check_direction(board, row, col, checker, rows, columns, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, rows, columns, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, rows, columns, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, checker, rows, columns, 1, -1):
        return True
    
    return False


def is_board_full(board, rows, columns):
    """
    Check if the board is completely full.
    
    Args:
        board (list): The 2D game board
        rows (int): Number of rows in the board
        columns (int): Number of columns in the board
    
    Returns:
        bool: True if board is full, False otherwise
    """
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == " ":
                return False
    return True


def get_player_move(board, current_player, num_players, columns, rows):
    """
    Get valid move input from the current player.
    
    Args:
        board (list): The 2D game board
        current_player (int): Index of the current player
        num_players (int): Total number of players
        columns (int): Number of columns in the board
        rows (int): Number of rows in the board
    
    Returns:
        int: The column index where the checker will be placed
    """
    checker = CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ")
        
        is_valid, column_index = is_valid_column(user_input, columns)
        
        if not is_valid:
            print("Invalid input. Please enter a single letter between A and " + 
                  chr(65 + columns - 1) + ".")
            continue
        
        if not can_place_checker(board, column_index, rows):
            print("This column is full. Please choose another column.")
            continue
        
        return column_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    
    game_over = False
    winner = None
    
    # Main game loop
    while not game_over:
        # Get player's move
        column = get_player_move(board, current_player, NUM_PLAYERS, COLUMNS, ROWS)
        
        # Place checker on the board
        row = place_checker(board, column, CHECKERS[current_player], ROWS)
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, row, column, CHECKERS[current_player], ROWS, COLUMNS):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
            winner = current_player
        
        # Check for draw
        elif is_board_full(board, ROWS, COLUMNS):
            print("It's a draw!")
            game_over = True
        
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
