import os
import random
import string

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Must be between 2 and 5
WIN_COUNT = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constant constraints
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5"
assert 1 <= ROWS and 1 <= COLS <= 26, "Board dimensions must be positive and columns <= 26"


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()

    # Print column headers (A, B, C, ...)
    headers = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(headers))

    # Separator line
    sep = "+" + "---+" * len(board[0])

    for row in range(len(board)):
        print(sep)
        # Print each cell in row with vertical bars
        print("| " + " | ".join(board[row]) + " |")
    print(sep)


def valid_column_input(user_input, cols):
    """Check if user input is a single uppercase alpha character within column range."""
    if len(user_input) != 1:
        return False
    if user_input not in string.ascii_uppercase[:cols]:
        return False
    return True


def find_lowest_empty_row(board, col):
    """Return the index of the lowest empty row in the chosen column, or None if full."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None


def place_checker(board, col, checker):
    """Place checker in the column at the lowest available space."""
    row = find_lowest_empty_row(board, col)
    if row is None:
        return False  # Column full
    board[row][col] = checker
    return True


def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal down-right check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal up-right check
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False


def board_full(board):
    """Return True if no empty spaces, False otherwise."""
    return all(cell != " " for row in board for cell in row)


def get_next_player_index(current_index, total_players):
    return (current_index + 1) % total_players


def main():
    board = create_board(ROWS, COLS)

    # Pick a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    players_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    print_board(board)

    while True:
        checker = players_checkers[current_player]
        prompt = f"Player {checker}, please enter a column: "

        while True:
            user_input = input(prompt).strip().upper()

            # Validate user input
            if not valid_column_input(user_input, COLS):
                print(f"Invalid input. Please enter a letter from A to {string.ascii_uppercase[COLS - 1]}.")
                continue

            col = string.ascii_uppercase.index(user_input)

            # Check if the column has space
            if find_lowest_empty_row(board, col) is None:
                # According to spec, if the column is full, the player loses the turn
                print(f"Column {user_input} is full. You lose your turn.")
                break

            # Valid and available move
            place_checker(board, col, checker)
            break

        print_board(board)

        # Check win if the move was valid (i.e., checker placed)
        if find_lowest_empty_row(board, col) is not None:  # checker was placed
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break

        # Check draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next turn
        current_player = get_next_player_index(current_player, NUM_PLAYERS)


if __name__ == "__main__":
    main()
