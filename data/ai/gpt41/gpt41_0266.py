import random
import os
import string
import sys

# -------------------- CONSTANTS ----------------------
NUM_ROWS = 6                      # Board rows (height), can be changed
NUM_COLS = 7                      # Board columns (width), can be up to 26
NUM_PLAYERS = 2                   # Number of players (2 - 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players
WIN_LENGTH = 4                    # Number in a row to win

# -------------------- FUNCTIONS ----------------------

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty game board with given dimensions.
    Each cell initialized to whitespace (' ').
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board with column headers (A, B, ...).
    """
    rows = len(board)
    cols = len(board[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    col_label = "  " + "   ".join(letters)
    divider = "+" + ("---+" * cols)
    print(col_label)
    print(divider)
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print(divider)

def get_valid_columns(board):
    """
    Returns a list of column indices that are not full.
    """
    cols = len(board[0])
    return [c for c in range(cols) if board[0][c] == ' ']

def column_input_to_index(inp):
    """
    Converts column input letter (e.g. 'A') to the corresponding index.
    Returns -1 if invalid.
    """
    inp = inp.upper()
    if len(inp) != 1 or inp < 'A' or inp > chr(ord('A') + NUM_COLS - 1):
        return -1
    return ord(inp) - ord('A')

def make_move(board, column, checker):
    """
    Attempts to place 'checker' in the given 'column' on the board.
    Returns the row index if successful, None if the column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row
    return None

def is_board_full(board):
    """
    Returns True if the board is full (no empty spaces left), False otherwise.
    """
    return all(cell != ' ' for cell in board[0])

def check_direction(board, row, col, checker, delta_row, delta_col):
    """
    Checks one direction (given by delta_row, delta_col) for WIN_LENGTH in a row.
    Returns True if found.
    """
    count = 0
    r, c = row, col
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, checker):
    """
    Checks if placing 'checker' at (row, col) wins the game.
    Must check all four directions.
    Returns True if win is found.
    """
    directions = [ (0,1), (1,0), (1,1), (-1,1) ]  # horiz, vert, diag /, diag \
    for dr, dc in directions:
        count = 1  # Current piece
        # Count one direction
        count += count_in_dir(board, row, col, checker, dr, dc)
        # Count the opposite direction
        count += count_in_dir(board, row, col, checker, -dr, -dc)
        if count >= WIN_LENGTH:
            return True
    return False

def count_in_dir(board, row, col, checker, dr, dc):
    """
    Count consecutive checkers of the same player in one direction.
    (Used for win checking: doesn't include the current starting position.)
    """
    cnt = 0
    r, c = row + dr, col + dc
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        cnt += 1
        r += dr
        c += dc
    return cnt

# -------------------- GAME ---------------------------

def main():
    # Setup
    if NUM_COLS > 26 or NUM_COLS < 1 or NUM_ROWS < 1:
        print("Column and row dimensions must be valid (Cols max 26).")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return

    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Start game
    while True:
        clear_screen()
        print_board(board)
        if is_board_full(board):
            print("The game is a draw!")
            break
        checker = players[current_player]
        print(f"Player {checker}, please enter a column:", end=" ")

        valid_move = False
        while not valid_move:
            user_input = input().strip()
            col = column_input_to_index(user_input)
            if col == -1:
                print(f"Invalid input. Please enter a column (A-{chr(ord('A')+NUM_COLS-1)}):", end=" ")
                continue
            if board[0][col] != ' ':
                print("Column is full. Turn is lost.")
                break  # Lose turn
            row = make_move(board, col, checker)
            if row is not None:
                valid_move = True
            else:
                # Should not occur as we check for full columns
                print("Column is full. Please choose another column:", end=" ")

        # Only check for win if the move was made
        if valid_move:
            if check_win(board, row, col, checker):
                clear_screen()
                print_board(board)
                print(f"Player {checker} won!")
                break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
