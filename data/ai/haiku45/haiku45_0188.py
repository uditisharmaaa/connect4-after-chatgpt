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
    Initialize the board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the board in the required format.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col):3}", end=" ")
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


def is_valid_column(column_input, cols):
    """
    Validate if the column input is valid.
    
    Args:
        column_input: The input from the user
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) if valid, -1 otherwise
    """
    if len(column_input) != 1:
        return -1
    
    if not column_input.isalpha():
        return -1
    
    column_input = column_input.upper()
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def is_column_full(board, col_index):
    """
    Check if a column is completely full.
    
    Args:
        board: The game board
        col_index: The column index to check
    
    Returns:
        True if the column is full, False otherwise
    """
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col_index: The column index where to place the checker
        checker: The checker symbol to place
    
    Returns:
        True if placement was successful, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def get_player_move(board, current_player, checker, cols):
    """
    Get and validate a move from the current player.
    
    Args:
        board: The game board
        current_player: The current player number
        checker: The checker symbol for the current player
        cols: Number of columns in the board
    
    Returns:
        The column index where the checker was placed
    """
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip()
        
        col_index = is_valid_column(user_input, cols)
        
        if col_index == -1:
            print("Invalid column. Please enter a valid column letter.")
            continue
        
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        place_checker(board, col_index, checker)
        return col_index


def check_win(board, col_index, row_index, checker):
    """
    Check if the last move resulted in a win.
    
    Args:
        board: The game board
        col_index: The column index of the last placed checker
        row_index: The row index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    col = col_index - 1
    while col >= 0 and board[row_index][col] == checker:
        count += 1
        col -= 1
    # Check right
    col = col_index + 1
    while col < cols and board[row_index][col] == checker:
        count += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check down
    row = row_index + 1
    while row < rows and board[row][col_index] == checker:
        count += 1
        row += 1
    # Check up
    row = row_index - 1
    while row >= 0 and board[row][col_index] == checker:
        count += 1
        row -= 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    row, col = row_index - 1, col_index - 1
    while row >= 0 and col >= 0 and board[row][col] == checker:
        count += 1
        row -= 1
        col -= 1
    # Check down-right
    row, col = row_index + 1, col_index + 1
    while row < rows and col < cols and board[row][col] == checker:
        count += 1
        row += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    row, col = row_index - 1, col_index + 1
    while row >= 0 and col < cols and board[row][col] == checker:
        count += 1
        row -= 1
        col += 1
    # Check down-left
    row, col = row_index + 1, col_index - 1
    while row < rows and col >= 0 and board[row][col] == checker:
        count += 1
        row += 1
        col -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def get_row_index(board, col_index):
    """
    Get the row index of the last placed checker in a column.
    
    Args:
        board: The game board
        col_index: The column index
    
    Returns:
        The row index of the last placed checker
    """
    for row in range(len(board)):
        if board[row][col_index] != " ":
            return row
    return -1


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    return board[0].count(" ") == 0


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select a random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player's checker
        checker = CHECKERS[current_player_index]
        
        # Get player's move
        col_index = get_player_move(board, current_player_index, checker, COLS)
        
        # Get the row index where the checker was placed
        row_index = get_row_index(board, col_index)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, col_index, row_index, checker):
            print(f"Player {checker} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        # Move to next player
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
