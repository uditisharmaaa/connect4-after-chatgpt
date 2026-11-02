import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
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
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C...)
    col_labels = string.ascii_uppercase[:num_cols]
    header = "  " + "   ".join(col_labels)
    print(header)

    # Print board rows
    for row in board:
        print("+---" * num_cols + "+")
        row_str = "|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
    print("+---" * num_cols + "+")

def get_column_input(current_player_checker, num_cols):
    """
    Gets and validates the player's column input.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The 0-based index of the chosen column.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = ord(user_input) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Column '{user_input}' is out of bounds. Please choose a column from A to {string.ascii_uppercase[num_cols - 1]}.")
        except Exception:
            print("Invalid input. Please enter a single letter.")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for.
        win_condition (int): The number of checkers in a row needed to win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
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
    for row in board:
        if " " in row:
            return False
    return True

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to play a game of Connect 4.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner = None

    print_board(board)
    print(f"Player {players[current_player_index]} goes first!")

    while not game_over:
        current_player_checker = players[current_player_index]

        col_index = get_column_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_index, current_player_checker):
            print_board(board)

            if check_win(board, current_player_checker, WIN_CONDITION):
                winner = current_player_checker
                game_over = True
            elif check_draw(board):
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column was full, current player's turn is not lost, they try again
            print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
            # Don't switch player, just re-print board for clarity and let them try again.
            print_board(board)


    # --- Game End ---
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_connect_4()
