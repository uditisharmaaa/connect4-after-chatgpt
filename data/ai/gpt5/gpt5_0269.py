import os, random, string

# Constants (submission must use 6x7 and 2 players)
ROWS, COLS = 6, 7
NUM_PLAYERS = 2  # supports 2..5
TOKENS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
EMPTY = ' '
LETTERS = [chr(ord('A') + i) for i in range(COLS)]

def create_board(r, c):
    return [[EMPTY for _ in range(c)] for _ in range(r)]

def print_board(board):
    hdr = "  " + "   ".join(LETTERS)
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(hdr)
    print(sep)
    for r in range(ROWS - 1, -1, -1):
        print("| " + " | ".join(board[r]) + " |")
        print(sep)

def next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == EMPTY:
            return r
    return None

def check_win(board, t):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != t: 
                continue
            # horiz
            if c + 3 < COLS and all(board[r][c+i] == t for i in range(4)): return True
            # vert
            if r + 3 < ROWS and all(board[r+i][c] == t for i in range(4)): return True
            # diag down-right
            if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == t for i in range(4)): return True
            # diag up-right
            if r - 3 >= 0 and c + 3 < COLS and all(board[r-i][c+i] == t for i in range(4)): return True
    return False

def draw(board):
    return all(board[ROWS-1][c] != EMPTY for c in range(COLS))

def get_valid_column():
    while True:
        s = input("Player {}, please enter a column: ".format(current_token)).strip().upper()
        if s in LETTERS:
            return LETTERS.index(s)
        print("Invalid input. Use letters A-{}.".format(LETTERS[-1]))

board = create_board(ROWS, COLS)
current = random.randrange(NUM_PLAYERS)

while True:
    os.system('clear')
    print_board(board)
    current_token = TOKENS[current]
    col = get_valid_column()
    row = next_open_row(board, col)
    if row is None:
        print("Column {} is full! Turn lost.".format(LETTERS[col]))
        current = (current + 1) % NUM_PLAYERS
        input("Press Enter to continue...")
        continue
    board[row][col] = current_token
    if check_win(board, current_token):
        os.system('clear')
        print_board(board)
        print("Player {} won!".format(current_token))
        break
    if draw(board):
        os.system('clear')
        print_board(board)
        print("It's a draw!")
        break
    current = (current + 1) % NUM_PLAYERS
