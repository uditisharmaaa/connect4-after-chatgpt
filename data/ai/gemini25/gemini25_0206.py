import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for i in range(cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print("")

    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print("")

    # Print rows with checkers and borders
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("")
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print("")

def get_column_index(col_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its corresponding index (0).

    Args:
        col_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if not isinstance(col_char, str) or len(col_char) != 1 or not col_char.isalpha() or not col_char.isupper():
        return -1
    index = ord(col_char) - ord('A')
    if 0 <= index < num_cols:
        return index
    return -1

def is_valid_move(board, col_index):
    """
    Checks if a move to the given column is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if not (0 <= col_index < len(board[0])):
        return False
    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def place_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol for the current player.

    Returns:
        tuple: A tuple (row, col) of where the checker was placed, or (-1, -1) if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return -1, -1 # Column is full

def check_win(board, last_row, last_col, checker, win_condition):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The game board.
        last_row (int): The row of the last placed checker.
        last_col (int): The column of the last placed checker.
        checker (str): The checker symbol for the current player.
        win_condition (int): The number of checkers needed to win.

    Returns:
        bool: True if a win condition is met, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Helper to check a specific direction
    def check_direction(dr, dc):
        count = 0
        # Check in one direction
        r, c = last_row, last_col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the opposite direction (excluding the starting cell again)
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        return count >= win_condition

    # Check horizontal
    if check_direction(0, 1):
        return True
    # Check vertical
    if check_direction(1, 0):
        return True
    # Check diagonal (top-left to bottom-right)
    if check_direction(1, 1):
        return True
    # Check diagonal (top-right to bottom-left)
    if check_direction(1, -1):
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
                return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winning_player_checker = None

    while not game_over:
        clear_screen()
        print_board(board)

        current_player_checker = CHECKERS[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        valid_input = False
        col_index = -1
        while not valid_input:
            player_input = input().strip().upper()
            col_index = get_column_index(player_input, NUM_COLS)

            if col_index == -1:
                print("Invalid column. Please enter a letter from A to", chr(ord('A') + NUM_COLS - 1) + ":")
            elif not is_valid_move(board, col_index):
                print("That column is full or invalid. Please choose another column:")
            else:
                valid_input = True

        # Place the checker
        last_row, last_col = place_checker(board, col_index, current_player_checker)

        # Check for win
        if check_win(board, last_row, last_col, current_player_checker, WIN_CONDITION):
            clear_screen()
            print_board(board)
            winning_player_checker = current_player_checker
            game_over = True
        # Check for draw
        elif check_draw(board):
            clear_screen()
            print_board(board)
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over message
    if winning_player_checker:
        print(f"Player {winning_player_checker} won!")
    else:
        print("It's a draw!")

# --- Start the game ---
if __name__ == "__main__":
    play_game()
