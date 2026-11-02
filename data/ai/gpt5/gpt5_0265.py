import os
import random
import string

# Constants (change these to test different settings; submission must be 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Game rules
WIN_LENGTH = 4  # a player needs 4 in a row to win

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header
    letters = list(string.ascii_uppercase)
    header = "  " + "   ".join(letters[:cols])
    print(header)

    # Top border
    print("+" + "---+" * cols)

    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)

def col_from_input(inp):
    inp = inp.strip().upper()
    if len(inp) != 1:
        return None
    if not inp.isalpha():
        return None
    index = ord(inp) - ord('A')
    if index < 0 or index >= COLS:
        return None
    return index

def get_lowest_empty_row(board, col):
    # Return the row index where the checker will land, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, last_r, last_c, checker):
    # Check 4 in a row in all directions using last move
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # include last placed
        # forward direction
        r, c = last_r + dr, last_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # backward direction
        r, c = last_r - dr, last_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Basic validations for constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    board = create_board(ROWS, COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        current_checker = CHECKERS[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        # Input validation loop for entry format and in-range column
        while True:
            user_input = input(prompt)
            col = col_from_input(user_input)
            if col is None:
                print("Invalid input. Please enter a single uppercase letter for a valid column (e.g., A-G).")
                continue
            break

        # Try to place checker
        target_row = get_lowest_empty_row(board, col)
        if target_row is None:
            # Column full -> turn is invalid and player loses the turn
            print(f"Column {chr(ord('A') + col)} is full. Turn lost.")
            input("Press Enter to continue...")
            # Switch player and continue
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Place the checker
        board[target_row][col] = current_checker

        # Check for win
        if check_win(board, target_row, col, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
