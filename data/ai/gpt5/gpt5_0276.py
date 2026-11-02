import os
import random
import string

# ====== Configuration (submission requires these exact values) ======
ROWS = 6                 # number of rows (height)
COLS = 7                 # number of columns (width), max 26
NUM_PLAYERS = 2          # number of players, between 2 and 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4           # number in a row needed to win

# ====== Utility and Game Functions ======

def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Support up to 26 columns using uppercase letters A..Z
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    cols = len(board[0])
    labels = column_labels(cols)

    # Header
    print("  " + "   ".join(labels))
    # Top border
    print("+" + ("---+" * cols))

    # Rows
    for r in range(len(board)):
        row_cells = "|".join(f" {board[r][c]} " for c in range(cols))
        print(f"|{row_cells}|")
        print("+" + ("---+" * cols))


def get_valid_input(valid_labels, current_player):
    while True:
        user_in = input(f"Player {current_player}, please enter a column: ").strip()
        if not user_in:
            print("Invalid input. Please enter a column letter.")
            continue

        # Accept lowercase but convert to uppercase
        user_in = user_in.upper()

        if len(user_in) != 1 or user_in not in valid_labels:
            print("Invalid input. Please enter a valid column letter shown above.")
            continue

        return user_in


def find_drop_row(board, col_index):
    # Return the lowest available row index in the column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return None


def drop_checker(board, col_index, checker):
    row_index = find_drop_row(board, col_index)
    if row_index is None:
        return None  # column full
    board[row_index][col_index] = checker
    return row_index


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, last_row, last_col, checker):
    # If no piece placed (e.g., turn lost due to full column), skip
    if last_row is None or last_col is None:
        return False

    rows, cols = len(board), len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # count the last placed checker
        # Check one way
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite way
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def check_draw(board):
    # Draw if no spaces left in the top row (or anywhere)
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Validate configuration
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
    assert 1 <= COLS <= 26, "COLS must be between 1 and 26"
    assert ROWS >= 1, "ROWS must be at least 1"

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    labels = column_labels(COLS)
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_index = random.randrange(NUM_PLAYERS)

    # Initial screen
    clear_screen()
    print_board(board)

    while True:
        current_player = players[current_index]
        # Prompt for input (must be a valid column label)
        col_label = get_valid_input(labels, current_player)
        col_index = labels.index(col_label)

        # Attempt to drop checker
        row_index = drop_checker(board, col_index, current_player)
        if row_index is None:
            # Column full -> invalid turn and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {col_label} is full. Player {current_player} loses the turn.")
            # Advance to next player
            current_index = (current_index + 1) % NUM_PLAYERS
            # Check for draw even if no move made? Not necessary, but safe:
            if check_draw(board):
                print("It's a draw!")
                break
            continue

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row_index, col_index, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
