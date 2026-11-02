import os
import random

# Constants (you may change ROWS, COLS, and N_PLAYERS for testing; submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26 columns (A-Z)
N_PLAYERS = 2  # Between 2 and 5 players
WIN_LENGTH = 4

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # In order


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])
    # Header letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Top border
    print("+" + "+".join(["---"] * cols) + "+")
    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "+".join(["---"] * cols) + "+")


def get_valid_column_input(cols):
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter:")
            continue
        ch = user_input[0]
        if ch < 'A' or ch > 'Z':
            print("Invalid input. Please enter a column letter (A-Z):")
            continue
        idx = ord(ch) - ord('A')
        if idx < 0 or idx >= cols:
            print("Invalid column. Please enter a valid column within the board:")
            continue
        return idx, ch


def drop_checker(board, col, symbol):
    # Place from bottom up; return row index if placed, else None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r
    return None


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, down-right, down-left
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
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    count += 1
                    if count == WIN_LENGTH:
                        return True
                    rr += dr
                    cc += dc
    return False


def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True


def main():
    # Basic validations
    if N_PLAYERS < 2 or N_PLAYERS > 5:
        print("N_PLAYERS must be between 2 and 5.")
        return
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    players = PLAYER_SYMBOLS[:N_PLAYERS]
    board = create_board(ROWS, COLS)

    current_player_index = random.randint(0, N_PLAYERS - 1)

    # Initial display
    print_board(board)
    print(f"Player {players[current_player_index]}, please enter a column:")

    while True:
        col_index, col_letter = get_valid_column_input(COLS)
        symbol = players[current_player_index]

        placed_row = drop_checker(board, col_index, symbol)

        # After turn (whether placed or not), clear and print board
        clear_screen()

        if placed_row is None:
            # Column full: player loses the turn
            print_board(board)
            print(f"Column {col_letter} is full. Player {symbol} loses the turn.")
            # Switch player
            current_player_index = (current_player_index + 1) % N_PLAYERS
            # Prompt next player
            print(f"Player {players[current_player_index]}, please enter a column:")
            continue

        # Successful placement: check for win
        print_board(board)
        if check_win(board, symbol):
            print(f"Player {symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % N_PLAYERS
        print(f"Player {players[current_player_index]}, please enter a column:")


if __name__ == "__main__":
    main()
