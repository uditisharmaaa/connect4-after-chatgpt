import os, random, string

ROWS, COLS = 6, 7
SYMS = "XOVHM"     # Player symbols in order
NUM_PLAYERS = 2    # Set between 2 and 5

def clear(): os.system('clear')
def show(b):
    print("  " + " ".join(string.ascii_uppercase[:COLS]))
    for r in range(ROWS):
        print("| " + " ".join(b[r]) + " |")
    print()

def drop(b, c, ch):
    for r in range(ROWS-1, -1, -1):
        if b[r][c] == ' ':
            b[r][c] = ch
            return r, c
    return None

def win(b, r, c, ch):
    for dr, dc in ((1,0),(0,1),(1,1),(1,-1)):
        cnt = 1
        for s in (1,-1):
            rr, cc = r+dr*s, c+dc*s
            while 0<=rr<ROWS and 0<=cc<COLS and b[rr][cc]==ch:
                cnt += 1; rr += dr*s; cc += dc*s
        if cnt >= 4: return True
    return False

def full(b): return all(b[0][c] != ' ' for c in range(COLS))

def main():
    players = list(SYMS[:NUM_PLAYERS])
    b = [[' ']*COLS for _ in range(ROWS)]
    turn = random.randrange(len(players))
    while True:
        clear(); show(b)
        ch = players[turn]
        inp = input(f"Player {ch}, choose column A-{chr(ord('A')+COLS-1)}: ").strip().upper()
        if len(inp)!=1 or not ('A' <= inp <= chr(ord('A')+COLS-1)):
            print("Invalid column."); input("Enter to continue."); continue
        c = ord(inp)-ord('A')
        pos = drop(b, c, ch)
        if not pos:
            print("Column full."); input("Enter to continue."); continue
        r, c = pos
        if win(b, r, c, ch):
            clear(); show(b); print(f"Player {ch} wins!"); break
        if full(b):
            clear(); show(b); print("It's a draw."); break
        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
