import os
import random
import sys

# Constants (adjustable, but submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header with column letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_str)
        print(sep)

def column_from_input(s):
    if len(s) != 1:
        return None
    ch = s.upper()
    if not ('A' <= ch <= 'Z'):
        return None
    idx = ord(ch) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return None

def drop_checker(board, col, checker):
    # Place checker in lowest available row in given column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # Column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, checker):
    # Check all directions: horizontal, vertical, diag down-right, diag up-right
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (-1, 1),  # diag up-right
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(rr, cc) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count == WIN_LENGTH:
                    return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def prompt_for_column(player_checker):
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        except EOFError:
            # Graceful exit on EOF
            print()
            sys.exit(0)
        col = column_from_input(user_input)
        if col is None:
            print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
            continue
        return col

def game_loop():
    if COLS > 26:
        print("Maximum supported columns is 26.")
        return

    board = create_board(ROWS, COLS)
    # Random starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player_idx]

        # Ask for a valid column letter
        col = prompt_for_column(player_checker)

        # Try to drop the checker; if column full, player loses turn
        placed = drop_checker(board, col, player_checker)
        clear_screen()
        print_board(board)

        if not placed:
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {player_checker} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for win after a successful placement
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

def main():
    random.seed()
    game_loop()

if __name__ == "__main__":
    main()
