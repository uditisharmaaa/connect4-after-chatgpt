import os, random

ROWS, COLS = 6, 7
COL_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players
NUM_PLAYERS = 3  # Change between 2 and 5 here
PLAYERS = PLAYERS[:NUM_PLAYERS]

def clear(): os.system('clear')
def print_board(b):
    print(' '.join(COL_LABELS))
    for r in range(ROWS):
        print(' '.join(b[r]))
def valid_choice(col, board):
    return col in COL_LABELS and board[0][COL_LABELS.index(col)] == '.'

def drop_piece(board, col, p):
    c = COL_LABELS.index(col)
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == '.':
            board[r][c] = p
            return r, c

def check_dir(board, r, c, dr, dc, p):
    count = 0
    for i in range(4):
        rr, cc = r + dr*i, c + dc*i
        if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == p:
            count += 1
        else:
            break
    return count == 4

def check_win(board, r, c, p):
    return (check_dir(board, r, c, 1, 0, p) or    # vertical
            check_dir(board, r, c, 0, 1, p) or    # horizontal
            check_dir(board, r, c, 1, 1, p) or    # diag down-right
            check_dir(board, r, c, 1, -1, p))     # diag down-left

def is_draw(board):
    return all(board[0][c] != '.' for c in range(COLS))

def main():
    board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
    turn = random.randint(0, NUM_PLAYERS-1)

    while True:
        clear()
        print_board(board)
        p = PLAYERS[turn]
        col = input(f"Player {p}, choose column (A-G): ").upper()
        if not valid_choice(col, board):
            print("Invalid move, try again.")
            continue
        r, c = drop_piece(board, col, p)
        if check_win(board, r, c, p):
            clear()
            print_board(board)
            print(f"Player {p} wins!")
            break
        if is_draw(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
