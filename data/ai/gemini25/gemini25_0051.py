import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

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
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

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
    for i in range(num_cols):
        print(f"{string.ascii_uppercase[i]}   ", end="")
    print("\n" + "+---" * num_cols + "+")

    # Print board rows
    for r in range(len(board)):
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print("\n" + "+---" * num_cols + "+")

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
            if len(col_char) != 1 or not 'A' <= col_char <= string.ascii_uppercase[num_cols - 1]:
                raise ValueError
            
            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError:
            print(f"Invalid input. Please enter a single letter from A to {string.ascii_uppercase[num_cols - 1]}.")

def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has achieved a winning condition (4 in a row).

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
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Manages the main Connect 4 game flow.
    """
    # Initialization
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker, NUM_COLS)

        if not drop_checker(board, col_index, current_player_checker):
            print(f"Column {string.ascii_uppercase[col_index]} is full! Player {current_player_checker} loses their turn.")
            # Player does not lose turn, they are prompted again.
            # The prompt is handled by the loop in get_column_input.
            # However, the assignment states "If the column is already completely filled with checkers, 
            # the turn is invalid and the player loses the turn."
            # So, if drop_checker returns False, we should proceed to the next player.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue # Skip win/draw check for this invalid move

        if check_win(board, current_player_checker):
            print_board(board)
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board) # Print final board state

    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()
