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
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the board to the console.
    
    Args:
        board: 2D list representing the game board
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print rows
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

def get_valid_column(board, player_checker):
    """
    Get a valid column input from the player.
    
    Args:
        board: 2D list representing the game board
        player_checker: The checker symbol for the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: 2D list representing the game board
        col: Column index (0-based) where the checker should be placed
        player_checker: The checker symbol for the current player
    
    Returns:
        The row index (0-based) where the checker was placed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row
    
    return -1  # Should not reach here if validation is done correctly

def check_win(board, row, col, player_checker):
    """
    Check if the player has won after placing a checker at (row, col).
    
    Args:
        board: 2D list representing the game board
        row: Row index (0-based) of the last placed checker
        col: Column index (0-based) of the last placed checker
        player_checker: The checker symbol for the current player
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (/), diagonal (\)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dx, dy in directions:
        count = 1  # Count the checker we just placed
        
        # Check in positive direction
        x, y = row + dx, col + dy
        while 0 <= x < rows and 0 <= y < cols and board[x][y] == player_checker:
            count += 1
            x += dx
            y += dy
        
        # Check in negative direction
        x, y = row - dx, col - dy
        while 0 <= x < rows and 0 <= y < cols and board[x][y] == player_checker:
            count += 1
            x -= dx
            y -= dy
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def check_draw(board):
    """
    Check if the game is a draw (board is full with no winner).
    
    Args:
        board: 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    # Check if the top row is completely filled
    return all(cell != " " for cell in board[0])

def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Create list of player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_checker = player_checkers[current_player_index]
        
        # Get valid column from player
        col = get_valid_column(board, current_checker)
        
        # Place checker on the board
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
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()

if __name__ == "__main__":
    main()
