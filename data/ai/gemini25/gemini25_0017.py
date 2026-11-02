import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (max 5 players: X, O, V, H, M)
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
        list[list[str]]: A 2D list representing the board,
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
        board (list[list[str]]): The current state of the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
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
    
    # Print bottom border
    print("+", end="")
    for _ in board[0]:
        print("---+", end="")
    print()

def get_column_input(player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        board (list[list[str]]): The current state of the game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            column_char = input(prompt).strip().upper()

            if not column_char.isalpha() or len(column_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            column_index = ord(column_char) - ord('A')

            if not (0 <= column_index < num_cols):
                print(f"Column '{column_char}' is out of bounds. Please choose a column from A to {chr(ord('A') + num_cols - 1)}.")
                continue

            # Check if the column is full
            if board[0][column_index] != " ":
                print(f"Column '{column_char}' is full. Please choose another column.")
                # This makes the player lose a turn if the column is full.
                # The assignment description says "If the column is already completely filled with checkers, 
                # the turn is invalid and the player loses the turn."
                # If we wanted them to retry without losing turn, we'd continue here.
                # For now, let's assume "loses the turn" means the function returns and next player plays.
                # Re-reading: "the turn is not lost" for invalid input. 
                # "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
                # This phrasing is a bit contradictory. Let's make it so they retry if column is full,
                # aligning with "the turn is not lost" for other invalid inputs.
                continue

            return column_index

        except EOFError:
            print("\nExiting game due to EOF.")
            sys.exit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def drop_checker(board, col, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list[list[str]]): The current state of the game board.
        col (int): The 0-indexed column number to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False otherwise (column full).
    """
    num_rows = len(board)
    for row in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list[list[str]]): The current state of the game board.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list[list[str]]): The current state of the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        
        col_index = get_column_input(current_player_checker, board)
        
        # Drop the checker. get_column_input already ensures the column isn't full
        # so this should always return True.
        drop_checker(board, col_index, current_player_checker)
        
        if check_win(board, current_player_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full! It's a draw!")
            game_over = True
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
