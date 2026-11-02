import os, random

ROWS, COLS = 6, 7
PLAYERS = "XOVHM"
N_PLAYERS = 2  # set 2..5

def clear(): os.system('clear')

def new_board(): return [[' ']*COLS for _ in range(ROWS)]

def print_board(b):
    print('  ' + ' '.join('A B C D E F G'.split()))
    for r in b: print(' |' + '|'.join(c if c!=' ' else '.' for c in r) + '|')
    print('  ' + '--'*COLS)

def drop(b, col, p):
    for r in range(ROWS-1, -1, -1):
        if b[r][col] == ' ':
            b[r][col] = p
            return r
    return -1

def inb(r,c): return 0 <= r < ROWS and 0 <= c < COLS

def won(b, r, c, p):
    for dr, dc in [(1,0),(0,1),(1,1),(1,-1)]:
        cnt = 1
        for s in (1,-1):
            rr, cc = r+dr*s, c+dc*s
            while inb(rr,cc) and b[rr][cc]==p:
                cnt += 1; rr += dr*s; cc += dc*s
        if cnt >= 4: return True
    return False

def full(b): return all(b[0][c] != ' ' for c in range(COLS))

def get_move(b, p):
    while True:
        s = input(f"Player {p}, choose column A-G: ").strip().upper()
        if len(s)==1 and 'A' <= s <= 'G':
            col = ord(s)-65
            if b[0][col] != ' ':
                print("Column full.")
            else:
                return col
        else:
            print("Invalid input.")

def main():
    players = PLAYERS[:N_PLAYERS]
    b = new_board()
    turn = random.randrange(len(players))
    while True:
        clear(); print_board(b)
        p = players[turn]
        c = get_move(b, p)
        r = drop(b, c, p)
        clear(); print_board(b)
        if won(b, r, c, p):
            print(f"Player {p} wins!")
            break
        if full(b):
            print("Draw.")
            break
        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
