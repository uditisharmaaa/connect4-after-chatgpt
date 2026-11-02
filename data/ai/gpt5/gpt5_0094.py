import os
import random
import sys

# Constants (as required for submission)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Checker symbols in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Ensure constraints
if COLS > 26:
    print("Error: Maximum number of columns is 26.")
    sys.exit(1)
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: Number of players must be between 2 and 5.")
    sys.exit(1)

# Prepare active players
PLAYERS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Header with column letters
    header = "  " + "   ".join(COLUMN_LABELS)
    border = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    print(border)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(border)


def is_valid_column_letter(s):
    # Accept single alphabetic character that maps to existing column
    if len(s) != 1 or not s.isalpha():
        return False
    s = s.upper()
    return s in COLUMN_LABELS


def get_column_index(letter):
    return ord(letter.upper()) - ord('A')


def get_lowest_empty_row(board, col):
    # Return the row index where checker should land, or None if column full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag down-left
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]

    for dr, dc in directions:
        count = 1  # include current piece
        # extend in positive direction
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc
        # extend in negative direction
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False


def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        player_symbol = PLAYERS[current_player_index]
        # Ask for input until a valid column letter is provided
        while True:
            user_input = input(f"Player {player_symbol}, please enter a column: ").strip()
            if not is_valid_column_letter(user_input):
                # Invalid input, ask again
                clear_screen()
                print_board(board)
                print("Invalid input. Please enter a valid column letter.")
                continue
            else:
                break

        col = get_column_index(user_input)

        # Try to place the checker
        row = get_lowest_empty_row(board, col)
        if row is None:
            # Column is full -> turn lost
            clear_screen()
            print_board(board)
            print("Column is full. Turn lost.")
            # Next player's turn
            current_player_index = (current_player_index + 1) * 1 % NUM_PLAYERS
            continue

        # Place checker
        board[row][col] = player_symbol

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
