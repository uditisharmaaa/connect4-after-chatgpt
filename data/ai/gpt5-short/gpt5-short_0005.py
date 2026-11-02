import os, random, string

ROWS, COLS = 6, 7
PLAYERS_ALL = "XOVHM"
N_PLAYERS = 2  # set 2..5
PLAYERS = list(PLAYERS_ALL[:N_PLAYERS])
COL_NAMES = list("ABCDEFG")

def clear(): os.system('clear')

def new_board(): return [[" "]*COLS for _ in range(ROWS)]

def print_board(b):
    print("  " + " ".join(COL_NAMES))
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(b[r][c] if b[r][c]!=" " else "." for c in range(COLS)))
    print()

def drop(b, col, sym):
    for r in range(ROWS-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def inb(r,c): return 0 <= r < ROWS and 0 <= c < COLS

def win_from(b, r, c):
    sym = b[r][c]
    if sym == " ": return False
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        cnt = 1
        for s in (1,-1):
            nr, nc = r + s*dr, c + s*dc
            while inb(nr,nc) and b[nr][nc]==sym:
                cnt += 1
                nr += s*dr; nc += s*dc
        if cnt >= 4: return True
    return False

def full(b): return all(b[0][c]!=" " for c in range(COLS))

def get_move(b, sym):
    while True:
        s = input(f"Player {sym}, pick column (A-G): ").strip().upper()
        if len(s)==1 and s in COL_NAMES:
            c = COL_NAMES.index(s)
            if b[0][c]!=" ":
                print("Column full.")
            else:
                return c
        else:
            print("Invalid input.")

def main():
    b = new_board()
    turn = random.randrange(len(PLAYERS))
    last = None
    while True:
        clear()
        print_board(b)
        sym = PLAYERS[turn]
        c = get_move(b, sym)
        rc = drop(b, c, sym)
        if rc is None: continue
        r, c = rc
        if win_from(b, r, c):
            clear(); print_board(b)
            print(f"Player {sym} wins!")
            break
        if full(b):
            clear(); print_board(b)
            print("Draw!")
            break
        turn = (turn + 1) % len(PLAYERS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
