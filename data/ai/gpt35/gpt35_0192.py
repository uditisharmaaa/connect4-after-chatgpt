import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5

CHECKERS = ["X", "O", "V", "H", "M"]

NUM_PLAYERS = 2  # Must be between MIN_PLAYERS and MAX_PLAYERS
WIN_CONDITION = 4

assert 1 < NUM_PLAYERS <= MAX_PLAYERS, f"NUM_PLAYERS must be between 2 and {MAX_PLAYERS}"
assert COLS <= MAX_COLS, f"COLS must be at most {MAX_COLS}"

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column letters
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(letters))
    horizontal_line = "+" + "---+" * cols
    rows = len(board)
    for r in range(rows):
        print(horizontal_line)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(horizontal_line)

def get_column_index(input_str, cols):
    if len(input_str) != 1:
        return -1
    letter = input_str.upper()
    if letter not in string.ascii_uppercase[:cols]:
        return -1
    return string.ascii_uppercase.index(letter)

def place_checker(board, col, checker):
    # Place checker in the lowest available row in column col
    # Return True if placed, False if column full
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def is_winning_line(line, checker):
    count = 0
    for ch in line:
        if ch == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for r in range(rows):
        if is_winning_line(board[r], checker):
            return True

    # Check vertical
    for c in range(cols):
        col_line = [board[r][c] for r in range(rows)]
        if is_winning_line(col_line, checker):
            return True

    # Check diagonal /
    # Diagonal /: from bottom-left to top-right
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            diag = [board[r + i][c + i] for i in range(WIN_CONDITION)]
            if all(ch == checker for ch in diag):
                return True

    # Check diagonal \
    # Diagonal \: from top-left to bottom-right
    for r in range(WIN_CONDITION - 1, rows):
        for c in range(cols - WIN_CONDITION + 1):
            diag = [board[r - i][c + i] for i in range(WIN_CONDITION)]
            if all(ch == checker for ch in diag):
                return True

    return False

def is_draw(board):
    # If top row all occupied => board full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS -1)

    while True:
        print_board(board)
        current_checker = players[current_player_index]
        input_prompt = f"Player {current_checker}, please enter a column: "
        col_input = input(input_prompt).strip().upper()
        col_index = get_column_index(col_input, COLS)

        if col_index == -1:
            # Invalid input: not a single valid column letter
            continue

        placed = place_checker(board, col_index, current_checker)
        if not placed:
            # Column full, turn lost
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Check win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
