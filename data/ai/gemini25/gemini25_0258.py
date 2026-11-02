import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS] # List of checkers based on NUM_PLAYERS

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console with column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    # Clear the screen for a fresh board display
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col in range(len(board[0])):
        print(f" {chr(ord('A') + col)} ", end="")
    print()

    # Print the board rows
    for row in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for col in range(len(board[0])):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print the bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

# --- Game Logic Functions ---

def get_column_input(current_player_checker, max_cols):
    """
    Prompts the current player for a column input and validates it.
    Keeps asking until a valid input (uppercase letter A-Z within bounds) is provided.

    Args:
        current_player_checker (str): The checker of the current player.
        max_cols (int): The maximum number of columns allowed (for input validation).

    Returns:
        int: The 0-indexed integer representation of the chosen column.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + max_cols - 1)):
                print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")
                continue
            
            col_index = ord(col_char) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")

def drop_checker(board, col_index, checker):
    """
    Drops the player's checker into the specified column.
    The checker occupies the lowest available space in that column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the given player (with 'checker') has won the game
    by having WIN_CONDITION checkers in a row horizontally, vertically, or diagonally.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal wins
    for r in range(rows):
        for c in range(cols - (WIN_CONDITION - 1)):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(cols):
        for r in range(rows - (WIN_CONDITION - 1)):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (positive slope: bottom-left to top-right)
    for r in range(rows - (WIN_CONDITION - 1)):
        for c in range(cols - (WIN_CONDITION - 1)):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (negative slope: top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, rows): # Start checking from row WIN_CONDITION-1
        for c in range(cols - (WIN_CONDITION - 1)):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full (draw), False otherwise.
    """
    for row in board:
        if " " in row: # If any empty space is found, it's not a draw
            return False
    return True # No empty spaces found, it's a draw

# --- Main Game Loop ---

def play_game():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles player turns, checks for wins and draws.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    print_board(board)

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]

        # Get and validate column input
        while True:
            col_input_index = get_column_input(current_player_checker, NUM_COLS)
            
            # Attempt to drop the checker
            if drop_checker(board, col_input_index, current_player_checker):
                break  # Valid move, exit input loop
            else:
                print(f"Column {chr(ord('A') + col_input_index)} is full. Please choose another column.")
                # Player does not lose turn, will be asked for new input

        print_board(board)

        # Check for win
        if check_win(board, current_player_checker):
            winner = current_player_checker
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# --- Entry Point ---

if __name__ == "__main__":
    play_game()
