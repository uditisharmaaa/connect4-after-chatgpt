import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns for letter labels
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_CONDITION = 4

# --- Global Variables ---
board = []
players = []
current_player_index = 0

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def initialize_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def initialize_players():
    """Initializes the players with their respective checkers."""
    global players
    players = CHECKERS[:NUM_PLAYERS]

def print_board():
    """Prints the Connect 4 board to the console."""
    clear_screen()

    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for col in range(NUM_COLS):
        print(f" {chr(ord('A') + col)} ", end="")
    print()

    # Print board rows
    for row in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for col in range(NUM_COLS):
            print(f" {board[row][col]} |", end="")
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
            col_char = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Column '{col_char}' is out of bounds. Please enter a column between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            # Check if column is full
            if board[0][col_index] != ' ':
                print(f"Column '{col_char}' is full. Please choose another column.")
                continue

            return col_index
        except Exception:
            print("Invalid input. Please try again.")

def drop_checker(col_index, checker):
    """
    Drops the checker into the specified column.
    Returns the row index where the checker landed, or -1 if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1 # Column is full (should be caught by get_column_input, but good for safety)

def check_win(row, col, checker):
    """Checks if the current player has won after placing a checker at (row, col)."""

    # Check horizontal win
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical win
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < NUM_ROWS and c < NUM_COLS:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Check diagonal (top-right to bottom-left)
    count = 0
    start_row = row - min(row, NUM_COLS - 1 - col)
    start_col = col + min(row, NUM_COLS - 1 - col)
    r, c = start_row, start_col
    while r < NUM_ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c -= 1

    return False

def check_draw():
    """Checks if the board is full, indicating a draw."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == ' ':
                return False  # Board is not full
    return True  # Board is full

def main():
    """Main function to run the Connect 4 game."""
    global current_player_index

    initialize_board()
    initialize_players()

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner = None

    while not game_over:
        current_checker = players[current_player_index]
        print_board()

        col_to_drop = get_column_input(current_checker)
        row_landed = drop_checker(col_to_drop, current_checker)

        if row_landed != -1: # Successfully dropped checker
            if check_win(row_landed, col_to_drop, current_checker):
                print_board()
                winner = current_checker
                game_over = True
            elif check_draw():
                print_board()
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # If row_landed == -1, the column was full, and get_column_input already prompted for re-entry.
        # So the turn is not lost, and current_player_index does not change.

    print_board() # Print final board
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
