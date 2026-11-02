import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_index in range(num_cols):
        print(f"{chr(ord('A') + col_index)}   ", end="")
    print()

    # Print board content
    for row in board:
        print("+---" * num_cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * num_cols + "+")

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its corresponding 0-based index.

    Args:
        column_char (str): The character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return -1
    
    col_index = ord(column_char.upper()) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return -1

def is_valid_move(board, col_index):
    """
    Checks if a move to the given column is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the chosen column.

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
        col_index (int): The 0-based index of the chosen column.
        checker (str): The checker symbol to place.

    Returns:
        int: The row index where the checker was placed, or -1 if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r  # Return the row where the checker was placed
    return -1 # Column was full

def check_win(board, checker):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    
    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True
                
    return False

def check_draw(board):
    """
    Checks if the game is a draw (board is full).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # An empty space is found, not a draw yet
    return True  # Board is full, it's a draw

# --- Main Game Logic ---

def play_game():
    """
    Manages the Connect 4 game flow.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False
    winner_found = False

    while not game_over:
        print_board(board)
        
        col_char = ""
        col_index = -1
        
        # Input loop for current player
        while True:
            print(f"Player {current_player_checker}, please enter a column: ", end="")
            col_char = input().strip().upper()
            
            col_index = get_column_index(col_char, NUM_COLS)

            if col_index == -1:
                print("Invalid column. Please enter a letter from A to", chr(ord('A') + NUM_COLS - 1) + ".")
            elif not is_valid_move(board, col_index):
                print("This column is full. Please choose another column.")
            else:
                break # Valid input and valid move, exit input loop

        # Place the checker
        drop_checker(board, col_index, current_player_checker)

        # Check for win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        
        # Switch to the next player if the game is not over
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = PLAYER_CHECKERS[current_player_index]

# --- Entry Point ---
if __name__ == "__main__":
    play_game()
