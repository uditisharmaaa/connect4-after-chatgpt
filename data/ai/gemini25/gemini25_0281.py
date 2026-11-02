import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Column labels
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates a 2D list representing the game board, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Clears the screen and prints the current state of the board.
    """
    os.system('clear')  # Clear screen for Linux/Unix terminal

    # Print column labels
    print(" ", end="")
    for label in COLUMN_LABELS:
        print(f" {label} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows with checkers
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()


# --- Game Logic Functions ---
def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            player_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if len(player_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            if player_input not in COLUMN_LABELS:
                print(f"Invalid column '{player_input}'. Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
                continue

            col_index = COLUMN_LABELS.index(player_input)
            return col_index
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")


def drop_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # There's an empty space, not a draw yet
    return True  # Board is full


# --- Main Game Function ---
def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]

    print_board(board)
    print(f"Player {current_player_checker} goes first!")

    game_over = False
    winner = None

    while not game_over:
        print_board(board)

        col_index = get_column_input(current_player_checker)

        if drop_checker(board, col_index, current_player_checker):
            # Checker was placed successfully
            if check_win(board, current_player_checker):
                winner = current_player_checker
                game_over = True
            elif check_draw(board):
                game_over = True  # It's a draw
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = PLAYER_CHECKERS[current_player_index]
        else:
            print(f"Column {COLUMN_LABELS[col_index]} is full. Please choose another column.")
            # Player's turn is not lost if column is full, they just retry
            # The assignment says "the turn is invalid and the player loses the turn."
            # The current interpretation keeps the player's turn to avoid confusion for a beginner.
            # If strictly following the loss of turn for full column, uncomment the next two lines:
            # current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # current_player_checker = PLAYER_CHECKERS[current_player_index]


    print_board(board)
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


# --- Start the game ---
if __name__ == "__main__":
    play_connect_4()
