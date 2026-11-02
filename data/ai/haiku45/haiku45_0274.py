import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

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
        print("+---" * cols + "+")
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")

def is_valid_input(column_letter, cols):
    """
    Validate the column input from the player.
    
    Args:
        column_letter: The letter representing the column
        cols: Number of columns in the board
    
    Returns:
        True if input is valid, False otherwise
    """
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isupper():
        return False
    
    column_index = ord(column_letter) - ord('A')
    
    if column_index < 0 or column_index >= cols:
        return False
    
    return True

def get_column_index(column_letter):
    """
    Convert column letter to column index.
    
    Args:
        column_letter: The letter representing the column (e.g., 'A', 'B')
    
    Returns:
        The column index (0-based)
    """
    return ord(column_letter) - ord('A')

def is_column_full(board, col_index):
    """
    Check if a column is completely filled.
    
    Args:
        board: The 2D list representing the game board
        col_index: The column index to check
    
    Returns:
        True if column is full, False otherwise
    """
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the game board
        col_index: The column index where the checker will be placed
        checker: The player's checker character
    
    Returns:
        True if checker was placed successfully, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column (start from bottom)
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    # Column is full
    return False

def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check for 4 in a row in a specific direction from a given position.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the checker
        col: The column index of the checker
        checker: The checker character to look for
        row_delta: Direction to move in rows (-1, 0, or 1)
        col_delta: Direction to move in columns (-1, 0, or 1)
    
    Returns:
        True if 4 checkers in a row are found in that direction, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    count = 1  # Count the current checker
    
    # Check in positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH

def check_win(board, row, col, checker):
    """
    Check if the last placed checker results in a win.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker character of the player
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, checker, 1, -1):
        return True
    
    return False

def is_board_full(board):
    """
    Check if the board is completely filled (draw condition).
    
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

def get_player_move(board, current_player, checker):
    """
    Get a valid move from the current player.
    
    Args:
        board: The 2D list representing the game board
        current_player: The current player number (0-indexed)
        checker: The checker character of the player
    
    Returns:
        The column index where the player wants to place their checker
    """
    cols = len(board[0])
    
    while True:
        column_letter = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_input(column_letter, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = get_column_index(column_letter)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("This column is full. Please choose another column.")
            continue
        
        # Valid move
        return col_index

def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player]
        
        # Get player's move
        col_index = get_player_move(board, current_player, checker)
        
        # Find the row where the checker was placed
        for row in range(ROWS - 1, -1, -1):
            if board[row][col_index] == " ":
                board[row][col_index] = checker
                placed_row = row
                break
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, placed_row, col_index, checker):
            print(f"Player {checker} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS

def main():
    """
    Entry point of the program.
    """
    play_game()

if __name__ == "__main__":
    main()
