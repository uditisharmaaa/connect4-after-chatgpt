import os
import random
import string

# ====== CONFIGURATION CONSTANTS ======
ROWS = 6            # Number of rows (default 6)
COLUMNS = 7         # Number of columns (default 7, max 26)
NUM_PLAYERS = 2     # Number of players (2 to 5)
WIN_COUNT = 4       # Number in a row needed to win (always 4 per assignment)

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # In order, first NUM_PLAYERS are used

# ====== VALIDATIONS ON CONSTANTS ======
if COLUMNS < 1 or COLUMNS > 26:
    raise ValueError("COLUMNS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    # Create a rows x cols board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)

    # Top border
    print("+---" * cols + "+")

    # Each row
    for r in range(rows):
        line = ""
        for c in range(cols):
            line += f"| {board[r][c]} "
        line += "|"
        print(line)
        print("+---" * cols + "+")


def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def drop_checker(board, col_index, symbol):
    # Place the symbol in the lowest empty spot in the column.
    # Return the (row_index) where it was placed, or -1 if column is full.
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = symbol
            return r
    return -1  # Column full


def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    # Count same symbol in both directions starting from (start_r, start_c)
    count = 1  # Count the starting cell
    # One direction
    r, c = start_r + dr, start_c + dc
    while in_bounds(board, r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    # Opposite direction
    r, c = start_r - dr, start_c - dc
    while in_bounds(board, r, c) and board[r][c] == symbol:
        count += 1
        r -= dr
        c -= dc
    return count


def check_win(board, last_r, last_c, symbol):
    # Check all four directions using the last placed checker
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        if count_in_direction(board, last_r, last_c, dr, dc, symbol) >= WIN_COUNT:
            return True
    return False


def get_valid_column_input(cols):
    # Continuously prompt until a valid column letter is given
    while True:
        user_input = input("Player {}, please enter a column: ".format(current_player_symbol)).strip().upper()
        if len(user_input) != 1:
            print("Invalid input! Please enter exactly one uppercase letter.")
            continue
        if not user_input.isalpha():
            print("Invalid input! Please enter a letter.")
            continue
        index = ord(user_input) - ord('A')
        if index < 0 or index >= cols:
            print("Invalid column! Please choose a letter between A and {}.".format(chr(ord('A') + cols - 1)))
            continue
        return index


# ====== MAIN GAME ======
def main():
    global current_player_symbol  # Used in input prompt function
    board = create_board(ROWS, COLUMNS)

    # Select player symbols
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_index = random.randrange(NUM_PLAYERS)
    current_player_symbol = players[current_player_index]

    # Initial board print
    print_board(board)

    while True:
        # Show prompt with current player
        cols = COLUMNS

        # Ask for a valid column letter
        col_index = get_valid_column_input(cols)

        # Try to drop the checker
        row_index = drop_checker(board, col_index, current_player_symbol)

        # Print updated board after the attempt
        print_board(board)

        if row_index == -1:
            # Column was full, player loses turn
            print("Column is full. {} loses the turn.".format(current_player_symbol))
        else:
            # Check for win
            if check_win(board, row_index, col_index, current_player_symbol):
                print("Player {} won!".format(current_player_symbol))
                break
            # Check for draw
            if is_board_full(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player_symbol = players[current_player_index]


if __name__ == "__main__":
    main()
