import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [' '] * COLS
        board.append(row)
    return board

def print_board(board):
    letters = ''
    for i in range(COLS):
        letters += '  ' + chr(ord('A') + i) + ' '
    print(letters)
    print('+---' * COLS + '+')
    for r in range(ROWS):
        line = ''
        for c in range(COLS):
            line += '| ' + board[r][c] + ' '
        line += '|'
        print(line)
        print('+---' * COLS + '+')

def input_column(player, board):
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col) != 1:
            continue
        c = col.upper()
        if c < 'A' or c >= chr(ord('A') + COLS):
            continue
        c_i = ord(c) - ord('A')
        if board[0][c_i] != ' ':
            # Column full, player loses turn
            return None
        return c_i

def place_checker(board, col, checker):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col
    return None, None

def check_win(board, r, c, checker):
    # horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # diagonal /
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c < COLS -1:
        start_r -=1
        start_c +=1
    rr = start_r
    cc = start_c
    while rr < ROWS and cc >= 0:
        if board[rr][cc] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count=0
        rr +=1
        cc -=1
    # diagonal \
    count =0
    start_r = r
    start_c = c
    while start_r > 0 and start_c >0:
        start_r -=1
        start_c -=1
    rr = start_r
    cc = start_c
    while rr < ROWS and cc < COLS:
        if board[rr][cc] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count=0
        rr +=1
        cc +=1
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    while True:
        clear()
        print_board(board)
        col = input_column(players[current], board)
        if col is None:
            # column full, lose turn
            current = (current +1) % PLAYERS
            continue
        r, c = place_checker(board, col, players[current])
        if check_win(board, r, c, players[current]):
            clear()
            print_board(board)
            print(f"Player {players[current]} won!")
            break
        if board_full(board):
            clear()
            print_board(board)
            print("Game is a draw!")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
