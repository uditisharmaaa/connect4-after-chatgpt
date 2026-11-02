import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.
    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the Connect 4 board.
    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear')  # Clear the screen

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board with separators
    for row_index in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

        print("|", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()

    # Print the bottom line
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

# --- Game Logic ---

def get_player_input(current_player_symbol, board):
    """
    Prompts the current player for their move and validates the input.
    Keeps asking until a valid column is entered.
    Args:
        current_player_symbol (str): The checker symbol for the current player.
        board (list): The 2D list representing the game board.
    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            user_input = input(f"Player {current_player_symbol}, please enter a column: ").strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
                continue

            if board[0][col_index] != " ":
                print(f"Column {col_char} is full. Please choose another column.")
                continue

            return col_index
        except (ValueError, IndexError):
            print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")

def drop_checker(board, col_index, checker_symbol):
    """
    Places the checker in the lowest available position in the specified column.
    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number where the checker is dropped.
        checker_symbol (str): The checker symbol to place.
    Returns:
        int: The 0-indexed row number where the checker landed, or -1 if the column is full.
    """
    num_rows = len(board)
    for row_index in range(num_rows - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker_symbol
            return row_index
    return -1  # Column is full (should be handled by get_player_input)

def check_win(board, row, col, checker_symbol, win_condition):
    """
    Checks if the last placed checker resulted in a win.
    Args:
        board (list): The 2D list representing the game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker_symbol (str): The checker symbol of the current player.
        win_condition (int): The number of checkers needed to win.
    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers in a direction
    def count_consecutive(delta_row, delta_col):
        count = 0
        for i in range(-win_condition + 1, win_condition):
            r, c = row + i * delta_row, col + i * delta_col
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker_symbol:
                count += 1
                if count >= win_condition:
                    return True
            else:
                count = 0
        return False

    # Check horizontal
    if count_consecutive(0, 1):
        return True
    # Check vertical
    if count_consecutive(1, 0):
        return True
    # Check diagonal (top-left to bottom-right)
    if count_consecutive(1, 1):
        return True
    # Check anti-diagonal (top-right to bottom-left)
    if count_consecutive(1, -1):
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
    for row_index in range(len(board)):
        for col_index in range(len(board[0])):
            if board[row_index][col_index] == " ":
                return False
    return True

# --- Main Game Function ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_COLS > 26:
        print("Error: Number of columns exceeds 26. Column labels will not work correctly.")
        sys.exit(1)
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)

    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_symbol = players[current_player_index]

    game_over = False
    winner_symbol = None

    print_board(board)
    print(f"Player {current_player_symbol} starts first!")

    while not game_over:
        col_to_drop = get_player_input(current_player_symbol, board)
        
        # Drop the checker and get the row where it landed
        row_landed = drop_checker(board, col_to_drop, current_player_symbol)
        # Note: row_landed will not be -1 here because get_player_input already validates full columns

        print_board(board)

        if check_win(board, row_landed, col_to_drop, current_player_symbol, WIN_CONDITION):
            winner_symbol = current_player_symbol
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_symbol = players[current_player_index]

    # End of game messages
    if winner_symbol:
        print(f"Player {winner_symbol} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
