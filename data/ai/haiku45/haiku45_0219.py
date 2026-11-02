import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Create and return a 2D board with all cells initialized to whitespace.
    
    Returns:
        list: A 2D list representing the game board
    """
    board = [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    return board


def print_board(board):
    """
    Print the Connect 4 board in a formatted manner.
    
    Args:
        board (list): The 2D game board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(BOARD_WIDTH):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print board rows with borders
    for row in board:
        print("+---" * BOARD_WIDTH + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * BOARD_WIDTH + "+")


def get_next_available_row(board, col):
    """
    Find the next available row in a given column (from bottom to top).
    
    Args:
        board (list): The 2D game board
        col (int): The column index
    
    Returns:
        int: The row index where the checker should be placed, or -1 if column is full
    """
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def is_valid_input(user_input, board):
    """
    Validate user input for column selection.
    
    Args:
        user_input (str): The user's input
        board (list): The 2D game board
    
    Returns:
        tuple: (is_valid, column_index) where is_valid is a boolean and column_index is int or None
    """
    # Check if input is a single character
    if len(user_input) != 1:
        return False, None
    
    # Check if it's a letter
    if not user_input.isalpha():
        return False, None
    
    # Convert to uppercase and get column index
    col = ord(user_input.upper()) - ord('A')
    
    # Check if column is within board bounds
    if col < 0 or col >= BOARD_WIDTH:
        return False, None
    
    # Check if column is not full
    if get_next_available_row(board, col) == -1:
        return False, None
    
    return True, col


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board (list): The 2D game board
        col (int): The column index
        checker (str): The player's checker symbol
    
    Returns:
        bool: True if placement was successful, False otherwise
    """
    row = get_next_available_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    return False


def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in a given direction.
    
    Args:
        board (list): The 2D game board
        row (int): Starting row index
        col (int): Starting column index
        checker (str): The player's checker symbol
        row_delta (int): Row direction (-1, 0, or 1)
        col_delta (int): Column direction (-1, 0, or 1)
    
    Returns:
        int: Count of consecutive checkers in the given direction
    """
    count = 0
    current_row = row
    current_col = col
    
    while (0 <= current_row < BOARD_HEIGHT and 
           0 <= current_col < BOARD_WIDTH and 
           board[current_row][current_col] == checker):
        count += 1
        current_row += row_delta
        current_col += col_delta
    
    return count


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board (list): The 2D game board
        row (int): Row index of the last placed checker
        col (int): Column index of the last placed checker
        checker (str): The player's checker symbol
    
    Returns:
        bool: True if the player won, False otherwise
    """
    # Check horizontally
    left_count = check_direction(board, row, col, checker, 0, -1) - 1
    right_count = check_direction(board, row, col, checker, 0, 1) - 1
    if left_count + right_count + 1 >= WIN_LENGTH:
        return True
    
    # Check vertically
    up_count = check_direction(board, row, col, checker, -1, 0) - 1
    down_count = check_direction(board, row, col, checker, 1, 0) - 1
    if up_count + down_count + 1 >= WIN_LENGTH:
        return True
    
    # Check diagonally (top-left to bottom-right)
    up_left_count = check_direction(board, row, col, checker, -1, -1) - 1
    down_right_count = check_direction(board, row, col, checker, 1, 1) - 1
    if up_left_count + down_right_count + 1 >= WIN_LENGTH:
        return True
    
    # Check diagonally (top-right to bottom-left)
    up_right_count = check_direction(board, row, col, checker, -1, 1) - 1
    down_left_count = check_direction(board, row, col, checker, 1, -1) - 1
    if up_right_count + down_left_count + 1 >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board (list): The 2D game board
    
    Returns:
        bool: True if the board is full, False otherwise
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
    # Initialize the board
    board = initialize_board()
    
    # Get player checkers
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Main game loop
    game_over = False
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid input from the player
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip()
            is_valid, col = is_valid_input(user_input, board)
            
            if is_valid:
                break
            else:
                print("Invalid input. Please enter a valid column letter.")
        
        # Find the row to place the checker and place it
        row = get_next_available_row(board, col)
        place_checker(board, col, current_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        # Move to the next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
