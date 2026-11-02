import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    
    Args:
        board: The game board (2D list)
    """
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    
    # Print top border
    print("+" + "+".join(["---"] * cols) + "+")
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "+".join(["---"] * cols) + "+")


def get_valid_column_input(board, num_players, current_player):
    """
    Get a valid column input from the current player.
    
    Args:
        board: The game board (2D list)
        num_players: Number of players
        current_player: Index of the current player
    
    Returns:
        The column index (0-based) where the checker will be placed
    """
    cols = len(board[0])
    checker = CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col_index, player_index):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The game board (2D list)
        col_index: The column index (0-based)
        player_index: Index of the player
    
    Returns:
        True if placement was successful, False otherwise
    """
    rows = len(board)
    checker = CHECKERS[player_index]
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    
    return False


def check_horizontal_win(board, player_index):
    """
    Check if the current player has won horizontally.
    
    Args:
        board: The game board (2D list)
        player_index: Index of the player
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    checker = CHECKERS[player_index]
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_vertical_win(board, player_index):
    """
    Check if the current player has won vertically.
    
    Args:
        board: The game board (2D list)
        player_index: Index of the player
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    checker = CHECKERS[player_index]
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_diagonal_win(board, player_index):
    """
    Check if the current player has won diagonally.
    
    Args:
        board: The game board (2D list)
        player_index: Index of the player
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    checker = CHECKERS[player_index]
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, player_index):
    """
    Check if the current player has won the game.
    
    Args:
        board: The game board (2D list)
        player_index: Index of the player
    
    Returns:
        True if the player has won, False otherwise
    """
    return (check_horizontal_win(board, player_index) or
            check_vertical_win(board, player_index) or
            check_diagonal_win(board, player_index))


def check_draw(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(board[0][col] != ' ' for col in range(len(board[0])))


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get valid input from current player
        col_index = get_valid_column_input(board, NUM_PLAYERS, current_player)
        
        # Place the checker
        place_checker(board, col_index, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
