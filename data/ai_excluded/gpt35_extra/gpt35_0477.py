import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')
def create_board(): return [[" "]*COLS for _ in range(ROWS)]
def print_board(b):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for r in range(ROWS):
        print("| " + " | ".join(b[r]) + " |")
        print("+---"*COLS + "+")
def valid_input(ch):
    if len(ch)!=1: return False
    c = ord(ch)-ord('A')
    return 0 <= c < COLS
def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1
def check_direction(b, r, c, dr, dc, chk):
    count = 0
    for _ in range(4):
        if 0<=r<ROWS and 0<=c<COLS and b[r][c]==chk:
            count +=1
            r += dr
            c += dc
        else:
            break
    return count==4
def check_win(b, r, c, chk):
    return (check_direction(b,r,c,0,1,chk) or
            check_direction(b,r,c,1,0,chk) or
            check_direction(b,r,c,1,1,chk) or
            check_direction(b,r,c,1,-1,chk))
def board_full(b): return all(b[0][c]!=" " for c in range(COLS))
board = create_board()
players = CHECKERS[:PLAYERS]
current = random.randint(0,PLAYERS-1)
print_board(board)
while True:
    checker = players[current]
    col_in = input(f"Player {checker}, please enter a column: ").strip().upper()
    if not valid_input(col_in):
        continue
    col = ord(col_in) - ord('A')
    row = place_checker(board, col, checker)
    if row==-1:
        current = (current+1)%PLAYERS
        continue
    print_board(board)
    if check_win(board, row, col, checker):
        print(f"Player {checker} won!")
        break
    if board_full(board):
        print("The game is a draw!")
        break
    current = (current+1)%PLAYERS
