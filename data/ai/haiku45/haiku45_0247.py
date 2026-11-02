import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with all cells containing whitespace.
    
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
    Print the board in a formatted manner with column labels and borders.
    
    Args:
        board: 2D list representing the board
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def get_valid_column(board):
    """
    Get a valid column input from the player.
    
    Args:
        board: 2D list representing the board
    
    Returns:
        Valid column index (0-based)
    """
    cols = len(board[0])
    
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
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
        
        # Validate column is within board
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        # Validate column is not full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: 2D list representing the board
        col: Column index (0-based)
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if unsuccessful
    """
    rows = len(board)
    
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the placed checker results in a win.
    
    Args:
        board: 2D list representing the board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if the player won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal /, diagonal \
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]
    
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
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: 2D list representing the board
    
    Returns:
        True if the board is full, False otherwise
    """
    # Check if the top row is completely filled
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get checker symbols for the players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {player_checkers[current_player_index]} starts the game!\n")
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_checker = player_checkers[current_player_index]
        print(f"Player {current_checker}, ", end="")
        
        # Get valid column from player
        col = get_valid_column(board)
        
        # Place the checker
        row = place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        # Switch to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Main entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
