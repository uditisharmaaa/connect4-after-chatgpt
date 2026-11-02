import os
import random
import string

# --------------------------- #
#       Global Constants      #
# --------------------------- #

NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26  # For future expandability
NUM_PLAYERS = 2  # Should be between 2 and 5
PLAYER_CHARS = ["X", "O", "V", "H", "M"]

# Safety for player count and column count
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert 1 <= NUM_COLS <= MAX_COLS, "Number of columns must be between 1 and 26."

# --------------------------- #
#     Helper Functions        #
# --------------------------- #

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Print column headers
    print("  " + "   ".join(string.ascii_uppercase[:cols]))
    print("+" + "---+" * cols)

    # Print board rows
    for r in range(rows):
        print("|" + "".join(" {} |".format(board[r][c]) for c in range(cols)))
        print("+" + "---+" * cols)

def get_valid_columns(board):
    cols = len(board[0])
    valid = []
    for c in range(cols):
        if board[0][c] == " ":
            valid.append(string.ascii_uppercase[c])
    return valid

def get_column_index(col_input):
    col_input = col_input.strip().upper()
    if len(col_input) != 1:
        return -1
    if col_input not in string.ascii_uppercase[:NUM_COLS]:
        return -1
    return string.ascii_uppercase.index(col_input)

def place_checker(board, col_idx, checker):
    """
    Places the player's checker in the specified column (as low as possible)
    Returns the row index where the checker lands, or -1 if the column is full
    """
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row
    return -1  # Column is full

def is_board_full(board):
    for col in range(NUM_COLS):
        if board[0][col] == " ":
            return False
    return True

def check_win(board, last_row, last_col, checker):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1),  # Diagonal /
    ]
    for dr, dc in directions:
        count = 1  # Last placed checker itself
        # Check one way
        r, c = last_row + dr, last_col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the other way
        r, c = last_row - dr, last_col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check if 4 in a row found
        if count >= 4:
            return True
    return False

def ask_for_column(player_char, valid_cols):
    while True:
        col = input(f"Player {player_char}, please enter a column: ").strip().upper()
        if len(col) != 1 or col not in string.ascii_uppercase[:NUM_COLS]:
            print("Invalid column. Please enter a letter from A to {}.".format(string.ascii_uppercase[NUM_COLS-1]))
            continue
        if col not in valid_cols:
            print(f"Column {col} is full. Pick another column.")
            continue
        return col

# --------------------------- #
#     Main Game Function      #
# --------------------------- #

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHARS[:NUM_PLAYERS]

    # Randomize starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        player_char = players[current_player_idx]
        valid_columns = get_valid_columns(board)

        # If board is full, it's a draw
        if not valid_columns:
            print("It's a draw!")
            break

        # Get valid column input
        col_letter = ask_for_column(player_char, valid_columns)
        col_idx = get_column_index(col_letter)

        # Place checker
        row_idx = place_checker(board, col_idx, player_char)

        # (Should never be -1 here due to input validation)
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row_idx, col_idx, player_char):
            print(f"Player {player_char} won!")
            break

        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
