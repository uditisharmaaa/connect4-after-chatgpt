import os
import random

# Game constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers (in order)
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    """
    Initialize the game board with empty cells (whitespaces).
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Print the current state of the board.
    
    Args:
        board: The game board (2D list)
    """
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Cell content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()

def get_valid_column(board, num_players, current_player):
    """
    Get valid column input from the current player.
    
    Args:
        board: The game board (2D list)
        num_players: Total number of players
        current_player: Index of current player (0-based)
    
    Returns:
        Column index (0-based) where the checker will be placed
    """
    cols = len(board[0])
    
    while True:
        try:
            user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
            
            # Check if input is a single character
            if len(user_input) != 1:
                print(f"Invalid input. Please enter a single letter between A and {chr(ord('A') + cols - 1)}.")
                continue
            
            # Check if input is a letter
            if not user_input.isalpha():
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
                continue
            
            # Convert letter to column index
            col = ord(user_input) - ord('A')
            
            # Check if column is within bounds
            if col < 0 or col >= cols:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
                continue
            
            # Check if column is full
            if board[0][col] != ' ':
                print("That column is full. Please choose another column.")
                continue
            
            return col
        
        except Exception as e:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")

def place_checker(board, col, current_player):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col: Column index (0-based)
        current_player: Index of current player (0-based)
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = CHECKERS[current_player]
            return row
    
    return -1

def check_win(board, row, col, current_player):
    """
    Check if the current player has won after placing a checker.
    
    Args:
        board: The game board (2D list)
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        current_player: Index of current player (0-based)
    
    Returns:
        True if the current player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    checker = CHECKERS[current_player]
    
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the placed checker itself
        
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
        
        # Check if we have 4 or more in a row
        if count >= WIN_LENGTH:
            return True
    
    return False

def check_draw(board):
    """
    Check if the board is completely filled (draw condition).
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if the board is full, False otherwise
    """
    # Check if the top row is completely filled
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def main():
    """
    Main game loop for Connect 4.
    """
    # Clear screen
    os.system('clear')
    
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    winner = None
    
    while not game_over:
        # Get valid column from current player
        col = get_valid_column(board, NUM_PLAYERS, current_player)
        
        # Place the checker
        row = place_checker(board, col, current_player)
        
        # Clear screen and print updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
            winner = current_player
        
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        
        # Switch to next player
        if not game_over:
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
