import os
import random

# Global constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WINNING_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The game board (2D list)
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(ord('A') + i)} ", end=" ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * cols + "+")


def get_valid_column(board, num_cols):
    """
    Get a valid column input from the player.
    
    Args:
        board: The game board (2D list)
        num_cols: Number of columns in the board
    
    Returns:
        Column index (0-based) that is valid and not full
    """
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
        
        # Validate column is within board bounds
        if col_index < 0 or col_index >= num_cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available position.
    
    Args:
        board: The game board (2D list)
        col: Column index (0-based)
        checker: The checker character to place
    
    Returns:
        Tuple (row, col) where the checker was placed, or None if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return (row, col)
    
    return None


def check_win(board, row, col, checker, winning_length):
    """
    Check if the last placed checker creates a winning condition.
    Checks horizontal, vertical, and both diagonal directions.
    
    Args:
        board: The game board (2D list)
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The checker character to check for
        winning_length: Number of checkers in a row needed to win
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (down-right)
        (1, -1)   # Diagonal (down-left)
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Count in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Count in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= winning_length:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the game board is completely full (draw condition).
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_checker(player_index):
    """
    Get the checker character for a given player.
    
    Args:
        player_index: Index of the player (0-based)
    
    Returns:
        Checker character for the player
    """
    return CHECKERS[player_index]


def play_game(board_rows, board_cols, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        board_rows: Number of rows in the board
        board_cols: Number of columns in the board
        num_players: Number of players in the game
    """
    # Validate number of players
    if num_players < 2 or num_players > 5:
        print("Invalid number of players. Must be between 2 and 5.")
        return
    
    # Validate board dimensions
    if board_cols > 26:
        print("Invalid number of columns. Maximum is 26.")
        return
    
    # Initialize the board
    board = initialize_board(board_rows, board_cols)
    
    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {get_player_checker(current_player)} starts first!")
    input("Press Enter to continue...")
    
    # Game loop
    game_over = False
    winner = None
    
    while not game_over:
        print_board(board)
        
        # Get valid input from current player
        checker = get_player_checker(current_player)
        print(f"Player {checker}, please enter a column: ", end="")
        col = get_valid_column(board, board_cols)
        
        # Place the checker
        placement = place_checker(board, col, checker)
        
        if placement is None:
            print("Error placing checker.")
            continue
        
        row, col = placement
        
        # Check for win
        if check_win(board, row, col, checker, WINNING_LENGTH):
            game_over = True
            winner = checker
        # Check for draw
        elif is_board_full(board):
            game_over = True
            winner = None
        
        # Switch to next player
        current_player = (current_player + 1) % num_players
    
    # Print final board
    print_board(board)
    
    # Print game result
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


def main():
    """
    Main entry point for the Connect 4 game.
    """
    play_game(BOARD_ROWS, BOARD_COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
