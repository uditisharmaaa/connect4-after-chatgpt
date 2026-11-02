import os, random, string

# CONFIG
ROWS, COLS = 6, 7
COL_LABELS = list("ABCDEFG")
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # available pieces
N_PLAYERS = 2  # set from 2 to 5

def clear():
    os.system('clear')

def new_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COL_LABELS))
    for r in range(ROWS):
        print(str(ROWS - r) + ' ' + ' '.join(board[r]))
    print()

def col_from_input(s):
    if not s or len(s) != 1: return None
    s = s.upper()
    return COL_LABELS.index(s) if s in COL_LABELS else None

def drop_piece(board, col, piece):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = piece
            return r, col
    return None  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, r, c, piece):
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for dr, dc in dirs:
        cnt = 1
        for s in (1, -1):
            nr, nc = r + s*dr, c + s*dc
            while in_bounds(nr, nc) and board[nr][nc] == piece:
                cnt += 1
                if cnt >= 4: return True
                nr += s*dr; nc += s*dc
    return False

def board_full(board):
    return all(board[0][c] != '.' for c in range(COLS))

def main():
    players = PLAYERS[:max(2, min(5, N_PLAYERS))]
    turn = random.randrange(len(players))
    board = new_board()

    while True:
        clear()
        print_board(board)
        cur = players[turn]
        move = input(f"Player {cur}, choose column ({'/'.join(COL_LABELS)}): ").strip()
        col = col_from_input(move)
        if col is None:
            print("Invalid column. Press Enter."); input(); continue
        pos = drop_piece(board, col, cur)
        if pos is None:
            print("Column full. Press Enter."); input(); continue
        r, c = pos
        if check_win(board, r, c, cur):
            clear(); print_board(board)
            print(f"Player {cur} wins!")
            break
        if board_full(board):
            clear(); print_board(board)
            print("It's a draw!")
            break
        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
