import os
import random

# Game configuration constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
SYMBOLS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Create and initialize a board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Display the current state of the board with proper formatting.
    
    Args:
        board: The game board to display
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print row separator
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


def get_valid_column(board, num_players, current_player):
    """
    Prompt the current player for a valid column input.
    
    Args:
        board: The game board
        num_players: Number of players in the game
        current_player: The index of the current player
    
    Returns:
        The column index (0-based) where the checker will be placed
    """
    cols = len(board[0])
    symbol = SYMBOLS[current_player]
    
    while True:
        user_input = input(f"Player {symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= cols:
            print(f"Invalid column. Please enter a column between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, symbol):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The game board
        col: The column index (0-based)
        symbol: The symbol of the player's checker
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    
    return -1


def check_win(board, row, col, symbol):
    """
    Check if the last move resulted in a win (4 in a row).
    
    Args:
        board: The game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        symbol: The symbol of the player
    
    Returns:
        True if the player won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (top-left to bottom-right), diagonal (top-right to bottom-left)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        # Count checkers in both directions from the placed checker
        count = 1
        
        # Count in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        
        # Count in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        
        # Check if we have 4 or more in a row
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely filled (draw condition).
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for cell in board[0]:
        if cell == ' ':
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get valid input from current player
        col = get_valid_column(board, NUM_PLAYERS, current_player)
        
        # Place the checker
        symbol = SYMBOLS[current_player]
        row = place_checker(board, col, symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, symbol):
            print(f"Player {symbol} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
