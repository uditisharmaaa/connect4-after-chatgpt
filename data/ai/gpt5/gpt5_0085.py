import os, random, string

# Constants (submission must be 6x7 with 2 players)
ROWS, COLS = 6, 7
NUM_PLAYERS = 2  # between 2 and 5
TOKENS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
LETTERS = list(string.ascii_uppercase[:COLS])

def clear():
    os.system('clear')

def create_board(r, c):
    return [[' ' for _ in range(c)] for _ in range(r)]

def print_board(board):
    clear()
    hdr = '  ' + '   '.join(LETTERS)
    line = '+' + '---+' * COLS
    print(hdr)
    print(line)
    for r in range(ROWS):
        row = '|'.join(f' {board[r][c]} ' for c in range(COLS))
        print('|' + row + '|')
        print(line)

def drop_checker(board, col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, token):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token: continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r+dr, c+dc
                while cnt < 4 and in_bounds(rr, cc) and board[rr][cc] == token:
                    cnt += 1
                    rr += dr; cc += dc
                if cnt == 4:
                    return True
    return False

def board_full(board):
    return all(board[r][c] != ' ' for r in range(ROWS) for c in range(COLS))

def get_valid_column():
    while True:
        s = input('Please enter a column: ').strip().upper()
        if len(s) == 1 and s in LETTERS:
            return LETTERS.index(s)
        print('Invalid input. Use a letter between A and', LETTERS[-1])

def main():
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    print_board(board)
    while True:
        token = TOKENS[current]
        print(f"Player {token}, please enter a column:")
        col = get_valid_column()
        row = drop_checker(board, col, token)
        if row is None:
            print(f"Column {LETTERS[col]} is full. Turn lost.")
        else:
            print_board(board)
            if check_win(board, token):
                print(f"Player {token} won!")
                return
            if board_full(board):
                print("It's a draw!")
                return
        current = (current + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
