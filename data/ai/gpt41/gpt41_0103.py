import os
import random
import string
import sys

# === CONSTANTS ===
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # 2 to 5

PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

COLUMN_LABELS = list(string.ascii_uppercase)[:COLUMNS]

# === FUNCTIONS ===

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')


def create_board(rows, columns):
    """Creates a 2D board (list of lists filled with white space)"""
    return [[' ' for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    """Prints the board with column headers as shown in description"""
    clear_screen()
    # Print column labels
    header = '  ' + '   '.join(COLUMN_LABELS)
    print(header)
    # Print top border
    print('+' + '---+' * COLUMNS)
    # Print each row
    for row in board:
        row_str = '|' + '|'.join(f' {cell} ' for cell in row) + '|'
        print(row_str)
        print('+' + '---+' * COLUMNS)


def get_valid_column_input(board):
    """Prompt the user for a column and check if input is valid, repeat if not"""
    while True:
        col_input = input("Please enter a column: ").strip()
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            print(f'Invalid input. Please enter a valid column (A-{COLUMN_LABELS[-1]}).')
            continue
        col_index = COLUMN_LABELS.index(col_input)
        # Check if column is full
        if board[0][col_index] != ' ':
            print('Column is full! You lose your turn.')
            return None  # Signal that this was a lost turn (per rules)
        return col_index


def place_checker(board, col_index, checker):
    """Place a checker in the lowest available row in the chosen column"""
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index  # Return where the checker was placed
    return None  # Theoretically unreachable if we checked for full columns


def check_for_win(board, last_row, last_col, checker):
    """Checks for a win. Checks all four directions from the last placed checker."""
    def count_deltas(delta_row, delta_col):
        count = 0
        r, c = last_row + delta_row, last_col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    # Four directions: (vertical, horizontal, diag1, diag2)
    directions = [
        ((-1, 0), (1, 0)),   # vertical
        ((0, -1), (0, 1)),   # horizontal
        ((-1, -1), (1, 1)),  # diagonal /
        ((-1, 1), (1, -1)),  # diagonal \
    ]
    for dir1, dir2 in directions:
        count = 1  # Count the placed checker itself
        count += count_deltas(*dir1)
        count += count_deltas(*dir2)
        if count >= 4:
            return True
    return False


def check_for_draw(board):
    """Returns True if the board is full and there is no winner."""
    for col in range(COLUMNS):
        if board[0][col] == ' ':
            return False
    return True


def main():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, NUM_PLAYERS-1)

    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player_idx]} starts!\n")

    winner = None
    while True:
        checker = PLAYER_CHECKERS[current_player_idx]
        print(f"Player {checker}, ", end='')
        col_index = get_valid_column_input(board)
        if col_index is None:
            # Invalid or full column: player loses turn, move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue
        row_index, col_index = place_checker(board, col_index, checker)
        print_board(board)
        # Check for win after placing new checker
        if check_for_win(board, row_index, col_index, checker):
            print(f'Player {checker} won!')
            return
        # Check for draw
        if check_for_draw(board):
            print('The game is a draw!')
            return
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == '__main__':
    main()
