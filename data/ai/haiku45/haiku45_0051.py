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
    Initialize the game board with all empty cells (whitespaces).
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """
    Print the current state of the game board with formatting.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    rows = len(board)
    columns = len(board[0])
    
    # Print column headers
    header = "  "
    for col in range(columns):
        header += chr(ord('A') + col) + "   "
    print(header)
    
    # Print top border
    border = "+---" * columns + "+"
    print(border)
    
    # Print each row
    for row in board:
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
        print(border)


def get_valid_column_input(board):
    """
    Get a valid column input from the player.
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    columns = len(board[0])
    valid_columns = [chr(ord('A') + i) for i in range(columns)]
    
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Validate input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a valid column letter
        if user_input not in valid_columns:
            print(f"Invalid column. Please enter a letter between A and {valid_columns[-1]}.")
            continue
        
        column = ord(user_input) - ord('A')
        
        # Check if column is full
        if board[0][column] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return column


def place_checker(board, column, checker):
    """
    Place a checker in the specified column at the lowest available position.
    
    Args:
        board: The 2D list representing the game board
        column: The column index where the checker will be placed
        checker: The checker symbol to place
    
    Returns:
        True if the checker was placed successfully, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won the game.
    
    Args:
        board: The 2D list representing the game board
        checker: The checker symbol to check for a win
    
    Returns:
        True if the checker has 4 in a row, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
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


def check_draw(board):
    """
    Check if the game is a draw (board is full with no winner).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is completely filled, False otherwise
    """
    return all(board[0][col] != " " for col in range(len(board[0])))


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        current_player_number = current_player_index + 1
        
        print(f"Player {current_checker}, please enter a column:")
        column = get_valid_column_input(board)
        
        # Place checker
        place_checker(board, column, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
