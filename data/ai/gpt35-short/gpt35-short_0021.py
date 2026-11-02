import os, random

ROWS, COLS = 6, 7
COL_LABELS = 'A B C D E F G'.split()
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # up to 5 players
NUM_PLAYERS = 3  # Change between 2 and 5 here

def clear(): os.system('clear' if os.name != 'nt' else 'cls')

def create_board():
    return [['.' for _ in range(COLS)] for __ in range(ROWS)]

def print_board(board):
    print(' '.join(COL_LABELS))
    for r in board:
        print(' '.join(r))

def get_col_input(current):
    while True:
        col = input(f"Player {current}'s turn. Choose column A-G: ").upper()
        if col in COL_LABELS:
            c = COL_LABELS.index(col)
            if board[0][c] == '.': 
                return c
            else:
                print("Column full! Try another.")
        else:
            print("Invalid column! Use letters A-G.")

def drop_piece(board, col, symbol):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = symbol
            return r, col

def check_win(board, r, c, symbol):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            rr, cc = r, c
            while True:
                rr += dr*step
                cc += dc*step
                if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == symbol:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != '.' for c in range(COLS))

board = create_board()
players = PLAYERS[:NUM_PLAYERS]
current_i = random.randrange(NUM_PLAYERS)

while True:
    clear()
    print_board(board)
    player = players[current_i]
    col = get_col_input(player)
    row, col = drop_piece(board, col, player)
    if check_win(board, row, col, player):
        clear()
        print_board(board)
        print(f"Player {player} wins!")
        break
    if is_draw(board):
        clear()
        print_board(board)
        print("It's a draw!")
        break
    current_i = (current_i + 1) % NUM_PLAYERS
