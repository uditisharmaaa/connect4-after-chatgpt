import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
NUM_PLAYERS = 2
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
EMPTY = ' '

# Select only as many tokens as players
TOKENS = PLAYER_TOKENS[:NUM_PLAYERS]


def clear_screen():
    """Clears the screen using os.system."""
    os.system('clear')


def create_board(rows, cols):
    """Creates and returns a 2D board initialized with EMPTY spaces."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Prints the current state of the board."""
    # Print header (A, B, ...)
    col_labels = '  ' + '   '.join(string.ascii_uppercase[:len(board[0])])
    print(col_labels)
    print('+' + '---+' * len(board[0]))

    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+' * len(board[0]))


def get_valid_columns(board):
    """Returns a list of column letters (A, B, ...) where there is at least one empty space."""
    return [string.ascii_uppercase[i] for i in range(len(board[0])) if board[0][i] == EMPTY]


def get_column_index(col_input, num_cols):
    """
    Converts column letter to an index.
    Returns the index if valid, else returns None.
    """
    if len(col_input) != 1:
        return None
    if col_input.isalpha():
        col_input = col_input.upper()
        idx = ord(col_input) - ord('A')
        if 0 <= idx < num_cols:
            return idx
    return None


def is_column_full(board, col):
    """Checks if a column is full (i.e., no EMPTY space top to bottom for given column index)."""
    return board[0][col] != EMPTY


def place_checker(board, col, token):
    """
    Tries to place the checker in the given column.
    Returns (row_index, col_index) if placed, else None.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == EMPTY:
            board[row][col] = token
            return (row, col)
    return None  # Column is full


def check_win(board, token):
    """Checks if the given token has 4 in a row in any direction."""
    rows = len(board)
    cols = len(board[0])

    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for row in range(rows):
        for col in range(cols):
            if board[row][col] != token:
                continue
            for dr, dc in directions:
                count = 1
                r, c = row, col
                while True:
                    r += dr
                    c += dc
                    if 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
                        count += 1
                        if count == 4:
                            return True
                    else:
                        break
    return False


def is_draw(board):
    """Returns True if the board is full and no more moves can be made."""
    for col in range(len(board[0])):
        if board[0][col] == EMPTY:
            return False
    return True


def main():
    # Game setup
    board = create_board(ROWS, COLUMNS)
    player_tokens = TOKENS
    num_players = NUM_PLAYERS

    # Randomly select starting player
    current_player = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)

    while True:
        # Show current player
        token = player_tokens[current_player]
        print(f"Player {token}, please enter a column:")

        valid_columns = get_valid_columns(board)

        while True:
            col_input = input().strip().upper()
            col_idx = get_column_index(col_input, COLUMNS)
            if col_idx is None:
                print("Invalid input. Please enter a valid column letter (A-G).")
                continue

            if is_column_full(board, col_idx):
                print(f"Column {col_input} is full. You lose your turn!")
                col_idx = None
                break  # Lose turn

            break

        # If valid column, try to place the checker
        # If col_idx is None (full column), lose turn
        checker_placed = None
        if col_idx is not None:
            checker_placed = place_checker(board, col_idx, token)

        clear_screen()
        print_board(board)

        # Only check for win condition if a checker was successfully placed
        if checker_placed:
            if check_win(board, token):
                print(f"Player {token} won!")
                return

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            return

        # Next player's turn (regardless if turn was lost due to full column!)
        current_player = (current_player + 1) % num_players


if __name__ == '__main__':
    main()
