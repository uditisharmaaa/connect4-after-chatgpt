import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board,
              initialized with spaces.
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
    clear_screen()
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board content
    for row_index in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        
        print("|", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to its
    corresponding 0-based index.

    Args:
        column_char (str): The uppercase letter representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based column index, or -1 if invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return -1
    
    char_code = ord(column_char.upper())
    a_code = ord('A')
    
    col_index = char_code - a_code
    
    if 0 <= col_index < num_cols:
        return col_index
    return -1

def is_valid_move(board, col_index):
    """
    Checks if a move to the given column is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if not (0 <= col_index < len(board[0])):
        return False  # Column out of bounds
    
    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        int: The row index where the checker was placed, or -1 if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index
    return -1 # Column is full, though this should be caught by is_valid_move

def check_win(board, row, col, checker, win_condition):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers needed to win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(max(0, col - win_condition + 1), min(num_cols, col + win_condition)):
        if board[row][c] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(max(0, row - win_condition + 1), min(num_rows, row + win_condition)):
        if board[r][col] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row - min(row, col) # Move to the top-leftmost cell in this diagonal
    start_col = col - min(row, col)
    
    for i in range(min(num_rows - start_row, num_cols - start_col)):
        r = start_row + i
        c = start_col + i
        if board[r][c] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check diagonal (top-right to bottom-left)
    count = 0
    # Determine start of diagonal: move up-right as far as possible
    start_row = row - min(row, num_cols - 1 - col)
    start_col = col + min(row, num_cols - 1 - col)
    
    for i in range(min(num_rows - start_row, start_col + 1)):
        r = start_row + i
        c = start_col - i
        if board[r][c] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for col in range(len(board[0])):
        if board[0][col] == " ":  # If any cell in the top row is empty, game is not a draw
            return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Runs the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        
        valid_input = False
        col_to_drop = -1
        
        while not valid_input:
            prompt = f"Player {current_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()
            
            if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + NUM_COLS - 1):
                col_to_drop = get_column_index(user_input, NUM_COLS)
                if is_valid_move(board, col_to_drop):
                    valid_input = True
                else:
                    print("Column is full or invalid. Please choose another column.")
            else:
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
        
        # Drop the checker
        placed_row = drop_checker(board, col_to_drop, current_checker)
        
        # Check for win
        if check_win(board, placed_row, col_to_drop, current_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Entry Point ---

if __name__ == "__main__":
    play_game()
