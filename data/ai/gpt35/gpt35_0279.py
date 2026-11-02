import os
import random
import string

# Constants
ROWS = 6
COLS = 7  # max 26 allowed, this assignment fixed to 7
PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
# We'll slice CHECKERS for number of players

WIN_COUNT = 4


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(headers))
    # Print separator line function
    def sep_line():
        return "+" + "+".join(["---"] * cols) + "+"

    for r in range(len(board)):
        print(sep_line())
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep_line())


def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    return 'A' <= col_char < chr(ord('A') + cols)


def col_to_index(col_char):
    return ord(col_char.upper()) - ord('A')


def place_checker(board, col_idx, checker):
    """
    Places checker in lowest available cell in column col_idx.
    Returns True if placed successfully, False if column full.
    """
    # start from bottom row upwards
    for r in reversed(range(len(board))):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return True
    return False  # column full


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Diagonal check (bottom-left to top-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            # check diagonal sequence
            count = 0
            for i in range(WIN_COUNT):
                if board[r + i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    # Diagonal check (top-left to bottom-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r - i][c + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True

    return False


def check_draw(board):
    # Draw if no empty space in top row (since checkers stack from bottom)
    # or if all cells filled
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        checker = players[current_player_idx]
        # prompt player for input, validate input, redo if invalid
        while True:
            print(f"Player {checker}, please enter a column:")
            col_input = input().strip().upper()
            if not is_valid_column(col_input, COLS):
                print("Invalid input. Please enter a valid column letter.")
                continue

            col_idx = col_to_index(col_input)
            placed = place_checker(board, col_idx, checker)
            if not placed:
                # According to spec: "If the column is already completely filled with checkers,
                # the turn is invalid and the player loses the turn."
                # So no retry, just break this while and move to next player
                print(f"Column {col_input} is full. Player {checker} loses the turn.")
                break
            else:
                # Successfully placed checker
                break

        print_board(board)

        # If player placed checker, check win (if placed == False, player lost turn and did not place)
        if placed:
            if check_winner(board, checker):
                print(f"Player {checker} won!")
                break

        # Check draw
        if check_draw(board):
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS


if __name__ == "__main__":
    main()
