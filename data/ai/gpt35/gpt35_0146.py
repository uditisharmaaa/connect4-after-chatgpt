import os
import random

# Constants for the board dimensions and players
ROWS = 6                # Number of rows in the board
COLUMNS = 7             # Number of columns in the board (max 26)
NUM_PLAYERS = 2         # Number of players (between 2 and 5)
WIN_CONDITION = 4       # Number of checkers in a row needed to win

# Player checkers in order; slice according to NUM_PLAYERS
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """
    Create and return a 2D board initialized with spaces.
    Board is ROWS x COLUMNS dimension.
    """
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """
    Print the current board status with column labels.
    The board rows are printed from top to bottom (0th index is top).
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    labels = [chr(ord("A") + i) for i in range(COLUMNS)]
    print("  " + "   ".join(labels))

    # Print rows with separators
    horizontal_line = "+" + "---+" * COLUMNS
    for row in board:
        print(horizontal_line)
        # Each cell surrounded by |, fill with checker or empty space
        print("| " + " | ".join(row) + " |")
    print(horizontal_line)

def get_valid_column_input(board, player_checker):
    """
    Prompt the current player to input a valid column letter.
    Performs input validation:
      - input should be 1 letter
      - representing a valid column (A to corresponding letter)
    Returns the column index (0-based) if valid.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input: please enter exactly one letter corresponding to a column.")
            continue
        if not ('A' <= user_input <= chr(ord('A') + COLUMNS - 1)):
            print(f"Invalid input: please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        col = ord(user_input) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Column full - player loses this turn
            print(f"Column {user_input} is full. You lose your turn.")
            return None
        return col

def place_checker(board, col, player_checker):
    """
    Place the player_checker in the given column.
    Checker falls to lowest empty row in that column.
    """
    # Start from bottom row upwards to find empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row, col  # Return position placed
    # Should not reach here because we check for full column before placing
    return None

def check_win(board, player_checker, last_row, last_col):
    """
    Check if the player_checker has 4 in a row on the board including the last move.
    Check horizontal, vertical and both diagonal directions.
    Returns True if player won, False otherwise.
    """

    def count_consecutive(r_step, c_step):
        """
        Count consecutive checkers in direction (r_step, c_step) and its opposite.
        Includes last placed position.
        """
        count = 1  # Count the last placed checker itself

        # Check one direction
        r, c = last_row + r_step, last_col + c_step
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r += r_step
            c += c_step

        # Check opposite direction
        r, c = last_row - r_step, last_col - c_step
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r -= r_step
            c -= c_step
        
        return count

    # Directions to check: horizontal (0,1), vertical (1,0), diagonal1 (1,1), diagonal2 (1,-1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r_step, c_step in directions:
        if count_consecutive(r_step, c_step) >= WIN_CONDITION:
            return True
    return False

def is_board_full(board):
    """
    Checks if the board is full (no empty spaces).
    Returns True if full, False otherwise.
    """
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    # Initialize board
    board = create_board()

    # Randomly select first player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        player_checker = PLAYER_CHECKERS[current_player_index]

        col = get_valid_column_input(board, player_checker)
        # If player loses turn due to full column, skip placing checker and switch player
        if col is None:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place the checker
        last_row, last_col = place_checker(board, col, player_checker)

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, player_checker, last_row, last_col):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
