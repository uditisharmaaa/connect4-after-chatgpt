import os
import random

# Constants (for submission requirements)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # support up to 5 players, but will use only NUM_PLAYERS

WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column headers
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Print top border
    horizontal_line = "+" + "---+" * COLS
    for r in range(ROWS):
        print(horizontal_line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(horizontal_line)


def is_valid_column(col_char):
    return col_char in COLUMN_LABELS


def column_index(col_char):
    return ord(col_char) - ord('A')


def place_checker(board, col_idx, checker):
    # Place checker in lowest available spot in column col_idx
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # column full


def check_win(board, row, col, checker):
    # Check 4 directions (horizontal, vertical, both diagonals)
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def is_draw(board):
    # If any cell in the top row is empty, not draw
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player = players[current_player_index]
        print(f"Player {player}, please enter a column:")

        col_char = input().strip().upper()

        # Validate input
        if not is_valid_column(col_char):
            print("Invalid column. Please enter a valid column letter.")
            continue

        col_idx = column_index(col_char)
        pos = place_checker(board, col_idx, player)
        if pos is None:
            # Column full => lose turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        row, col = pos
        if check_win(board, row, col, player):
            print(f"Player {player} won!")
            break

        if is_draw(board):
            print("Game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
