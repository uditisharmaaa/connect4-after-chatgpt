import os
import random
import sys

# =========================
# Configuration (Submission requirements)
# =========================
ROWS = 6               # Number of rows (default 6)
COLUMNS = 7            # Number of columns (default 7, max 26)
NUM_PLAYERS = 2        # Between 2 and 5 players inclusive

# Checker symbols in order for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# =========================
# Utility and Game Functions
# =========================

def clear_screen():
    # Clears the terminal screen (Linux/Unix as required)
    os.system('clear')


def create_board(rows, cols):
    # Create a 2D list initialized with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    clear_screen()

    # Header with column letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)

    # Horizontal separator line
    sep = "+" + "+".join("---" for _ in range(cols)) + "+"

    # Print each row
    for r in range(rows):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(sep)


def is_valid_column_input(user_input, cols):
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    if not ('A' <= ch <= 'Z'):
        return False
    index = ord(ch) - ord('A')
    return 0 <= index < cols


def find_drop_row(board, col):
    # Return the row index where the checker should land in the given column
    # or None if the column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def board_full(board):
    # If no spaces left in any cell
    return all(cell != " " for row in board for cell in row)


def check_winner(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            sym = board[r][c]
            if sym == " ":
                continue
            for dr, dc in directions:
                if has_four_in_a_row(board, r, c, dr, dc, sym):
                    return sym
    return None


def has_four_in_a_row(board, r, c, dr, dc, sym):
    rows = len(board)
    cols = len(board[0])
    for k in range(4):
        rr = r + dr * k
        cc = c + dc * k
        if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
            return False
        if board[rr][cc] != sym:
            return False
    return True


def get_player_symbols(num_players):
    if num_players < 2 or num_players > 5:
        raise ValueError("Number of players must be between 2 and 5.")
    return CHECKERS[:num_players]


def prompt_for_column(current_symbol, cols):
    # Keep asking until the user gives a syntactically valid column letter within range.
    while True:
        try:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
        except EOFError:
            # If input stream is closed, exit gracefully
            print()
            sys.exit(0)

        if is_valid_column_input(user_input, cols):
            return ord(user_input) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter.")


def play_game(rows, cols, num_players):
    if cols > 26:
        raise ValueError("Maximum number of columns is 26.")

    board = create_board(rows, cols)
    players = get_player_symbols(num_players)
    current_player_index = random.randrange(num_players)

    # Initial board print
    print_board(board)

    while True:
        current_symbol = players[current_player_index]

        # Prompt until we get a syntactically valid column (letter within range)
        col = prompt_for_column(current_symbol, cols)

        # Attempt to drop checker
        drop_row = find_drop_row(board, col)
        if drop_row is None:
            # Column full: player loses the turn
            print("Column is full. You lose your turn.")
            # After the message, reprint board to keep consistent view before moving on.
            print_board(board)
            # Switch to next player
            current_player_index = (current_player_index + 1) % num_players
            # Check for win/draw (no change occurred; safe to check anyway)
            winner = check_winner(board)
            if winner:
                print("Player " + winner + " won!")
                return
            if board_full(board):
                print("The game is a draw.")
                return
            continue

        # Place the checker
        board[drop_row][col] = current_symbol

        # Print updated board
        print_board(board)

        # Check for a winner
        winner = check_winner(board)
        if winner:
            print("Player " + winner + " won!")
            return

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            return

        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players


def main():
    play_game(ROWS, COLUMNS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
