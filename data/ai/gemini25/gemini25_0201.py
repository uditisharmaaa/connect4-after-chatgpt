import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print the board content
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[r])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number if valid.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(user_input) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("Invalid input. Please try again.")

def drop_checker(board, col, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.
    Checks for horizontal, vertical, and diagonal wins.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == " ":
                return False  # There's an empty space
    return True # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        current_player_checker = PLAYERS[current_player_index]

        col_input = get_column_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_input, current_player_checker):
            # Check for win after successful drop
            if check_win(board, current_player_checker):
                print_board(board) # Print final board with win
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board) # Print final board for draw
                print("The board is full. It's a draw!")
                game_over = True
            else:
                # Switch to next player if no win or draw
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Column is full! Please choose another column.")
            # Player does not lose turn if column is full, they just retry.
            # The assignment says "the turn is invalid and the player loses the turn"
            # but then "the player will be asked to provide another input until the input is valid (the turn is not lost)"
            # This implementation keeps the turn for the player to re-enter a column.
            # If the strict interpretation of "loses the turn" is preferred, remove the 'else' block
            # and simply let the loop continue with the same player_index.
            # For simplicity and user experience, we'll let them re-enter.

if __name__ == "__main__":
    play_game()
