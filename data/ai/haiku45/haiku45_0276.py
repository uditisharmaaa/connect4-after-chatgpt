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
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the current state of the board with formatting.
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
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


def is_column_full(board, col):
    """
    Check if a column is completely filled.
    Returns True if full, False otherwise.
    """
    return board[0][col] != " "


def get_lowest_empty_row(board, col):
    """
    Get the lowest empty row index in a given column.
    Returns the row index or -1 if column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    Returns True if placement was successful, False otherwise.
    """
    if is_column_full(board, col):
        return False
    
    row = get_lowest_empty_row(board, col)
    if row == -1:
        return False
    
    board[row][col] = checker
    return True


def validate_input(user_input, cols):
    """
    Validate user input for column selection.
    Returns the column index (0-6) if valid, -1 if invalid.
    """
    if len(user_input) != 1:
        return -1
    
    if not user_input.isalpha():
        return -1
    
    col_letter = user_input.upper()
    col_index = ord(col_letter) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return -1
    
    return col_index


def check_win(board, last_row, last_col, checker):
    """
    Check if the current player has won after placing a checker.
    Returns True if there's a win, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    count = 1
    # Check left
    col = last_col - 1
    while col >= 0 and board[last_row][col] == checker:
        count += 1
        col -= 1
    # Check right
    col = last_col + 1
    while col < cols and board[last_row][col] == checker:
        count += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check down
    row = last_row + 1
    while row < rows and board[row][last_col] == checker:
        count += 1
        row += 1
    # Check up
    row = last_row - 1
    while row >= 0 and board[row][last_col] == checker:
        count += 1
        row -= 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    row, col = last_row - 1, last_col - 1
    while row >= 0 and col >= 0 and board[row][col] == checker:
        count += 1
        row -= 1
        col -= 1
    # Check down-right
    row, col = last_row + 1, last_col + 1
    while row < rows and col < cols and board[row][col] == checker:
        count += 1
        row += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    row, col = last_row - 1, last_col + 1
    while row >= 0 and col < cols and board[row][col] == checker:
        count += 1
        row -= 1
        col += 1
    # Check down-left
    row, col = last_row + 1, last_col - 1
    while row < rows and col >= 0 and board[row][col] == checker:
        count += 1
        row += 1
        col -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely filled (draw condition).
    Returns True if full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Get checkers for the number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        current_player_number = current_player_index + 1
        
        # Get valid input from player
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ")
            col_index = validate_input(user_input, COLS)
            
            if col_index == -1:
                print("Invalid input. Please enter a valid column (A-G).")
                continue
            
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place the checker
        row_index = get_lowest_empty_row(board, col_index)
        place_checker(board, col_index, current_checker)
        
        # Print the board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
