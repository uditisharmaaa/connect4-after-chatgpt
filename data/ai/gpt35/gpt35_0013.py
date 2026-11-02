import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+' * COLS)

def valid_input(s):
    return len(s) == 1 and s.isalpha() and 'A' <= s <= chr(ord('A') + COLS - 1)

def get_col_index(s):
    return ord(s) - ord('A')

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for dir in [1, -1]:
            nr, nc = r, c
            while True:
                nr += dr*dir
                nc += dc*dir
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                    count += 1
                else:
                    break
        if count >=4:
            return True
    return False

def board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        checker = players[current]
        print(f'Player {checker}, please enter a column:')
        col_input = input().strip().upper()
        if not valid_input(col_input):
            continue
        col = get_col_index(col_input)
        r = place_checker(board, col, checker)
        if r == -1:
            current = (current +1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, r, col, checker):
            print(f'Player {checker} won!')
            break
        if board_full(board):
            print('Draw!')
            break
        current = (current +1) % PLAYERS

if __name__ == '__main__':
    main()
