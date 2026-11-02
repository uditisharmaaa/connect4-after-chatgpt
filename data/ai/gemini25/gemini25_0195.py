import os
import random
import sys

# --- Global Constants (Editable for different game configurations) ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_CONDITION = 4  # Number of checkers in a row to win
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

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
    print("  " + "   ".join([chr(ord('A') + i) for i in range(num_cols)]))

    # Print board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")

def get_player_input(current_player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board (list): The game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (A-Z).")
                continue

            col_index = ord(user_input) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Invalid column. Please enter a column between A and {chr(ord('A') + num_cols - 1)}.")
                continue

            if board[0][col_index] != " ":
                print("That column is full. Please choose another column.")
                continue

            return col_index
        except KeyboardInterrupt:
            print("\nGame ended by player. Goodbye!")
            sys.exit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available row of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be placed.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Should not be reached if validation is done correctly before calling

def check_win(board, checker):
    """
    Checks if the given player (checker) has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check.

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
    for c in range(num_cols):
        for r in range(num_rows - WIN_CONDITION + 1):
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
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles player turns, checks for wins/draws.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randrange(NUM_PLAYERS)
    
    # Game loop
    while True:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)
        
        col_index = get_player_input(current_player_checker, board)
        
        # Place checker (validation ensures it's always placed in a valid spot)
        place_checker(board, col_index, current_player_checker)

        # Check for win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
