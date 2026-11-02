import os
import random
import string
import sys

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4

# Checker symbols in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers
    headers = '  ' + '   '.join(string.ascii_uppercase[:cols])
    sep = '+' + '---+' * cols

    print(headers)
    print(sep)
    for r in range(rows):
        row_str = '|'
        for c in range(cols):
            row_str += f' {board[r][c]} |'
        print(row_str)
        print(sep)


def column_from_input(inp, cols):
    if len(inp) != 1 or inp not in string.ascii_uppercase[:cols]:
        return None
    return ord(inp) - ord('A')


def get_player_symbols(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    return CHECKERS[:num_players]


def is_column_full(board, col):
    return board[0][col] != ' '


def drop_checker(board, col, symbol):
    # Place in the lowest empty cell in this column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col
    return None  # Shouldn't reach here if checked before


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    L = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                cnt = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    cnt += 1
                    if cnt == L:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    # Draw if no spaces left in top row
    return all(cell != ' ' for cell in board[0])


def main():
    # Validate constraints
    if COLS > 26:
        print("Error: COLS must be at most 26.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    board = create_board(ROWS, COLS)
    players = get_player_symbols(NUM_PLAYERS)
    current = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        current_symbol = players[current]
        prompt = f"Player {current_symbol}, please enter a column: "

        # Read and validate input (format/character only)
        col_index = None
        while col_index is None:
            try:
                user_in = input(prompt).strip().upper()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting game.")
                return
            col_index = column_from_input(user_in, COLS)
            if col_index is None:
                print("Invalid input. Please enter a valid column letter.")
                # Reprint board to keep interface consistent
                clear_screen()
                print_board(board)

        # If column full, turn is invalid and player loses the turn
        if is_column_full(board, col_index):
            # Move to next player
            current = (current + 1) % NUM_PLAYERS
            continue

        # Place checker
        drop_checker(board, col_index, current_symbol)

        # Check for win
        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
