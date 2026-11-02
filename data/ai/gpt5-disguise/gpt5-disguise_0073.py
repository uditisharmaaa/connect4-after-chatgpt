import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def new_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_col_input(token):
    while True:
        s = input(f"Player {token}, please enter a column: ").strip().upper()
        if len(s) != 1:
            print("Invalid input.")
            continue
        a = ord('A')
        z = a + COLS - 1
        ch = ord(s)
        if ch < a or ch > z:
            print("Invalid input.")
            continue
        return ch - a

def place_token(b, col, token):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r
    return None

def check_win(b, token):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != token:
                continue
            if c + 3 < COLS and all(b[r][c + k] == token for k in range(4)):
                return True
            if r + 3 < ROWS and all(b[r + k][c] == token for k in range(4)):
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(b[r + k][c + k] == token for k in range(4)):
                return True
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
    b = new_board()
    current = random.randrange(NUM_PLAYERS)
    clear_screen()
    print_board(b)
    while True:
        token = TOKENS[current]
        col = get_col_input(token)
        row = place_token(b, col, token)
        clear_screen()
        print_board(b)
        if row is None:
            current = (current + 1) % NUM_PLAYERS
        else:
            if check_win(b, token):
                print(f"Player {token} won!")
                break
            if board_full(b):
                print("It's a draw!")
                break
            current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
