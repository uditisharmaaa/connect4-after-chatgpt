import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M) - up to 5 players
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
# The actual checkers used based on NUM_PLAYERS
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board,
              initialized with whitespaces.
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
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"   {chr(ord('A') + col_index)}", end="")
    print("\n+---+", end="")
    for _ in range(len(board[0]) - 1):
        print("---+", end="")
    print("---+\n", end="") # End of first separator line

    # Print rows with checkers
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n+---+", end="")
        for _ in range(len(board[0]) - 1):
            print("---+", end="")
        print("---+\n", end="") # End of row separator line

def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol for the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the chosen valid column.
    """
    while True:
        try:
            column_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            # Check if input is a single letter
            if not (len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + num_cols - 1)):
                print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")
                continue

            col_index = ord(column_input) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column was full.
    """
    num_rows = len(board)
    # Iterate from the bottom row upwards
    for row in range(num_rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True  # Checker placed successfully
    return False  # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a line (horizontal, vertical, or diagonal)
    def check_line(r, c, dr, dc):
        count = 0
        for i in range(win_condition):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < num_rows and 0 <= nc < num_cols and board[nr][nc] == player_checker:
                count += 1
            else:
                break # Stop if sequence is broken or out of bounds
        return count >= win_condition

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if check_line(r, c, 0, 1): # (r, c) starting point, (0, 1) direction for horizontal
                return True

    # Check vertical wins
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols):
            if check_line(r, c, 1, 0): # (r, c) starting point, (1, 0) direction for vertical
                return True

    # Check diagonal wins (positive slope: /)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if check_line(r, c, 1, 1): # (r, c) starting point, (1, 1) direction for positive diagonal
                return True

    # Check diagonal wins (negative slope: \)
    for r in range(win_condition - 1, num_rows): # Start from row `win_condition - 1` to `num_rows - 1`
        for c in range(num_cols - win_condition + 1):
            if check_line(r, c, -1, 1): # (r, c) starting point, (-1, 1) direction for negative diagonal
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False  # Found an empty space, so not a draw
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles turns, checks for wins/draws, and ends the game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = len(ACTIVE_CHECKERS)

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)

    game_over = False
    winner = None

    while not game_over:
        current_player_checker = ACTIVE_CHECKERS[current_player_index]

        print_board(board)

        # Get and validate column input
        col_index = get_column_input(current_player_checker, NUM_COLS)

        # Drop the checker
        if drop_checker(board, col_index, current_player_checker):
            # Check for win
            if check_win(board, current_player_checker, WIN_CONDITION):
                print_board(board)
                winner = current_player_checker
                game_over = True
            # Check for draw if no win
            elif check_draw(board):
                print_board(board)
                game_over = True
        else:
            print("Column is full! You lose your turn. Please choose another column.")
            # Player does not lose turn if column full, they are prompted again (as per assignment)
            # Revert player index to ensure same player gets to try again
            current_player_index = (current_player_index - 1 + num_players) % num_players
            input("Press Enter to continue...") # Pause to allow user to read message
            continue # Skip to next iteration to re-prompt the same player

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

    # Game End Message
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# Ensure the game runs when the script is executed
if __name__ == "__main__":
    play_game()
