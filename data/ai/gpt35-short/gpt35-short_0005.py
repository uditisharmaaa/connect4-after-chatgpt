import os, random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
COL_LABELS = 'ABCDEFG'

def clear(): os.system('clear')

def print_board(b):
    print(' '.join(COL_LABELS))
    for r in b:
        print(' '.join(r))

def make_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def valid_col(b, c):
    return 0 <= c < COLS and b[0][c] == '.'

def drop_piece(b, c, p):
    for r in reversed(range(ROWS)):
        if b[r][c] == '.':
            b[r][c] = p
            return r

def check_win(b, r, c, p):
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for dr, dc in dirs:
        count = 1
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0 <= nr < ROWS and 0 <= nc < COLS and b[nr][nc] == p:
                    count += 1
                else:
                    break
        if count >= 4: return True
    return False

def board_full(b):
    return all(b[0][c] != '.' for c in range(COLS))

def main():
    n = 0
    while n < 2 or n > 5:
        try: n = int(input(f"Players (2-5): "))
        except: pass
    players = PLAYERS[:n]
    board = make_board()
    current = random.randint(0, n-1)

    while True:
        clear()
        print_board(board)
        print(f"Player {players[current]}'s turn")
        col_in = input(f"Choose column (A-{COL_LABELS[n-1]}): ").upper()
        if col_in not in COL_LABELS:
            continue
        c = COL_LABELS.index(col_in)
        if not valid_col(board, c):
            continue
        r = drop_piece(board, c, players[current])
        if check_win(board, r, c, players[current]):
            clear()
            print_board(board)
            print(f"Player {players[current]} wins!")
            break
        if board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % n

if __name__ == '__main__':
    main()
