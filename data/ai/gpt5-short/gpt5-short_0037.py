import os, random, string

ROWS, COLS = 6, 7
COL_NAMES = "A B C D E F G".split()
PLAYERS = "XOVHM"   # up to 5 distinct tokens
NUM_PLAYERS = 2     # set 2..5

def clear():
    os.system('clear')

def new_board():
    return [[" "]*COLS for _ in range(ROWS)]

def show(board, turn_idx):
    clear()
    print("Connect 4 — {} players: {}\n".format(NUM_PLAYERS, " ".join(PLAYERS[:NUM_PLAYERS])))
    print("  " + " ".join(COL_NAMES))
    for r in range(ROWS):
        print("| " + " ".join(board[r]) + " |")
    print("\nPlayer {}'s turn ({})".format(turn_idx+1, PLAYERS[turn_idx]))

def drop(board, col, sym):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r, col
    return None

def inside(r,c): 
    return 0 <= r < ROWS and 0 <= c < COLS

def won(board, r, c):
    sym = board[r][c]
    if sym == " ": return False
    for dr, dc in [(1,0),(0,1),(1,1),(1,-1)]:
        cnt = 1
        for s in (1,-1):
            nr, nc = r+dr*s, c+dc*s
            while inside(nr,nc) and board[nr][nc]==sym:
                cnt += 1
                nr += dr*s; nc += dc*s
        if cnt >= 4:
            return True
    return False

def full(board):
    return all(board[0][c] != " " for c in range(COLS))

def get_move(board):
    while True:
        mv = input("Pick column (A-G): ").strip().upper()
        if len(mv)==1 and mv in COL_NAMES:
            col = COL_NAMES.index(mv)
            if board[0][col] != " ":
                print("That column is full.")
            else:
                return col
        else:
            print("Enter a single letter A-G.")

def main():
    assert 2 <= NUM_PLAYERS <= 5
    board = new_board()
    turn = random.randrange(NUM_PLAYERS)
    last_rc = None
    while True:
        show(board, turn)
        col = get_move(board)
        rc = drop(board, col, PLAYERS[turn])
        if rc is None: 
            continue
        r,c = rc
        if won(board, r, c):
            show(board, turn)
            print("Player {} ({}) wins!".format(turn+1, PLAYERS[turn]))
            break
        if full(board):
            show(board, turn)
            print("It's a draw.")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
