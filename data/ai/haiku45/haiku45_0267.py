import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLUMNS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board(rows, columns):
    """
    Create a 2D board initialized with empty spaces.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """
    Print the board in a formatted manner with column labels and borders.
    
    Args:
        board: The game board to print
    """
    os.system("clear")
    
    rows = len(board)
    columns = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(columns):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print top border
    print("+---" * columns + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(columns):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * columns + "+")


def get_column_input(board, player_symbol):
    """
    Get valid column input from the player.
    
    Args:
        board: The game board
        player_symbol: The symbol of the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    columns = len(board[0])
    
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within bounds
        if col_index < 0 or col_index >= columns:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("That column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, column, player_symbol):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        column: The column index where to place the checker
        player_symbol: The symbol of the player's checker
    
    Returns:
        True if placement was successful, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_symbol
            return True
    
    return False


def check_win(board, player_symbol):
    """
    Check if the specified player has won the game.
    
    Args:
        board: The game board
        player_symbol: The symbol of the player to check for a win
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == player_symbol for i in range(WIN_LENGTH)):
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


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Create the board
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Get player symbols
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid column input from player
        column = get_column_input(board, current_player)
        
        # Place the checker
        place_checker(board, column, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
