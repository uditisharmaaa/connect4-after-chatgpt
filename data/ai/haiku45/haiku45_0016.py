import os
import random

# Game constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the board with empty spaces.
    
    Returns:
        list: A 2D list representing the game board
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the game board to the console.
    
    Args:
        board (list): The game board to print
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * COLS + "+")


def get_column_input(current_player_checker):
    """
    Get valid column input from the player.
    
    Args:
        current_player_checker (str): The checker symbol of the current player
        
    Returns:
        int: The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board (list): The game board
        col (int): The column index where the checker should be placed
        checker (str): The checker symbol to place
        
    Returns:
        bool: True if the checker was placed successfully, False if the column is full
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    print("Column is full. Please choose another column.")
    return False


def check_win(board, checker):
    """
    Check if the specified player has won.
    
    Args:
        board (list): The game board
        checker (str): The checker symbol to check for a win
        
    Returns:
        bool: True if the player has won, False otherwise
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the game is a draw (board is full and no winner).
    
    Args:
        board (list): The game board
        
    Returns:
        bool: True if the board is full, False otherwise
    """
    for row in board:
        if " " in row:
            return False
    return True


def get_player_checkers(num_players):
    """
    Get the list of checker symbols for the given number of players.
    
    Args:
        num_players (int): The number of players
        
    Returns:
        list: A list of checker symbols
    """
    return CHECKERS[:num_players]


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Get player checkers
    player_checkers = get_player_checkers(NUM_PLAYERS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {player_checkers[current_player_index]} goes first!")
    input("Press Enter to continue...")
    
    # Game loop
    while True:
        print_board(board)
        
        current_checker = player_checkers[current_player_index]
        
        # Get column input from the current player
        while True:
            col = get_column_input(current_checker)
            if place_checker(board, col, current_checker):
                break
            # If placement failed, the loop continues and asks for input again
        
        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
