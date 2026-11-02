import os
import random

# Constants
ROWS = 6
COLUMNS = 7
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # Must be between 2 and 5
WIN_CONDITION = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print top border line
    print("+---" * COLUMNS + "+")
    for row in board:
        # Print row with vertical separators
        print("| " + " | ".join(row) + " |")
        # Print separator line
        print("+---" * COLUMNS + "+")


def input_valid_column(input_str):
    if len(input_str) != 1:
        return False
    ch = input_str.upper()
    return ch in COLUMN_LABELS


def get_column_index(column_letter):
    return ord(column_letter) - ord('A')


def place_checker(board, col, checker):
    # Place checker at lowest available spot in the column
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][col] == " ":
            board[row_idx][col] = checker
            return row_idx, col
    return None  # Column full


def check_win(board, row, col, checker):
    # Directions: horiz, vert, diagonal /, diagonal \
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count the placed checker itself

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_CONDITION:
            return True
    return False


def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True


def main():
    # Initialize board
    board = create_board(ROWS, COLUMNS)
    # Players' checkers (only as many as NUM_PLAYERS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        # Prompt player input with validation
        while True:
            print(f"Player {checker}, please enter a column:")
            user_input = input().strip().upper()
            if not input_valid_column(user_input):
                continue
            col = get_column_index(user_input)
            # Check if column full
            if board[0][col] != " ":
                # Turn lost if column full, print message then break input loop
                break  # Lose turn
            else:
                break  # Valid input and can place checker

        # If column full, player loses turn
        if board[0][col] != " ":
            print_board(board)
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place checker
        row, _ = place_checker(board, col, checker)
        print_board(board)

        # Check win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
