import os
import random
import string

# ======= Constants =======
ROWS = 6
COLS = 7
MAX_COLS = 26  # Max columns (A-Z)
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # For submission set to 2
WIN_COUNT = 4

# ======= Functions =======

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current game board."""
    cols = len(board[0])
    header = "  " + "   ".join([string.ascii_uppercase[i] for i in range(cols)])
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_column_index(col_char, cols):
    """Converts column character to index. Returns -1 if invalid."""
    if len(col_char) != 1 or not col_char.isalpha():
        return -1
    col_char = col_char.upper()
    idx = ord(col_char) - ord('A')
    if 0 <= idx < cols:
        return idx
    return -1

def is_valid_column(board, col):
    """Checks if the column can accept another checker."""
    return board[0][col] == " "

def get_next_open_row(board, col):
    """Returns the lowest empty row in the given column (or None if full)."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None

def get_user_input(player_checker, board):
    """Prompts user for column selection and validates input."""
    cols = len(board[0])
    valid = False
    while not valid:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        idx = get_column_index(col_input, cols)
        if idx == -1:
            print("Invalid column letter. Please select a valid column (A-G).")
            continue
        if not is_valid_column(board, idx):
            print("That column is full. Turn lost.")
            return None  # The turn is lost for this round
        valid = True
    return idx

def drop_checker(board, col, checker):
    """Places checker in the given column. Returns True if successful."""
    row = get_next_open_row(board, col)
    if row is not None:
        board[row][col] = checker
        return row, col
    return None, None

def check_win(board, checker, row, col):
    """Checks whether the last move wins the game."""
    return (
        check_direction(board, checker, row, col, 0, 1)   # Horizontal
        or check_direction(board, checker, row, col, 1, 0)  # Vertical
        or check_direction(board, checker, row, col, 1, 1)  # Diagonal /
        or check_direction(board, checker, row, col, 1, -1)  # Diagonal \
    )

def check_direction(board, checker, row, col, delta_row, delta_col):
    """Checks for WIN_COUNT in a row in a particular direction from (row, col)."""
    count = 1
    # Forward direction
    r, c = row + delta_row, col + delta_col
    while in_bounds(board, r, c) and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    # Backward direction
    r, c = row - delta_row, col - delta_col
    while in_bounds(board, r, c) and board[r][c] == checker:
        count += 1
        r -= delta_row
        c -= delta_col
    return count >= WIN_COUNT

def in_bounds(board, row, col):
    """Checks if (row, col) is within board boundaries."""
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def check_draw(board):
    """Returns True if the board is full (draw), else False."""
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def select_first_player(num_players):
    """Returns a random player index (starting from 0)."""
    return random.randint(0, num_players - 1)

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Select who starts randomly
    current_player = select_first_player(NUM_PLAYERS)
    clear_screen()
    print_board(board)

    winner = None
    while True:
        player_checker = players[current_player]
        col = get_user_input(player_checker, board)
        clear_screen()

        if col is None:
            print_board(board)
            # Skip turn if column was full
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row, col_real = drop_checker(board, col, player_checker)
        print_board(board)

        if row is not None:
            if check_win(board, player_checker, row, col_real):
                print(f"Player {player_checker} won!")
                winner = player_checker
                break

            if check_draw(board):
                print("It's a draw!")
                break

            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            # Should not happen due to validation, but just in case:
            print("Could not place checker. Turn lost.")
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
