import os, random

ROWS, COLS = 6, 7
PLAYERS = ['X','O','V','H','M']  # max 5
P_COUNT = 3  # Change between 2 and 5

def clear(): os.system('clear')
def board_str(b):
    header = ' '.join('ABCDEFG')
    rows = [' '.join(b[r*COLS:(r+1)*COLS]) for r in range(ROWS)]
    return header + '\n' + '\n'.join(rows)

def col_index(c):
    c = c.upper()
    return ord(c)-65 if 'A' <= c <= 'G' else -1

def valid_move(b, c):
    return 0 <= c < COLS and b[c] == '.'

def make_move(b, c, p):
    for r in range(ROWS-1,-1,-1):
        i = r*COLS + c
        if b[i] == '.':
            b[i] = p
            return i
    return -1

def check_dir(b,i,dx,dy,p):
    count=1
    for d in [1,-1]:
        x,y = i%COLS, i//COLS
        while True:
            x+=d*dx; y+=d*dy
            if 0<=x<COLS and 0<=y<ROWS and b[y*COLS+x]==p:
                count+=1
            else:
                break
    return count >=4

def winner(b, i, p):
    return any(check_dir(b,i,dx,dy,p) for dx,dy in [(1,0),(0,1),(1,1),(1,-1)])

def full(b):
    return all(x != '.' for x in b)

def main():
    players = PLAYERS[:P_COUNT]
    b = ['.']*ROWS*COLS
    turn = random.randint(0,P_COUNT-1)

    while True:
        clear()
        print(board_str(b))
        p = players[turn]
        move = input(f"Player {p}, choose column (A-G): ").strip()
        c = col_index(move)
        if c == -1 or not valid_move(b,c):
            print("Invalid move, try again.")
            continue
        i = make_move(b,c,p)
        if winner(b,i,p):
            clear()
            print(board_str(b))
            print(f"Player {p} wins!")
            break
        if full(b):
            clear()
            print(board_str(b))
            print("It's a draw!")
            break
        turn = (turn+1) % P_COUNT

if __name__ == "__main__":
    main()
