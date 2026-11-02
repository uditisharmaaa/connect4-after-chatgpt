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
        A 2D list representing the board filled with spaces
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the current state of the board with proper formatting.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(ord('A') + col)}   ", end="")
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

def is_valid_move(board, col):
    """
    Check if a move to a specific column is valid (column not full).
    
    Args:
        board: The 2D list representing the game board
        col: The column index (0-based)
    
    Returns:
        True if the column is not full, False otherwise
    """
    return board[0][col] == " "

def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    
    Args:
        board: The 2D list representing the game board
        col: The column index (0-based)
        checker: The checker symbol to place
    
    Returns:
        The row where the checker was placed, or -1 if placement failed
    """
    # Start from bottom and find the first empty space
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def get_valid_column_input(board, num_players, current_player):
    """
    Get and validate user input for column selection.
    Keeps asking until valid input is provided.
    
    Args:
        board: The 2D list representing the game board
        num_players: The number of players in the game
        current_player: The index of the current player
    
    Returns:
        The column index (0-based) of the player's move
    """
    cols = len(board[0])
    checker = CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col < 0 or col >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col):
            print("This column is full. Please choose another column.")
            continue
        
        return col

def check_win(board, row, col, checker):
    """
    Check if the last placed checker results in a win.
    Checks horizontally, vertically, and diagonally.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if the checker placement results in a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    for c in range(col - 1, -1, -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    # Check right
    for c in range(col + 1, cols):
        if board[row][c] == checker:
            count += 1
        else:
            break
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    for r in range(row - 1, -1, -1):
        if board[r][col] == checker:
            count += 1
        else:
            break
    # Check down
    for r in range(row + 1, rows):
        if board[r][col] == checker:
            count += 1
        else:
            break
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c -= 1
        else:
            break
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
            r += 1
            c += 1
        else:
            break
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols:
        if board[r][c] == checker:
            count += 1
            r -= 1
            c += 1
        else:
            break
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            r += 1
            c -= 1
        else:
            break
    if count >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
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
    Main game loop. Handles initialization, game flow, and win/draw conditions.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Print initial board
    print_board(board)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get valid column input from current player
        col = get_valid_column_input(board, NUM_PLAYERS, current_player)
        
        # Place the checker
        checker = CHECKERS[current_player]
        row = place_checker(board, col, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        # Switch to next player
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

def main():
    """
    Entry point of the program.
    """
    play_game()

if __name__ == "__main__":
    main()
