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
    Initialize the game board with empty cells (whitespaces).
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board, columns):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The game board (2D list)
        columns: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    header = "  "
    for i in range(columns):
        header += chr(ord('A') + i) + "   "
    print(header)
    
    # Print each row with separators
    for row in board:
        print("+---" * columns + "+")
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print("+---" * columns + "+")


def get_valid_input(columns):
    """
    Get and validate player input for column selection.
    
    Args:
        columns: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input().strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        column_index = ord(user_input) - ord('A')
        
        # Check if column index is within valid range
        if column_index < 0 or column_index >= columns:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        
        return column_index


def place_checker(board, column, checker, rows, columns):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        column: The column index where the checker should be placed
        checker: The checker symbol (X, O, V, H, or M)
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if the checker was successfully placed, False if the column is full
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_horizontal_win(board, checker, rows, columns):
    """
    Check if there is a horizontal win for the given checker.
    
    Args:
        board: The game board (2D list)
        checker: The checker symbol to check for
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if there is a win, False otherwise
    """
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, checker, rows, columns):
    """
    Check if there is a vertical win for the given checker.
    
    Args:
        board: The game board (2D list)
        checker: The checker symbol to check for
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if there is a win, False otherwise
    """
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, checker, rows, columns):
    """
    Check if there is a diagonal win for the given checker.
    
    Args:
        board: The game board (2D list)
        checker: The checker symbol to check for
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if there is a win, False otherwise
    """
    # Check diagonals (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker, rows, columns):
    """
    Check if there is a win for the given checker.
    
    Args:
        board: The game board (2D list)
        checker: The checker symbol to check for
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if there is a win, False otherwise
    """
    return (check_horizontal_win(board, checker, rows, columns) or
            check_vertical_win(board, checker, rows, columns) or
            check_diagonal_win(board, checker, rows, columns))


def check_draw(board, rows, columns):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The game board (2D list)
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == " ":
                return False
    return True


def play_game(rows, columns, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
        num_players: Number of players in the game
    """
    # Initialize the board
    board = initialize_board(rows, columns)
    
    # Select random starting player
    current_player = random.randint(0, num_players - 1)
    
    # Print the initial board
    print_board(board, columns)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        
        # Get valid input from player
        column = get_valid_input(columns)
        
        # Try to place the checker
        if place_checker(board, column, checker, rows, columns):
            # Print the updated board
            print_board(board, columns)
            
            # Check for win
            if check_win(board, checker, rows, columns):
                print(f"Player {checker} won!")
                break
            
            # Check for draw
            if check_draw(board, rows, columns):
                print("Draw!")
                break
            
            # Move to next player
            current_player = (current_player + 1) % num_players
        else:
            # Turn is lost if column is full, move to next player
            print_board(board, columns)
            current_player = (current_player + 1) % num_players


def main():
    """
    Main function to start the Connect 4 game.
    """
    play_game(ROWS, COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
