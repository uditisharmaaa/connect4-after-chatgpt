import os, random

ROWS, COLS = 6, 7
COLUMNS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players
NUM_PLAYERS = 3  # change this between 2 and 5

def clear(): os.system('clear')

def init_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COLUMNS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-'*(2*COLS+1))

def col_to_index(c):
    return COLUMNS.find(c.upper())

def valid_move(board, c):
    i = col_to_index(c)
    return 0 <= i < COLS and board[0][i] == ' '

def make_move(board, c, p):
    i = col_to_index(c)
    for r in reversed(range(ROWS)):
        if board[r][i] == ' ':
            board[r][i] = p
            return r, i

def check_dir(board, r, c, dr, dc, p):
    count = 0
    for i in range(4):
        rr, cc = r+dr*i, c+dc*i
        if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == p:
            count += 1
        else:
            break
    return count == 4

def check_win(board, r, c, p):
    return (check_dir(board, r, c, 1, 0, p) or  # vertical
            check_dir(board, r, c, 0, 1, p) or  # horizontal
            check_dir(board, r, c, 1, 1, p) or  # diagonal \
            check_dir(board, r, c, 1, -1, p))   # diagonal /

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = init_board()
    players = PLAYERS[:NUM_PLAYERS]
    turn = random.randint(0, NUM_PLAYERS-1)

    while True:
        clear()
        print_board(board)
        p = players[turn]
        move = input(f"Player {p}, choose column (A-G): ").strip().upper()
        if len(move) != 1 or not valid_move(board, move):
            print("Invalid move, try again.")
            input("Press Enter...")
            continue

        r, c = make_move(board, move, p)

        if check_win(board, r, c, p):
            clear()
            print_board(board)
            print(f"Player {p} wins!")
            break
        if check_draw(board):
            clear()
            print_board(board)
            print("Game is a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
