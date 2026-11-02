import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_LENGTH = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


# --- Helper Functions ---
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
    return [[' ' for _ in range(cols)] for _ in range(rows)]


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
    sys.stdout.write('  ')
    for col_idx in range(num_cols):
        sys.stdout.write(f'{chr(ord("A") + col_idx)}   ')
    sys.stdout.write('\n')

    for row_idx in range(num_rows):
        sys.stdout.write('+')
        sys.stdout.write('---+') * num_cols
        sys.stdout.write('\n')

        sys.stdout.write('|')
        for col_idx in range(num_cols):
            sys.stdout.write(f' {board[row_idx][col_idx]} |')
        sys.stdout.write('\n')

    sys.stdout.write('+')
    sys.stdout.write('---+') * num_cols
    sys.stdout.write('\n')


def get_column_from_input(prompt, num_cols):
    """
    Prompts the player for a column input and validates it.

    Args:
        prompt (str): The message to display to the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_input = input(prompt).upper()
            if len(col_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_char = col_input[0]
            col_idx = ord(col_char) - ord('A')

            if 0 <= col_idx < num_cols:
                return col_idx
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("Invalid input. Please enter a single letter (e.g., A, B).")


def drop_checker(board, col_idx, player_checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_idx (int): The 0-indexed column number to drop the checker into.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    num_rows = len(board)
    for row_idx in range(num_rows - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player_checker
            return True
    return False


def check_win(board, player_checker, win_length):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the player to check.
        win_length (int): The number of checkers in a row required to win.

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
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(win_length - 1, num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_length)):
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
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


# --- Main Game Logic ---
def play_game():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return
    if NUM_COLS > 26:
        print("Error: NUM_COLS cannot exceed 26 for A-Z labeling.")
        return
    if NUM_ROWS < WIN_LENGTH or NUM_COLS < WIN_LENGTH:
        print(f"Error: Board dimensions ({NUM_ROWS}x{NUM_COLS}) are too small for a win length of {WIN_LENGTH}.")
        return

    # Initialize game state
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Game starts! Player {players[current_player_idx]} goes first.")

    while not game_over:
        current_checker = players[current_player_idx]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        col_chosen = False
        while not col_chosen:
            col_idx = get_column_from_input(f"Player {current_checker}, enter column (A-{chr(ord('A') + NUM_COLS - 1)}): ", NUM_COLS)

            if drop_checker(board, col_idx, current_checker):
                col_chosen = True
            else:
                print(f"Column {chr(ord('A') + col_idx)} is full. Please choose another column.")
                # Player does not lose turn for choosing a full column

        # After dropping, re-print board to show placement
        print_board(board)

        # Check for win
        if check_win(board, current_checker, WIN_LENGTH):
            winner_checker = current_checker
            game_over = True
            print_board(board)  # Final board before win message
            print(f"Player {winner_checker} won!")
        # Check for draw
        elif check_draw(board):
            game_over = True
            print_board(board)  # Final board before draw message
            print("The board is full. It's a draw!")
        else:
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
