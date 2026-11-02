import os, random, string

ROWS, COLS = 6, 7
SYMS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set 2..5

def clear(): os.system('clear')

def new_board(): return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(b):
    clear()
    print('  ' + ' '.join(list('A B C D E F G'.split())))
    for r in b:
        print('  ' + ' '.join(r))

def drop(b, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == '.':
            b[r][col] = sym
            return r, col
    return None

def in_bounds(r, c): return 0 <= r < ROWS and 0 <= c < COLS

def won(b, r, c, sym):
    for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
        cnt = 1
        for sgn in (1, -1):
            nr, nc = r, c
            while True:
                nr, nc = nr + dr*sgn, nc + dc*sgn
                if in_bounds(nr, nc) and b[nr][nc] == sym:
                    cnt += 1
                else:
                    break
        if cnt >= 4: return True
    return False

def draw(b): return all(b[0][c] != '.' for c in range(COLS))

def get_move(b, sym):
    while True:
        s = input(f"Player {sym}, choose column A-G: ").strip().upper()
        if len(s) == 1 and s in string.ascii_uppercase[:COLS]:
            col = ord(s) - ord('A')
            if b[0][col] != '.':
                print("Column full. Try again.")
            else:
                return col
        else:
            print("Invalid input. Use A-G.")

def main():
    assert 2 <= NUM_PLAYERS <= 5
    players = SYMS[:NUM_PLAYERS]
    board = new_board()
    turn = random.randrange(NUM_PLAYERS)
    while True:
        print_board(board)
        col = get_move(board, players[turn])
        pos = drop(board, col, players[turn])
        r, c = pos
        if won(board, r, c, players[turn]):
            print_board(board)
            print(f"Player {players[turn]} wins!")
            break
        if draw(board):
            print_board(board)
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
