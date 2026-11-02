import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


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
    Print the current state of the game board.
    
    Args:
        board: The current game board (2D list)
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()
    
    # Print board with borders
    for row_idx in range(rows):
        # Print top border
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col_idx in range(cols):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()


def get_valid_input(board, num_players, current_player):
    """
    Get and validate user input for column selection.
    
    Args:
        board: The current game board
        num_players: Total number of players in the game
        current_player: Current player number (0-indexed)
    
    Returns:
        The column index (0-indexed) where the checker will be placed
    """
    cols = len(board[0])
    checker = CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_idx = ord(user_input) - ord('A')
        
        # Check if column is within board bounds
        if col_idx < 0 or col_idx >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col_idx] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_idx


def place_checker(board, col_idx, current_player):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        col_idx: The column index where to place the checker
        current_player: Current player number (0-indexed)
    
    Returns:
        The row index where the checker was placed
    """
    checker = CHECKERS[current_player]
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row_idx in range(rows - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx
    
    return -1  # Should not reach here if input is validated


def check_win(board, row, col, current_player):
    """
    Check if the current player has won after placing a checker.
    
    Args:
        board: The current game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        current_player: Current player number (0-indexed)
    
    Returns:
        True if the player has won, False otherwise
    """
    checker = CHECKERS[current_player]
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal down-right, diagonal down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
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


def check_draw(board):
    """
    Check if the game is a draw (board is full with no winner).
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    # Check if top row is full
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Choose a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get valid input from current player
        col_idx = get_valid_input(board, NUM_PLAYERS, current_player)
        
        # Place the checker
        row_idx = place_checker(board, col_idx, current_player)
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_idx, col_idx, current_player):
            checker = CHECKERS[current_player]
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
