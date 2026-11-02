import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
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

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for i in range(NUM_COLS):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print the board with separators
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        for c in range(NUM_COLS):
            print(f"| {board[r][c]} ", end="")
        print("|")
    print("+---" * NUM_COLS + "+")

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            if not user_input:
                print("Invalid input: Please enter a column letter (e.g., A).")
                continue

            # Convert column letter to 0-indexed integer
            col_index = ord(user_input[0]) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid input: Column '{user_input}' is out of bounds. Please choose between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return col_index
        except (ValueError, IndexError):
            print("Invalid input: Please enter a single uppercase letter for the column (e.g., A).")


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check ascending diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check descending diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
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
                return False  # An empty space found, game is not a draw yet
    return True  # No empty spaces, board is full

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers for the specified number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly choose the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False

    while not game_over:
        current_player_checker = player_checkers[current_player_index]
        
        print_board(board)
        
        # Get and validate player input
        valid_move = False
        while not valid_move:
            col_index = get_column_input(current_player_checker)
            if drop_checker(board, col_index, current_player_checker):
                valid_move = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
        
        print_board(board) # Print board after valid move

        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    play_game()
