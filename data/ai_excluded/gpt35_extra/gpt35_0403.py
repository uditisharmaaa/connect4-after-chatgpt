import os
import random
import string

# Constants - Change here for different configurations
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # between 2 and 5
WIN_LENGTH = 4

# Player checkers order
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print top border line
    print("+" + "---+" * COLUMNS)
    for row in board:
        # Print each row with vertical bars
        print("| " + " | ".join(row) + " |")
        # Print border line below each row
        print("+" + "---+" * COLUMNS)


def is_valid_column(col):
    return col in COLUMN_LABELS


def column_index(col):
    # Convert column letter to zero-based index
    return COLUMN_LABELS.index(col)


def is_column_full(board, col_idx):
    # Top row in column filled means no more space
    return board[0][col_idx] != " "


def place_checker(board, col_idx, checker):
    """
    Place the checker in the selected column.
    The checker falls to the lowest empty row in that column.
    Returns True if placed, False if column full.
    """
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False


def check_win(board, checker):
    """
    Checks all possible directions for 4 connected checkers of the given player.
    Returns True if found, False otherwise.
    """

    # Horizontal check
    for r in range(ROWS):
        count = 0
        for c in range(COLUMNS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(COLUMNS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == WIN_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal (down-right) check
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Diagonal (down-left) check
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[r + i][c - i] == checker for i in range(WIN_LENGTH)):
                return True

    return False


def board_full(board):
    # If no empty spaces in top row (or anywhere), board is full
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True


def get_player_input(player_checker):
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not col or len(col) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        if not is_valid_column(col):
            print(f"Invalid column. Please enter a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        return col


def main():
    board = create_board(ROWS, COLUMNS)
    # Randomly choose first player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    print_board(board)

    while True:
        player_checker = CHECKERS[current_player_idx]
        col_letter = get_player_input(player_checker)
        col_idx = column_index(col_letter)

        if is_column_full(board, col_idx):
            print(f"Column {col_letter} is full. Player {player_checker} loses the turn.")
            # Switch player turn even if invalid (turn is lost)
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        placed = place_checker(board, col_idx, player_checker)
        # placed should always be True here because we check column full before

        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
