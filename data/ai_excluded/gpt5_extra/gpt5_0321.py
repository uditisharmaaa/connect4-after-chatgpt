import random
import os
import string

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(headers))
    # Print grid
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(" " if board[r][c] == " " else board[r][c])
        print("|" + "|".join(f" {cell} " for cell in row_cells) + "|")
    print(sep)


def get_valid_column_input(cols):
    while True:
        user_in = input("Please enter a column: ").strip().upper()
        if len(user_in) != 1:
            print("Invalid input. Enter a single letter for the column.")
            continue
        if user_in < 'A' or user_in >= chr(ord('A') + cols):
            print("Invalid column. Please choose a valid column letter.")
            continue
        return ord(user_in) - ord('A')


def drop_checker(board, col, symbol):
    # Drop the checker into the lowest empty spot in the column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r, col
    return None  # Column full


def check_direction(board, start_r, start_c, dr, dc, symbol):
    count = 0
    r = start_r
    c = start_c
    rows = len(board)
    cols = len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        if count == 4:
            return True
        r += dr
        c += dc
    return False


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            # Check right
            if c + 3 < cols and all(board[r][c + k] == symbol for k in range(4)):
                return True
            # Check down
            if r + 3 < rows and all(board[r + k][c] == symbol for k in range(4)):
                return True
            # Check down-right
            if r + 3 < rows and c + 3 < cols and all(board[r + k][c + k] == symbol for k in range(4)):
                return True
            # Check down-left
            if r + 3 < rows and c - 3 >= 0 and all(board[r + k][c - k] == symbol for k in range(4)):
                return True
    return False


def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Basic validations for constraints
    if COLS > 26:
        raise ValueError("Maximum number of columns is 26.")
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("Number of players must be between 2 and 5.")

    # Initialize
    board = create_board(ROWS, COLS)
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.randrange(NUM_PLAYERS)

    # Show initial board and starting player
    print_board(board)
    print(f"Player {symbols[current_player]}, you start!")

    # Game loop
    while True:
        print_board(board)
        print(f"Player {symbols[current_player]}, it's your turn.")
        print(f"Player {symbols[current_player]}, please enter a column:")
        col = get_valid_column_input(COLS)

        result = drop_checker(board, col, symbols[current_player])
        if result is None:
            print(f"Column {chr(ord('A') + col)} is full. Turn lost.")
            current_player = (current_player + 1) % NUM_PLAYERS
            input("Press Enter to continue...")
            continue

        # Check for win
        if check_win(board, symbols[current_player]):
            print_board(board)
            print(f"Player {symbols[current_player]} won!")
            break

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

    # End
    # No further action required


if __name__ == "__main__":
    main()
