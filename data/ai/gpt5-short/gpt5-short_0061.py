import os, random, string

ROWS, COLS = 6, 7
PLAYERS = 2  # set 2..5
SYMS = "XOVHM"

assert 2 <= PLAYERS <= 5
P = SYMS[:PLAYERS]
COL_LETTERS = list("ABCDEFG")

def clear(): os.system('clear')

def new_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def show(b):
    print("  " + " ".join(COL_LETTERS))
    for r in b:
        print(" |" + "|".join(r) + "|")
    print()

def drop(b, col, ch):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == '.':
            b[r][col] = ch
            return r, col
    return None

def inb(r, c): return 0 <= r < ROWS and 0 <= c < COLS

def won(b, r, c, ch):
    for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
        cnt = 1
        for s in (1, -1):
            nr, nc = r + s*dr, c + s*dc
            while inb(nr, nc) and b[nr][nc] == ch:
                cnt += 1
                nr += s*dr; nc += s*dc
        if cnt >= 4: return True
    return False

def full(b): return all(b[0][c] != '.' for c in range(COLS))

def col_index(inp):
    if len(inp) != 1: return None
    if inp in COL_LETTERS: return COL_LETTERS.index(inp)
    return None

def main():
    b = new_board()
    turn = random.randrange(PLAYERS)
    clear(); show(b)
    while True:
        ch = P[turn]
        inp = input(f"Player {ch}, pick column A-G (or Q to quit): ").strip().upper()
        if inp == 'Q': print("Bye!"); return
        c = col_index(inp)
        if c is None: print("Invalid column."); continue
        pos = drop(b, c, ch)
        if pos is None: print("Column full."); continue
        clear(); show(b)
        r, c = pos
        if won(b, r, c, ch):
            print(f"Player {ch} wins!")
            return
        if full(b):
            print("Draw!")
            return
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
