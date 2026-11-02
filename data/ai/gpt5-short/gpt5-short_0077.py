#!/usr/bin/env python3
import os, random, sys

ROWS, COLS = 6, 7
COL_LABELS = "ABCDEFG"
ALL_PLAYERS = ['X', 'O', 'V', 'H', 'M']
N_PLAYERS = 2  # set 2..5

def clear(): os.system('clear')

def new_board(): return [[' ']*COLS for _ in range(ROWS)]

def show(b):
    clear()
    print('  ' + ' '.join(COL_LABELS))
    for r in b: print('| ' + ' '.join(r))
    print()

def drop(b, col, p):
    for r in range(ROWS-1, -1, -1):
        if b[r][col] == ' ':
            b[r][col] = p
            return r, col
    return None

def inside(r,c): return 0 <= r < ROWS and 0 <= c < COLS

def won(b, r, c):
    p = b[r][c]
    for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
        cnt = 1
        for s in (1,-1):
            rr, cc = r+dr*s, c+dc*s
            while inside(rr,cc) and b[rr][cc]==p:
                cnt += 1; rr += dr*s; cc += dc*s
        if cnt >= 4: return True
    return False

def full(b): return all(b[0][c] != ' ' for c in range(COLS))

def get_move(p):
    while True:
        mv = input(f"Player {p}, choose column (A-G): ").strip().upper()
        if len(mv)==1 and mv in COL_LABELS:
            return COL_LABELS.index(mv)
        print("Invalid input. Try A-G.")

def main():
    players = ALL_PLAYERS[:max(2, min(5, N_PLAYERS))]
    turn = random.randrange(len(players))
    b = new_board()
    while True:
        show(b)
        p = players[turn]
        col = get_move(p)
        spot = drop(b, col, p)
        if spot is None:
            print("Column full. Try another."); input("Press Enter...")
            continue
        r,c = spot
        if won(b, r, c):
            show(b); print(f"Player {p} wins!"); break
        if full(b):
            show(b); print("It's a draw!"); break
        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
