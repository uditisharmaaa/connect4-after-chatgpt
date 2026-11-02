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
    Initialize the game board with empty spaces.
    
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
    Print the current state of the board.
    
    Args:
        board: The game board
    """
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
        
        # Print row separator
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()


def clear_screen():
    """Clear the game screen."""
    os.system('clear')


def is_valid_column(column_input, cols):
    """
    Validate if the column input is valid.
    
    Args:
        column_input: User input for column
        cols: Number of columns in the board
    
    Returns:
        Column index (0-based) if valid, -1 if invalid
    """
    if len(column_input) != 1:
        return -1
    
    if not column_input.isalpha():
        return -1
    
    column_input = column_input.upper()
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def can_place_checker(board, col):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The game board
        col: Column index (0-based)
    
    Returns:
        True if checker can be placed, False otherwise
    """
    rows = len(board)
    return board[0][col] == " "


def place_checker(board, col, checker):
    """
    Place a checker in the given column.
    
    Args:
        board: The game board
        col: Column index (0-based)
        checker: The checker symbol to place
    
    Returns:
        Row where the checker was placed, -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_winner(board, row, col, checker):
    """
    Check if the last placed checker at (row, col) results in a win.
    
    Args:
        board: The game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The checker symbol
    
    Returns:
        True if there is a winner, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal1, diagonal2
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        # If we have 4 or more in a row, it's a win
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board
    
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


def get_player_input(current_player, cols):
    """
    Get valid column input from the current player.
    
    Args:
        current_player: Current player number (0-based)
        cols: Number of columns in the board
    
    Returns:
        Valid column index (0-based)
    """
    checker = CHECKERS[current_player]
    
    while True:
        try:
            user_input = input(f"Player {checker}, please enter a column: ").strip()
            col_index = is_valid_column(user_input, cols)
            
            if col_index == -1:
                print("Invalid input. Please enter a valid column letter (A-G).")
                continue
            
            return col_index
        except Exception:
            print("Invalid input. Please try again.")


def play_game():
    """
    Main game loop.
    """
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    clear_screen()
    print_board(board)
    
    game_over = False
    winner = None
    
    # Main game loop
    while not game_over:
        # Get player input
        col = get_player_input(current_player, COLS)
        
        # Check if column is full
        if not can_place_checker(board, col):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        row = place_checker(board, col, CHECKERS[current_player])
        
        # Clear screen and print updated board
        clear_screen()
        print_board(board)
        
        # Check for winner
        if check_winner(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
            winner = current_player
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
