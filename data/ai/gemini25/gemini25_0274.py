import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for letter labels)
NUM_PLAYERS = 2  # Number of players (between 2 and 5)
WIN_LENGTH = 4  # Number of checkers needed in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# The actual checkers used for the game based on NUM_PLAYERS
GAME_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
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
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear the screen before printing the updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(NUM_COLS):
        print(f" {chr(ord('A') + col_index)} ", end=" ")
    print()

    # Print the board with separators
    for row_index in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for col_index in range(NUM_COLS):
            print(f" {board[row_index][col_index]} |", end="")
        print()
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def get_player_input(current_player_index):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_index (int): The index of the current player.

    Returns:
        int: The 0-based index of the chosen column.
    """
    player_checker = GAME_CHECKERS[current_player_index]
    while True:
        try:
            column_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if not column_input.isalpha() or len(column_input) != 1:
                raise ValueError("Invalid input. Please enter a single letter (A-G).")

            column_index = ord(column_input) - ord('A')

            if not (0 <= column_index < NUM_COLS):
                raise ValueError(f"Column '{column_input}' is out of bounds. Please enter a column between A and {chr(ord('A') + NUM_COLS - 1)}.")

            return column_index
        except ValueError as e:
            print(f"Error: {e}")

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space of the chosen column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to place the checker.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    game_over = False
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)

    while not game_over:
        player_checker = GAME_CHECKERS[current_player_index]

        # Get and validate player input
        col_index = get_player_input(current_player_index)

        # Place the checker
        if place_checker(board, col_index, player_checker):
            print_board(board)  # Print board only if checker was placed successfully

            # Check for win
            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                game_over = True
            # Check for draw if no win
            elif check_draw(board):
                print("It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # If column was full, inform the player and let them try again (same turn)
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Do not change current_player_index, the player gets to try again

if __name__ == "__main__":
    play_connect_4()
