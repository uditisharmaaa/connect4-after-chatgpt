#!/usr/bin/env python3

import os
import random
import string

# Constants for the board dimensions (rows x columns)
ROWS = 6
COLUMNS = 7

# Constants for players (max 5 players supported)
PLAYERS = 2  # Change this to 2-5 for more players
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of checkers in a row to win
WIN_COUNT = 4


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, columns):
    """
    Create a board with given dimensions filled with spaces.

    Args:
        rows (int): number of rows in the board
        columns (int): number of columns in the board

    Returns:
        list: 2D list representing the board
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """
    Print the board with column labels and horizontal separator lines.

    Args:
        board (list): 2D list representing the board
    """
    columns = len(board[0])
    # Print column labels (A, B, C, ...)
    print(" ", end=" ")
    for c in range(columns):
        print(f" {chr(ord('A') + c)} ", end=" ")
    print()

    # Print horizontal line and rows
    row_separator = "+" + ("---+" * columns)
    for row in range(len(board)):
        print(row_separator)
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
    print(row_separator)


def get_valid_column_input(current_player, columns, board):
    """
    Prompt the current player to input a valid column letter.

    Args:
        current_player (str): current player's checker character
        columns (int): number of columns on the board
        board (list): current state of the board

    Returns:
        int or None: column index (0-based) or None if column is full (turn lost)
    """
    valid_letters = [chr(ord('A') + i) for i in range(columns)]
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").upper().strip()
        if len(user_input) != 1:
            # Input must be a single character
            print("Invalid input. Please enter exactly one column letter (A - {}).".format(valid_letters[-1]))
            continue
        if user_input not in valid_letters:
            # Input must be a valid column letter
            print("Invalid column. Please enter a letter from A to {}.".format(valid_letters[-1]))
            continue
        col_idx = ord(user_input) - ord('A')
        # Check if the column is full (top row occupied)
        if board[0][col_idx] != " ":
            # Turn lost if full
            print(f"Column {user_input} is full! You lose this turn.")
            return None
        # Valid input and column not full
        return col_idx


def place_checker(board, col, checker):
    """
    Place the checker in the lowest empty cell in the specified column.

    Args:
        board (list): 2D list representing the board
        col (int): column index to place the checker
        checker (str): player's checker character

    Returns:
        tuple: (row, col) coordinates where the checker was placed
    """
    # Start from bottom row and find first empty cell in the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return (row, col)
    # Should never reach here if input validation is correct
    return None


def check_win(board, last_row, last_col, checker):
    """
    Check if placing checker at (last_row, last_col) caused a win.

    Args:
        board (list): 2D list representing the board
        last_row (int): row index of last placed checker
        last_col (int): column index of last placed checker
        checker (str): player's checker character

    Returns:
        bool: True if player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        """
        Count checkers matching 'checker' starting from last placed checker
        going in the (dr, dc) direction and opposite direction.

        Args:
            dr (int): row delta
            dc (int): column delta

        Returns:
            int: total count of consecutive checkers in both directions minus 1
        """
        count = 1
        # Check one direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        return count

    # Directions to check: horizontal, vertical, diagonal /
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        if count_direction(dr, dc) >= WIN_COUNT:
            return True
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).

    Args:
        board (list): 2D list representing the board

    Returns:
        bool: True if board is full, False otherwise
    """
    # If any cell in top row is empty, game is not a draw
    return all(cell != " " for cell in board[0])


def main():
    # Initialize board
    board = create_board(ROWS, COLUMNS)

    # Select players' checkers
    players = CHECKERS[:PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]

        # Get player's valid input column or None if column full (turn lost)
        col = get_valid_column_input(current_checker, COLUMNS, board)
        if col is not None:
            # Place checker in the board
            position = place_checker(board, col, current_checker)

            # Check win condition
            if check_win(board, position[0], position[1], current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            # Check draw condition
            if check_draw(board):
                clear_screen()
                print_board(board)
                print("Game is a draw!")
                break

        # Advance to next player regardless of turn lost or not
        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
