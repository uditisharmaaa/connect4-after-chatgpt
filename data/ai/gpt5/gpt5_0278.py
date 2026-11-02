import os
import random
import string

# Constants (you may change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

CHECKERS = ["X", "O", "V", "H", "M"]  # In order

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    # Header
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

def clear_and_print(board):
    clear_screen()
    print_board(board)

def letter_to_col(letter):
    if len(letter) != 1:
        return None
    letter = letter.upper()
    if letter < 'A' or letter > chr(ord('A') + COLS - 1):
        return None
    return ord(letter) - ord('A')

def get_input_column(current_checker):
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col = letter_to_col(user_input)
        if col is None:
            print("Invalid column. Please enter a valid column letter.")
            continue
        return col

def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the given column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return (r, col)
    return None  # Column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, last_r, last_c, checker):
    # Check 4 directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count both directions from the last placed checker
        total = 1  # count the last placed itself
        total += count_in_line(board, last_r, last_c, dr, dc, checker)
        total += count_in_line(board, last_r, last_c, -dr, -dc, checker)
        if total >= 4:
            return True
    return False

def count_in_line(board, r, c, dr, dc, checker):
    cnt = 0
    nr, nc = r + dr, c + dc
    while in_bounds(nr, nc) and board[nr][nc] == checker:
        cnt += 1
        nr += dr
        nc += dc
    return cnt

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Basic validations for constants
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    clear_and_print(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]

        # Ask for input column (validate input type and range)
        col = get_input_column(current_checker)

        # Try to drop checker
        drop_pos = drop_checker(board, col, current_checker)
        if drop_pos is None:
            # Column full: lose the turn
            clear_and_print(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses the turn.")
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Successful move: print updated board
        clear_and_print(board)

        # Check win
        r, c = drop_pos
        if check_win(board, r, c, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
