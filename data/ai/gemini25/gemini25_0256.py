import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (max 5 players as per assignment)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


# --- Utility Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


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
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print board content
    for r in range(num_rows):
        print("+---" * num_cols + "+")
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * num_cols + "+")


def get_column_input(current_player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        board_cols (int): The number of columns on the board.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < board_cols):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + board_cols - 1)}.")
                continue

            return col_index
        except Exception:
            print("Invalid input. Please try again.")


def place_checker(board, col, player_checker):
    """
    Places the player's checker in the lowest available space of the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col (int): The column index (0-based) where the checker should be placed.
        player_checker (str): The checker of the current player.

    Returns:
        tuple: (bool, int) - True if placement was successful, False otherwise.
               If successful, also returns the row index where the checker was placed.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row up
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True, r
    return False, -1  # Column is full


def check_win(board, player_checker, last_row, last_col, win_condition):
    """
    Checks if the current player has won the game after placing a checker.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Directions to check: horizontal, vertical, and two diagonals
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]

    for dr, dc in directions:
        count = 1  # Count of checkers in a line, starting with the last placed one

        # Check in positive direction
        for i in range(1, win_condition):
            r, c = last_row + dr * i, last_col + dc * i
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_checker:
                count += 1
            else:
                break

        # Check in negative direction (for extending the line)
        for i in range(1, win_condition):
            r, c = last_row - dr * i, last_col - dc * i
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_checker:
                count += 1
            else:
                break

        if count >= win_condition:
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
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True


# --- Main Game Logic ---

def play_connect4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    turn_count = 0

    print_board(board)
    print(f"Player {players[current_player_index]} starts!")

    while not game_over:
        current_player_checker = players[current_player_index]

        # Get and validate column input
        while True:
            col_index = get_column_input(current_player_checker, NUM_COLS)
            
            # Attempt to place checker
            success, last_row = place_checker(board, col_index, current_player_checker)

            if success:
                turn_count += 1
                break
            else:
                print("Column is full. Please choose another column.")
        
        print_board(board)

        # Check for win
        if check_win(board, current_player_checker, last_row, col_index, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_connect4()
