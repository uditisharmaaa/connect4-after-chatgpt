import os
import random
import sys

# Constants (you can change ROWS, COLS, and NUM_PLAYERS for testing)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Supported range: 2 to 5

# Player tokens in order
TOKENS = ["X", "O", "V", "H", "M"]

# Validation for constants
if COLS > 26:
    print("Error: Maximum number of columns is 26.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: Number of players must be between 2 and 5.")
    sys.exit(1)

ACTIVE_TOKENS = TOKENS[:NUM_PLAYERS]


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    # Clear screen for Unix/Linux/macOS
    os.system('clear')


def print_board(board, col_labels):
    clear_screen()
    # Header with column labels
    header = "  " + "   ".join(col_labels)
    print(header)
    sep = "+" + ("---+" * len(col_labels))
    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(len(col_labels)):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep)


def get_valid_column_input(num_cols, current_token):
    col_labels = [chr(ord('A') + i) for i in range(num_cols)]
    prompt = f"Player {current_token}, please enter a column: "
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single uppercase letter for the column.")
            continue
        if user_input not in col_labels:
            print(f"Invalid column. Please enter a letter between {col_labels[0]} and {col_labels[-1]}.")
            continue
        return ord(user_input) - ord('A')


def drop_checker(board, col, token):
    # Place in the lowest available row in the given column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = token
            return row
    return None  # Column full


def check_win(board, token):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, down-right, down-left
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1),
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == token:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    col_labels = [chr(ord('A') + i) for i in range(COLS)]

    # Randomly select starting player index
    current_player_index = random.randrange(NUM_PLAYERS)

    # Game loop
    while True:
        print_board(board, col_labels)
        current_token = ACTIVE_TOKENS[current_player_index]

        # Get valid column input (invalid inputs do not lose the turn)
        col = get_valid_column_input(COLS, current_token)

        # Try to drop checker (if column full, turn is lost)
        placed_row = drop_checker(board, col, current_token)
        if placed_row is None:
            print(f"Column {chr(ord('A') + col)} is full. Player {current_token} loses the turn.")
            input("Press Enter to continue...")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # After a successful move, check for win or draw
        if check_win(board, current_token):
            print_board(board, col_labels)
            print(f"Player {current_token} won!")
            break

        if is_board_full(board):
            print_board(board, col_labels)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
