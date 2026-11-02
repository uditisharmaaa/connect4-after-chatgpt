import os
import random

# Constants for board dimensions
ROWS = 6
COLS = 7

# Constants for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
NUM_PLAYERS = 2  # Set to 2 players as per submission requirement

WIN_LENGTH = 4  # Number of checkers in a row needed to win


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """
    Create a 2D board initialized with spaces.
    Board[row][col], where row 0 is the top of the board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the Connect 4 board with column letters."""
    clear_screen()
    cols = len(board[0])
    rows = len(board)

    # Print column headers (A,B,C,...)
    col_headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(col_headers)

    # Print the board rows with separators
    line_sep = "+" + "---+" * cols
    for r in range(rows):
        print(line_sep)
        # Each cell in the row
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line_sep)


def get_valid_column_input(current_player, cols, board):
    """
    Prompt the current player for a column input until a valid
    uppercase letter within the board range and with at least one empty slot is entered.
    Return column index (0-based). If column is full, player loses turn.
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip()
        # Validate length and uppercase letter
        if len(user_input) != 1 or not user_input.isalpha() or not user_input.isupper():
            print(f"Invalid input. Please enter a single uppercase letter between A and {chr(ord('A')+cols-1)}.")
            continue

        col_idx = ord(user_input) - ord('A')
        # Check if column is inside board
        if col_idx < 0 or col_idx >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A')+cols-1)}.")
            continue

        # Check if column has space to place a checker
        if board[0][col_idx] != " ":  # top row is occupied -> full
            print(f"Column {user_input} is full. You lose your turn.")
            return None
        return col_idx


def place_checker(board, col_idx, checker):
    """
    Place the checker in the lowest available row in the chosen column.
    Return the row index where checker was placed.
    """
    rows = len(board)
    # Start from bottom row and go up until find empty space
    for row in reversed(range(rows)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row
    return None  # Should never happen if checked before placing


def check_win(board, row, col, checker):
    """
    Check from the placed location (row, col) if player has 4 in a row
    horizontally, vertically or diagonally.
    Return True if win detected else False.
    """

    def count_in_direction(delta_r, delta_c):
        """Count continuous checkers matching 'checker' starting from (row,col) in given direction."""
        r, c = row + delta_r, col + delta_c
        count = 0
        rows = len(board)
        cols = len(board[0])
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += delta_r
            c += delta_c
        return count

    # Directions to check: horizontal, vertical, two diagonals
    directions = [
        ((0, 1), (0, -1)),    # Horizontal right & left
        ((1, 0), (-1, 0)),    # Vertical down & up
        ((1, 1), (-1, -1)),   # Diagonal down-right & up-left
        ((1, -1), (-1, 1))    # Diagonal down-left & up-right
    ]

    for dir1, dir2 in directions:
        count = 1  # count current checker
        count += count_in_direction(*dir1)
        count += count_in_direction(*dir2)
        if count >= WIN_LENGTH:
            return True
    return False


def check_draw(board):
    """Return True if board is full (draw), otherwise False."""
    return all(cell != " " for cell in board[0])


def main():
    # Initialize board
    board = create_board(ROWS, COLS)

    # Player checkers based on NUM_PLAYERS
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Choose random starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board and show who starts
    print_board(board)
    print(f"Player {players[current_player_idx]} starts the game.")

    while True:
        current_checker = players[current_player_idx]

        col_idx = get_valid_column_input(current_checker, COLS, board)

        # If column full (None returned), turn is lost
        if col_idx is not None:
            row_idx = place_checker(board, col_idx, current_checker)
            print_board(board)

            # Check for win
            if check_win(board, row_idx, col_idx, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if check_draw(board):
                print("Game is a draw!")
                break
        else:
            # Player lost their turn due to full column
            print_board(board)

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
