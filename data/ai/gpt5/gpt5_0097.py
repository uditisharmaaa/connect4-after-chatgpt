import os
import random

# Constants (you can change these for testing, but submission should be 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Header letters
    header = "  "
    for c in range(cols):
        header += f" {chr(ord('A') + c)}  "
    print(header)
    # Top border
    print("+" + "---+" * cols)
    # Rows
    for r in range(len(board)):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+" * cols)

def input_to_col(user_input):
    if len(user_input) != 1:
        return None
    ch = user_input.upper()
    if not ('A' <= ch <= 'Z'):
        return None
    col = ord(ch) - ord('A')
    if 0 <= col < COLS:
        return col
    return None

def drop_checker(board, col, checker):
    # Place checker in the lowest empty row in the given column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # column full

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def check_four_in_a_row(board, r, c, dr, dc, checker):
    count = 0
    rr, cc = r, c
    for _ in range(4):
        if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        else:
            break
    return count == 4

def check_win(board, checker):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                if check_four_in_a_row(board, r, c, dr, dc, checker):
                    return True
    return False

def main():
    # Basic validations for constants (not strictly necessary, but helpful)
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return

    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    print_board(board)

    while True:
        # Check draw at the start of a turn (in case the board is already full)
        if is_draw(board):
            print("It's a draw!")
            break

        current_checker = CHECKERS[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        # Get valid input (letters only within board range). If invalid input, ask again.
        while True:
            user_in = input().strip()
            col = input_to_col(user_in)
            if col is None:
                print("Invalid input. Please enter a valid column letter.")
                continue
            break

        # Try to drop checker
        row_placed = drop_checker(board, col, current_checker)
        if row_placed is None:
            # Column is full, turn is lost
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Turn lost.")
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move, print the updated board
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw after a successful move
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
