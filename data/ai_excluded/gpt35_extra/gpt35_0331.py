import os
import random
import sys

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_CONDITION = 4

# Players and their checkers in order
PLAYERS_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Settings for submission
NUM_PLAYERS = 2  # Set to 2 players for submission


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    # Create a board filled with spaces " "
    return [[' ' for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    columns = len(board[0])

    # Print column headers
    header = '  '
    for c in range(columns):
        header += f'  {chr(ord("A") + c)} '
    print(header)

    # Print board rows with separators
    separator = '+' + ('---+' * columns)
    for row in board:
        print(separator)
        row_str = '|'
        for cell in row:
            row_str += f' {cell} |'
        print(row_str)
    print(separator)


def is_valid_column_input(col_char, columns):
    if len(col_char) != 1:
        return False
    if not (col_char.isalpha() and col_char.isupper()):
        return False
    index = ord(col_char) - ord('A')
    if index < 0 or index >= columns:
        return False
    return True


def get_lowest_empty_row(board, col):
    # Returns the index of the lowest empty row in column col
    # or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None


def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is None:
        # Column full
        return False
    board[row][col] = checker
    return True


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0

    # Diagonal check (bottom-left to top-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            win = True
            for i in range(WIN_CONDITION):
                if board[r + i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    # Diagonal check (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            win = True
            for i in range(WIN_CONDITION):
                if board[r - i][c + i] != checker:
                    win = False
                    break
            if win:
                return True

    return False


def check_draw(board):
    # Draw if all cells are filled (no spaces left)
    for row in board:
        if ' ' in row:
            return False
    return True


def select_random_player(num_players):
    return random.randint(0, num_players - 1)


def main():
    # Validate constants for safety
    if COLUMNS > MAX_COLUMNS:
        print(f"Error: max columns supported is {MAX_COLUMNS}")
        sys.exit(1)
    if NUM_PLAYERS < MIN_PLAYERS or NUM_PLAYERS > MAX_PLAYERS:
        print(f"Error: number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}")
        sys.exit(1)

    board = create_board(ROWS, COLUMNS)
    players = PLAYERS_CHECKERS[:NUM_PLAYERS]

    current_player_index = select_random_player(NUM_PLAYERS)
    print_board(board)

    while True:
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "

        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column_input(user_input, COLUMNS):
                # Invalid input, ask again
                continue

            col_index = ord(user_input) - ord('A')
            lowest_row = get_lowest_empty_row(board, col_index)

            if lowest_row is None:
                # Column full, player loses turn as per spec
                break

            # Place checker and break to check win
            place_checker(board, col_index, current_checker)
            break

        print_board(board)

        # If checker was placed this turn, check for win
        if lowest_row is not None:
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
