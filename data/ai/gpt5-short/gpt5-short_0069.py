# Connect 4: 6x7, columns A-G, 2–5 players, random first, input validated, wins/draws, clears screen
import os, random

ROWS, COLS = 6, 7
LABELS = "ABCDEFG"
TOKENS = "XOVHM"      # up to 5 players: X O V H M
NUM_PLAYERS = 2       # set 2–5

assert 2 <= NUM_PLAYERS <= 5
TOKENS = TOKENS[:NUM_PLAYERS]

def new_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def draw(board, cur_token):
    os.system('clear')
    print("Connect 4  | Players:", ' '.join(TOKENS), "| Turn:", cur_token)
    print('  ' + ' '.join(LABELS))
    for r in board:
        print(' |' + ' '.join(r))
    print()

def drop(board, col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = token
            return r, col
    return None

def inb(r, c): return 0 <= r < ROWS and 0 <= c < COLS

def won(board, r, c, t):
    for dr, dc in [(0,1),(1,0),(1,1),(-1,1)]:
        cnt = 1
        for s in (1, -1):
            nr, nc = r + s*dr, c + s*dc
            while inb(nr, nc) and board[nr][nc] == t:
                cnt += 1; nr += s*dr; nc += s*dc
        if cnt >= 4: return True
    return False

def full(board): return all(board[0][c] != '.' for c in range(COLS))

def get_move(board, token):
    while True:
        s = input(f"Player {token}, pick column A-G: ").strip().upper()
        if len(s) == 1 and s in LABELS:
            c = LABELS.index(s)
            if board[0][c] == '.': return c
            else: print("Column full.")
        else:
            print("Invalid input.")

def game():
    board = new_board()
    turn = random.randrange(NUM_PLAYERS)
    last_move = None
    while True:
        cur = TOKENS[turn]
        draw(board, cur)
        if last_move and won(board, *last_move, cur):  # show win screen one turn late? adjust:
            # Re-draw with the winner token from previous move
            draw(board, cur)
            print(f"Player {cur} wins!")
            break
        if full(board):
            print("It's a draw.")
            break
        c = get_move(board, cur)
        pos = drop(board, c, cur)
        last_move = (*pos, cur)
        # After placing, check immediate win
        if won(board, pos[0], pos[1], cur):
            draw(board, cur)
            print(f"Player {cur} wins!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    game()
