import os
import random
import string
import sys

# CONSTANTS FOR CONFIGURATION
ROWS = 6               # Number of rows in the board
COLS = 7               # Number of columns in the board (max 26)
NUM_PLAYERS = 2        # Number of players (2-5 supported)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Markers per player
WIN_LENGTH = 4         # Number of checkers in a row needed to win

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def create_board(rows, cols):
    """Creates a board with the given dimensions initialized with whitespaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the game board in a formatted way."""
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+' * cols)


def get_player_input(player_checker, cols, board):
    """Asks the player for a valid input and returns the column index to place the checker."""
    valid_cols = string.ascii_uppercase[:cols]
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Input validation
        if len(user_input) != 1 or user_input not in valid_cols:
            print(f"Invalid input! Please enter a letter between A and {valid_cols[-1]}.")
            continue
        col_idx = valid_cols.index(user_input)
        # Check if column is full
        if board[0][col_idx] != ' ':
            print("Column is full! You lose your turn.")
            return None
        return col_idx


def drop_checker(board, col_idx, checker):
    """
    Attempts to drop a checker in the column.
    Returns the row index where the checker lands, or None if the column is full.
    """
    rows = len(board)
    for row in range(rows-1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row
    return None  # Should not reach here as we check for full columns before


def board_full(board):
    """Returns True if the board is full (all cells are occupied), else False."""
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            return False
    return True


def check_win(board, row, col, checker):
    """
    Checks if placing 'checker' at (row, col) creates a sequence
    of WIN_LENGTH of the same marker horizontally, vertically, or diagonally.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False


def main():
    # Set up the board and other game variables
    board = create_board(ROWS, COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        player_checker = player_checkers[current_player]
        col_idx = get_player_input(player_checker, COLS, board)
        if col_idx is None:
            # Invalid turn, skip player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row_idx = drop_checker(board, col_idx, player_checker)

        clear_screen()
        print_board(board)

        if check_win(board, row_idx, col_idx, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
