import os
import random

# Game Configuration Constants
ROWS = 6
COLS = 7
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
MAX_PLAYERS = 5

def initialize_board(rows, cols):
    """
    Initialize the game board with all cells containing whitespace.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board, cols):
    """
    Print the game board in a formatted manner with column headers and grid lines.
    
    Args:
        board: The 2D list representing the game board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row with borders
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        
        # Print row separator
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()

def is_valid_move(board, col, cols):
    """
    Check if a move is valid (column exists and is not completely filled).
    
    Args:
        board: The 2D list representing the game board
        col: Column index (0-based)
        cols: Total number of columns
    
    Returns:
        True if the move is valid, False otherwise
    """
    if col < 0 or col >= cols:
        return False
    # Check if the top cell of the column is empty
    if board[0][col] != " ":
        return False
    return True

def get_player_move(board, cols, current_player):
    """
    Get and validate the player's move input.
    
    Args:
        board: The 2D list representing the game board
        cols: Total number of columns
        current_player: The current player's checker symbol
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if not is_valid_move(board, col, cols):
            print("This column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, checker, rows):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The 2D list representing the game board
        col: Column index (0-based)
        checker: The player's checker symbol
        rows: Total number of rows
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    # Start from the bottom row and move up to find the lowest empty cell
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker, rows, cols):
    """
    Check if the current player has won after placing a checker at (row, col).
    Checks horizontally, vertically, and diagonally for 4 in a row.
    
    Args:
        board: The 2D list representing the game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The player's checker symbol
        rows: Total number of rows
        cols: Total number of columns
    
    Returns:
        True if the player has won, False otherwise
    """
    def count_in_direction(dr, dc):
        """
        Count consecutive checkers in a given direction from the placed checker.
        
        Args:
            dr: Row direction (-1, 0, or 1)
            dc: Column direction (-1, 0, or 1)
        
        Returns:
            Count of consecutive checkers in the given direction
        """
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count
    
    # Check horizontal
    left = count_in_direction(0, -1)
    right = count_in_direction(0, 1)
    if left + right + 1 >= WIN_LENGTH:
        return True
    
    # Check vertical
    up = count_in_direction(-1, 0)
    down = count_in_direction(1, 0)
    if up + down + 1 >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    top_left = count_in_direction(-1, -1)
    bottom_right = count_in_direction(1, 1)
    if top_left + bottom_right + 1 >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    top_right = count_in_direction(-1, 1)
    bottom_left = count_in_direction(1, -1)
    if top_right + bottom_left + 1 >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board, rows, cols):
    """
    Check if the board is completely filled (draw condition).
    
    Args:
        board: The 2D list representing the game board
        rows: Total number of rows
        cols: Total number of columns
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True

def play_game(rows, cols, num_players):
    """
    Main game loop for playing Connect 4.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
        num_players: Number of players in the game
    """
    # Initialize the board
    board = initialize_board(rows, cols)
    
    # Select checkers for each player
    player_checkers = CHECKERS[:num_players]
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, cols)
    
    # Main game loop
    game_over = False
    while not game_over:
        current_player = player_checkers[current_player_index]
        
        # Get player move
        col = get_player_move(board, cols, current_player)
        
        # Place the checker
        row = place_checker(board, col, current_player, rows)
        
        # Print updated board
        print_board(board, cols)
        
        # Check for win
        if check_win(board, row, col, current_player, rows, cols):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board, rows, cols):
            print("It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player_index = (current_player_index + 1) % num_players

def main():
    """
    Main function to start the Connect 4 game.
    """
    play_game(ROWS, COLS, 2)

if __name__ == "__main__":
    main()
