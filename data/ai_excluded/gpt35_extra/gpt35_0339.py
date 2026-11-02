import os
import random

# Constants - Board dimensions and players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    """Create a new board filled with whitespace."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column labels and grid lines."""
    clear_screen()
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    # Print the board rows
    for row in range(len(board)):
        print('+' + '---+' * len(board[0]))
        row_str = '|'
        for col in range(len(board[0])):
            row_str += f' {board[row][col]} |'
        print(row_str)
    print('+' + '---+' * len(board[0]))


def is_valid_column(col_char):
    """Check if input column character is valid"""
    return col_char in COLUMN_LABELS


def get_column_index(col_char):
    """Convert column letter to zero-based index"""
    return ord(col_char) - ord('A')


def column_full(board, col_idx):
    """Check if a column is full (no empty spaces)"""
    return board[0][col_idx] != ' '


def place_checker(board, col_idx, checker):
    """
    Place the checker in the lowest available row in the column.
    Return the row index where checker was placed, or None if full column.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row
    return None


def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    """
    Check number of consecutive checkers starting from (start_row, start_col)
    in direction (delta_row, delta_col).
    """
    count = 0
    row, col = start_row, start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count


def check_win(board, row, col, checker):
    """
    Check all directions from (row, col) for 4 in a row for the player with checker.
    Returns True if player won.
    """
    # Directions: horizontal, vertical, diagonal down-right, diagonal down-left
    directions = [
        ((0, -1), (0, 1)),     # horizontal left & right
        ((-1, 0), (1, 0)),     # vertical up & down
        ((-1, -1), (1, 1)),    # diagonal up-left & down-right
        ((-1, 1), (1, -1))     # diagonal up-right & down-left
    ]

    for dir1, dir2 in directions:
        count = 1  # include the placed checker itself
        count += check_direction(board, row + dir1[0], col + dir1[1], dir1[0], dir1[1], checker)
        count += check_direction(board, row + dir2[0], col + dir2[1], dir2[0], dir2[1], checker)
        if count >= WIN_LENGTH:
            return True
    return False


def board_full(board):
    """Return True if board is full (no spaces left)"""
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            return False
    return True


def get_valid_input(current_player):
    """Prompt player for column until valid input is given."""
    while True:
        user_in = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(user_in) != 1:
            # Must be a single letter
            continue
        if not is_valid_column(user_in):
            continue
        yield user_in


def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    # Randomly select first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]

        # Get valid input
        for col_char in get_valid_input(current_checker):
            col_idx = get_column_index(col_char)

            if column_full(board, col_idx):
                # Column full, player loses turn as per spec
                # Just print nothing, next player to move
                break
            else:
                row_idx = place_checker(board, col_idx, current_checker)
                print_board(board)
                # Check win
                if check_win(board, row_idx, col_idx, current_checker):
                    print(f"Player {current_checker} won!")
                    return
                # Check draw
                if board_full(board):
                    print("Draw!")
                    return
                # Move to next player
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                break


if __name__ == "__main__":
    main()
