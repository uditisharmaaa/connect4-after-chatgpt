import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows in the board.
        cols (int): The number of columns in the board.

    Returns:
        list[list[str]]: A 2D list representing the board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list[list[str]]): The current state of the board.
    """
    clear_screen()

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))

    # Print top border
    print("+" + "---+".join(["" for _ in range(len(board[0]))]) + "---")

    # Print board rows
    for r in range(len(board)):
        row_str = "|"
        for c in range(len(board[r])):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+".join(["" for _ in range(len(board[0]))]) + "---")

def get_valid_column_input(current_player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        board (list[list[str]]): The current state of the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    num_cols = len(board[0])
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not col_char:
                print("Invalid input: Column cannot be empty. Please enter a letter from A to "
                      f"{COLUMN_LABELS[num_cols - 1]}.")
                continue

            if len(col_char) > 1:
                print("Invalid input: Please enter only one letter for the column.")
                continue

            if col_char not in COLUMN_LABELS[:num_cols]:
                print(f"Invalid input: Column '{col_char}' is out of board range. "
                      f"Please enter a letter from A to {COLUMN_LABELS[num_cols - 1]}.")
                continue

            col_index = COLUMN_LABELS.index(col_char)

            # Check if the column is full
            if board[0][col_index] != " ":
                print("Invalid move: This column is already full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print("Invalid input: Please enter a letter from A to "
                  f"{COLUMN_LABELS[num_cols - 1]}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space of the specified column.

    Args:
        board (list[list[str]]): The current state of the board.
        col_index (int): The 0-indexed column number to drop the checker into.
        checker (str): The checker symbol ('X', 'O', etc.) to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full (should be caught by validation earlier, but good for robustness)

def check_win(board, checker, win_condition):
    """
    Checks if the given player has won the game.

    Args:
        board (list[list[str]]): The current state of the board.
        checker (str): The checker symbol ('X', 'O', etc.) to check for.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check positively sloped diagonal (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check negatively sloped diagonal (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list[list[str]]): The current state of the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_COLS > 26:
        print("Error: Maximum 26 columns supported due to A-Z labeling.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)
    if WIN_CONDITION > NUM_ROWS and WIN_CONDITION > NUM_COLS:
        print("Warning: Win condition is greater than both rows and columns. A win might be impossible.")

    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner = None

    print_board(board)
    print(f"Starting game with {NUM_PLAYERS} players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} starts!")

    while not game_over:
        current_player_checker = players[current_player_index]

        # Get valid column input
        col_index = get_valid_column_input(current_player_checker, board)

        # Drop the checker
        drop_checker(board, col_index, current_player_checker)

        # Print the updated board
        print_board(board)

        # Check for a win
        if check_win(board, current_player_checker, WIN_CONDITION):
            winner = current_player_checker
            game_over = True
        # Check for a draw if no one won
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End of game messages
    print("\n--- Game Over ---")
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
