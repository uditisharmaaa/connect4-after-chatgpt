import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board filled with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def get_column_label(col_index):
    """
    Converts a column index (0-based) to an uppercase letter (A-Z).
    Handles up to 26 columns.
    """
    if col_index < 0 or col_index >= 26:
        raise ValueError("Column index out of valid range (0-25)")
    return chr(ord('A') + col_index)

def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board.
    """
    os.system('clear')  # Clear the console screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f" {get_column_label(col_idx)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        # Print row separator
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

# --- Game Logic ---

def get_player_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-based column index.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Invalid column. Please enter a column between A and {get_column_label(num_cols - 1)}.")
                continue

            return col_index
        except Exception:
            print("An unexpected error occurred during input. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True, row_index, col_index  # Return success and placement coordinates
    return False, -1, -1  # Column is full

def check_win(board, checker, last_row, last_col, win_condition):
    """
    Checks if the last placed checker resulted in a win (horizontal, vertical, or diagonal).
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(cols):
        if board[last_row][c] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(rows):
        if board[r][last_col] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check positive slope diagonal (bottom-left to top-right)
    # Start at the actual last_row, last_col and move to the bottom-left edge of the diagonal
    temp_row, temp_col = last_row, last_col
    while temp_row < rows - 1 and temp_col > 0:
        temp_row += 1
        temp_col -= 1
    
    count = 0
    while temp_row >= 0 and temp_col < cols:
        if board[temp_row][temp_col] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0
        temp_row -= 1
        temp_col += 1

    # Check negative slope diagonal (top-left to bottom-right)
    # Start at the actual last_row, last_col and move to the top-left edge of the diagonal
    temp_row, temp_col = last_row, last_col
    while temp_row > 0 and temp_col > 0:
        temp_row -= 1
        temp_col -= 1

    count = 0
    while temp_row < rows and temp_col < cols:
        if board[temp_row][temp_col] == checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0
        temp_row += 1
        temp_col += 1

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # There's an empty space
    return True  # Board is full

# --- Main Game Flow ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randrange(NUM_PLAYERS)  # Randomly choose first player

    game_over = False
    last_placed_row, last_placed_col = -1, -1

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        col_input_valid = False
        while not col_input_valid:
            chosen_col_index = get_player_input(current_player_checker, NUM_COLS)
            
            placed, last_placed_row, last_placed_col = drop_checker(board, chosen_col_index, current_player_checker)
            if not placed:
                print(f"Column {get_column_label(chosen_col_index)} is full. Please choose another column.")
                # Player does NOT lose turn for a full column, they must choose again.
            else:
                col_input_valid = True

        # After a valid placement, check for win or draw
        if check_win(board, current_player_checker, last_placed_row, last_placed_col, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Exiting.")
        sys.exit(0)
