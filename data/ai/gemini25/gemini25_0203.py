import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {string.ascii_uppercase[col_index]} ", end="")
    print()

    # Print board content
    for row in board:
        print("+", end="")
        for _ in row:
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()

def get_column_index(col_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding integer index.

    Args:
        col_char (str): The uppercase character representing the column.

    Returns:
        int: The integer index of the column, or -1 if invalid.
    """
    if len(col_char) == 1 and 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]:
        return ord(col_char) - ord('A')
    return -1

def is_valid_column_input(col_char, num_cols):
    """
    Checks if the user's column input is valid.

    Args:
        col_char (str): The user's input for the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return False
    
    col_char = col_char.upper()
    
    if 'A' <= col_char <= string.ascii_uppercase[num_cols - 1]:
        return True
    return False

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The index of the column to drop the checker into.
        checker (str): The checker symbol for the current player.

    Returns:
        tuple: (True, row_index) if the checker was placed successfully,
               (False, -1) if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True, row_index
    return False, -1  # Column is full

# --- Win Condition Functions ---

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    if check_horizontal_win(board, checker, last_row):
        return True
    # Check vertical
    if check_vertical_win(board, checker, last_col):
        return True
    # Check diagonal (top-left to bottom-right)
    if check_diagonal_win_tlbr(board, checker, last_row, last_col):
        return True
    # Check diagonal (bottom-left to top-right)
    if check_diagonal_win_bltr(board, checker, last_row, last_col):
        return True
    return False

def check_horizontal_win(board, checker, row_index):
    """
    Checks for a horizontal win in a given row.
    """
    count = 0
    for col_index in range(NUM_COLS):
        if board[row_index][col_index] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
    return False

def check_vertical_win(board, checker, col_index):
    """
    Checks for a vertical win in a given column.
    """
    count = 0
    for row_index in range(NUM_ROWS):
        if board[row_index][col_index] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
    return False

def check_diagonal_win_tlbr(board, checker, last_row, last_col):
    """
    Checks for a diagonal win (top-left to bottom-right) passing through (last_row, last_col).
    """
    # Find the start of the diagonal (top-leftmost cell)
    start_row = last_row
    start_col = last_col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1

    count = 0
    row, col = start_row, start_col
    while row < NUM_ROWS and col < NUM_COLS:
        if board[row][col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        row += 1
        col += 1
    return False

def check_diagonal_win_bltr(board, checker, last_row, last_col):
    """
    Checks for a diagonal win (bottom-left to top-right) passing through (last_row, last_col).
    """
    # Find the start of the diagonal (bottom-leftmost cell)
    start_row = last_row
    start_col = last_col
    while start_row < NUM_ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1

    count = 0
    row, col = start_row, start_col
    while row >= 0 and col < NUM_COLS:
        if board[row][col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        row -= 1
        col += 1
    return False

def check_draw(board):
    """
    Checks if the board is full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for col_index in range(NUM_COLS):
        if board[0][col_index] == " ":  # If the top row of any column is empty
            return False
    return True

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        
        print(f"Player {current_checker}, please enter a column:")
        
        valid_move = False
        while not valid_move:
            try:
                col_input = input().strip().upper()
                if not is_valid_column_input(col_input, NUM_COLS):
                    print("Invalid input. Please enter a valid column letter (e.g., A, B).")
                    continue
                
                col_index = get_column_index(col_input)
                
                # Check if column is full before dropping
                if board[0][col_index] != " ":
                    print(f"Column {col_input} is full. Please choose another column.")
                    continue

                placed_successfully, row = drop_checker(board, col_index, current_checker)
                if placed_successfully:
                    last_placed_row = row
                    last_placed_col = col_index
                    valid_move = True
                else:
                    # This case should ideally be caught by board[0][col_index] != " " check
                    print(f"Could not place checker in column {col_input}. Please choose another column.") 

            except EOFError: # Handles Ctrl+D input
                print("\nExiting game.")
                return
            except Exception:
                print("An unexpected error occurred. Please try again.")

        # After a valid move, check for win or draw
        if check_win(board, current_checker, last_placed_row, last_placed_col):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    play_connect_4()
