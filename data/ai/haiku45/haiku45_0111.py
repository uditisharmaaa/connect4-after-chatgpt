import os
import random

# Global constants
ROWS = 6
COLS = 7
WIN_LENGTH = 4
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows (int): Number of rows in the board
        cols (int): Number of columns in the board
    
    Returns:
        list: A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the current state of the board.
    
    Args:
        board (list): The game board
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print top border
    print(" +", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print(" |", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print row separator
        print(" +", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


def get_valid_column(board, players_checker):
    """
    Get a valid column input from the player.
    
    Args:
        board (list): The game board
        players_checker (str): The current player's checker symbol
    
    Returns:
        int: The column index (0-based)
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {players_checker}, please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Validate column is within board bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a column between A and {chr(65 + cols - 1)}.")
            continue
        
        # Validate column is not full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board (list): The game board
        col (int): The column index (0-based)
        checker (str): The checker symbol to place
    
    Returns:
        int: The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the player has won after placing a checker.
    
    Args:
        board (list): The game board
        row (int): The row index of the last placed checker
        col (int): The column index of the last placed checker
        checker (str): The checker symbol to check
    
    Returns:
        bool: True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 0
    for c in range(cols):
        if board[row][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(rows):
        if board[r][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find the starting point
    r, c = row, col
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    
    # Check the diagonal
    while r < rows and c < cols:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-right to bottom-left)
    count = 0
    # Find the starting point
    r, c = row, col
    while r > 0 and c < cols - 1:
        r -= 1
        c += 1
    
    # Check the diagonal
    while r < rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board (list): The game board
    
    Returns:
        bool: True if the board is full, False otherwise
    """
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
    current_player = random.randint(0, PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get the current player's checker
        checker = CHECKERS[current_player]
        
        # Get valid column input from player
        col = get_valid_column(board, checker)
        
        # Place the checker on the board
        row = place_checker(board, col, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check if the current player has won
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check if the board is full (draw)
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to the next player
        current_player = (current_player + 1) % PLAYERS


if __name__ == "__main__":
    play_game()
