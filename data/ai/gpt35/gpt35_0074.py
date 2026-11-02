import os
import random

# Constants for the game configuration
ROWS = 6          # Number of rows on the board
COLUMNS = 7       # Number of columns on the board
PLAYERS = 2       # Number of players (between 2 and 5)
WIN_COUNT = 4     # Number of consecutive checkers needed to win

# Checkers assigned to players in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate players count and assign checkers accordingly
assert 2 <= PLAYERS <= 5, "Number of players must be between 2 and 5"
PLAYER_CHECKERS = CHECKERS[:PLAYERS]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """
    Creates and returns a board initialized with spaces.
    Board is a list of rows, each row is a list of columns.
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board with column labels and horizontal separators.
    Board columns are labeled with letters starting from 'A'.
    """
    rows = len(board)
    columns = len(board[0])
    # Print column labels
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(columns))
    print(labels)
    # Print each row with separators
    for row in range(rows):
        print("+---" * columns + "+")
        row_str = "|"
        for col in range(columns):
            row_str += f" {board[row][col]} |"
        print(row_str)
    print("+---" * columns + "+")

def is_valid_column_input(input_str, columns):
    """
    Checks if the input string is a single uppercase letter within board range.
    """
    if len(input_str) != 1:
        return False
    if not input_str.isalpha():
        return False
    col_index = ord(input_str.upper()) - ord('A')
    return 0 <= col_index < columns

def get_column_index(input_str):
    """
    Converts column letter input (e.g. 'A') to zero-based column index.
    """
    return ord(input_str.upper()) - ord('A')

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available row in the given column.
    Returns True if placed successfully, False if the column is full (loses turn).
    """
    # Start from bottom row and move upward
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    """
    Checks all directions (horizontal, vertical, diagonal) for a win condition.
    Returns True if the player with 'checker' has 4 in a row.
    """
    rows = len(board)
    columns = len(board[0])

    # Check horizontal
    for row in range(rows):
        count = 0
        for col in range(columns):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for col in range(columns):
        count = 0
        for row in range(rows):
            if board[row][col] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_COUNT + 1):
        for col in range(columns - WIN_COUNT + 1):
            count = 0
            for offset in range(WIN_COUNT):
                if board[row + offset][col + offset] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_COUNT - 1, rows):
        for col in range(columns - WIN_COUNT + 1):
            count = 0
            for offset in range(WIN_COUNT):
                if board[row - offset][col + offset] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False

def check_draw(board):
    """
    Returns True if the board is full (no spaces left), else False.
    """
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Create the board
    board = create_board(ROWS, COLUMNS)

    # Select random starting player
    current_player_index = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        checker = PLAYER_CHECKERS[current_player_index]
        print(f"Player {checker}, please enter a column:")

        # Get valid input from player
        while True:
            user_input = input("> ").strip()
            if not is_valid_column_input(user_input, COLUMNS):
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
                continue
            col = get_column_index(user_input)
            break

        # Try to place checker
        placed = place_checker(board, col, checker)
        if not placed:
            # Column full - lose turn without placement
            # Inform player politely and go to next player
            clear_screen()
            print_board(board)
            print(f"Column {user_input.upper()} is full. Player {checker} loses the turn.")
            # Switch player
            current_player_index = (current_player_index + 1) % PLAYERS
            input("Press Enter to continue...")
            continue

        # Check for win after placing checker
        if check_win(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
