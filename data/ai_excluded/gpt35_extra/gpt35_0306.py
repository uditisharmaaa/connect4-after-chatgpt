import os
import random

# Constants for the game configuration
ROWS = 6                  # Number of rows in the board
COLUMNS = 7               # Number of columns in the board (max 26)
NUM_PLAYERS = 2           # Number of players (between 2 and 5)
WIN_CONDITION = 4         # Number of consecutive checkers needed to win
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """
    Create and initialize the board with whitespaces.

    Args:
        rows (int): Number of rows
        columns (int): Number of columns

    Returns:
        list: 2D list representing the game board
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Print the current game board with column labels.

    Args:
        board (list): 2D list representing the game board
    """
    clear_screen()
    # Print column headers A-G ...
    column_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(column_labels))
    # Print the board rows
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def get_valid_column_input(current_player, columns, board):
    """
    Prompt the current player to enter a valid column letter.

    Args:
        current_player (str): The checker character of the current player
        columns (int): Number of columns in the board
        board (list): The current board state

    Returns:
        int or None: The index of the column chosen if valid, None if column is full
    """
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(choice) != 1:
            # Input should be a single letter
            continue
        col_index = ord(choice) - ord('A')
        if col_index < 0 or col_index >= columns:
            # Out of range
            continue
        # Check if column is full (top-most row is occupied)
        if board[0][col_index] != " ":
            # Column full, player loses turn
            return None
        return col_index

def place_checker(board, col, checker):
    """
    Place the checker in the lowest available slot in the selected column.

    Args:
        board (list): The current board state
        col (int): The column index to place the checker
        checker (str): The checker symbol to place

    Returns:
        tuple: (row_index, col) where checker was placed
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return (row, col)
    # This should not happen since we check for full column before
    return None

def check_win(board, row, col, checker):
    """
    Check all directions for a win starting from the last placed checker.

    Args:
        board (list): The current board state
        row (int): The row index of the last placed checker
        col (int): The column index of the last placed checker
        checker (str): The checker symbol to check

    Returns:
        bool: True if the player has won, False otherwise
    """
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the placed checker itself

        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    """
    Check if the board is full (no empty spaces).

    Args:
        board (list): The current board state

    Returns:
        bool: True if board is full, False otherwise
    """
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Use only the needed checkers for the configured players
    players = CHECKERS[:NUM_PLAYERS]

    # Create the game board
    board = create_board(ROWS, COLUMNS)

    # Choose random player index to start
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        # Get a valid column index or None if full
        col = get_valid_column_input(current_checker, COLUMNS, board)
        if col is None:
            # Full column - player loses turn and move on to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place checker on board
        pos = place_checker(board, col, current_checker)

        print_board(board)

        # Check for win after placing
        if check_win(board, pos[0], pos[1], current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
