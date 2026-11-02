import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with all empty spaces.
    
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
        board: The current game board
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print each row with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def get_valid_column(board, num_players, current_player):
    """
    Get a valid column input from the current player.
    
    Args:
        board: The current game board
        num_players: Total number of players
        current_player: Index of the current player (0-indexed)
    
    Returns:
        Column index (0-indexed) where the checker should be placed
    """
    cols = len(board[0])
    checker = CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, current_player):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        col: Column index (0-indexed)
        current_player: Index of the current player (0-indexed)
    
    Returns:
        Row index where the checker was placed, or -1 if column is full
    """
    rows = len(board)
    checker = CHECKERS[current_player]
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_winner(board, row, col, current_player):
    """
    Check if the current player has won after placing a checker.
    
    Args:
        board: The current game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        current_player: Index of the current player (0-indexed)
    
    Returns:
        True if the current player has won, False otherwise
    """
    checker = CHECKERS[current_player]
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (\), diagonal (/)
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
        
        # If we have 4 or more in a row, the player wins
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for cell in board[0]:
        if cell == " ":
            return False
    return True


def get_next_player(current_player, num_players):
    """
    Get the index of the next player.
    
    Args:
        current_player: Index of the current player (0-indexed)
        num_players: Total number of players
    
    Returns:
        Index of the next player (0-indexed)
    """
    return (current_player + 1) % num_players


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get valid column from current player
        col = get_valid_column(board, NUM_PLAYERS, current_player)
        
        # Place the checker
        row = place_checker(board, col, current_player)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_winner(board, row, col, current_player):
            checker = CHECKERS[current_player]
            print(f"Player {checker} won!")
            game_over = True
        
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        else:
            # Move to the next player
            current_player = get_next_player(current_player, NUM_PLAYERS)


if __name__ == "__main__":
    play_game()
