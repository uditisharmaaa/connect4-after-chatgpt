import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty game board with specified dimensions."""
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"   {chr(ord('A') + col_index)}", end="")
    print()

    # Print board content
    for row_index in range(len(board)):
        print(" ", end="")
        print("+---" * len(board[0]) + "+")
        print("|", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()
    print(" ", end="")
    print("+---" * len(board[0]) + "+")

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-based column index.
    """
    while True:
        try:
            col_letter = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not col_letter.isalpha() or len(col_letter) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_letter) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Column '{col_letter}' is out of bounds. Please choose a column between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except Exception:
            print("Invalid input. Please enter a single letter.")

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available row of the specified column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the current player (with 'checker') has won the game
    by checking horizontal, vertical, and diagonal lines.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """Checks if the board is completely full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # There's an empty space, not a draw yet
    return True  # Board is full

# --- Main Game Logic ---

def main():
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)

        col_index = get_column_input(current_player_checker)

        if place_checker(board, col_index, current_player_checker):
            # Checker was placed, now check for win or draw
            if check_win(board, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Game continues, switch to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = CHECKERS[current_player_index]
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # The player does not lose their turn if the column is full,
            # so we just let the loop repeat with the same player.

if __name__ == "__main__":
    main()
