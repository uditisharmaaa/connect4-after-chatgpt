import os
import random
import string

# Constants (submission must use 6 rows, 7 cols, 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # allowed: 2..5

# Checker symbols in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_letters(cols):
    # Return list of column labels: A, B, C, ...
    letters = list(string.ascii_uppercase[:cols])
    return letters


def print_board(board):
    letters = column_letters(len(board[0]))
    # Header
    print("  " + "   ".join(letters))
    # Rows
    horiz = "+" + "+".join(["---"] * len(letters)) + "+"
    for r in range(len(board)):
        print(horiz)
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(horiz)


def get_valid_input(cols):
    letters = column_letters(cols)
    while True:
        user_in = input("Please enter a column: ").strip()
        if len(user_in) != 1:
            print("Invalid input. Enter a single uppercase letter for a column.")
            continue
        ch = user_in.upper()
        if ch not in letters:
            print("Invalid column. Choose from:", " ".join(letters))
            continue
        return letters.index(ch)


def find_drop_row(board, col):
    # Return the row index where the checker will land, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, down-right, down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Setup
    if COLS > 26:
        raise ValueError("Maximum supported columns is 26.")
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("Number of players must be between 2 and 5.")

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {players[current]}, you start.")

    # Game loop
    while True:
        # Show board and ask input for current player
        # Show prompt including player
        print(f"Player {players[current]}, it's your turn.")
        col_index = get_valid_input(COLS)

        drop_row = find_drop_row(board, col_index)
        if drop_row is None:
            # Column full: lose turn
            print(f"Column {column_letters(COLS)[col_index]} is full. Player {players[current]} loses the turn.")
            input("Press Enter to continue...")
            clear_screen()
            print_board(board)
            # Next player
            current = (current + 1) % NUM_PLAYERS
            continue

        # Place checker
        board[drop_row][col_index] = players[current]

        # Clear and show updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, players[current]):
            print(f"Player {players[current]} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player
        current = (current + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
