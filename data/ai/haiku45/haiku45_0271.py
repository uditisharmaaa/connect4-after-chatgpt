import os
import random

# Constants for board dimensions and players
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the current state of the board in a formatted manner.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with borders
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


def get_next_available_row(board, col):
    """
    Find the next available row in a given column (lowest empty space).
    
    Args:
        board: The 2D list representing the game board
        col: The column index
    
    Returns:
        The row index where the checker should be placed, or -1 if column is full
    """
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def is_valid_input(user_input, board):
    """
    Validate user input for column selection.
    
    Args:
        user_input: The user's input string
        board: The 2D list representing the game board
    
    Returns:
        True if input is valid, False otherwise
    """
    cols = len(board[0])
    
    # Check if input is a single character
    if len(user_input) != 1:
        return False
    
    # Check if it's a letter
    if not user_input.isalpha():
        return False
    
    # Convert to uppercase and check if it's within valid range
    col_index = ord(user_input.upper()) - ord('A')
    if col_index < 0 or col_index >= cols:
        return False
    
    # Check if column is not full
    if get_next_available_row(board, col_index) == -1:
        return False
    
    return True


def get_player_move(board, player_checker):
    """
    Get a valid move from the current player.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol of the current player
    
    Returns:
        The column index where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        if is_valid_input(user_input, board):
            col_index = ord(user_input) - ord('A')
            return col_index
        else:
            print("Invalid input. Please enter a valid column letter.")


def place_checker(board, col, player_checker):
    """
    Place a checker on the board in the specified column.
    
    Args:
        board: The 2D list representing the game board
        col: The column index
        player_checker: The checker symbol to place
    
    Returns:
        True if placement was successful, False otherwise
    """
    row = get_next_available_row(board, col)
    if row != -1:
        board[row][col] = player_checker
        return True
    return False


def check_direction(board, row, col, player_checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The 2D list representing the game board
        row: The starting row
        col: The starting column
        player_checker: The checker symbol to check for
        row_delta: The change in row per step
        col_delta: The change in column per step
    
    Returns:
        True if 4 checkers in a row are found, False otherwise
    """
    count = 0
    rows = len(board)
    cols = len(board[0])
    
    for i in range(-WIN_LENGTH + 1, WIN_LENGTH):
        new_row = row + i * row_delta
        new_col = col + i * col_delta
        
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if board[new_row][new_col] == player_checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0
        else:
            count = 0
    
    return False


def check_win(board, row, col, player_checker):
    """
    Check if the current player has won the game.
    
    Args:
        board: The 2D list representing the game board
        row: The row where the last checker was placed
        col: The column where the last checker was placed
        player_checker: The checker symbol of the current player
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    if check_direction(board, row, col, player_checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, player_checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, player_checker, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, player_checker, 1, -1):
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


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_player_checker)
        
        # Place checker
        row = get_next_available_row(board, col)
        place_checker(board, col, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
