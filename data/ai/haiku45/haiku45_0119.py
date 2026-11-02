import os
import random

# Constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board in a formatted manner with column labels and grid.
    
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
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print rows
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
        print("+---" * cols + "+")


def get_valid_column_input(board, num_players, current_player, checkers):
    """
    Get and validate column input from the player.
    
    Args:
        board: The 2D list representing the game board
        num_players: Number of players in the game
        current_player: Index of the current player
        checkers: List of checker symbols for each player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    cols = len(board[0])
    
    while True:
        try:
            user_input = input(f"Player {checkers[current_player]}, please enter a column: ").strip().upper()
            
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
            if col_index < 0 or col_index >= cols:
                print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
                continue
            
            # Check if column is not full
            if board[0][col_index] != " ":
                print("Column is full. Please choose another column.")
                continue
            
            return col_index
        
        except Exception:
            print("Invalid input. Please try again.")


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column. The checker falls to the lowest available space.
    
    Args:
        board: The 2D list representing the game board
        col_index: The column index where the checker should be placed
        checker: The symbol of the checker to place
    
    Returns:
        True if the checker was placed successfully, False otherwise
    """
    rows = len(board)
    
    # Find the lowest available space in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_win(board, row, col, checker, win_length=WIN_LENGTH):
    """
    Check if placing the checker at (row, col) results in a win.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The symbol of the checker to check for
        win_length: Number of checkers in a row needed to win
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    # Check right
    j = col + 1
    while j < cols and board[row][j] == checker:
        count += 1
        j += 1
    if count >= win_length:
        return True
    
    # Check vertical
    count = 1
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    # Check down
    i = row + 1
    while i < rows and board[i][col] == checker:
        count += 1
        i += 1
    if count >= win_length:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    # Check down-right
    i, j = row + 1, col + 1
    while i < rows and j < cols and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= win_length:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # Check down-left
    i, j = row + 1, col - 1
    while i < rows and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= win_length:
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    
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


def get_row_of_checker(board, col_index):
    """
    Get the row index where the checker was placed in the given column.
    
    Args:
        board: The 2D list representing the game board
        col_index: The column index
    
    Returns:
        The row index of the checker, or -1 if no checker is in the column
    """
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] != " ":
            return row
    return -1


def play_game(board_rows, board_cols, num_players, checkers):
    """
    Main game loop for Connect 4.
    
    Args:
        board_rows: Number of rows in the board
        board_cols: Number of columns in the board
        num_players: Number of players
        checkers: List of checker symbols for each player
    """
    # Initialize the board
    board = initialize_board(board_rows, board_cols)
    
    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get valid column input
        col_index = get_valid_column_input(board, num_players, current_player, checkers)
        
        # Place the checker
        place_checker(board, col_index, checkers[current_player])
        
        # Get the row where the checker was placed
        row_index = get_row_of_checker(board, col_index)
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, row_index, col_index, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Switch to the next player
        if not game_over:
            current_player = (current_player + 1) % num_players


def main():
    """
    Main function to start the Connect 4 game.
    """
    # Use the checkers based on the number of players
    checkers = CHECKERS[:NUM_PLAYERS]
    
    # Start the game
    play_game(BOARD_ROWS, BOARD_COLS, NUM_PLAYERS, checkers)


if __name__ == "__main__":
    main()
