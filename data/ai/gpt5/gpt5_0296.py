import os
import random
import sys

# ====== CONFIGURATION CONSTANTS ======
ROWS = 6                 # Number of rows (e.g., 6)
COLS = 7                 # Number of columns (e.g., 7); must be <= 26
NUM_PLAYERS = 2          # Between 2 and 5 inclusive
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols used in order

# ====== VALIDATIONS FOR CONSTANTS ======
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5 inclusive.")
if COLS > 26 or COLS < 1:
    raise ValueError("COLS must be between 1 and 26 inclusive.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")


def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    # Initialize a board as a list of lists filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, players, current_player_index):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Column headers (A, B, C, ...)
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(headers)
    # Top border
    print("+" + ("---+" * cols))
    # Board rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + ("---+" * cols))

    # Prompt line
    current_symbol = players[current_player_index]
    print(f"Player {current_symbol}, please enter a column:")


def letter_to_col(letter):
    if len(letter) != 1:
        return None
    if not letter.isalpha():
        return None
    idx = ord(letter.upper()) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return None


def get_valid_input():
    # Repeatedly prompts until a syntactically valid, in-bounds column letter is given.
    # This does not check if the column is full (that causes loss of turn, per spec).
    while True:
        try:
            user_input = input().strip()
        except EOFError:
            # Exit gracefully on EOF
            print("\nInput closed. Exiting game.")
            sys.exit(0)

        if len(user_input) == 0:
            print("Invalid input. Please enter a column letter (e.g., A-G):")
            continue

        col_idx = letter_to_col(user_input)
        if col_idx is None:
            print("Invalid input. Please enter a valid column letter (e.g., A-G):")
            continue

        return col_idx


def place_checker(board, col, symbol):
    # Place checker in the lowest available row within the column.
    # Returns the row index where the checker lands, or None if column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def check_win(board, last_row, last_col, symbol):
    # Check four directions from the last move:
    # horizontal (0,1), vertical (1,0), diag down-right (1,1), diag down-left (1,-1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    rows = len(board)
    cols = len(board[0])

    def count_in_direction(r, c, dr, dc):
        count = 0
        rr, cc = r, c
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc
        return count

    for dr, dc in directions:
        # Count in the positive direction
        pos = count_in_direction(last_row, last_col, dr, dc)
        # Count in the negative direction (excluding starting cell)
        neg = count_in_direction(last_row, last_col, -dr, -dc) - 1
        if pos + neg >= 4:
            return True
    return False


def check_draw(board):
    # If no spaces remain, it's a draw
    return all(cell != " " for row in board for cell in row)


def main():
    # Prepare game settings
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly choose first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial print of empty board
    print_board(board, players, current_player_index)

    # Game loop
    while True:
        # Get valid column input (only format and bounds checked here)
        col = get_valid_input()

        # Try to place checker
        symbol = players[current_player_index]
        row = place_checker(board, col, symbol)

        # After action, always reprint board (spec says clear before printing updated board)
        if row is None:
            # Column full -> invalid turn and player loses the turn
            print_board(board, players, current_player_index)
            print(f"Column {chr(ord('A') + col)} is full. Player {symbol} loses the turn.")
            # Advance to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Show board for next player prompt
            print_board(board, players, current_player_index)
            continue
        else:
            # Checker placed -> check win/draw
            print_board(board, players, current_player_index)

            if check_win(board, row, col, symbol):
                print(f"Player {symbol} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board, players, current_player_index)


if __name__ == "__main__":
    main()
