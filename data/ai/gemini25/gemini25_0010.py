import os
import random
import sys

# --- Global Constants ---
# Board dimensions (can be changed, max 26 columns)
NUM_ROWS = 6
NUM_COLS = 7

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers in a row to win
CONNECT_N = 4

# --- Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    # Clear the terminal screen
    os.system('clear')

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for col_idx in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + col_idx)} ")
    sys.stdout.write("\n")

    # Print top border
    sys.stdout.write("+")
    for _ in range(len(board[0])):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

    # Print rows with checkers and borders
    for row in board:
        sys.stdout.write("|")
        for cell in row:
            sys.stdout.write(f" {cell} |")
        sys.stdout.write("\n")
        # Print row separator
        sys.stdout.write("+")
        for _ in range(len(board[0])):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

def get_player_move(player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        board_cols (int): The total number of columns on the board.

    Returns:
        int: The validated column index (0-based) where the player wants to drop the checker.
    """
    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            # Check if input is a single uppercase letter
            if len(col_input) != 1 or not ('A' <= col_input[0] <= chr(ord('A') + board_cols - 1)):
                print(f"Invalid input. Please enter a single letter between A and {chr(ord('A') + board_cols - 1)}.")
                continue

            # Convert letter to 0-based column index
            col_index = ord(col_input[0]) - ord('A')
            return col_index

        except ValueError:
            print("Invalid input. Please enter a letter corresponding to a column.")
        except IndexError:
            # This catch might be redundant due to the 'len(col_input) != 1' check
            print("Invalid input. Please enter a letter.")

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    # Iterate from the bottom row upwards
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = player_checker
            return True, row_idx, col_index  # Return success and the position of the dropped checker
    return False, -1, -1 # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the given player has won the game after their last move.
    It checks horizontally, vertically, and both diagonals from the last dropped checker's position.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check for a win.
        last_row (int): The row index where the last checker was dropped.
        last_col (int): The column index where the last checker was dropped.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a specific direction
    def check_direction(dr, dc):
        count = 0
        # Check in one direction
        for i in range(-CONNECT_N + 1, CONNECT_N):
            r, c = last_row + i * dr, last_col + i * dc
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
                if count >= CONNECT_N:
                    return True
            else:
                count = 0  # Reset count if the checker is not ours or out of bounds
        return False

    # Check horizontally (dr=0, dc=1)
    if check_direction(0, 1):
        return True

    # Check vertically (dr=1, dc=0)
    if check_direction(1, 0):
        return True

    # Check diagonally (top-left to bottom-right, dr=1, dc=1)
    if check_direction(1, 1):
        return True

    # Check anti-diagonally (top-right to bottom-left, dr=1, dc=-1)
    if check_direction(1, -1):
        return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full (draw), False otherwise.
    """
    for row in board:
        if " " in row:
            return False  # Found an empty space, game is not a draw yet
    return True  # No empty spaces found, board is full

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")

    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = CHECKERS[current_player_idx]
        print_board(board)
        print(f"It's Player {current_checker}'s turn.")

        col_index = get_player_move(current_checker, NUM_COLS)

        # Drop the checker and validate column is not full
        success, last_row, last_col = drop_checker(board, col_index, current_checker)

        if not success:
            print("That column is full. Please choose another column.")
            # The turn is not lost, the current player tries again
            continue

        # Check for a win after dropping the checker
        if check_win(board, current_checker, last_row, last_col):
            print_board(board)
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # End of game messages
    print_board(board) # Print final board one last time
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
