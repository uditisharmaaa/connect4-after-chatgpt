import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    letters = []
    for i in range(len(board[0])):
        letters.append(chr(ord('A') + i))
    print("  " + "   ".join(letters))
    for r in range(len(board)):
        print("+" + "---+"*len(board[0]))
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+"*len(board[0]))

def get_col_index(user_input, cols):
    if len(user_input) != 1:
        return -1
    c = user_input.upper()
    if c < 'A' or c >= chr(ord('A') + cols):
        return -1
    return ord(c) - ord('A')

def place_checker(board, col, checker):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_win(board, row, col, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        # check one way
        r = row + dr
        c = col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check other way
        r = row - dr
        c = col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

board = create_board(ROWS, COLS)
current_player = random.randint(0, PLAYERS-1)

while True:
    clear()
    print_board(board)
    checker = CHECKERS[current_player]
    print(f"Player {checker}, please enter a column:")
    inp = input()
    col = get_col_index(inp, COLS)
    if col == -1:
        continue
    pos = place_checker(board, col, checker)
    if pos == -1:
        # column full, lose turn
        current_player = (current_player + 1) % PLAYERS
        continue
    if check_win(board, pos, col, checker):
        clear()
        print_board(board)
        print(f"Player {checker} won!")
        break
    if board_full(board):
        clear()
        print_board(board)
        print("Game is a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
