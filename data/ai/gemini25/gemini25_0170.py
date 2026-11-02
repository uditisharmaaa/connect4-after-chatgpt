import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for letter labels)
NUM_PLAYERS = 2  # Number of players (2 to 5)
WIN_LENGTH = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# A list containing the checkers for the active players
ACTIVE_PLAYER_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear screen before printing updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"  {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board with separators
    for row in board:
        print("+---" * len(row) + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= chr(ord('A') + NUM_COLS - 1):
                raise ValueError("Invalid column. Please enter a single letter within the board range.")
            
            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available row of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be placed.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    # Check if the column is within valid bounds
    if not (0 <= col_index < NUM_COLS):
        print(f"Error: Column {chr(ord('A') + col_index)} is out of board range.")
        return False

    # Find the lowest available row in the column
    for row_index in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = checker
            return True
    
    # If loop finishes, column is full
    print(f"Error: Column {chr(ord('A') + col_index)} is already full. Please choose another column.")
    return False

def check_win(board, checker):
    """
    Checks if the given player has won the game.
    A player wins if they have WIN_LENGTH checkers in a row horizontally, vertically, or diagonally.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal win
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical win
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal win (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal win (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
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
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

def main():
    """Main function to run the Connect 4 game."""

    # 1. Initialization
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False

    # 2. Game Phase
    while not game_over:
        current_player_checker = ACTIVE_PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        
        col_index = get_column_input(current_player_checker)

        # Attempt to place the checker
        if place_checker(board, col_index, current_player_checker):
            # Checker was placed successfully, now check for win/draw
            
            if check_win(board, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                # No win or draw, switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # If place_checker returned False (column full), the turn is lost and the loop
        # will restart asking the same player for input (as per assignment spec: "the turn is not lost").
        # If the spec meant "the turn is lost" for a full column, then the `else` block above
        # (switching players) would be placed directly after `if place_checker(...)`.
        # The current implementation correctly handles "the turn is not lost" for invalid inputs (including full column).


if __name__ == "__main__":
    main()
