import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the board to the console with proper formatting.
    
    Args:
        board: The current game board
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_input(col_input, cols):
    """
    Validate the player's input.
    
    Args:
        col_input: The input provided by the player
        cols: Number of columns in the board
    
    Returns:
        True if input is valid, False otherwise
    """
    if len(col_input) != 1:
        return False
    
    if not col_input.isalpha():
        return False
    
    col_index = ord(col_input.upper()) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def get_player_move(board, player_checker):
    """
    Get a valid move from the player.
    
    Args:
        board: The current game board
        player_checker: The checker symbol of the current player
    
    Returns:
        The column index where the player wants to place their checker
    """
    cols = len(board[0])
    
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        if not is_valid_input(col_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(col_input) - ord('A')
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        col: The column index
        player_checker: The checker symbol of the current player
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row
    
    return -1


def check_horizontal_win(board, row, col, player_checker):
    """
    Check if the player has won horizontally.
    
    Args:
        board: The current game board
        row: The row of the last placed checker
        col: The column of the last placed checker
        player_checker: The checker symbol of the current player
    
    Returns:
        True if player has won, False otherwise
    """
    cols = len(board[0])
    count = 0
    
    # Check left and right from the placed position
    for c in range(cols):
        if board[row][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_vertical_win(board, row, col, player_checker):
    """
    Check if the player has won vertically.
    
    Args:
        board: The current game board
        row: The row of the last placed checker
        col: The column of the last placed checker
        player_checker: The checker symbol of the current player
    
    Returns:
        True if player has won, False otherwise
    """
    rows = len(board)
    count = 0
    
    # Check up and down from the placed position
    for r in range(rows):
        if board[r][col] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    return False


def check_diagonal_win(board, row, col, player_checker):
    """
    Check if the player has won diagonally.
    
    Args:
        board: The current game board
        row: The row of the last placed checker
        col: The column of the last placed checker
        player_checker: The checker symbol of the current player
    
    Returns:
        True if player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal from top-left to bottom-right
    count = 0
    r, c = row, col
    
    # Move to the start of the diagonal
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    
    # Check the diagonal
    while r < rows and c < cols:
        if board[r][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal from top-right to bottom-left
    count = 0
    r, c = row, col
    
    # Move to the start of the diagonal
    while r > 0 and c < cols - 1:
        r -= 1
        c += 1
    
    # Check the diagonal
    while r < rows and c >= 0:
        if board[r][c] == player_checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    
    return False


def check_win(board, row, col, player_checker):
    """
    Check if the player has won.
    
    Args:
        board: The current game board
        row: The row of the last placed checker
        col: The column of the last placed checker
        player_checker: The checker symbol of the current player
    
    Returns:
        True if player has won, False otherwise
    """
    return (check_horizontal_win(board, row, col, player_checker) or
            check_vertical_win(board, row, col, player_checker) or
            check_diagonal_win(board, row, col, player_checker))


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The current game board
    
    Returns:
        True if board is full, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player_checker = player_checkers[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_player_checker)
        
        # Place checker
        row = place_checker(board, col, current_player_checker)
        
        # Print the board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
