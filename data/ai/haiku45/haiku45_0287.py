import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, columns):
    """
    Initialize the board with empty spaces.
    
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
    Print the board in the required format.
    
    Args:
        board: The game board (2D list)
        columns: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * columns + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * columns + "+")


def is_valid_move(board, column, columns):
    """
    Check if a move is valid (column exists and is not full).
    
    Args:
        board: The game board (2D list)
        column: The column index (0-based)
        columns: Total number of columns
    
    Returns:
        True if the move is valid, False otherwise
    """
    if column < 0 or column >= columns:
        return False
    
    # Check if the top of the column is empty
    if board[0][column] == " ":
        return True
    
    return False


def place_checker(board, column, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        column: The column index (0-based)
        checker: The checker symbol ('X', 'O', 'V', 'H', or 'M')
    
    Returns:
        The row where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row
    
    return -1


def check_horizontal_win(board, rows, columns, checker):
    """
    Check if there is a horizontal win.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows
        columns: Number of columns
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, rows, columns, checker):
    """
    Check if there is a vertical win.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows
        columns: Number of columns
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, rows, columns, checker):
    """
    Check if there is a diagonal win (both directions).
    
    Args:
        board: The game board (2D list)
        rows: Number of rows
        columns: Number of columns
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    # Check diagonal down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal up-right
    for row in range(WIN_LENGTH - 1, rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, rows, columns, checker):
    """
    Check if the current player has won.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows
        columns: Number of columns
        checker: The checker symbol to check for
    
    Returns:
        True if there is a win, False otherwise
    """
    return (check_horizontal_win(board, rows, columns, checker) or
            check_vertical_win(board, rows, columns, checker) or
            check_diagonal_win(board, rows, columns, checker))


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(cell != " " for row in board for cell in row)


def get_player_input(columns):
    """
    Get and validate player input for column selection.
    
    Args:
        columns: Number of columns in the board
    
    Returns:
        The column index (0-based) selected by the player
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        column = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if column < 0 or column >= columns:
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + columns - 1)}.")
            continue
        
        return column


def play_game():
    """
    Main game loop that runs the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get list of players (checkers)
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    
    # Game loop
    while True:
        current_checker = players[current_player_index]
        
        # Get player input
        print(f"Player {current_checker}, please enter a column: ", end="")
        column = get_player_input(COLUMNS)
        
        # Validate the move
        if not is_valid_move(board, column, COLUMNS):
            print("Invalid move. The column is full. Try again.")
            continue
        
        # Place the checker
        place_checker(board, column, current_checker)
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, ROWS, COLUMNS, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
