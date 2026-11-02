import os, random

ROWS, COLS = 6, 7
COLUMNS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # 2 to 5 players
NUM_PLAYERS = 3  # Change as needed (2 to 5)
PLAYERS = PLAYERS[:NUM_PLAYERS]

def clear(): os.system('clear')

def print_board(b):
    print(' ' + ' '.join(COLUMNS))
    for r in b:
        print('|' + '|'.join(r) + '|')
    print()

def make_board():
    return [[' ']*COLS for _ in range(ROWS)]

def col_to_index(c):
    return COLUMNS.find(c.upper())

def valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def drop_piece(board, col, p):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = p
            return r, col

def check_line(board, r, c, dr, dc):
    p = board[r][c]
    if p == ' ': return False
    for i in range(1, 4):
        nr, nc = r + dr*i, c + dc*i
        if nr<0 or nr>=ROWS or nc<0 or nc>=COLS or board[nr][nc] != p:
            return False
    return True

def check_win(board, r, c):
    return (check_line(board, r, c, 0, 1) or  # horizontal
            check_line(board, r, c, 1, 0) or  # vertical
            check_line(board, r, c, 1, 1) or  # diag down-right
            check_line(board, r, c, 1, -1))   # diag down-left

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = make_board()
    current = random.randint(0, NUM_PLAYERS-1)
    while True:
        clear(); print_board(board)
        p = PLAYERS[current]
        move = input(f"Player {p}, choose column (A-G): ").strip().upper()
        col = col_to_index(move)
        if not valid_move(board, col):
            print("Invalid move, try again.")
            continue
        r,c = drop_piece(board, col, p)
        if check_win(board, r, c):
            clear(); print_board(board)
            print(f"Player {p} wins!")
            break
        if check_draw(board):
            clear(); print_board(board)
            print("Draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
