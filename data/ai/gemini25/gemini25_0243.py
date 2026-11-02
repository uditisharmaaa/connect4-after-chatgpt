import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f"  {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print the board
    for row_idx in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for col_idx in range(len(board[0])):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    
    # Print the bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()


# --- Game Logic Functions ---
def get_player_input(current_player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., 'A').")
                continue

            col_char = user_input[0]
            col_idx = ord(col_char) - ord('A')

            if not (0 <= col_idx < board_cols):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + board_cols - 1)}.")
                continue

            return col_idx
        except Exception:
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_idx, checker):
    """
    Drops the checker into the specified column.
    Returns True if the checker was placed successfully, False otherwise (column full).
    """
    for row_idx in range(len(board) - 1, -1, -1):  # Iterate from bottom row up
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True, row_idx, col_idx  # Return True and position of dropped checker
    return False, -1, -1  # Column is full


def check_win(board, last_row, last_col, checker):
    """
    Checks if the last placed checker resulted in a win (4 in a row).
    Checks horizontally, vertically, and both diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(cols):
        if board[last_row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(rows):
        if board[r][last_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check positive diagonal (top-left to bottom-right)
    # Start point (row, col) for potential win lines
    for start_r in range(rows - WIN_CONDITION + 1):
        for start_c in range(cols - WIN_CONDITION + 1):
            diag_count = 0
            for i in range(WIN_CONDITION):
                if board[start_r + i][start_c + i] == checker:
                    diag_count += 1
                else:
                    diag_count = 0 # Reset if current one breaks the sequence
                if diag_count >= WIN_CONDITION:
                    return True

    # Check negative diagonal (bottom-left to top-right)
    # Start point (row, col) for potential win lines
    for start_r in range(WIN_CONDITION - 1, rows):
        for start_c in range(cols - WIN_CONDITION + 1):
            diag_count = 0
            for i in range(WIN_CONDITION):
                if board[start_r - i][start_c + i] == checker:
                    diag_count += 1
                else:
                    diag_count = 0 # Reset if current one breaks the sequence
                if diag_count >= WIN_CONDITION:
                    return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # An empty space found, game is not a draw yet
    return True  # No empty spaces, board is full


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)
        
        col_to_drop = get_player_input(current_player_checker, NUM_COLS)
        
        placed, last_row, last_col = drop_checker(board, col_to_drop, current_player_checker)
        
        if not placed:
            print(f"Column {chr(ord('A') + col_to_drop)} is full. Player {current_player_checker} loses their turn!")
            # The assignment states "the turn is not lost" for invalid input,
            # but for a full column, it states "the player loses the turn."
            # So, we advance the player here. If the intent was to re-ask,
            # this logic would need to change.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            input("Press Enter to continue...") # Pause to allow user to read message
            continue

        print_board(board) # Print board after checker is placed

        if check_win(board, last_row, last_col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        
        if game_over:
            input("Press Enter to exit.") # Pause before exiting

if __name__ == "__main__":
    main()
