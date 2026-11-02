import os, random, string, sys

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2 to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LEN = 4

assert 2 <= NUM_PLAYERS <= 5
assert 1 <= COLS <= 26

LETTERS = string.ascii_uppercase[:COLS]

def clear():
    os.system('clear')

def create_board(r, c):
    return [[' ' for _ in range(c)] for _ in range(r)]

def print_board(board):
    clear()
    header = '  ' + '   '.join(LETTERS)
    sep = '+' + '---+' * COLS
    print(header)
    print(sep)
    for r in range(ROWS):
        row = '|' + '|'.join(f' {board[r][c]} ' for c in range(COLS)) + '|'
        print(row)
        print(sep)

def valid_col_letter(s):
    return len(s) == 1 and s in LETTERS

def drop_checker(board, col, ch):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = ch
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, ch):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != ch:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < WIN_LEN and in_bounds(rr, cc) and board[rr][cc] == ch:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= WIN_LEN:
                    return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    turn = random.randrange(NUM_PLAYERS)
    print_board(board)
    while True:
        ch = players[turn]
        try:
            while True:
                print(f"Player {ch}, please enter a column:")
                s = input().strip().upper()
                if not valid_col_letter(s):
                    print_board(board)
                    continue
                col = ord(s) - ord('A')
                break
        except (EOFError, KeyboardInterrupt):
            print()
            return
        pos = drop_checker(board, col, ch)
        print_board(board)
        if pos is None:
            # Column full, turn lost
            turn = (turn + 1) % NUM_PLAYERS
            continue
        if check_win(board, ch):
            print(f"Player {ch} won!")
            return
        if board_full(board):
            print("The game is a draw.")
            return
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
