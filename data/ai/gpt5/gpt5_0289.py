import os
import random
import string

# Constants (submission requires 6 rows x 7 cols and 2 players)
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # can be between 2 and 5

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYERS = CHECKERS[:NUM_PLAYERS]

# Create an empty board (rows x columns) filled with spaces
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Clear screen and print the board with column headers
def print_board(board):
    os.system('clear')
    cols = len(board[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_str)
    print(sep)

# Validate user input: must be a single uppercase letter within range
def get_valid_column_input(cols):
    valid_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in string.ascii_uppercase:
            print("Invalid input. Enter a single letter.")
            continue
        if user_input not in valid_letters:
            print("Invalid column. Choose from:", " ".join(valid_letters))
            continue
        return ord(user_input) - ord('A')

# Try to place a checker in the chosen column; return (placed, row_index)
def place_checker(board, col, checker):
    # Start from bottom row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True, r
    return False, None  # column full

# Check if the given checker has 4 in a row including (row, col)
def is_winning_move(board, row, col, checker):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # count the placed checker itself
        # check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# Check if the board is full (draw)
def is_draw(moves_made, rows, cols):
    return moves_made >= rows * cols

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randrange(NUM_PLAYERS)
    moves_made = 0

    # Show initial empty board and who starts
    print_board(board)
    print(f"Player {PLAYERS[current_player_idx]} starts.")
    # Main game loop
    while True:
        print_board(board)
        print(f"Player {PLAYERS[current_player_idx]}, please enter a column:")
        col = get_valid_column_input(COLUMNS)

        placed, row = place_checker(board, col, PLAYERS[current_player_idx])
        if not placed:
            # Valid input but column full -> lose the turn
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {PLAYERS[current_player_idx]} loses the turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        moves_made += 1

        # Check for win
        if is_winning_move(board, row, col, PLAYERS[current_player_idx]):
            print_board(board)
            print(f"Player {PLAYERS[current_player_idx]} won!")
            break

        # Check for draw
        if is_draw(moves_made, ROWS, COLUMNS):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        # Graceful exit on Ctrl+D / Ctrl+C
        print()
