import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
AVAILABLE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# --- Board Initialization ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board filled with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

# --- Board Display ---
def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows with checkers and separators
    for r in range(NUM_ROWS):
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

# --- Game Logic ---
def get_player_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = col_input[0]
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column '{col_char}'. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except IndexError:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")
        except TypeError:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available row of the given column.
    Returns True if placement was successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == ' ':
            board[r][col_index] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game by getting 4 checkers in a row
    (horizontally, vertically, or diagonally).
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (positive slope: /)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (negative slope: \)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # An empty space found, not a draw yet
    return True  # Board is full, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {AVAILABLE_CHECKERS[current_player_index]} starts the game!")

    game_over = False
    while not game_over:
        current_player_checker = AVAILABLE_CHECKERS[current_player_index]

        col_index = get_player_input(current_player_checker)

        if place_checker(board, col_index, current_player_checker):
            print_board(board)

            if check_win(board, current_player_checker):
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # The player does not lose their turn, they are asked again.

if __name__ == "__main__":
    main()
