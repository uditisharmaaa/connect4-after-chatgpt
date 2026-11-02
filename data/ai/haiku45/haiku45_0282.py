import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()


def is_valid_move(board, col):
    """
    Check if a move in the given column is valid.
    
    Args:
        board: The 2D list representing the game board
        col: The column index (0-based)
    
    Returns:
        True if the move is valid, False otherwise
    """
    if col < 0 or col >= len(board[0]):
        return False
    
    # Check if the top cell of the column is empty
    if board[0][col] == " ":
        return True
    
    return False


def get_player_move(board, player_checker):
    """
    Get a valid move from the player.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol for the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if not is_valid_move(board, col):
            print("Invalid move. Column is either out of bounds or full.")
            continue
        
        return col


def place_checker(board, col, player_checker):
    """
    Place a checker in the given column at the lowest available position.
    
    Args:
        board: The 2D list representing the game board
        col: The column index (0-based)
        player_checker: The checker symbol to place
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return


def check_horizontal_win(board, player_checker):
    """
    Check if the player has won horizontally.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, player_checker):
    """
    Check if the player has won vertically.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, player_checker):
    """
    Check if the player has won diagonally.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check diagonal going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, player_checker):
    """
    Check if the player has won.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    return (check_horizontal_win(board, player_checker) or
            check_vertical_win(board, player_checker) or
            check_diagonal_win(board, player_checker))


def is_board_full(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Get player checkers
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = checkers[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_checker)
        
        # Place checker on the board
        place_checker(board, col, current_checker)
        
        # Print updated board
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
