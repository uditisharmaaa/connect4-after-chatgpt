import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print('  ' + '   '.join(chr(ord('A')+i) for i in range(COLS)))
    print('+' + '---+'*COLS)
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+'*COLS)

def valid_input(inp, board):
    if len(inp) != 1 or not ('A' <= inp <= chr(ord('A')+COLS-1)):
        return False
    col = ord(inp) - ord('A')
    return board[0][col] == ' '

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col

def check_win(board, r, c, ch):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == ch:
                    count +=1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[turn]
        inp = input(f'Player {checker}, please enter a column: ').upper()
        if not valid_input(inp, board):
            continue
        col = ord(inp) - ord('A')
        pos = place_checker(board, col, checker)
        if not pos:
            turn = (turn+1) % PLAYERS
            continue
        print_board(board)
        r,c = pos
        if check_win(board, r, c, checker):
            print(f'Player {checker} won!')
            break
        if board_full(board):
            print("Game is a draw!")
            break
        turn = (turn+1) % PLAYERS

if __name__ == '__main__':
    main()
