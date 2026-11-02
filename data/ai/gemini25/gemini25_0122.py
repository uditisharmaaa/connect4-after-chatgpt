import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win
CHECKERS = ["X", "O", "V", "H", "M"]  # Available checkers for up to 5 players

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear screen before printing updated board

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(NUM_COLS):
        print(f"   {chr(ord('A') + col_idx)}", end="")
    print("\n+---+", end="")
    for _ in range(NUM_COLS - 1):
        print("---+", end="")
    print("---+")

    # Print rows with checkers
    for row_idx in range(NUM_ROWS):
        print("|", end="")
        for col_idx in range(NUM_COLS):
            print(f" {board[row_idx][col_idx]} |", end="")
        print("\n+---+", end="")
        for _ in range(NUM_COLS - 1):
            print("---+", end="")
        print("---+")

def get_player_input(current_player_checker):
    """
    Prompts the current player for their move and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-based index of the chosen column.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return col_index
        except TypeError:
            print("Invalid input. Please enter a letter.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol of the current player.

    Returns:
        tuple: A tuple containing (True, row_index, col_index) if the checker was placed successfully,
               or (False, None, None) if the column is full.
    """
    for row_idx in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = checker
            return True, row_idx, col_index  # Return success and the position
    return False, None, None  # Column is full

def check_win(board, last_row, last_col, checker):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The game board.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.
        checker (str): The checker symbol of the player who just moved.

    Returns:
        bool: True if a win is detected, False otherwise.
    """

    # Helper function to check a specific direction
    def _check_direction(dr, dc):
        count = 0
        # Check forward direction
        r, c = last_row, last_col
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction (excluding the starting checker, as it was counted once)
        r, c = last_row - dr, last_col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        return count >= WIN_CONDITION

    # Check horizontal
    if _check_direction(0, 1):
        return True

    # Check vertical
    if _check_direction(1, 0):
        return True

    # Check diagonal (top-left to bottom-right)
    if _check_direction(1, 1):
        return True

    # Check diagonal (top-right to bottom-left)
    if _check_direction(1, -1):
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players_checkers = CHECKERS[:NUM_PLAYERS]  # Select checkers based on NUM_PLAYERS
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_found = False

    while not game_over:
        current_player_checker = players_checkers[current_player_index]
        print_board(board)
        print() # Add an empty line for better readability

        col_index = get_player_input(current_player_checker)

        placed_successfully, last_row, last_col = drop_checker(board, col_index, current_player_checker)

        if not placed_successfully:
            print("Column is full! Please choose another column.")
            # Player does not lose turn if column is full, they just get to try again.
            continue
        
        # Check for a win after every successful move
        if check_win(board, last_row, last_col, current_player_checker):
            print_board(board)  # Print the final board with the winning move
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        elif check_draw(board):
            print_board(board)  # Print the final board
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    main()
