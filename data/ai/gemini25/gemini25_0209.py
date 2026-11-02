import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the empty board,
              initialized with whitespaces.
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
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print board content
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to its
    corresponding 0-based integer index.

    Args:
        column_char (str): The uppercase letter representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index if valid, otherwise None.
    """
    if len(column_char) != 1 or not column_char.isalpha():
        return None
    
    col_index = ord(column_char.upper()) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return None

def is_valid_move(board, col_index):
    """
    Checks if a move to the given column is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to check.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if not (0 <= col_index < len(board[0])):
        return False  # Column index out of bounds
    
    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        tuple: (row, col) of where the checker was placed, or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return None # Column is full (should be caught by is_valid_move before)

def check_win(board, checker):
    """
    Checks if the given checker has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_draw(board):
    """
    Checks if the board is completely filled (a draw).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True # No empty spaces found

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to play a game of Connect 4.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        
        valid_input = False
        while not valid_input:
            prompt = f"Player {current_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            col_index = get_column_index(user_input, NUM_COLS)

            if col_index is None:
                print("Invalid column. Please enter a letter from A to", chr(ord('A') + NUM_COLS - 1) + ".")
            elif not is_valid_move(board, col_index):
                print(f"Column {user_input} is full. Please choose another column.")
            else:
                valid_input = True
        
        # Place the checker
        drop_result = drop_checker(board, col_index, current_checker)
        
        # This check should theoretically not be needed if is_valid_move is correct
        # but it's good practice for robustness.
        if drop_result is None:
            print("Error: Could not place checker. This should not happen if previous checks were correct.")
            continue

        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_connect_4()
