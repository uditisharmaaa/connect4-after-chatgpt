import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear(): os.system('clear')
def create_board(): return [[" "]*COLS for _ in range(ROWS)]
def print_board(b):
    clear()
    print("  "+"   ".join(chr(65+i) for i in range(COLS)))
    print("+---"*COLS+"+")
    for r in range(ROWS):
        print("| " + " | ".join(b[r]) + " |")
        print("+---"*COLS+"+")
def valid_input(s): 
    return len(s)==1 and 'A' <= s <= chr(64+COLS)
def place_checker(b, col, ch):
    for r in range(ROWS-1,-1,-1):
        if b[r][col]==" ":
            b[r][col] = ch
            return r
    return -1
def check_win(b, r, c, ch):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
    for dr,dc in directions:
        count=1
        for step in [1,-1]:
            nr,nc = r+step*dr, c+step*dc
            while 0<=nr<ROWS and 0<=nc<COLS and b[nr][nc]==ch:
                count+=1
                nr+=step*dr; nc+=step*dc
        if count>=4: return True
    return False
def board_full(b): return all(b[0][c]!=" " for c in range(COLS))

board = create_board()
current = random.randint(0, PLAYERS-1)
print_board(board)

while True:
    ch = CHECKERS[current]
    inp = input(f"Player {ch}, please enter a column: ").upper()
    if not valid_input(inp):
        continue
    col = ord(inp) - 65
    pos = place_checker(board, col, ch)
    if pos == -1:
        current = (current + 1) % PLAYERS
        continue
    print_board(board)
    if check_win(board, pos, col, ch):
        print(f"Player {ch} won!")
        break
    if board_full(board):
        print("Game is a draw!")
        break
    current = (current + 1) % PLAYERS
