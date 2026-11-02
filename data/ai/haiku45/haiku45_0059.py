import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(width, height):
    """
    Create and initialize a game board with empty spaces.
    
    Args:
        width: Number of columns
        height: Number of rows
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(width)] for _ in range(height)]
    return board


def print_board(board):
    """
    Print the game board to the console.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    
    width = len(board[0])
    height = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(width):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print("+---" * width + "+")
    
    # Print each row
    for row in range(height):
        print("|", end="")
        for col in range(width):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * width + "+")


def is_valid_column(column_letter, width):
    """
    Validate if the given column letter is valid.
    
    Args:
        column_letter: The column letter to validate
        width: The width of the board
    
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(column_letter, str) or len(column_letter) != 1:
        return False
    if column_letter.upper() not in [chr(65 + i) for i in range(width)]:
        return False
    return True


def column_letter_to_index(column_letter):
    """
    Convert a column letter to its index.
    
    Args:
        column_letter: The column letter (A, B, C, etc.)
    
    Returns:
        The column index (0-based)
    """
    return ord(column_letter.upper()) - 65


def is_column_full(board, col_index):
    """
    Check if a column is completely filled.
    
    Args:
        board: The game board
        col_index: The column index to check
    
    Returns:
        True if the column is full, False otherwise
    """
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col_index: The column index
        checker: The checker symbol to place
    
    Returns:
        True if placement was successful, False if column is full
    """
    height = len(board)
    
    # Find the lowest empty row in the column
    for row in range(height - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The game board
        row: The starting row
        col: The starting column
        checker: The checker symbol to look for
        row_delta: The row direction (-1, 0, or 1)
        col_delta: The column direction (-1, 0, or 1)
    
    Returns:
        True if 4 checkers in a row are found, False otherwise
    """
    height = len(board)
    width = len(board[0])
    count = 1
    
    # Check in the positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < height and 0 <= c < width and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in the negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < height and 0 <= c < width and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH


def check_win(board, checker):
    """
    Check if the current player has won.
    
    Args:
        board: The game board
        checker: The checker symbol to check for a win
    
    Returns:
        True if the player has won, False otherwise
    """
    height = len(board)
    width = len(board[0])
    
    for row in range(height):
        for col in range(width):
            if board[row][col] == checker:
                # Check horizontal
                if check_direction(board, row, col, checker, 0, 1):
                    return True
                # Check vertical
                if check_direction(board, row, col, checker, 1, 0):
                    return True
                # Check diagonal (top-left to bottom-right)
                if check_direction(board, row, col, checker, 1, 1):
                    return True
                # Check diagonal (top-right to bottom-left)
                if check_direction(board, row, col, checker, 1, -1):
                    return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely filled.
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_input(width):
    """
    Get and validate player input for column selection.
    
    Args:
        width: The width of the board
    
    Returns:
        The column index (0-based)
    """
    while True:
        try:
            user_input = input("Please enter a column: ").strip().upper()
            
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not is_valid_column(user_input, width):
                print(f"Invalid column. Please enter a letter between A and {chr(65 + width - 1)}.")
                continue
            
            return column_letter_to_index(user_input)
        
        except Exception:
            print("An error occurred. Please try again.")


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    
    # Create list of checkers for the number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        current_player_number = current_player_index + 1
        
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid player input
        col_index = get_player_input(BOARD_WIDTH)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("That column is full. Please try another column.")
            continue
        
        # Place the checker
        place_checker(board, col_index, current_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
