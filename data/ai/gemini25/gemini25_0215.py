import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers needed to win

# Valid checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # For Windows, it's 'cls'. For Unix/Linux/macOS, it's 'clear'.
    os.system('cls' if os.name == 'nt' else 'clear')

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
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column headers (A, B, C...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print board rows and separators
    for r_idx, row in enumerate(board):
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def get_column_input(player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        board_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Invalid input. Please enter a column letter (e.g., A, B).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if not ('A' <= col_char <= chr(ord('A') + board_cols - 1)):
                print(f"Invalid input. Column must be between A and {chr(ord('A') + board_cols - 1)}.")
            elif len(user_input) > 1:
                print("Invalid input. Please enter only a single column letter.")
            else:
                return col_index
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted by user.")
            sys.exit()
        except Exception: # Catch any unexpected input errors
            print("An unexpected error occurred. Please try again.")

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space of the chosen column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number where the checker is to be placed.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: A tuple (row, col) of the placed checker's position if successful,
               otherwise (None, None) if the column is full.
    """
    for r_idx in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[r_idx][col_index] == " ":
            board[r_idx][col_index] = player_checker
            return r_idx, col_index
    return None, None  # Column is full

def check_win(board, last_row, last_col, player_checker, win_condition):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The 2D list representing the game board.
        last_row (int): The row index of the last placed checker.
        last_col (int): The column index of the last placed checker.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(cols):
        if board[last_row][c] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(rows):
        if board[r][last_col] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find the top-leftmost cell of this diagonal that contains a checker
    start_row_tlbr = last_row - min(last_row, last_col)
    start_col_tlbr = last_col - min(last_row, last_col)
    for i in range(min(rows - start_row_tlbr, cols - start_col_tlbr)):
        r = start_row_tlbr + i
        c = start_col_tlbr + i
        if board[r][c] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check diagonal (top-right to bottom-left)
    count = 0
    # Find the top-rightmost cell of this diagonal that contains a checker
    start_row_trbl = last_row - min(last_row, cols - 1 - last_col)
    start_col_trbl = last_col + min(last_row, cols - 1 - last_col)
    for i in range(min(rows - start_row_trbl, start_col_trbl + 1)):
        r = start_row_trbl + i
        c = start_col_trbl - i
        if board[r][c] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False  # There's still an empty space
    return True  # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Main function to play the Connect 4 game.
    Initializes the board, handles turns, checks for wins/draws, and manages game flow.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"\nCurrent Player: {current_player_checker}")

        col_index = get_column_input(current_player_checker, NUM_COLS)
        row_placed, col_placed = place_checker(board, col_index, current_player_checker)

        if row_placed is None:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn, re-prompt for input
            continue

        if check_win(board, row_placed, col_placed, current_player_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = PLAYER_CHECKERS[current_player_index]

if __name__ == "__main__":
    play_game()
