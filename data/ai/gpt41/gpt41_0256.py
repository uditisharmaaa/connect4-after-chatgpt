import os
import random
import string
import sys

# Constants (can change these for other dimensions, but for submission use 6 rows, 7 cols, 2 players)
ROWS = 6
COLS = 7
MAX_COLS = 26  # do not allow more than 26 columns (alphabet letters)
NUM_PLAYERS = 2  # between 2-5
CHECKERS = ["X", "O", "V", "H", "M"]

# Board creation: creates a 2D list (list of lists)
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Print the game board to the terminal in the proper format
def print_board(board, col_labels):
    os.system('clear')  # Clear the terminal (if on linux/mac)
    # Print column headers
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * len(col_labels))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(col_labels))

# Input: letter of the column. 
def get_valid_column_input(current_player_checker, col_labels, board):
    while True:
        entry = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if len(entry) != 1 or entry not in col_labels:
            print("Invalid input. Enter a single letter corresponding to a column label.")
            continue
        col_idx = col_labels.index(entry)
        # Check if the column is already full
        if board[0][col_idx] != " ":
            print(f"Column {entry} is full. You lose your turn.")
            return None  # Lose the turn as per assignment
        return col_idx

# Place the checker in the chosen column. Return the row number where the checker landed, or None if column is full.
def place_checker(board, col, checker):
    for row in reversed(range(len(board))):  # bottom up
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # In case the column is full (should not happen after input validation)

# Check win conditions from the last placed checker (row, col).
def check_win(board, row, col, checker):
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while in_bounds(r, c, board) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while in_bounds(r, c, board) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def in_bounds(r, c, board):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

# Check if the board is full (draw)
def check_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    if COLS > MAX_COLS:
        print(f"Error: Max allowed columns is {MAX_COLS}.")
        sys.exit(1)
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Only 2 to 5 players supported.")
        sys.exit(1)

    board = create_board(ROWS, COLS)
    col_labels = list(string.ascii_uppercase[:COLS])
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    print_board(board, col_labels)

    while True:
        player_checker = player_checkers[current_player]
        col_idx = get_valid_column_input(player_checker, col_labels, board)
        if col_idx is None:
            # Lose turn, move to next
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row_idx = place_checker(board, col_idx, player_checker)
        print_board(board, col_labels)
        # Check for win
        if check_win(board, row_idx, col_idx, player_checker):
            print(f"Player {player_checker} won!")
            break
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
