import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (max 5 players: X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


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
        list: A 2D list representing the game board,
              initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print the board with separators
    for r in range(len(board)):
        print(f"+{('---+' * num_cols)}")
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print(f"+{('---+' * num_cols)}")


def get_column_index(col_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its 0-based index.

    Args:
        col_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index, or None if invalid.
    """
    if len(col_char) != 1 or not col_char.isalpha():
        return None
    
    col_char = col_char.upper()
    col_index = ord(col_char) - ord('A')
    
    if 0 <= col_index < num_cols:
        return col_index
    else:
        return None


def get_player_input(current_player_char, board):
    """
    Prompts the current player for a column choice and validates it.

    Args:
        current_player_char (str): The checker symbol for the current player.
        board (list): The game board.

    Returns:
        int: The 0-based index of the chosen and validated column.
    """
    num_cols = len(board[0])
    while True:
        col_input = input(f"Player {current_player_char}, please enter a column: ").strip()
        col_index = get_column_index(col_input, num_cols)

        if col_index is None:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")
        elif board[0][col_index] != ' ':  # Check if top row of column is full
            print("That column is full. Please choose another column.")
        else:
            return col_index


def drop_checker(board, col_index, player_char):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        player_char (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False otherwise
              (e.g., column is full).
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == ' ':
            board[r][col_index] = player_char
            return True
    return False  # Column is full


def check_win(board, player_char, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_char (str): The checker symbol of the player to check.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_char for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_char for i in range(win_condition)):
                return True

    # Check positively sloped diagonal (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_char for i in range(win_condition)):
                return True

    # Check negatively sloped diagonal (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_char for i in range(win_condition)):
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
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_char = players[current_player_index]
        print_board(board)

        col_index = get_player_input(current_player_char, board)
        
        # Drop checker. We already validated the column isn't full in get_player_input,
        # so drop_checker should always return True here.
        drop_checker(board, col_index, current_player_char)

        # Check for win
        if check_win(board, current_player_char, WIN_CONDITION):
            print_board(board) # Print final board with winning move
            print(f"Player {current_player_char} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board) # Print final board
            print("The board is full! It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
