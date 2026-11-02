import os
import random

# Constants for the game configuration
ROWS = 6               # Number of rows in the board
COLUMNS = 7            # Number of columns in the board (max 26)
NUM_PLAYERS = 2        # Number of players (between 2 and 5)
WIN_LENGTH = 4         # Number of consecutive checkers to win

# Player checkers in order; supports up to 5 players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    """Clear the terminal screen using 'clear' command."""
    os.system("clear")


def create_board(rows, cols):
    """
    Initialize the game board as a 2D list filled with empty spaces.
    
    Args:
        rows: Number of rows.
        cols: Number of columns.
    
    Returns:
        board: 2D list representing the board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board with column labels and row separators.
    
    Args:
        board: 2D list representing the board.
    """
    clear_screen()

    # Header: Column labels from A to ...
    column_labels = [chr(ord("A") + i) for i in range(len(board[0]))]
    print("  " + "   ".join(column_labels))

    # Print the board rows with separators
    separator = "+" + "---+" * len(board[0])
    for row in board:
        print(separator)
        # Each cell with vertical bars
        print("| " + " | ".join(row) + " |")
    print(separator)


def is_valid_column(col_input, cols):
    """
    Check if the user input for a column is valid:
    - Length 1
    - Uppercase letter within board columns
    
    Args:
        col_input: input string
        cols: total number of columns
    
    Returns:
        bool: True if valid, False otherwise
    """
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    col_upper = col_input.upper()
    col_index = ord(col_upper) - ord("A")
    if 0 <= col_index < cols:
        return True
    return False


def get_column_index(col_input):
    """
    Convert column letter input to zero-based column index.
    
    Args:
        col_input: single character string for column
    
    Returns:
        int: column index
    """
    return ord(col_input.upper()) - ord("A")


def place_checker(board, col, checker):
    """
    Place the player's checker in the lowest available space in the specified column.
    
    Args:
        board: 2D list representing the board
        col: integer index of column (0 based)
        checker: player's checker character
    
    Returns:
        bool: True if checker placed successfully, False if column is full
    """
    # Start from bottom row upwards
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full


def check_winner(board, checker):
    """
    Check if the given player has won the game by having 4 in a row, column, or diagonal.
    
    Args:
        board: 2D list representing the board
        checker: player's checker character
    
    Returns:
        bool: True if player has 4 in a row, else False
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal (left to right)
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical (top to bottom)
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (down-left)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_LENGTH)):
                return True

    return False


def check_draw(board):
    """
    Check if the board is full and no spaces remain.
    
    Args:
        board: 2D list representing the board
    
    Returns:
        bool: True if draw (board full), else False
    """
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Initialize the board and players
    board = create_board(ROWS, COLUMNS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        current_checker = checkers[current_player_index]
        # Prompt player for input until valid
        while True:
            col_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if not is_valid_column(col_input, COLUMNS):
                # Invalid input character or out of range
                continue
            col_index = get_column_index(col_input)
            # Try to place checker
            if not place_checker(board, col_index, current_checker):
                # Column full: player loses turn, break and continue game
                break
            else:
                # Successful placement
                break

        # Print updated board after move or lost turn
        print_board(board)

        # If checker placed successfully, check win
        if board[0][col_index] == current_checker or (board[ROWS - 1][col_index] == current_checker or True):
            # Only check win if checker placed (not if lost turn)
            if not place_checker(board, col_index, current_checker):
                # We just handled column full above, no checker placed => skip win check
                pass
            else:
                # Since we already placed checker above, check win
                pass

        # Check if the player actually placed a checker to check for win
        # To do so, we scan if checker present in column after move or if player lost turn
        # Alternative approach: We know place_checker returned True above if placed checker
        # So lets track that with a variable

        # Let's fix logic:
        # Actually, current approach doesn't track if checker placed to detect win.
        # Better to store placement success in a variable.

        # Let's adjust

def improved_main():
    # Initialize the board and players
    board = create_board(ROWS, COLUMNS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    while True:
        current_checker = checkers[current_player_index]
        # Attempt to get valid column input
        while True:
            col_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if not is_valid_column(col_input, COLUMNS):
                continue
            col_index = get_column_index(col_input)
            # Check if column full to decide if player loses the turn
            # place_checker returns False if full
            placed = place_checker(board, col_index, current_checker)
            break  # Exit input loop regardless of placement success (loses turn if not placed)

        # Print board after move or lost turn
        print_board(board)

        # If placed checker, check win
        if placed and check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # If not placed, player lost turn (per spec) skip win check

        # Check draw if board full
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    improved_main()
