import os
import random

# Configuration constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
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
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the board in a formatted way with column labels.
    
    Args:
        board: The 2D board list
        cols: Number of columns
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(65 + i)} ", end=" ")
    print()
    
    # Print top border
    print(" ", end="")
    for _ in range(cols):
        print("+---", end="")
    print("+")
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print row border
        print(" ", end="")
        for _ in range(cols):
            print("+---", end="")
        print("+")


def is_valid_column(column_input, cols):
    """
    Validate if the input is a valid column.
    
    Args:
        column_input: The user's column input
        cols: Number of columns
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_input) != 1:
        return False
    
    if not column_input.isalpha():
        return False
    
    column_index = ord(column_input.upper()) - 65
    
    if column_index < 0 or column_index >= cols:
        return False
    
    return True


def get_column_input(cols):
    """
    Get and validate column input from the player.
    
    Args:
        cols: Number of columns
    
    Returns:
        The column index (0-based)
    """
    while True:
        column_input = input()
        
        if not is_valid_column(column_input, cols):
            print(f"Invalid input. Please enter a column letter (A-{chr(65 + cols - 1)}):")
            continue
        
        column_index = ord(column_input.upper()) - 65
        return column_index


def place_checker(board, col, checker, rows, cols):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D board list
        col: The column index (0-based)
        checker: The player's checker symbol
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        True if checker was placed successfully, False if column is full
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_direction(board, row, col, checker, dr, dc, rows, cols):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The 2D board list
        row: Starting row
        col: Starting column
        checker: The player's checker symbol
        dr: Row direction (-1, 0, or 1)
        dc: Column direction (-1, 0, or 1)
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        Count of consecutive checkers in that direction
    """
    count = 0
    r, c = row, col
    
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    
    return count


def check_win(board, row, col, checker, rows, cols):
    """
    Check if the current move results in a win.
    
    Args:
        board: The 2D board list
        row: Row where the checker was placed
        col: Column where the checker was placed
        checker: The player's checker symbol
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        True if there's a win, False otherwise
    """
    # Directions to check: horizontal, vertical, diagonal-right, diagonal-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        # Count in both directions from the placed checker
        count_forward = check_direction(board, row, col, checker, dr, dc, rows, cols)
        count_backward = check_direction(board, row, col, checker, -dr, -dc, rows, cols)
        
        # Total count includes the current checker
        total = count_forward + count_backward - 1
        
        if total >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board, rows, cols):
    """
    Check if the board is completely filled.
    
    Args:
        board: The 2D board list
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        True if board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game(board, num_players, rows, cols):
    """
    Main game loop.
    
    Args:
        board: The 2D board list
        num_players: Number of players
        rows: Number of rows
        cols: Number of columns
    """
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, cols)
    
    while True:
        current_checker = CHECKERS[current_player_index]
        current_player_name = chr(65 + current_player_index) if current_player_index > 1 else current_checker
        
        print(f"Player {current_checker}, please enter a column:")
        column = get_column_input(cols)
        
        # Try to place the checker
        if not place_checker(board, column, current_checker, rows, cols):
            print(f"Column is full. Please choose another column:")
            continue
        
        print_board(board, cols)
        
        # Check for win
        # Find the row where the checker was placed
        placed_row = -1
        for row in range(rows):
            if board[row][column] == current_checker:
                placed_row = row
                break
        
        if check_win(board, placed_row, column, current_checker, rows, cols):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, rows, cols):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players


def main():
    """
    Main function to start the game.
    """
    board = initialize_board(ROWS, COLS)
    play_game(board, NUM_PLAYERS, ROWS, COLS)


if __name__ == "__main__":
    main()
