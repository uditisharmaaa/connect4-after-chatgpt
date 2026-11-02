import os
import random

# Constants for the game configuration
ROWS = 6            # Number of rows on the board
COLUMNS = 7         # Number of columns on the board (max 26)
NUM_PLAYERS = 2     # Number of players (between 2 and 5)
WIN_COUNT = 4       # Number of checkers in a row needed to win

# Players' checkers symbols in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Ensure we only use the required number of players and columns not exceeding max 26
PLAYER_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]
COLUMNS = min(COLUMNS, 26)

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('clear')

def create_board(rows, columns):
    """
    Creates a board initialized with empty spaces " ".
    Args:
        rows (int): number of rows
        columns (int): number of columns
    Returns:
        list: 2D list representing the board
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board to the terminal with column labels.
    Args:
        board (list): 2D board list
    """
    # Print column headers (A, B, C, ...)
    headers = "  "
    for c in range(len(board[0])):
        headers += "  " + chr(ord('A') + c) + " "
    print(headers)

    # Print the board with borders
    for r in range(len(board)):
        # horizontal separator line
        print("+" + "---+" * len(board[0]))
        # cells in row r
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    # bottom line
    print("+" + "---+" * len(board[0]))

def get_column_index(input_str):
    """
    Converts a column letter to its index.
    Args:
        input_str (str): single uppercase letter representing column
    Returns:
        int: column index or -1 if invalid
    """
    if len(input_str) != 1 or not input_str.isalpha() or not input_str.isupper():
        return -1
    index = ord(input_str) - ord('A')
    if 0 <= index < COLUMNS:
        return index
    return -1

def is_column_full(board, col):
    """
    Checks if a column is full (no empty spaces).
    Args:
        board (list): 2D board list
        col (int): column index
    Returns:
        bool: True if full, False otherwise
    """
    return board[0][col] != " "

def place_checker(board, col, checker):
    """
    Places a checker in the lowest available space in the given column.
    Args:
        board (list): 2D board list
        col (int): column index to place checker
        checker (str): player's checker symbol
    Returns:
        bool: True if placed successfully, False if column is full
    """
    for row in range(len(board)-1, -1, -1):  # start from bottom row up
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # column full

def check_win(board, checker):
    """
    Checks if the given player has won (4 in a row).
    Args:
        board (list): 2D board list
        checker (str): player's checker symbol
    Returns:
        bool: True if player won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full (no empty spaces).
    Args:
        board (list): 2D board list
    Returns:
        bool: True if draw, False otherwise
    """
    # If any cell in top row is empty, not a draw yet
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def get_valid_input(board):
    """
    Prompts the player for a valid column input until valid.
    Args:
        board (list): 2D board list
    Returns:
        int: valid column index or None if player loses turn due to full column
    """
    while True:
        player_input = input("please enter a column: ").strip().upper()
        col = get_column_index(player_input)
        if col == -1:
            print("Invalid input. Please enter a valid column letter (A - {}).".format(chr(ord('A') + COLUMNS - 1)))
            continue
        if is_column_full(board, col):
            # If full, player loses turn - return None
            return None
        return col

def main():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)

    # Randomly select first player index
    current_player_index = random.randint(0, NUM_PLAYERS -1)

    while True:
        clear_screen()
        print_board(board)
        current_player = PLAYER_CHECKERS[current_player_index]
        print(f"Player {current_player}, ", end="")

        col = get_valid_input(board)
        if col is None:
            # Column full -> lose turn, skip to next player
            print(f"Column full! Player {current_player} loses the turn.")
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Place checker
        placed = place_checker(board, col, current_player)
        # placed should always be True because we checked for full column already

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
