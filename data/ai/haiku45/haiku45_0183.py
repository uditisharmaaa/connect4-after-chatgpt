import os
import random

# Global constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Initialize the game board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
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
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with separators
    for row in range(rows):
        # Print top separator
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom separator
    print("+---" * cols + "+")


def get_valid_move(board, player_checker):
    """
    Get a valid column input from the player.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol of the current player
    
    Returns:
        The column index (0-based) where the checker will be placed
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Validate column is within bounds
        if col < 0 or col >= cols:
            print(f"Invalid input. Please enter a column between A and {chr(65 + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The 2D list representing the game board
        col: The column index (0-based) where the checker will be placed
        player_checker: The checker symbol of the current player
    
    Returns:
        True if checker was placed successfully, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_checker
            return True
    
    return False


def check_win(board, player_checker):
    """
    Check if the current player has won the game.
    
    Args:
        board: The 2D list representing the game board
        player_checker: The checker symbol of the player to check
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the game is a draw (board is full).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is full (draw), False otherwise
    """
    return all(board[0][col] != ' ' for col in range(len(board[0])))


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize board
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Get player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = player_checkers[current_player_index]
        
        # Get valid move from player
        col = get_valid_move(board, current_checker)
        
        # Place checker
        place_checker(board, col, current_checker)
        
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
