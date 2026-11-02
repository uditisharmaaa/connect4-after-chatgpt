import os
import random
import string
import sys

# Constants (you may change these for testing; final submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # Must be <= 26
NUM_PLAYERS = 2  # Between 2 and 5

TOKENS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear screen before printing the board
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    # Header
    print("  " + "   ".join(letters))
    # Rows
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print(sep)

def get_valid_input(valid_letters, current_token):
    prompt = f"Player {current_token}, please enter a column: "
    while True:
        user_in = input(prompt).strip().upper()
        if len(user_in) != 1 or user_in not in valid_letters:
            print(f"Invalid input. Please enter a column letter between {valid_letters[0]} and {valid_letters[-1]}.")
            continue
        return user_in

def drop_checker(board, col_idx, token):
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = token
            return True, r
    return False, None  # Column is full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc) for right, down, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                # Step forward
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    if count >= 4:
                        return True
                    nr += dr
                    nc += dc
                # Optionally could check backward, but counting forward from each start is sufficient
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Basic validations for constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

    board = create_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]
    letters = [string.ascii_uppercase[i] for i in range(COLS)]

    # Randomly select first player
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board
    print_board(board)

    while True:
        current_token = players[current_idx]
        # Ask for input and validate the column letter
        col_letter = get_valid_input(letters, current_token)
        col_idx = letters.index(col_letter)

        # Try to drop the checker
        placed, row_idx = drop_checker(board, col_idx, current_token)

        # After move attempt, print updated board
        print_board(board)

        if not placed:
            # Column is full, turn is lost
            print(f"Column {col_letter} is full. Player {current_token} loses the turn.")
            # Move to next player
            current_idx = (current_idx + 1) * 1 % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
