import os
import random
import sys

# Constants (you may change these for testing, but submit with these values)
ROWS = 6
COLUMNS = 7  # up to 26 max
NUM_PLAYERS = 2  # between 2 and 5

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Ensure constraints
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLUMNS < 1 or COLUMNS > 26:
    print("COLUMNS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_and_print_board(board):
    os.system('clear')
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    # Leading two spaces to match example alignment
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)

    # Top border and rows
    border = "+" + ("---+" * cols)
    for r in range(rows):
        print(border)
        row_cells = "|"
        for c in range(cols):
            row_cells += " " + board[r][c] + " |"
        print(row_cells)
    print(border)

def get_valid_column_input(cols, current_player):
    while True:
        entry = input(f"Player {current_player}, please enter a column: ").strip().upper()
        # Validate that it's a single uppercase letter within range
        if len(entry) == 1 and 'A' <= entry <= chr(ord('A') + cols - 1):
            return ord(entry) - ord('A')
        # Also allow user to type more than one char if first is valid single letter?
        # Spec says uppercase letter; keep strict.
        # Invalid input: prompt again (turn is not lost)
        # No message required by spec; silently reprompt is acceptable.

def drop_checker(board, col, checker):
    # Returns True if placed, False if column is full
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def is_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, diag down-right, diag down-left
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1),
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False

def main():
    board = create_board(ROWS, COLUMNS)
    # Randomly select first player index
    current_index = random.randrange(NUM_PLAYERS)

    # Print initial empty board before game starts
    clear_and_print_board(board)

    while True:
        # If the board is full before a move, it's a draw
        if is_full(board):
            print("It's a draw!")
            break

        current_player = PLAYERS[current_index]

        # Prompt for a valid column letter
        col = get_valid_column_input(COLUMNS, current_player)

        # Attempt to place checker
        placed = drop_checker(board, col, current_player)

        # Print updated board every turn (clear screen before printing)
        clear_and_print_board(board)

        if placed:
            # Check for win
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            # Check for draw after successful placement
            if is_full(board):
                print("It's a draw!")
                break
        else:
            # Column was full; player loses the turn (no re-prompt)
            pass

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
