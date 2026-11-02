import os
import random
import sys

# --- Global Constants ---
# Board dimensions (can be changed for different board sizes)
NUM_ROWS = 6
NUM_COLS = 7

# Maximum number of columns is 26 (A-Z)
if NUM_COLS > 26:
    print("Error: Maximum number of columns is 26.")
    sys.exit()

# Number of players (can be changed from 2 to 5)
NUM_PLAYERS = 2

# Checkers for players (up to 5 players)
CHECKERS = ["X", "O", "V", "H", "M"]

# Check if NUM_PLAYERS is within the valid range
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: Number of players must be between 2 and 5.")
    sys.exit()

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

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
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear the screen before printing the updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(NUM_COLS):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print the board content
    for r_idx in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

        print("|", end="")
        for c_idx in range(NUM_COLS):
            print(f" {board[r_idx][c_idx]} |", end="")
        print()

    # Print the bottom border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def get_player_input(current_player_checker):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            column_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            # Check if input is a single uppercase letter
            if len(column_input) != 1 or not ('A' <= column_input[0] <= chr(ord('A') + NUM_COLS - 1)):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            # Convert letter to 0-indexed column number
            col = ord(column_input[0]) - ord('A')
            return col
        except ValueError:
            print("Invalid input. Please enter a letter.")

def drop_checker(board, col, checker):
    """
    Places the checker in the lowest available space within the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col (int): The 0-indexed column number to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[row][col] == " ":
            board[row][col] = checker
            return True, row, col  # Return True and the position where checker was placed
    return False, -1, -1  # Column is full

def check_win(board, last_row, last_col, checker):
    """
    Checks if the last placed checker resulted in a win (4 in a row).

    Args:
        board (list): The 2D list representing the game board.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.
        checker (str): The checker symbol of the player who just moved.

    Returns:
        bool: True if a win condition is met, False otherwise.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[last_row][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][last_col] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check positive diagonal (bottom-left to top-right)
    # Find the starting point of the diagonal that passes through (last_row, last_col)
    # The sum of row and column indices (r + c) is constant for this diagonal type
    start_row_pos_diag = last_row - min(last_row, last_col)
    start_col_pos_diag = last_col - min(last_row, last_col)
    
    count = 0
    for i in range(min(NUM_ROWS, NUM_COLS)):
        r = start_row_pos_diag + i
        c = start_col_pos_diag + i
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
            if board[r][c] == checker:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
        else: # Out of bounds for the current diagonal, reset count
            count = 0 
            
    # Check negative diagonal (top-left to bottom-right)
    # The difference of row and column indices (r - c) is constant for this diagonal type
    start_row_neg_diag = last_row - min(last_row, NUM_COLS - 1 - last_col)
    start_col_neg_diag = last_col + min(last_row, NUM_COLS - 1 - last_col)

    count = 0
    for i in range(min(NUM_ROWS, NUM_COLS)):
        r = start_row_neg_diag + i
        c = start_col_neg_diag - i
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
            if board[r][c] == checker:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
        else: # Out of bounds for the current diagonal, reset count
            count = 0

    return False

def check_draw(board):
    """
    Checks if the board is completely filled (game is a draw).

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers for the number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    print_board(board)

    while not game_over:
        current_player_checker = player_checkers[current_player_index]

        col_chosen = get_player_input(current_player_checker)

        # Validate if the chosen column is within bounds (already handled by get_player_input)
        # Now, check if the column is full
        success, last_row, last_col = drop_checker(board, col_chosen, current_player_checker)

        if not success:
            print(f"Column {chr(ord('A') + col_chosen)} is full. Player {current_player_checker}, please choose another column.")
            # Player does not lose turn if column is full
            continue 

        print_board(board)

        # Check for win
        if check_win(board, last_row, last_col, current_player_checker):
            winner_checker = current_player_checker
            game_over = True
            break

        # Check for draw
        if check_draw(board):
            game_over = True
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End Message
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

# Ensure the main function runs when the script is executed
if __name__ == "__main__":
    main()
