import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Create and initialize a 2D board with all cells as whitespaces.
    
    Returns:
        list: A 2D list representing the game board
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the board to the console with proper formatting.
    
    Args:
        board (list): The current game board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(COLS):
        print("---+", end="")
    print()
    
    # Print each row with borders
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(COLS):
            print("---+", end="")
        print()


def get_player_input(current_player_symbol):
    """
    Get and validate player input for column selection.
    
    Args:
        current_player_symbol (str): The symbol of the current player
        
    Returns:
        int: The column index (0-6) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {current_player_symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter (A-" + chr(65 + COLS - 1) + ").")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board range
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid input. Please enter a letter (A-{chr(65 + COLS - 1)}).")
            continue
        
        return col_index


def place_checker(board, col, player_symbol):
    """
    Place a checker in the specified column, dropping it to the lowest available row.
    
    Args:
        board (list): The current game board
        col (int): The column index where the checker should be placed
        player_symbol (str): The symbol of the current player
        
    Returns:
        bool: True if the checker was placed successfully, False if the column is full
    """
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, player_symbol):
    """
    Check if the current player has won by checking all four directions.
    
    Args:
        board (list): The current game board
        player_symbol (str): The symbol of the player to check for a win
        
    Returns:
        bool: True if the player has won, False otherwise
    """
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonally (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board (list): The current game board
        
    Returns:
        bool: True if all cells are filled, False otherwise
    """
    for row in board:
        if " " in row:
            return False
    return True


def get_random_player():
    """
    Randomly select the first player.
    
    Returns:
        int: The index of the randomly selected player (0 to NUM_PLAYERS - 1)
    """
    return random.randint(0, NUM_PLAYERS - 1)


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board()
    
    # Get player symbols
    player_symbols = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = get_random_player()
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player_symbol = player_symbols[current_player_index]
        
        # Get valid input from player
        valid_placement = False
        while not valid_placement:
            col = get_player_input(current_player_symbol)
            valid_placement = place_checker(board, col, current_player_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, current_player_symbol):
            print(f"Player {current_player_symbol} won!")
            game_over = True
        # Check if the board is full (draw)
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
