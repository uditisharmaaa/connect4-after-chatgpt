import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

TOKENS = ["X", "O", "V", "H", "M"]


def clear():
    os.system('clear')


def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(b):
    labels = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(labels))
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        s = "|"
        for c in range(COLS):
            s += " " + b[r][c] + " |"
        print(s)
        print("+" + "---+" * COLS)


def get_input():
    max_label = chr(ord('A') + COLS - 1)
    while True:
        try:
            x = input().strip().upper()
        except EOFError:
            x = ""
        if len(x) == 1 and 'A' <= x <= max_label:
            return ord(x) - ord('A')
        print(f"Invalid input. Please enter a column between A and {max_label}:")


def place(b, col, token):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None


def check_win(b, token):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != token:
                continue
            # right
            if c + 3 < COLS and all(b[r][c + k] == token for k in range(4)):
                return True
            # down
            if r + 3 < ROWS and all(b[r + k][c] == token for k in range(4)):
                return True
            # diag down-right
            if r + 3 < ROWS and c + 3 < COLS and all(b[r + k][c + k] == token for k in range(4)):
                return True
            # diag down-left
            if r + 3 < ROWS and c - 3 >= 0 and all(b[r + k][c - k] == token for k in range(4)):
                return True
    return False


def board_full(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True


def main():
    players = TOKENS[:max(2, min(5, NUM_PLAYERS))]
    b = make_board(ROWS, COLS)
    turn = random.randint(0, len(players) - 1)

    clear()
    print_board(b)

    while True:
        p = players[turn]
        print(f"Player {p}, please enter a column:")
        col = get_input()

        placed = place(b, col, p)
        if placed is None:
            print("Column is full. Turn lost.")
            turn = (turn + 1) % len(players)
            clear()
            print_board(b)
            continue

        clear()
        print_board(b)

        if check_win(b, p):
            print(f"Player {p} won!")
            break

        if board_full(b):
            print("It's a draw!")
            break

        turn = (turn + 1) % len(players)


if __name__ == "__main__":
    main()
