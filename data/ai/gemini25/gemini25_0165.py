import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Board Initialization ---
def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" "] * cols for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board to the console."""
    os.system('clear')  # Clear the screen

    # Print column labels
    col_labels = string.ascii_uppercase[:NUM_COLS]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

# --- Game Logic ---
def get_player_input(current_player_checker, board):
    """Gets and validates player input for a column choice."""
    col_labels = string.ascii_uppercase[:NUM_COLS]

    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(user_input) != 1 or user_input not in col_labels:
                raise ValueError("Invalid input. Please enter a single uppercase letter (e.g., A, B).")

            col_index = col_labels.index(user_input)
            if board[0][col_index] != " ":
                raise ValueError("Column is full. Please choose another column.")

            return col_index
        except ValueError as e:
            print(f"Error: {e}")

def drop_checker(board, col_index, checker):
    """Drops the checker into the lowest available spot in the column."""
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r, col_index  # Return success and position
    return False, -1, -1 # Should not happen if validation is correct

def check_win(board, checker, last_row, last_col):
    """Checks if the last placed checker resulted in a win."""

    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[last_row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][last_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    # Start at the top-leftmost cell of the potential diagonal
    start_row = last_row - min(last_row, last_col)
    start_col = last_col - min(last_row, last_col)
    count = 0
    while start_row < NUM_ROWS and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    # Check diagonal (top-right to bottom-left)
    # Start at the top-rightmost cell of the potential diagonal
    start_row = last_row - min(last_row, NUM_COLS - 1 - last_col)
    start_col = last_col + min(last_row, NUM_COLS - 1 - last_col)
    count = 0
    while start_row < NUM_ROWS and start_col >= 0:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col -= 1

    return False

def check_draw(board):
    """Checks if the board is full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Loop ---
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly choose first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)

        col_index = get_player_input(current_player_checker, board)
        
        # Drop checker and get its position
        placed, last_row, last_col = drop_checker(board, col_index, current_player_checker)

        if placed:
            if check_win(board, current_player_checker, last_row, last_col):
                winner_checker = current_player_checker
                game_over = True
            elif check_draw(board):
                game_over = True
            else:
                # Switch to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # If not placed (column was full), the turn is lost due to validation design.
        # The prompt says: "If the column is already completely filled with checkers,
        # the turn is invalid and the player loses the turn."
        # This implies `get_player_input` should handle this, and if it returns a valid col,
        # it *will* be placed. The `drop_checker` should always return True if `get_player_input`
        # is implemented correctly to prevent full columns.

    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
