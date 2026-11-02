import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear(): os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLS]
    print('  ' + '   '.join(letters))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+' * COLS)

def col_to_index(ch):
    if ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLS]:
        return ord(ch) - ord('A')
    return -1

def valid_input(s, board):
    if len(s) != 1: return False
    c = col_to_index(s)
    if c == -1 or board[0][c] != ' ': return False
    return True

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for step in (1,-1):
            nr, nc = r, c
            while True:
                nr += dr*step
                nc += dc*step
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current = random.randint(0, PLAYERS-1)
    clear()
    print_board(board)
    while True:
        checker = CHECKERS[current]
        inp = input(f'Player {checker}, please enter a column: ').upper()
        if not valid_input(inp, board):
            continue
        col = col_to_index(inp)
        pos = place_checker(board, col, checker)
        if not pos:
            current = (current+1)%PLAYERS # lose turn
        clear()
        print_board(board)
        if pos:
            r, c = pos
            if check_win(board, r, c, checker):
                print(f'Player {checker} won!')
                break
        if board_full(board):
            print('The game is a draw.')
            break
        current = (current+1) % PLAYERS

if __name__ == '__main__':
    main()
