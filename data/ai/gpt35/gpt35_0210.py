import os
import random

# Constants - board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Checkers for each player in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty board initialized with whitespaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the console with column letters and separators."""
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print(" ", end=" ")
    for label in col_labels:
        print(f" {label}  ", end="")
    print()

    # Print separator line
    sep_line = "+" + "---+" * cols
    for row in range(len(board)):
        print(sep_line)
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    print(sep_line)

def get_valid_column_input(player, board):
    """Prompt player for a valid column letter input and return the column index.
    If the column is full, the turn is lost (return None)."""
    cols = len(board[0])
    valid_letters = [chr(ord('A') + i) for i in range(cols)]

    while True:
        user_input = input(f"Player {player}, please enter a column: ").strip().upper()
        # Input validation: single letter, within valid range
        if len(user_input) != 1 or user_input not in valid_letters:
            print(f"Invalid input! Please enter a letter from A to {valid_letters[-1]}.")
            continue

        col = ord(user_input) - ord('A')
        # Check if the column is full:
        if board[0][col] != " ":
            # Column full, player loses turn
            print(f"Column {user_input} is full, you lose your turn!")
            return None

        return col

def place_checker(board, col, checker):
    """Place the checker in the lowest available row in column col."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col  # Return where checker was placed
    return None  # Should not happen if we check column fullness before

def check_for_win(board, row, col, checker):
    """Check whether placing 'checker' at (row, col) caused a win."""

    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def check_for_draw(board):
    """Returns True if all board is filled, else False."""
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Setup game:
    board = create_board(ROWS, COLS)

    # Select random first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    players = CHECKERS[:NUM_PLAYERS]

    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current_player_idx]

        col = get_valid_column_input(current_checker, board)
        if col is not None:
            # Place the checker if input was valid and column not full
            row, col = place_checker(board, col, current_checker)

            clear_screen()
            print_board(board)

            # Check for win
            if check_for_win(board, row, col, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if check_for_draw(board):
                print("The game is a draw!")
                break
        else:
            # col == None means column full and player lost turn
            # Just clear screen and print board again
            clear_screen()
            print_board(board)

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
