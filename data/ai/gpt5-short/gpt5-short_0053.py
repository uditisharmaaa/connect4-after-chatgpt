import os, random, sys

ROWS, COLS = 6, 7
TOKENS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
NUM_PLAYERS = 2                      # set 2..5

assert 2 <= NUM_PLAYERS <= 5
PLAYERS = TOKENS[:NUM_PLAYERS]
COL_LABELS = "ABCDEFG"

def clear(): os.system('clear')

def empty_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(b):
    print("  " + " ".join(COL_LABELS))
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(b[r]))
    print()

def drop(b, col, token):
    for r in range(ROWS-1, -1, -1):
        if b[r][col] == '.':
            b[r][col] = token
            return r, col
    return None  # column full

def inb(r,c): return 0 <= r < ROWS and 0 <= c < COLS

def won(b, r, c):
    t = b[r][c]
    if t == '.': return False
    for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
        cnt = 1
        for s in (1,-1):
            nr, nc = r, c
            while True:
                nr, nc = nr + s*dr, nc + s*dc
                if inb(nr,nc) and b[nr][nc] == t:
                    cnt += 1
                else:
                    break
        if cnt >= 4: return True
    return False

def full(b): return all(b[0][c] != '.' for c in range(COLS))

def get_move(b, token):
    while True:
        move = input(f"Player {token}, pick column A-G (or Q to quit): ").strip().upper()
        if move == 'Q': print("Bye!"); sys.exit(0)
        if len(move)==1 and move in COL_LABELS:
            c = COL_LABELS.index(move)
            if b[0][c] != '.':
                print("Column full. Try another.")
            else:
                return c
        else:
            print("Invalid input. Use A-G.")

def main():
    b = empty_board()
    turn = random.randrange(NUM_PLAYERS)
    while True:
        clear(); print_board(b)
        token = PLAYERS[turn]
        c = get_move(b, token)
        rc = drop(b, c, token)
        r, c = rc
        clear(); print_board(b)
        if won(b, r, c):
            print(f"Player {token} wins!")
            break
        if full(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
