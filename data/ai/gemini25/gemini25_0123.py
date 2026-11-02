import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]


# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for col_idx in range(len(board[0])):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print board rows
    for row_idx in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for col_idx in range(len(board[0])):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()


def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its integer index.
    Returns -1 for invalid characters.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return -1
    
    col_char_upper = column_char.upper()
    if 'A' <= col_char_upper <= chr(ord('A') + num_cols - 1):
        return ord(col_char_upper) - ord('A')
    return -1


def drop_checker(board, col_idx, checker):
    """
    Drops a checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_idx in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False


def is_board_full(board):
    """
    Checks if the board is completely filled (draw condition).
    """
    for col_idx in range(len(board[0])):
        if board[0][col_idx] == " ":  # Check if the top row of any column is empty
            return False
    return True


# --- Win Condition Checks ---
def check_win(board, checker):
    """
    Checks if the given checker has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(WIN_SEQUENCE_LENGTH - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False


# --- Game Loop ---
def main():
    """
    Main function to run the Connect 4 game.
    """
    # Validate constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= NUM_COLS <= 26):
        print("Error: NUM_COLS must be between 1 and 26 (A-Z).")
        return
    if not (1 <= NUM_ROWS):
        print("Error: NUM_ROWS must be at least 1.")
        return
    if not (1 <= WIN_SEQUENCE_LENGTH <= max(NUM_ROWS, NUM_COLS)):
        print("Error: WIN_SEQUENCE_LENGTH is invalid for current board dimensions.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = players[current_player_idx]
        print_board(board)
        
        valid_input = False
        while not valid_input:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input. Please enter a single letter (e.g., 'A', 'B').")
                continue

            col_idx = get_column_index(user_input, NUM_COLS)
            
            if col_idx == -1:
                print(f"Invalid column. Please enter a letter between 'A' and '{chr(ord('A') + NUM_COLS - 1)}'.")
            elif not drop_checker(board, col_idx, current_checker):
                print(f"Column {user_input} is full. Please choose another column.")
            else:
                valid_input = True
        
        # After a valid move, check for win or draw
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif is_board_full(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
