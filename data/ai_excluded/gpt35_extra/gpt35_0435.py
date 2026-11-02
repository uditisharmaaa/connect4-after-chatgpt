import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_COLUMNS = 1
MIN_ROWS = 1
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4

# Settings for submission
NUM_ROWS = 6
NUM_COLUMNS = 7
NUM_PLAYERS = 2


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for __ in range(rows)]


def print_board(board):
    clear_screen()

    columns = len(board[0])
    rows = len(board)

    # Print column letters
    header = '  '
    for i in range(columns):
        header += chr(ord('A') + i) + '   '
    print(header)

    # Print top border line of first row
    print('+' + '---+' * columns)

    for r in range(rows):
        row_str = '|'
        for c in range(columns):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
        print('+' + '---+' * columns)


def get_valid_column_input(current_player_checker, columns, board):
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            # invalid length
            continue
        col_letter = user_input[0]
        if not ('A' <= col_letter < chr(ord('A') + columns)):
            # invalid letter
            continue
        col_index = ord(col_letter) - ord('A')
        # Check if column is full - if full player loses turn
        if board[0][col_index] != ' ':
            # column full => losing turn
            return col_index, False
        return col_index, True


def drop_checker(board, col_index, checker):
    # from bottom row upwards find first empty cell
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return r, col_index
    # Should never reach here if checked before that the column is not full
    return None


def check_winner(board, last_row, last_col, checker):
    rows = len(board)
    columns = len(board[0])

    def count_in_direction(dr, dc):
        count = 0
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal, vertical, diagonal \, diagonal /
    directions = [
        ((0, -1), (0, 1)),    # horizontal
        ((-1, 0), (1, 0)),    # vertical
        ((-1, -1), (1, 1)),   # diagonal \
        ((-1, 1), (1, -1))    # diagonal /
    ]

    for (dir1, dir2) in directions:
        c1 = count_in_direction(*dir1)
        c2 = count_in_direction(*dir2)
        if (c1 + 1 + c2) >= WIN_COUNT:
            return True
    return False


def board_full(board):
    return all(cell != ' ' for cell in board[0])


def main():
    rows = NUM_ROWS
    columns = NUM_COLUMNS
    num_players = NUM_PLAYERS

    # Validate constraints (for general code safety)
    if not (MIN_ROWS <= rows and rows <= 1000):
        raise ValueError("Invalid number of rows")
    if not (MIN_COLUMNS <= columns <= MAX_COLUMNS):
        raise ValueError("Invalid number of columns")
    if not (MIN_PLAYERS <= num_players <= MAX_PLAYERS):
        raise ValueError("Invalid number of players")

    board = create_board(rows, columns)

    players = PLAYERS_CHECKERS[:num_players]

    # Select random starting player
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_index]

        # Get move input
        col_index, can_play = get_valid_column_input(current_checker, columns, board)

        if not can_play:
            # column full => lose turn
            current_player_index = (current_player_index + 1) % num_players
            continue

        # Place checker
        pos = drop_checker(board, col_index, current_checker)

        print_board(board)

        # Check for win
        if check_winner(board, pos[0], pos[1], current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("Game ended in a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
