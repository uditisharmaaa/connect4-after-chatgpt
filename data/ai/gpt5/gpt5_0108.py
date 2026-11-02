import os
import random
import sys

# Configuration constants
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

# Symbols assigned to players in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

WIN_LENGTH = 4  # Number of checkers in a row needed to win


def clear_screen():
    # Clear the terminal screen (Linux/Unix as required)
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)

    # Horizontal separator
    hline = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(hline)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(hline)


def get_col_index_from_input(prompt, max_cols):
    while True:
        user_input = input(prompt).strip()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        ch = user_input.upper()
        idx = ord(ch) - ord('A')
        if 0 <= idx < max_cols:
            return idx
        print("Invalid column. Please enter a letter between A and " + chr(ord('A') + max_cols - 1) + ".")


def drop_checker(board, col, symbol):
    # Place symbol in the lowest available row of the given column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True
    return False  # Column full


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
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
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol and count < WIN_LENGTH:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= WIN_LENGTH:
                    return True
    return False


def check_draw(board):
    # Draw if no spaces left in the top row (or anywhere)
    for row in board:
        if " " in row:
            return False
    return True


def main():
    # Basic validations for configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS > 26:
        print("COLS must be at most 26.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        print("Not enough player symbols defined.")
        sys.exit(1)

    # Initialize game
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial board
    clear_screen()
    print_board(board)

    while True:
        current_symbol = symbols[current_player_idx]
        prompt = f"Player {current_symbol}, please enter a column: "

        # Get valid column input (reprompt on invalid input)
        col = get_col_index_from_input(prompt, COLS)

        # Attempt to drop checker
        if not drop_checker(board, col, current_symbol):
            # Column is full; turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_symbol} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move, clear screen and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
