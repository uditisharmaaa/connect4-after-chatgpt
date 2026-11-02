import os, random, string

# Constants (submission requires 6x7 and 2 players)
ROWS, COLS = 6, 7
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
assert 2 <= NUM_PLAYERS <= 5 and 1 <= ROWS and 1 <= COLS <= 26

def clear():
    os.system('clear')

def create_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    cols = len(b[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    line = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(b)):
        print(line)
        print("|" + "|".join(f" {b[r][c]} " for c in range(cols)) + "|")
    print(line)

def get_column_input(cols, player_symbol):
    while True:
        s = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(s) == 1 and s in string.ascii_uppercase[:cols]:
            return ord(s) - ord('A')

def place_checker(b, col, sym):
    # place in lowest available row
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r
    return None  # column full

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, sym):
    R, C = len(b), len(b[0])
    dirs = [(1,0), (0,1), (1,1), (1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym: continue
            for dr, dc in dirs:
                ok = True
                for k in range(1,4):
                    nr, nc = r + dr*k, c + dc*k
                    if not in_bounds(nr, nc, R, C) or b[nr][nc] != sym:
                        ok = False; break
                if ok: return True
    return False

def is_draw(b):
    return all(cell != " " for row in b for cell in row)

def main():
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    while True:
        clear()
        print_board(board)
        col = get_column_input(COLS, CHECKERS[current])
        row = place_checker(board, col, CHECKERS[current])
        if row is None:
            current = (current + 1) % NUM_PLAYERS  # lose turn if column full
            continue
        if check_win(board, CHECKERS[current]):
            clear(); print_board(board); print(f"Player {CHECKERS[current]} won!")
            break
        if is_draw(board):
            clear(); print_board(board); print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
