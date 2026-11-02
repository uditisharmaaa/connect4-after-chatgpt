import os
import random
import string

# --- Constants (Global Variables for game configuration) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players (up to 5 players)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print board content
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_player_input(player_checker, board):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol for the current player.
        board (list): The 2D list representing the game board.

    Returns:
        int: The 0-based index of the chosen column.
    """
    num_cols = len(board[0])
    valid_columns = string.ascii_uppercase[:num_cols]

    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_input) != 1 or col_input not in valid_columns:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                continue

            col_index = ord(col_input) - ord('A')
            if not (0 <= col_index < num_cols):
                print(f"Invalid column. Please choose a column between A and {valid_columns[-1]}.")
                continue

            # Check if the column is full
            if board[0][col_index] != ' ':
                print("That column is full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a letter.")

def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the lowest available spot in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        tuple: A tuple (row, col) of the new checker's position, or None if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = player_checker
            return r, col_index
    return None # Should not happen if input validation is correct

def check_win(board, row, col, player_checker):
    """
    Checks if the current player has won after placing a checker at (row, col).

    Args:
        board (list): The 2D list representing the game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(max(0, col - (WIN_CONDITION - 1)), min(num_cols, col + WIN_CONDITION)):
        if c < num_cols and board[row][c] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r_idx in range(max(0, row - (WIN_CONDITION - 1)), min(num_rows, row + WIN_CONDITION)):
        if r_idx < num_rows and board[r_idx][col] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    for i in range(-(WIN_CONDITION - 1), WIN_CONDITION):
        r_idx, c_idx = row + i, col + i
        if 0 <= r_idx < num_rows and 0 <= c_idx < num_cols and board[r_idx][c_idx] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-right to bottom-left)
    count = 0
    for i in range(-(WIN_CONDITION - 1), WIN_CONDITION):
        r_idx, c_idx = row + i, col - i
        if 0 <= r_idx < num_rows and 0 <= c_idx < num_cols and board[r_idx][c_idx] == player_checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_game():
    """
    Manages the main Connect 4 game loop.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)

        col_to_drop = get_player_input(current_player_checker, board)
        
        # Drop the checker and get its position
        row_placed, col_placed = drop_checker(board, col_to_drop, current_player_checker)

        if check_win(board, row_placed, col_placed, current_player_checker):
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board) # Print final board
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# --- Start the game ---
if __name__ == "__main__":
    play_game()
