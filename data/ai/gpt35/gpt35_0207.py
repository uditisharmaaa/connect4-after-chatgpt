import os
import random
import string

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
WINNING_COUNT = 4
MAX_PLAYERS = 5

# Player tokens in order
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    # Create a board filled with spaces " "
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    # Print column headers
    col_labels = "  " + "   ".join(string.ascii_uppercase[:columns])
    print(col_labels)
    # Print rows
    sep_line = "+" + "---+" * columns
    for r in range(rows):
        print(sep_line)
        row_cells = "|"
        for c in range(columns):
            row_cells += " " + board[r][c] + " |"
        print(row_cells)
    print(sep_line)

def is_valid_column_input(user_input, columns):
    # Must be a single uppercase letter A-G (or column count)
    if len(user_input) != 1:
        return False
    if user_input not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_column_index(user_input):
    # Convert column letter to 0-based index
    return string.ascii_uppercase.index(user_input)

def place_checker(board, column, token):
    rows = len(board)
    # Place checker in lowest available row in the column
    for r in reversed(range(rows)):
        if board[r][column] == " ":
            board[r][column] = token
            return r  # Return the row where token was placed
    # Column full
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col, token):
    count = 0
    row = start_row
    col = start_col
    rows = len(board)
    cols = len(board[0])
    while 0 <= row < rows and 0 <= col < cols:
        if board[row][col] == token:
            count += 1
            if count == WINNING_COUNT:
                return True
        else:
            count = 0
        row += delta_row
        col += delta_col
    return False

def check_win(board, last_row, last_col, token):
    # Check horizontally
    # We'll check the entire row from left to right since placed checker could be anywhere
    row = last_row
    count = 0
    for c in range(len(board[0])):
        if board[row][c] == token:
            count += 1
            if count == WINNING_COUNT:
                return True
        else:
            count = 0

    # Check vertically
    col = last_col
    count = 0
    for r in range(len(board)):
        if board[r][col] == token:
            count += 1
            if count == WINNING_COUNT:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    # Find starting point on this diagonal
    r = last_row
    c = last_col
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    count = 0
    while r < len(board) and c < len(board[0]):
        if board[r][c] == token:
            count += 1
            if count == WINNING_COUNT:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Check diagonal (bottom-left to top-right)
    r = last_row
    c = last_col
    while r < len(board) - 1 and c > 0:
        r += 1
        c -= 1
    count = 0
    while r >= 0 and c < len(board[0]):
        if board[r][c] == token:
            count += 1
            if count == WINNING_COUNT:
                return True
        else:
            count = 0
        r -= 1
        c += 1

    return False

def check_draw(board):
    # If any cell in top row is empty, not a draw
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_TOKENS[:PLAYERS_COUNT]
    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    print_board(board)

    while True:
        token = players[current_player_idx]
        print(f"Player {token}, please enter a column:")
        user_input = input().strip().upper()

        # Validate input loop
        while not is_valid_column_input(user_input, COLUMNS):
            print("Invalid input. Please enter a valid column letter:")
            user_input = input().strip().upper()

        column = get_column_index(user_input)
        placed_row = place_checker(board, column, token)
        if placed_row is None:
            # Column full: player loses turn
            print_board(board)
            print(f"Column {user_input} is full. Player {token} loses the turn.")
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            continue

        print_board(board)

        # Check for win
        if check_win(board, placed_row, column, token):
            print(f"Player {token} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
