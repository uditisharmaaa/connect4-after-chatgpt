import os
import random
import string
import sys

# =============== CONSTANTS ================
BOARD_ROWS = 6
BOARD_COLS = 7    # max should be 26 (A-Z)
NUM_PLAYERS = 2   # 2-5 players supported
PLAYER_MARKS = ['X', 'O', 'V', 'H', 'M']

# ============== BOARD FUNCTIONS ============

def create_board(rows, cols):
    """Creates a 2D board (list of lists) filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_board(board):
    """Prints the board to the console in Connect 4 style."""
    cols = len(board[0])
    header_letters = " ".join("  {}".format(string.ascii_uppercase[i]) for i in range(cols))
    print("\n" + header_letters)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def is_full(board):
    """Checks if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

# ============== GAME LOGIC FUNCTIONS ============

def get_next_open_row(board, col):
    """
    Returns the index of the lowest empty cell in the given column,
    or None if the column is full.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def check_win(board, row, col, player_mark):
    """
    Checks if the current move at (row, col) by player_mark resulted in a win.
    Checks all four directions: horizontal, vertical, two diagonals.
    """
    directions = [
        (0, 1),  # horizontal /
        (1, 0),  # vertical |
        (1, 1),  # diagonal \
        (1, -1)  # diagonal /
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while in_bounds(board, r, c) and board[r][c] == player_mark:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while in_bounds(board, r, c) and board[r][c] == player_mark:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def in_bounds(board, row, col):
    """Checks if the position (row, col) is within the board."""
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def valid_column_input(input_str, cols):
    """Checks if the input string is a valid column letter for the current board size."""
    if len(input_str) == 1 and input_str.isalpha() and input_str.isupper():
        idx = ord(input_str) - ord('A')
        if 0 <= idx < cols:
            return idx
    return None

# ============= MAIN GAME LOOP ===============

def main():
    # Get player marks for the number of players
    player_marks = PLAYER_MARKS[:NUM_PLAYERS]

    # Create and display the board
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS-1)

    clear_screen()
    print_board(board)
    print(f'Player {player_marks[current_player_idx]} starts!\n')

    while True:
        player_mark = player_marks[current_player_idx]
        cols = len(board[0])
        move_made = False

        while not move_made:
            user_input = input(f"Player {player_mark}, please enter a column: ").strip().upper()
            col = valid_column_input(user_input, cols)
            if col is None:
                print("Invalid input. Please enter a valid column letter (A-{}).".format(string.ascii_uppercase[cols-1]))
                continue

            open_row = get_next_open_row(board, col)
            if open_row is not None:
                # Place checker
                board[open_row][col] = player_mark
                move_made = True
            else:
                print("Column is full! You lose your turn.")
                move_made = True  # As per assignment, turn is lost

        clear_screen()
        print_board(board)

        # Check for win
        if open_row is not None and check_win(board, open_row, col, player_mark):
            print(f"Player {player_mark} won!")
            break

        # Check for draw
        if is_full(board):
            print("Game is a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
