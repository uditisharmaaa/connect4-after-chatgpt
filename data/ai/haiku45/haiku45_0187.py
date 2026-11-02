import os
import random

# Constants
ROWS = 6
COLS = 7
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
        A 2D list representing the board with all spaces initialized to " "
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
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+---" * cols + "+")
        
        # Cell content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+---" * cols + "+")


def is_valid_column(column_input, cols):
    """
    Validate the column input.
    
    Args:
        column_input: The user's input string
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) if valid, -1 otherwise
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return -1
    
    # Check if input is a letter
    if not column_input.isalpha():
        return -1
    
    # Convert to uppercase
    column_input = column_input.upper()
    
    # Check if column is within board bounds
    col_index = ord(column_input) - ord('A')
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def can_place_checker(board, col):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The current game board
        col: Column index (0-based)
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    # Check if top row of column is empty
    return board[0][col] == " "


def place_checker(board, col, checker):
    """
    Place a checker in the given column.
    
    Args:
        board: The current game board
        col: Column index (0-based)
        checker: The checker symbol to place
    
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


def check_winner(board, row, col, checker):
    """
    Check if the last placed checker at (row, col) resulted in a win.
    
    Args:
        board: The current game board
        row: Row index of the last placed checker
        col: Column index of the last placed checker
        checker: The checker symbol that was placed
    
    Returns:
        True if there is a winner, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (top-left to bottom-right), diagonal (top-right to bottom-left)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dx, dy in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        x, y = row + dx, col + dy
        while 0 <= x < rows and 0 <= y < cols and board[x][y] == checker:
            count += 1
            x += dx
            y += dy
        
        # Check in negative direction
        x, y = row - dx, col - dy
        while 0 <= x < rows and 0 <= y < cols and board[x][y] == checker:
            count += 1
            x -= dx
            y -= dy
        
        # Check if we have 4 or more in a row
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_next_player(current_player, num_players):
    """
    Get the next player in turn.
    
    Args:
        current_player: Index of the current player (0-based)
        num_players: Total number of players
    
    Returns:
        Index of the next player (0-based)
    """
    return (current_player + 1) % num_players


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        while True:
            print(f"Player {checker}, please enter a column: ", end="")
            column_input = input().strip()
            
            # Validate column input
            col = is_valid_column(column_input, COLS)
            if col == -1:
                print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(ord('A') + COLS - 1)))
                continue
            
            # Check if column is not full
            if not can_place_checker(board, col):
                print("Column is full. Please choose another column.")
                continue
            
            # Valid input, break out of loop
            break
        
        # Place checker
        row = place_checker(board, col, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for winner
        if check_winner(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = get_next_player(current_player, NUM_PLAYERS)


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
