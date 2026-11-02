import os, random

ROWS, COLS = 6, 7
COL_LABELS = "ABCDEFG"
TOKENS = ['X', 'O', 'V', 'H', 'M']   # up to 5 players
NUM_PLAYERS = 2                      # set 2..5

def new_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(b):
    print("  " + " ".join(COL_LABELS))
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(b[r]))
    print()

def drop(b, col, ch):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == ' ':
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

def full(b): return all(b[0][c] != ' ' for c in range(COLS))

def get_move(b, ch):
    while True:
        mv = input(f"Player {ch}, choose column (A-G): ").strip().upper()
        if len(mv) == 1 and mv in COL_LABELS:
            c = COL_LABELS.index(mv)
            if b[0][c] == ' ':
                return c
            else:
                print("That column is full. Try again.")
        else:
            print("Invalid input. Enter a letter A-G.")

def main():
    assert 2 <= NUM_PLAYERS <= 5
    players = TOKENS[:NUM_PLAYERS]
    b = new_board()
    turn = random.randrange(NUM_PLAYERS)
    last_move = None

    while True:
        os.system('clear')
        print_board(b)
        ch = players[turn]
        c = get_move(b, ch)
        rc = drop(b, c, ch)
        if rc is None:
            print("Column full (race condition). Try again."); continue
        r, c = rc
        if won(b, r, c, ch):
            os.system('clear'); print_board(b)
            print(f"Player {ch} wins!")
            break
        if full(b):
            os.system('clear'); print_board(b)
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
