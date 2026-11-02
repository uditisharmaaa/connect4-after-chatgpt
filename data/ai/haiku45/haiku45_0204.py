import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the board with empty spaces.
    
    Returns:
        A 2D list representing the Connect 4 board.
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board.
    
    Args:
        board: The 2D list representing the board.
    """
    os.system('clear')
    
    # Print column headers
    header = "  "
    for col in range(COLUMNS):
        header += chr(ord('A') + col) + "   "
    print(header)
    
    # Print board with separators
    for row in range(ROWS):
        # Print separator line
        print("+---" * COLUMNS + "+")
        
        # Print row content
        row_str = "|"
        for col in range(COLUMNS):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    
    # Print bottom separator
    print("+---" * COLUMNS + "+")


def get_valid_column_input(player_checker):
    """
    Get and validate column input from the player.
    
    Args:
        player_checker: The checker symbol of the current player.
    
    Returns:
        The column index (0-based) where the player wants to place their checker.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
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
        
        # Check if column is within board dimensions
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the board.
        col: The column index where to place the checker.
        player_checker: The checker symbol to place.
    
    Returns:
        True if the checker was placed successfully, False if the column is full.
    """
    # Find the lowest empty row in the column (start from bottom)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, player_checker):
    """
    Check if the current player has won.
    
    Args:
        board: The 2D list representing the board.
        player_checker: The checker symbol to check for a win.
    
    Returns:
        True if the player has won, False otherwise.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The 2D list representing the board.
    
    Returns:
        True if the board is full, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def get_next_player(current_player, num_players):
    """
    Get the next player's index.
    
    Args:
        current_player: The index of the current player.
        num_players: The total number of players.
    
    Returns:
        The index of the next player.
    """
    return (current_player + 1) % num_players


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player]
        
        # Get valid column input
        col = get_valid_column_input(player_checker)
        
        # Try to place checker
        if not place_checker(board, col, player_checker):
            # Column was full, player loses turn but continues asking
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        # Move to next player
        else:
            current_player = get_next_player(current_player, NUM_PLAYERS)


if __name__ == "__main__":
    play_game()
