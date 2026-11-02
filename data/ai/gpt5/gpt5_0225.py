import os
import random

# Constants (you can change these for testing, but submit with ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    os.system('clear')
    cols = len(board[0])
    # Header with letters
    letters = []
    for i in range(cols):
        letters.append(chr(ord('A') + i))
    print("  " + "   ".join(letters))
    # Grid
    sep = "+" + ("---+" * cols)
    for r in range(len(board)):
        print(sep)
        row_str = ""
        for c in range(cols):
            row_str += "| " + board[r][c] + " "
        row_str += "|"
        print(row_str)
    print(sep)

def is_valid_column_input(s, cols):
    if len(s) != 1:
        return False
    if not s.isalpha() or not s.isupper():
        return False
    idx = ord(s) - ord('A')
    if idx < 0 or idx >= cols:
        return False
    return True

def drop_checker(board, col, checker):
    # Try to place checker in the lowest empty cell of the column.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontally
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r][c + 1] == checker and
                board[r][c + 2] == checker and
                board[r][c + 3] == checker):
                return True

    # Check vertically
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == checker and
                board[r + 1][c] == checker and
                board[r + 2][c] == checker and
                board[r + 3][c] == checker):
                return True

    # Check diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r + 1][c + 1] == checker and
                board[r + 2][c + 2] == checker and
                board[r + 3][c + 3] == checker):
                return True

    # Check diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r - 1][c + 1] == checker and
                board[r - 2][c + 2] == checker and
                board[r - 3][c + 3] == checker):
                return True

    return False

def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Basic validations
    if COLS > 26:
        print("Maximum number of columns is 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Random starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        # Read and validate input (invalid inputs are retried, column-full loses turn)
        while True:
            user_input = input().strip().upper()
            if is_valid_column_input(user_input, COLS):
                col_idx = ord(user_input) - ord('A')
                break
            else:
                print("Invalid input. Please enter a valid uppercase column letter:")
        # Try to drop checker
        row_placed = drop_checker(board, col_idx, current_checker)
        if row_placed is None:
            # Column full: turn lost
            print_board(board)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        # Successful move: print board and check for win/draw
        print_board(board)
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
