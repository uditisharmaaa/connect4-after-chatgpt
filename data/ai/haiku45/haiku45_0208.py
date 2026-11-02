import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with empty spaces.
    
    Returns:
        list: A 2D list representing the Connect 4 board.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board to the console.
    
    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(COLS):
        print("---+", end="")
    print()
    
    # Print rows with content
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        
        # Print row separator
        print("+", end="")
        for _ in range(COLS):
            print("---+", end="")
        print()


def is_valid_column(column_input, board):
    """
    Validate if the column input is valid and the column is not full.
    
    Args:
        column_input (str): The column letter entered by the player.
        board (list): The 2D list representing the game board.
    
    Returns:
        tuple: (is_valid, col_index) where is_valid is a boolean and col_index is the column number.
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return False, -1
    
    # Check if input is uppercase letter
    if not column_input.isupper() or not column_input.isalpha():
        return False, -1
    
    # Convert letter to column index
    col_index = ord(column_input) - 65
    
    # Check if column index is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False, -1
    
    # Check if column is not full
    if board[0][col_index] != " ":
        return False, -1
    
    return True, col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column, falling to the lowest available row.
    
    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The column index where the checker is placed.
        checker (str): The checker symbol (X, O, V, H, or M).
    
    Returns:
        int: The row index where the checker was placed, or -1 if placement fails.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1


def check_horizontal_win(board, row, col, checker):
    """
    Check if there is a horizontal win at the given position.
    
    Args:
        board (list): The 2D list representing the game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol to check for.
    
    Returns:
        bool: True if there is a win, False otherwise.
    """
    count = 1
    
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """
    Check if there is a vertical win at the given position.
    
    Args:
        board (list): The 2D list representing the game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol to check for.
    
    Returns:
        bool: True if there is a win, False otherwise.
    """
    count = 1
    
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, checker):
    """
    Check if there is a diagonal win (both directions) at the given position.
    
    Args:
        board (list): The 2D list representing the game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol to check for.
    
    Returns:
        bool: True if there is a win, False otherwise.
    """
    # Check diagonal from top-left to bottom-right
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 1
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board (list): The 2D list representing the game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol to check for.
    
    Returns:
        bool: True if there is a win, False otherwise.
    """
    return (check_horizontal_win(board, row, col, checker) or
            check_vertical_win(board, row, col, checker) or
            check_diagonal_win(board, row, col, checker))


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board (list): The 2D list representing the game board.
    
    Returns:
        bool: True if the board is full, False otherwise.
    """
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def get_player_move(board, player_checker):
    """
    Get a valid move from the current player.
    
    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
    
    Returns:
        int: The column index where the player wants to place their checker.
    """
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        is_valid, col_index = is_valid_column(column_input, board)
        
        if is_valid:
            return col_index
        else:
            print("Invalid input. Please enter a valid column letter (A-G) that is not full.")


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Choose a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get the current player's checker
        player_checker = CHECKERS[current_player]
        
        # Get the player's move
        col_index = get_player_move(board, player_checker)
        
        # Place the checker on the board
        row_index = place_checker(board, col_index, player_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row_index, col_index, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Move to the next player
        else:
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
