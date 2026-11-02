import os
import random
import string

# Constants (adjustable)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

# Validate constants
COLS = max(1, min(COLS, 26))
NUM_PLAYERS = max(2, min(NUM_PLAYERS, 5))
PLAYERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Header
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)
    # Rows
    sep = "+" + ("---+" * cols)
    for r in range(len(board)):
        print(sep)
        row_str = ""
        for c in range(cols):
            row_str += f"| {board[r][c]} "
        row_str += "|"
        print(row_str)
    print(sep)


def column_from_input(inp, cols):
    inp = inp.strip().upper()
    if len(inp) != 1 or inp < 'A' or inp > chr(ord('A') + cols - 1):
        return None
    return ord(inp) - ord('A')


def drop_checker(board, col, checker):
    # Place checker in lowest available row in this column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
                    count += 1
                    if count == WIN_LEN:
                        return True
                    nr += dr
                    nc += dc
    return False


def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board before the game starts
    print_board(board)

    while True:
        current_checker = PLAYERS[current_player_idx]
        # Prompt until valid input letter within range
        while True:
            user_inp = input(f"Player {current_checker}, please enter a column: ")
            col = column_from_input(user_inp, COLS)
            if col is not None:
                break
            print("Invalid input. Please enter a valid column letter.")

        # Attempt to drop checker
        placed = drop_checker(board, col, current_checker)
        if placed is None:
            # Column full, player loses the turn
            print_board(board)
            print("Column is full. Turn lost.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move, check for win
        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        print_board(board)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
