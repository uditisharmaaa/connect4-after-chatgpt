import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5

CHECKERS = ["X", "O", "V", "H", "M"]

# For this submission, must be 2 players and 6x7 board per assignment instructions
NUM_PLAYERS = 2


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(columns))
    print(labels)
    # Print board rows with +---+ separators
    row_separator = "+" + "---+" * columns
    for row in range(len(board)):
        print(row_separator)
        row_str = "|"
        for col in range(columns):
            row_str += " " + board[row][col] + " |"
        print(row_str)
    print(row_separator)


def choose_first_player(num_players):
    return random.randint(0, num_players - 1)


def valid_column_input(inp, columns):
    if len(inp) != 1:
        return False
    if not inp.isalpha():
        return False
    col_index = ord(inp.upper()) - ord('A')
    if col_index < 0 or col_index >= columns:
        return False
    return True


def column_full(board, col):
    # top row is index 0, if occupied means full
    return board[0][col] != " "


def place_checker(board, col, checker):
    """Place checker in lowest empty row in column col.
    Return True if placed, False if column full."""
    # rows go 0..ROWS-1 top to bottom, so place in bottom-most.
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # Column full


def check_win(board, player_checker, row, col):
    """Check if placing checker at (row, col) wins the game for player_checker.
    We only need to check from (row, col) in all directions."""

    def count_consecutive(r_step, c_step):
        count = 1  # include current cell
        # Check in positive direction
        r, c = row + r_step, col + c_step
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r += r_step
            c += c_step
        # Check in negative direction
        r, c = row - r_step, col - c_step
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r -= r_step
            c -= c_step
        return count

    # Directions: horizontal, vertical, diagonal /
    if count_consecutive(0, 1) >= 4:
        return True
    if count_consecutive(1, 0) >= 4:
        return True
    if count_consecutive(1, 1) >= 4:
        return True
    if count_consecutive(1, -1) >= 4:
        return True

    return False


def board_full(board):
    for col in range(len(board[0])):
        if not column_full(board, col):
            return False
    return True


def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_idx = choose_first_player(NUM_PLAYERS)
    current_player = players[current_player_idx]

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not valid_column_input(user_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = ord(user_input) - ord('A')
            if column_full(board, col):
                # According to spec, player loses turn if column full.
                # Inform player and break input loop to lose turn
                print(f"Column {user_input} is full. You lose your turn.")
                col = None
                break
            else:
                break

        if col is not None:
            row_placed = place_checker(board, col, current_player)
            print_board(board)
            if check_win(board, current_player, row_placed, col):
                print(f"Player {current_player} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break
        else:
            print_board(board)

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        current_player = players[current_player_idx]


if __name__ == "__main__":
    main()
