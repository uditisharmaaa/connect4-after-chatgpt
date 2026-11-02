import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26

NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    # Print board rows with separators
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def is_valid_input(inp, columns):
    if len(inp) != 1:
        return False
    c = inp[0]
    if c < 'A' or c >= chr(ord('A') + columns):
        return False
    return True

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place into the lowest available row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Full column

def check_direction(board, start_row, start_col, dr, dc, checker):
    count = 0
    r, c = start_row, start_col
    rows, cols = len(board), len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, checker):
    # Check 4 directions: horizontal, vertical, diag /
    # and diag \
    directions = [
        ((0, -1), (0, 1)),     # horizontal left and right
        ((-1, 0), (1, 0)),     # vertical up and down
        ((-1, -1), (1, 1)),    # diagonal \
        ((-1, 1), (1, -1))     # diagonal /
    ]
    for (d1, d2) in directions:
        count = 1
        count += check_direction(board, row + d1[0], col + d1[1], d1[0], d1[1], checker)
        count += check_direction(board, row + d2[0], col + d2[1], d2[0], d2[1], checker)
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    global NUM_PLAYERS, CHECKERS, ROWS, COLUMNS

    # Validate constants are within specs
    if not (2 <= NUM_PLAYERS <= 5):
        print("Number of players must be between 2 and 5.")
        return
    if not (1 <= ROWS and 1 <= COLUMNS <= MAX_COLUMNS):
        print(f"Board dimensions must be positive and columns <= {MAX_COLUMNS}.")
        return

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        # Prompt player for input
        col_input = ""
        while True:
            try:
                col_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            except EOFError:
                # Handle unexpected EOF gracefully
                print()
                return
            if not is_valid_input(col_input, COLUMNS):
                print(f"Invalid input! Please enter a single letter from A to {chr(ord('A') + COLUMNS -1)}.")
                continue
            col = ord(col_input) - ord('A')
            if column_full(board, col):
                # According to assignment, player loses turn if column full
                break
            else:
                break

        # If column full, player loses turn (skip placing checker)
        if column_full(board, col):
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        pos = place_checker(board, col, checker)
        print_board(board)

        # Check for win
        if check_win(board, pos[0], pos[1], checker):
            print(f"Player {checker} won!")
            return

        # Check for draw
        if board_full(board):
            print("Game is a draw!")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
