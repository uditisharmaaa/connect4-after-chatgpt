import os
import random
import string

# --- Global Constants (Adjustable) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    Each cell is initialized with a whitespace.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    Clears the screen before printing.
    """
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {string.ascii_uppercase[col_index]} ", end="")
    print()

    # Print board content
    for r_idx, row in enumerate(board):
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A') to its integer index.
    Returns -1 if the character is invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return -1
    
    upper_char = column_char.upper()
    if 'A' <= upper_char <= string.ascii_uppercase[NUM_COLS - 1]:
        return ord(upper_char) - ord('A')
    return -1

def is_valid_column_input(column_char, board):
    """
    Validates the player's column input.
    Checks if it's a valid letter and if the column isn't full.
    Returns (True, col_index) if valid, (False, -1) otherwise.
    """
    col_index = get_column_index(column_char)
    if col_index == -1:
        print("Invalid input. Please enter a single letter (e.g., A, B).")
        return False, -1
    
    if col_index >= len(board[0]):
        print(f"Column '{column_char.upper()}' is out of board range.")
        return False, -1
    
    # Check if the column is full
    if board[0][col_index] != " ":
        print(f"Column '{column_char.upper()}' is full. Please choose another column.")
        return False, -1
    
    return True, col_index

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.
    Returns the row index where the checker landed, or -1 if the column is full.
    """
    for r_idx in range(len(board) - 1, -1, -1):
        if board[r_idx][col_index] == " ":
            board[r_idx][col_index] = checker
            return r_idx
    return -1  # Column is full (should be caught by is_valid_column_input)

# --- Win Condition Functions ---

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win.
    Checks horizontally, vertically, and both diagonals.
    """
    # Helper to count consecutive checkers
    def count_consecutive(delta_row, delta_col):
        count = 0
        for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
            r, c = last_row + i * delta_row, last_col + i * delta_col
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0 # Reset count if sequence is broken
        return False

    # Check horizontal
    if count_consecutive(0, 1):
        return True
    
    # Check vertical
    if count_consecutive(1, 0):
        return True

    # Check main diagonal (top-left to bottom-right)
    if count_consecutive(1, 1):
        return True

    # Check anti-diagonal (top-right to bottom-left)
    if count_consecutive(1, -1):
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full

# --- Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get and validate player input
        while True:
            column_input = input().strip()
            is_valid, col_idx = is_valid_column_input(column_input, board)
            if is_valid:
                break
            # If invalid, the loop continues and prompts the player again

        # Place the checker
        row_idx = drop_checker(board, col_idx, current_checker)
        
        # Check for win
        if check_win(board, current_checker, row_idx, col_idx):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
            winner = current_checker
        
        # Check for draw if no win
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        
        # Switch to the next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
