import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with all empty spaces.
    
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
    Print the game board in a formatted way.
    
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
    
    # Print board with separators
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


def get_valid_column(board, cols):
    """
    Get a valid column input from the player.
    
    Args:
        board: The 2D list representing the game board
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) where the checker should be placed
    """
    while True:
        user_input = input("Enter a column (A-{}): ".format(chr(65 + cols - 1))).upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a column between A and {chr(65 + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the game board
        col: The column index (0-based) where the checker should be placed
        checker: The checker symbol to place
    
    Returns:
        The row index (0-based) where the checker was placed, or -1 if the column is full
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_win(board, row, col, checker, win_length):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
        win_length: The number of checkers in a row needed to win
    
    Returns:
        True if the player won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontally
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < cols and board[row][c] == checker:
        count += 1
        c += 1
    if count >= win_length:
        return True
    
    # Check vertically
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < rows and board[r][col] == checker:
        count += 1
        r += 1
    if count >= win_length:
        return True
    
    # Check diagonally (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= win_length:
        return True
    
    # Check diagonally (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= win_length:
        return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
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
    board = initialize_board(ROWS, COLS)
    
    # Create list of players and their checkers
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {players[current_player_index]} starts first!")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        # Print board
        print_board(board)
        
        # Get valid column from current player
        current_checker = players[current_player_index]
        print(f"\nPlayer {current_checker}, please enter a column:")
        col = get_valid_column(board, COLS)
        
        # Place checker
        row = place_checker(board, col, current_checker)
        
        # Check for win
        if check_win(board, row, col, current_checker, WIN_LENGTH):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
