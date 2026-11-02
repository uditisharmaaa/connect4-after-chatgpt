import os
import random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
    print('+' + '---+' * COLS)

def valid_col(col):
    return col.isalpha() and 'A' <= col <= chr(ord('A') + COLS - 1)

def place_checker(board, col, checker):
    col_idx = ord(col) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row, col_idx
    return None

def check_win(board, r, c, ch):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        # check forward direction
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == ch:
            count += 1
            nr += dr
            nc += dc
        # check backward direction
        nr, nc = r - dr, c - dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == ch:
            count += 1
            nr -= dr
            nc -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        ch = players[current]
        while True:
            col = input(f'Player {ch}, please enter a column: ').upper()
            if not valid_col(col):
                continue
            placed = place_checker(board, col, ch)
            if placed is None:
                # column full, lose turn
                break
            else:
                break
        print_board(board)
        if placed:
            r, c = placed
            if check_win(board, r, c, ch):
                print(f'Player {ch} won!')
                return
            if board_full(board):
                print('The game is a draw.')
                return
        current = (current + 1) % PLAYERS

if __name__ == '__main__':
    main()
