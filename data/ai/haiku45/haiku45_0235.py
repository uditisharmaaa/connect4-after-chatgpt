import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, columns):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    
    columns = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with separators
    for row in range(rows):
        # Print top separator
        print("+---" * columns + "+")
        
        # Print row content
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom separator
    print("+---" * columns + "+")


def is_valid_column(column_input, columns):
    """
    Validate if the column input is valid.
    
    Args:
        column_input: User input for column selection
        columns: Number of columns in the board
    
    Returns:
        Tuple (is_valid, column_index) where is_valid is boolean and column_index is int
    """
    if len(column_input) != 1:
        return False, -1
    
    if not column_input.isalpha():
        return False, -1
    
    column_input = column_input.upper()
    column_index = ord(column_input) - ord('A')
    
    if column_index < 0 or column_index >= columns:
        return False, -1
    
    return True, column_index


def can_place_checker(board, column):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The game board
        column: Column index where checker should be placed
    
    Returns:
        True if checker can be placed, False otherwise
    """
    return board[0][column] == " "


def place_checker(board, column, checker):
    """
    Place a checker in the given column.
    
    Args:
        board: The game board
        column: Column index where checker should be placed
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row
    
    return -1


def check_win(board, row, column, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The game board
        row: Row index of the last placed checker
        column: Column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (top-left to bottom-right), diagonal (bottom-left to top-right)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        r, c = row + dr, column + dc
        while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, column - dc
        while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board
    
    Returns:
        True if board is full, False otherwise
    """
    columns = len(board[0])
    
    for column in range(columns):
        if board[0][column] == " ":
            return False
    
    return True


def get_player_name(player_index, checker):
    """
    Get the player name based on checker symbol.
    
    Args:
        player_index: Index of the player
        checker: The checker symbol
    
    Returns:
        String representation of the player
    """
    return f"Player {checker}"


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_player]
        player_name = get_player_name(current_player, checker)
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            column_input = input(f"{player_name}, please enter a column: ")
            is_valid, column_index = is_valid_column(column_input, COLUMNS)
            
            if not is_valid:
                print("Invalid input. Please enter a valid column letter (A-G).")
                continue
            
            if not can_place_checker(board, column_index):
                print("Column is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Place checker and get row position
        row = place_checker(board, column_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, column_index, checker):
            print(f"{player_name} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """
    Main function to start the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
