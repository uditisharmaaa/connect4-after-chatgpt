import random, os

# Constants (adjust NUM_PLAYERS 2..5)
ROWS, COLS = 6, 7
LABELS = "ABCDEFG"
PLAYER_SYMBOLS = "XOVHM"
NUM_PLAYERS = 2  # set 2..5

assert 2 <= NUM_PLAYERS <= 5

def clear(): os.system('clear')

def new_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def draw(board):
    print('  ' + ' '.join(LABELS))
    for r in board: print('  ' + ' '.join(r))

def drop(board, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = sym
            return r, col
    return None

def inb(r,c): return 0 <= r < ROWS and 0 <= c < COLS

def won(board, r, c, sym):
    for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
        cnt = 1
        for s in (1,-1):
            rr, cc = r + s*dr, c + s*dc
            while inb(rr,cc) and board[rr][cc] == sym:
                cnt += 1; rr += s*dr; cc += s*dc
        if cnt >= 4: return True
    return False

def full(board): return all(board[0][c] != '.' for c in range(COLS))

def read_col(prompt, board):
    while True:
        x = input(prompt).strip().upper()
        if len(x)==1 and x in LABELS:
            col = LABELS.index(x)
            if board[0][col] == '.': return col
            print("Column full.")
        else:
            print("Enter a letter A-G.")

def main():
    board = new_board()
    syms = PLAYER_SYMBOLS[:NUM_PLAYERS]
    turn = random.randrange(NUM_PLAYERS)
    last = None
    while True:
        clear()
        draw(board)
        sym = syms[turn]
        col = read_col(f"Player {sym}, choose column A-G: ", board)
        pos = drop(board, col, sym)
        r,c = pos
        if won(board, r, c, sym):
            clear(); draw(board); print(f"Player {sym} wins!"); break
        if full(board):
            clear(); draw(board); print("It's a draw."); break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
