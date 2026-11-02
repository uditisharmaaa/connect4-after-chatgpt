import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for col_idx in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + col_idx)} ")
    sys.stdout.write("\n")

    # Print board content
    for r in range(len(board)):
        sys.stdout.write("+")
        for _ in range(len(board[0])):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for c in range(len(board[0])):
            sys.stdout.write(f" {board[r][c]} |")
        sys.stdout.write("\n")

    # Print bottom border
    sys.stdout.write("+")
    for _ in range(len(board[0])):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('clear')

# --- Game Logic ---

def get_player_input(player_name, board):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    num_cols = len(board[0])
    while True:
        try:
            col_input = input(f"Player {player_name}, please enter a column: ").upper()
            if not col_input:
                raise ValueError("Input cannot be empty.")

            col_index = ord(col_input) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
                continue

            # Check if column is full
            if board[0][col_index] != " ":
                print("That column is full. Please choose another column.")
                continue

            return col_index
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a single letter for the column.")
        except TypeError:
            print("Invalid input. Please enter a single letter for the column.")
        except Exception:
            print("An unexpected error occurred. Please enter a single letter for the column.")


def drop_checker(board, col, player_checker):
    """
    Places the player's checker in the lowest available row of the given column.
    Returns True if the checker was placed, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True
    return False # Column is full (should be caught by get_player_input, but good for safety)

def check_win(board, player_checker, connect_n=4):
    """
    Checks if the current player has won the game by getting `connect_n` checkers
    in a row, column, or diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - connect_n + 1):
            if all(board[r][c + i] == player_checker for i in range(connect_n)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - connect_n + 1):
            if all(board[r + i][c] == player_checker for i in range(connect_n)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - connect_n + 1):
        for c in range(num_cols - connect_n + 1):
            if all(board[r + i][c + i] == player_checker for i in range(connect_n)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(connect_n - 1, num_rows):
        for c in range(num_cols - connect_n + 1):
            if all(board[r - i][c + i] == player_checker for i in range(connect_n)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found

# --- Main Game Loop ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Player {CHECKERS[current_player_idx]} starts first!")

    while not game_over:
        player_checker = CHECKERS[current_player_idx]

        # Get and validate player input
        chosen_col = get_player_input(player_checker, board)

        # Place the checker
        drop_checker(board, chosen_col, player_checker)

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, player_checker):
            winner_checker = player_checker
            game_over = True
        # Check for draw
        elif check_draw(board):
            game_over = True
            print("The board is full! It's a draw!")
        else:
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    if winner_checker:
        print(f"Player {winner_checker} won!")
    print("Game over. Thanks for playing!")


if __name__ == "__main__":
    play_connect_4()
