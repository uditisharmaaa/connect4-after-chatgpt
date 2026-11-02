import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2
WIN_LENGTH = 4


def initialize_board(width, height):
    """
    Initialize an empty board with the given dimensions.
    
    Args:
        width: Number of columns
        height: Number of rows
    
    Returns:
        A 2D list representing the board, filled with spaces
    """
    board = [[" " for _ in range(width)] for _ in range(height)]
    return board


def print_board(board):
    """
    Print the current state of the board.
    
    Args:
        board: The game board (2D list)
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
    print("+", end="")
    for _ in range(width):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(width):
            print("---+", end="")
        print()


def is_valid_column(column_str, width):
    """
    Validate if the input is a valid column.
    
    Args:
        column_str: The input string from the user
        width: The width of the board
    
    Returns:
        The column index if valid, -1 otherwise
    """
    if len(column_str) != 1:
        return -1
    
    if not column_str.isalpha():
        return -1
    
    column_str = column_str.upper()
    column_index = ord(column_str) - ord('A')
    
    if column_index < 0 or column_index >= width:
        return -1
    
    return column_index


def is_column_full(board, column):
    """
    Check if a column is completely full.
    
    Args:
        board: The game board
        column: The column index
    
    Returns:
        True if the column is full, False otherwise
    """
    return board[0][column] != " "


def place_checker(board, column, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        column: The column index
        checker: The checker character to place
    
    Returns:
        True if placement was successful, False otherwise
    """
    height = len(board)
    
    # Find the lowest empty row in the column
    for row in range(height - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    
    return False


def check_winner(board, checker):
    """
    Check if the given checker has won.
    
    Args:
        board: The game board
        checker: The checker character to check
    
    Returns:
        True if the checker has won, False otherwise
    """
    height = len(board)
    width = len(board[0])
    
    # Check horizontal
    for row in range(height):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(width):
        for row in range(height - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, width):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(board[0][col] != " " for col in range(len(board[0])))


def get_valid_move(board, current_player, checker):
    """
    Get a valid move from the current player.
    
    Args:
        board: The game board
        current_player: The current player number
        checker: The checker character for the current player
    
    Returns:
        The column index of the valid move
    """
    width = len(board[0])
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        column = is_valid_column(user_input, width)
        
        if column == -1:
            print("Invalid input. Please enter a valid column letter (A-" + chr(65 + width - 1) + ").")
            continue
        
        if is_column_full(board, column):
            print("That column is full. Please choose another column.")
            continue
        
        return column


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(BOARD_WIDTH, BOARD_HEIGHT)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    print(f"Player {CHECKERS[current_player]} will start!")
    input("Press Enter to continue...")
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get valid move from player
        column = get_valid_move(board, current_player, checker)
        
        # Place the checker
        place_checker(board, column, checker)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_winner(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        
        # Check for a draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        
        else:
            # Move to the next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
