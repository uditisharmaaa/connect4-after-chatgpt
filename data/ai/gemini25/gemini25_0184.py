import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_LENGTH = 4

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = CHECKERS[:NUM_PLAYERS]


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
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C...)
    col_labels = [chr(ord('A') + i) for i in range(num_cols)]
    print("  " + "   ".join(col_labels))

    # Print board content
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")


def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed integer representing the chosen column.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except TypeError:
            print("Invalid input. Please enter a letter.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def drop_checker(board, col_index, player_checker):
    """
    Drops a player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: (True, row_placed) if the checker was successfully placed,
               (False, None) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True, r  # Return True and the row where it was placed
    return False, None  # Column is full


def check_win(board, player_checker, row_placed, col_placed):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        row_placed (int): The row index where the last checker was placed.
        col_placed (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a specific direction
    def check_direction(r_delta, c_delta):
        count = 0
        for i in range(-WIN_LENGTH + 1, WIN_LENGTH):
            r, c = row_placed + i * r_delta, col_placed + i * c_delta
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_checker:
                count += 1
                if count >= WIN_LENGTH:
                    return True
            else:
                count = 0  # Reset count if the sequence is broken
        return False

    # Check Horizontal
    if check_direction(0, 1):
        return True

    # Check Vertical
    if check_direction(1, 0):
        return True

    # Check Diagonal (top-left to bottom-right)
    if check_direction(1, 1):
        return True

    # Check Anti-Diagonal (top-right to bottom-left)
    if check_direction(1, -1):
        return True

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

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
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winning_player = None

    while not game_over:
        player_checker = PLAYERS[current_player_index]
        print_board(board)
        print(f"Player {player_checker}, it's your turn.")

        col_index = get_column_input(player_checker, NUM_COLS)
        successful_drop, row_placed = drop_checker(board, col_index, player_checker)

        if not successful_drop:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn, will be prompted again in next iteration
            continue

        if check_win(board, player_checker, row_placed, col_placed=col_index):
            print_board(board)
            winning_player = player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End Message
    print("\n--- GAME OVER ---")
    if winning_player:
        print(f"Player {winning_player} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
