import os
import random

# Constants for board configuration
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, columns):
    """
    Initialize a two-dimensional board with all cells set to whitespace.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list (board) with all cells initialized to whitespace
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Print the board with proper formatting including column labels and borders.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    rows = len(board)
    columns = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(columns):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * columns + "+")
    
    # Print each row with borders
    for row in range(rows):
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * columns + "+")

def get_column_input(board, current_player_checker):
    """
    Get valid column input from the current player.
    
    Args:
        board: The 2D list representing the game board
        current_player_checker: The checker symbol of the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    columns = len(board[0])
    
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= columns:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + columns - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The 2D list representing the game board
        col_index: The column index (0-based) where the checker will be placed
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1

def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The 2D list representing the game board
        row: The starting row index
        col: The starting column index
        checker: The checker symbol to check for
        row_delta: The row direction (-1, 0, or 1)
        col_delta: The column direction (-1, 0, or 1)
    
    Returns:
        True if 4 checkers are found in the given direction, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    count = 1  # Count the current checker
    
    # Check in positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH

def check_win(board, row, col, checker):
    """
    Check if the current player has won by placing a checker at the given position.
    
    Args:
        board: The 2D list representing the game board
        row: The row index where the checker was just placed
        col: The column index where the checker was just placed
        checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, checker, 1, -1):
        return True
    
    return False

def check_draw(board):
    """
    Check if the board is completely filled (draw condition).
    
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
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player_checker = CHECKERS[current_player_index]
        
        # Get valid input from the current player
        col_index = get_column_input(board, current_player_checker)
        
        # Place the checker
        row_index = place_checker(board, col_index, current_player_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, row_index, col_index, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """
    Entry point of the program.
    """
    play_game()

if __name__ == "__main__":
    main()
