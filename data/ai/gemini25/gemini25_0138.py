import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Maximum 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"] # Checkers for players 1 to 5
WIN_CONDITION = 4 # Number of checkers in a row to win

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
        list[list[str]]: A 2D list representing the board, initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list[list[str]]): The current state of the board.
    """
    clear_screen() # Clear the screen before printing the updated board

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f"  {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board rows
    for row in board:
        print("+---+", end="")
        for _ in range(len(row) - 1):
            print("---+", end="")
        print("---+") # End of a row's top border

        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()

    # Print the bottom border of the board
    print("+---+", end="")
    for _ in range(len(board[0]) - 1):
        print("---+", end="")
    print("---+")

def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            # Check if input is a single letter
            if len(col_char) != 1 or not 'A' <= col_char <= chr(ord('A') + num_cols - 1):
                raise ValueError("Invalid column. Please enter a letter from A to " + chr(ord('A') + num_cols - 1))

            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list[list[str]]): The current state of the board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    # Iterate from the bottom row upwards
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True # Checker placed successfully
    return False # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list[list[str]]): The current state of the board.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check positive diagonal wins (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check negative diagonal wins (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list[list[str]]): The current state of the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False # Found an empty space, not a draw
    return True # No empty spaces, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize game parameters based on constants
    current_players_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print(f"Player {current_players_checkers[current_player_index]} goes first!")
    input("Press Enter to start...")

    game_over = False
    winner_found = False

    while not game_over:
        current_player_checker = current_players_checkers[current_player_index]
        print_board(board)

        # Get and validate player input
        col_index = get_column_input(current_player_checker, NUM_COLS)

        # Drop checker and check if column is full
        if not drop_checker(board, col_index, current_player_checker):
            print(f"Column {chr(ord('A') + col_index)} is full. Player {current_player_checker} loses their turn!")
            input("Press Enter to continue...")
            # Player loses turn, so the current_player_index does not change.
            # However, the assignment states "the turn is not lost" for invalid input
            # and "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
            # This is a slight ambiguity. Assuming "loses the turn" means the next player plays.
            # If the intent is for the same player to re-try until a valid move,
            # then the `current_player_index = (current_player_index + 1) % NUM_PLAYERS` should be skipped for this case.
            # For this solution, I'll follow the "loses the turn" interpretation, meaning it's the next player's turn.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue # Skip win/draw check for this invalid move

        print_board(board) # Print board after a valid move

        # Check for win
        if check_win(board, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board) # Display final board
    print("Game Over!")

if __name__ == "__main__":
    main()
