import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(num_cols):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print board content
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_column_input(prompt, num_cols):
    """
    Prompts the player for a column input and validates it.

    Args:
        prompt (str): The message to display to the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if input is valid.
             None if the input loop should be broken (e.g., for testing).
    """
    while True:
        try:
            user_input = input(prompt).strip().upper()
            if not user_input:  # Handle empty input
                raise ValueError("Input cannot be empty.")
            
            col_char = user_input[0] # Take only the first character

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except (IndexError, ValueError):
            print("Invalid input. Please enter a single letter for the column.")
        except KeyboardInterrupt:
            print("\nGame interrupted. Exiting.")
            sys.exit()


def drop_checker(board, col_index, player_checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from the bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_length):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the player to check.
        win_length (int): The number of checkers in a row needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r][c + i] == player_checker for i in range(win_length)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_length + 1):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_length - 1, num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_length)):
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
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        column_placed = False
        while not column_placed:
            col_input = get_column_input(f"Player {current_checker}, please enter a column: ", NUM_COLS)
            if col_input is None: # For graceful exit via KeyboardInterrupt
                sys.exit()

            if drop_checker(board, col_input, current_checker):
                column_placed = True
            else:
                print(f"Column {chr(ord('A') + col_input)} is full. Please choose another column.")
        
        # After a checker is placed, check for win or draw
        if check_win(board, current_checker, WIN_SEQUENCE_LENGTH):
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over, print final board and result
    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
