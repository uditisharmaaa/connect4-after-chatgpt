import os
import random
import string

# Constants (you can change ROWS, COLS, and NUM_PLAYERS for testing; submission must be 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def clear_screen():
    # Clear screen for Unix/Linux
    os.system('clear')


def create_board(rows, cols):
    # Create a 2D board initialized with spaces
    board = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    # Print column labels (A, B, C, ...)
    labels = []
    for c in range(len(board[0])):
        labels.append(string.ascii_uppercase[c])
    print("  " + "   ".join(labels))
    # Print the grid
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print("+---" * len(board[0]) + "+")


def column_index_from_letter(letter):
    # Convert letter (A-Z) to column index
    if len(letter) != 1:
        return -1
    letter = letter.upper()
    if letter < 'A' or letter > 'Z':
        return -1
    idx = ord(letter) - ord('A')
    return idx


def is_valid_column_input(s, cols):
    # Validate that s is a single uppercase or lowercase letter within the board range
    if not s or len(s) != 1:
        return False
    if not s.isalpha():
        return False
    idx = column_index_from_letter(s)
    if idx < 0 or idx >= cols:
        return False
    return True


def drop_checker(board, col, symbol):
    # Place the checker in the lowest available row in the given column.
    # Return the row index where placed, or -1 if the column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return -1


def has_won(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r][c + 1] == symbol and
                board[r][c + 2] == symbol and
                board[r][c + 3] == symbol):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == symbol and
                board[r + 1][c] == symbol and
                board[r + 2][c] == symbol and
                board[r + 3][c] == symbol):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r + 1][c + 1] == symbol and
                board[r + 2][c + 2] == symbol and
                board[r + 3][c + 3] == symbol):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r - 1][c + 1] == symbol and
                board[r - 2][c + 2] == symbol and
                board[r - 3][c + 3] == symbol):
                return True

    return False


def is_board_full(board):
    # If any space remains, board is not full
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Limit checks
    total_cols = COLS
    total_rows = ROWS
    max_cols = 26
    if total_cols > max_cols:
        print("Maximum supported columns is 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        return

    # Initialize board
    board = create_board(total_rows, total_cols)

    # Select players' symbols
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Show initial board
    clear_screen()
    print_board(board)
    print("Player " + symbols[current_player_index] + ", please enter a column:")

    # Game loop
    while True:
        # Read and validate input (letters and bounds only; retry until valid)
        user_input = input().strip().upper()

        if not is_valid_column_input(user_input, total_cols):
            clear_screen()
            print_board(board)
            print("Invalid input. Please enter a valid column letter (A-" +
                  string.ascii_uppercase[total_cols - 1] + ").")
            print("Player " + symbols[current_player_index] + ", please enter a column:")
            continue

        col = column_index_from_letter(user_input)

        # Attempt to drop checker
        row_placed = drop_checker(board, col, symbols[current_player_index])

        clear_screen()
        print_board(board)

        if row_placed == -1:
            # Column full: turn is lost
            print("Column " + user_input + " is full. Turn lost.")
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Successful placement: check for win
            if has_won(board, symbols[current_player_index]):
                print("Player " + symbols[current_player_index] + " won!")
                break

            # Check for draw
            if is_board_full(board):
                print("The game is a draw!")
                break

            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

        # Prompt next player's turn
        print("Player " + symbols[current_player_index] + ", please enter a column:")


if __name__ == "__main__":
    main()
