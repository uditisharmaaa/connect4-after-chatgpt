import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Create and initialize a board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """
    Print the current state of the board with formatting.
    
    Args:
        board: The game board to print
    """
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print each row with borders
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


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def get_column_input(num_cols, current_player_checker):
    """
    Get and validate the column input from the player.
    
    Args:
        num_cols: Number of columns in the board
        current_player_checker: The checker symbol of the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is uppercase
        if not user_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Check if input is a valid column letter
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= num_cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col: The column index (0-based) where to place the checker
        checker: The checker symbol to place
    
    Returns:
        True if the checker was placed successfully, False if the column is full
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, row, col, checker):
    """
    Check if placing a checker at (row, col) results in a win.
    
    Args:
        board: The game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < cols and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < rows and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
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
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_checker_for_player(player_num):
    """
    Get the checker symbol for a given player number.
    
    Args:
        player_num: The player number (0-based)
    
    Returns:
        The checker symbol for the player
    """
    return PLAYER_CHECKERS[player_num]


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Clear screen and print initial board
    clear_screen()
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        current_checker = get_checker_for_player(current_player)
        
        # Get valid column input from player
        placed = False
        while not placed:
            col = get_column_input(BOARD_COLUMNS, current_checker)
            placed = place_checker(board, col, current_checker)
        
        # Clear screen and print updated board
        clear_screen()
        print_board(board)
        
        # Find the row where the checker was placed
        placed_row = -1
        for row in range(BOARD_ROWS):
            if board[row][col] == current_checker:
                placed_row = row
                break
        
        # Check for a win
        if check_win(board, placed_row, col, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for a draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
