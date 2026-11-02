import os
import random

# Game constants
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
    Print the current state of the game board.
    
    Args:
        board: The current game board
    """
    os.system('clear')
    
    columns = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(columns):
        print(f"{chr(65 + i)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * columns + "+")
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * columns + "+")


def is_valid_column(column_letter, columns):
    """
    Check if the column letter is valid.
    
    Args:
        column_letter: The column letter entered by the player
        columns: Total number of columns
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isupper():
        return False
    
    column_index = ord(column_letter) - ord('A')
    return 0 <= column_index < columns


def get_column_index(column_letter):
    """
    Convert column letter to column index.
    
    Args:
        column_letter: The column letter (e.g., 'A', 'B')
    
    Returns:
        The column index (0-based)
    """
    return ord(column_letter) - ord('A')


def can_place_checker(board, column_index):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The current game board
        column_index: The column index (0-based)
    
    Returns:
        True if the column is not full, False otherwise
    """
    return board[0][column_index] == " "


def place_checker(board, column_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        column_index: The column index (0-based)
        checker: The checker symbol (e.g., 'X', 'O')
    
    Returns:
        True if placement was successful, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return True
    
    return False


def check_horizontal_win(board, checker):
    """
    Check if there's a horizontal win for the given checker.
    
    Args:
        board: The current game board
        checker: The checker symbol to check
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, checker):
    """
    Check if there's a vertical win for the given checker.
    
    Args:
        board: The current game board
        checker: The checker symbol to check
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, checker):
    """
    Check if there's a diagonal win for the given checker.
    
    Args:
        board: The current game board
        checker: The checker symbol to check
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: The current game board
        checker: The checker symbol to check
    
    Returns:
        True if there's a win, False otherwise
    """
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    columns = len(board[0])
    for col in range(columns):
        if board[0][col] == " ":
            return False
    return True


def get_player_input(num_players, current_player, columns):
    """
    Get and validate player input for column selection.
    
    Args:
        num_players: Total number of players
        current_player: Current player number (0-based)
        columns: Total number of columns
    
    Returns:
        The valid column index (0-based)
    """
    checker = CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        if not is_valid_column(user_input, columns):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column_index = get_column_index(user_input)
        
        if not can_place_checker(board, column_index):
            print("Column is full. Please choose another column.")
            continue
        
        return column_index


def play_game():
    """
    Main game loop for Connect 4.
    """
    board = initialize_board(ROWS, COLUMNS)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get player input
        column_index = get_player_input(NUM_PLAYERS, current_player, COLUMNS)
        
        # Place checker
        checker = CHECKERS[current_player]
        place_checker(board, column_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
