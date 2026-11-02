import os
import random
import string

# Configurable constants
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2 to 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
LETTERS = string.ascii_uppercase[:COLS]

def clear():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear()
    header = "  " + "   ".join(LETTERS)
    sep = "+" + ("---+" * COLS)
    print(header)
    print(sep)
    for r in range(ROWS):
        print("|" + "|".join(f" {board[r][c]} " for c in range(COLS)) + "|")
        print(sep)

def drop_piece(board, col, checker):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, r, c, ch):
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for s in (1, -1):
            nr, nc = r + s*dr, c + s*dc
            while in_bounds(nr, nc) and board[nr][nc] == ch:
                count += 1
                nr += s*dr
                nc += s*dc
        if count >= 4:
            return True
    return False

def is_draw(moves):
    return moves >= ROWS * COLS

def get_valid_input(prompt):
    while True:
        try:
            col_str = input(prompt).strip().upper()
        except EOFError:
            col_str = ""
        if len(col_str) == 1 and col_str in LETTERS:
            return LETTERS.index(col_str)
        print("Invalid input. Please enter a valid column letter.")

def main():
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    moves = 0

    print_board(board)
    while True:
        checker = CHECKERS[current]
        col = get_valid_input(f"Player {checker}, please enter a column: ")

        row = drop_piece(board, col, checker)
        if row is None:
            print(f"Column {LETTERS[col]} is full. Turn lost.")
            # No board update; still check for draw (unlikely) and switch
            if is_draw(moves):
                print("It's a draw!")
                break
            current = (current + 1) % NUM_PLAYERS
            continue

        moves += 1
        print_board(board)

        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        if is_draw(moves):
            print("It's a draw!")
            break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
