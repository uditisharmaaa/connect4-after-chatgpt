import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
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
        board: The game board to print
    """
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+---" * cols + "+")
        
        # Row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} ", end="|")
        print()
    
    # Bottom border
    print("+---" * cols + "+")


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def get_valid_column(board, players, current_player):
    """
    Get a valid column input from the current player.
    
    Args:
        board: The game board
        players: List of player checkers
        current_player: Index of the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {players[current_player]}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col: The column index (0-based)
        checker: The checker to place
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the last placed checker creates a winning condition.
    
    Args:
        board: The game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker that was placed
    
    Returns:
        True if the player wins, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (\), diagonal (/)
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
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (game is a draw).
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def play_game():
    """Main game loop."""
    clear_screen()
    
    # Initialize board
    board = initialize_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_won = False
    
    while not game_won:
        # Get valid column input
        col = get_valid_column(board, players, current_player)
        
        # Place checker
        row = place_checker(board, col, players[current_player])
        
        # Clear screen and print updated board
        clear_screen()
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, players[current_player]):
            print(f"Player {players[current_player]} won!")
            game_won = True
        # Check for draw
        elif check_draw(board):
            print("Game is a draw!")
            game_won = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
