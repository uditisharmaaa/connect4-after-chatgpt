import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers, ordered for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

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
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(num_cols):
        print(f"   {chr(ord('A') + col_idx)}", end="")
    print("\n" + "+---" * num_cols + "+")

    # Print board rows
    for row_idx in range(num_rows):
        print("|", end="")
        for col_idx in range(num_cols):
            print(f" {board[row_idx][col_idx]} |", end="")
        print("\n" + "+---" * num_cols + "+")

def get_column_input(player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        board (list): The game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            col_char = input(prompt).strip().upper()

            if not col_char.isalpha() or len(col_char) != 1:
                print(f"Invalid input: '{col_char}'. Please enter a single uppercase letter (A-{chr(ord('A') + num_cols - 1)}).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Invalid column: '{col_char}'. Column must be between A and {chr(ord('A') + num_cols - 1)}.")
                continue

            if board[0][col_index] != ' ':  # Check if the top row of the column is occupied
                print(f"Column {col_char} is full. Please choose another column.")
                continue

            return col_index
        except EOFError:
            print("\nExiting game due to EOF. Goodbye!")
            sys.exit()
        except KeyboardInterrupt:
            print("\nExiting game. Goodbye!")
            sys.exit()

def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the lowest available space in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: (row_index, col_index) of the placed checker, or None if the column is full.
    """
    num_rows = len(board)
    for row_idx in range(num_rows - 1, -1, -1):
        if board[row_idx][col_index] == ' ':
            board[row_idx][col_index] = player_checker
            return (row_idx, col_index)
    return None  # Should not happen if get_column_input validates correctly

def check_win(board, last_row, last_col, player_checker, win_condition):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The game board.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers in a given direction
    def count_consecutive(delta_row, delta_col):
        count = 0
        for i in range(-win_condition + 1, win_condition):
            r, c = last_row + i * delta_row, last_col + i * delta_col
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_checker:
                count += 1
                if count >= win_condition:
                    return True
            else:
                count = 0
        return False

    # Check horizontal win
    if count_consecutive(0, 1):
        return True

    # Check vertical win
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
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def connect_4_game():
    """
    Main function to run the Connect 4 game.
    """
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit()
    if not (1 <= NUM_COLS <= 26):
        print("Error: NUM_COLS must be between 1 and 26 (for A-Z labels).")
        sys.exit()
    if not (WIN_CONDITION <= max(NUM_ROWS, NUM_COLS)):
        print("Error: WIN_CONDITION cannot exceed board dimensions.")
        sys.exit()


    current_checkers = CHECKERS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = current_checkers[current_player_index]

    game_over = False
    winner = None

    print_board(board)
    print(f"Player {current_player_checker} goes first!")

    while not game_over:
        current_player_checker = current_checkers[current_player_index]

        col_to_drop = get_column_input(current_player_checker, board)
        last_placement = drop_checker(board, col_to_drop, current_player_checker)

        # last_placement should not be None due to get_column_input's validation
        last_row, last_col = last_placement

        print_board(board)

        if check_win(board, last_row, last_col, current_player_checker, WIN_CONDITION):
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    connect_4_game()
