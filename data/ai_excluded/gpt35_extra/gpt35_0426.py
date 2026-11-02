import os
import random

# Constants for the game configuration
ROWS = 6                   # Number of rows in the board
COLS = 7                   # Number of columns in the board (max 26)
NUM_PLAYERS = 2            # Number of players (2 to 5)

# Checkers for players in the order of play
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Create a 2D list representing the board.
    Each cell initialized with a whitespace character ' '.
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Print the game board to the terminal with column headers labeled A, B, C...
    The board is printed from top row to bottom row.
    """
    cols = len(board[0])

    # Print column headers
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(headers)

    # Print rows with separators
    for row in board:
        print("+---" * cols + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * cols + "+")

def is_valid_column(input_str, cols):
    """
    Check if the input string is a single uppercase letter A to appropriate col letter.
    """
    if len(input_str) != 1:
        return False
    if not ('A' <= input_str <= chr(ord('A') + cols -1)):
        return False
    return True

def column_index(column_letter):
    """
    Convert column letter (A-G) to zero-based index.
    """
    return ord(column_letter) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in the lowest empty row in the specified column.
    Return True if placed, False if column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # column full

def check_winner(board, checker):
    """
    Check all directions for 4 in a row of 'checker'.
    Returns True if found, False otherwise.
    """

    rows = len(board)
    cols = len(board[0])
    in_a_row = 4

    # Horizontal check
    for r in range(rows):
        for c in range(cols - in_a_row + 1):
            if all(board[r][c+i] == checker for i in range(in_a_row)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - in_a_row + 1):
            if all(board[r+i][c] == checker for i in range(in_a_row)):
                return True

    # Diagonal (down-right) check
    for r in range(rows - in_a_row + 1):
        for c in range(cols - in_a_row + 1):
            if all(board[r+i][c+i] == checker for i in range(in_a_row)):
                return True

    # Diagonal (up-right) check
    for r in range(in_a_row - 1, rows):
        for c in range(cols - in_a_row + 1):
            if all(board[r - i][c + i] == checker for i in range(in_a_row)):
                return True

    return False

def is_board_full(board):
    """
    Check if the board is full (no empty spaces).
    """
    for row in board:
        if " " in row:
            return False
    return True

def get_valid_column_input(board, player_checker):
    """
    Prompt the player for a valid column input.
    Validate input and handle invalid or out-of-range letters.
    Return the zero-based column index for placing the checker.
    If the column is full, inform the player and return None (loses turn).
    """
    cols = len(board[0])
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, cols):
            # Invalid input format
            continue
        col_idx = column_index(user_input)
        if not place_checker(board, col_idx, player_checker):
            # Column is full, player loses turn
            return None
        else:
            # Successfully placed, return col index
            return col_idx

def main():
    # Initialize board
    board = create_board(ROWS, COLS)

    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Corresponding checkers for players playing this game
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    while True:
        clear_screen()
        print_board(board)

        # Current player's checker symbol
        checker = players[current_player_index]

        # Get player's move
        col_index_placed = get_valid_column_input(board, checker)
        # If column was full and no checker placed, lose turn (current_player_index changes)
        if col_index_placed is None:
            # Inform player of turn loss due to full column
            print(f"Column is full. Player {checker} loses their turn.")
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # After move, check for win
        if check_winner(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Check draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
