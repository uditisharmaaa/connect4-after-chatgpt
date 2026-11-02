import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns for letter labels
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# --- Global Variables ---
board = []
current_player_index = 0

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty cells."""
    global board
    board = [[EMPTY_CELL for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(NUM_COLS):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board rows
    for row in board:
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            if len(user_input) != 1 or not 'A' <= user_input <= chr(ord('A') + NUM_COLS - 1):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            col_index = ord(user_input) - ord('A')

            if board[0][col_index] != EMPTY_CELL:
                print(f"Column {user_input} is full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full (though validation should prevent this).
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == EMPTY_CELL:
            board[row_index][col_index] = player_checker
            return True
    return False # Should not be reached with proper input validation

def check_win(player_checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False

def check_draw():
    """Checks if the board is full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

# --- Main Game Logic ---

def main():
    global current_player_index

    available_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False

    while not game_over:
        print_board()

        current_player_checker = available_checkers[current_player_index]
        
        col = get_column_input(current_player_checker)
        drop_checker(col, current_player_checker)

        if check_win(current_player_checker):
            print_board()
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw():
            print_board()
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
