import os
import random
import string

# --- Global Constants (Adjust these for testing different setups) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print("")

    # Print board content
    for r in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print("")

        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print("")

    # Print bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print("")

def get_player_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= string.ascii_uppercase[num_cols - 1]:
                raise ValueError
            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError:
            print(f"Invalid input. Please enter a single letter between A and {string.ascii_uppercase[num_cols - 1]}.")

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False # Column is full

def check_win(board, player_checker, win_length):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        win_length (int): The number of consecutive checkers needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_length + 1):
            if all(board[r][c + i] == player_checker for i in range(win_length)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - win_length + 1):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_length + 1):
        for c in range(cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - win_length + 1):
        for c in range(win_length - 1, cols):
            if all(board[r + i][c - i] == player_checker for i in range(win_length)):
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
                return False  # Found an empty space, game is not a draw yet
    return True # Board is full

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        col_index = get_player_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_index, current_player_checker):
            if check_win(board, current_player_checker, WIN_SEQUENCE_LENGTH):
                winner_checker = current_player_checker
                game_over = True
            elif check_draw(board):
                game_over = True
            else:
                # Move to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
            # Player does not lose turn, will be prompted again

    print_board(board) # Print final board state

    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

# --- Start the game ---
if __name__ == "__main__":
    play_connect_4()
