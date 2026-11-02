import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with all empty cells (whitespace).
    
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
    Print the board in a formatted manner with column labels and grid lines.
    
    Args:
        board: The game board (2D list)
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with grid lines
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_column(column_input, cols):
    """
    Validate if the column input is valid.
    
    Args:
        column_input: User input for column (should be a single uppercase letter)
        cols: Number of columns in the board
    
    Returns:
        Column index (0-based) if valid, -1 otherwise
    """
    if len(column_input) != 1:
        return -1
    
    if not column_input.isupper():
        return -1
    
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def is_column_full(board, col_index):
    """
    Check if a column is completely full.
    
    Args:
        board: The game board (2D list)
        col_index: Index of the column to check
    
    Returns:
        True if column is full, False otherwise
    """
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column. The checker falls to the lowest
    available position in that column.
    
    Args:
        board: The game board (2D list)
        col_index: Index of the column where checker should be placed
        checker: The checker symbol (character) to place
    
    Returns:
        Tuple (row_index, col_index) where checker was placed, or None if invalid
    """
    rows = len(board)
    
    if is_column_full(board, col_index):
        return None
    
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return (row, col_index)
    
    return None


def check_direction(board, row, col, dr, dc, checker, cols, rows):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The game board (2D list)
        row: Starting row index
        col: Starting column index
        dr: Row direction (-1, 0, or 1)
        dc: Column direction (-1, 0, or 1)
        checker: The checker symbol to check for
        cols: Number of columns in the board
        rows: Number of rows in the board
    
    Returns:
        Number of consecutive checkers in that direction
    """
    count = 0
    r, c = row, col
    
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    
    return count


def check_win(board, row, col, checker):
    """
    Check if the placement of a checker results in a win.
    
    Args:
        board: The game board (2D list)
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The checker symbol of the player
    
    Returns:
        True if the player wins, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal1, diagonal2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        # Count in both directions from the placed checker
        count_forward = check_direction(board, row, col, dr, dc, checker, cols, rows)
        count_backward = check_direction(board, row, col, -dr, -dc, checker, cols, rows)
        
        # Subtract 1 because the placed checker is counted twice
        total_count = count_forward + count_backward - 1
        
        if total_count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_move(board, player_checker, cols):
    """
    Get a valid move from the current player.
    
    Args:
        board: The game board (2D list)
        player_checker: The checker symbol for the current player
        cols: Number of columns in the board
    
    Returns:
        Column index where the checker should be placed
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        col_index = is_valid_column(user_input, cols)
        
        if col_index == -1:
            print("Invalid input. Please enter a single letter from A to {}.".format(chr(65 + cols - 1)))
            continue
        
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Get player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, BOARD_COLUMNS)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player_checker = player_checkers[current_player_index]
        
        # Get valid move from player
        col_index = get_player_move(board, current_player_checker, BOARD_COLUMNS)
        
        # Place checker
        placement = place_checker(board, col_index, current_player_checker)
        
        if placement is None:
            print("Error placing checker. Please try again.")
            continue
        
        row_index, _ = placement
        
        # Print updated board
        print_board(board, BOARD_COLUMNS)
        
        # Check for win
        if check_win(board, row_index, col_index, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        # Switch to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
