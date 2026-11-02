import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  "+"   ".join(chr(65+i) for i in range(COLS)))
    print("+---"*COLS+"+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS+"+")

def valid_column(col):
    return col.isalpha() and len(col) == 1 and ('A' <= col <= chr(65+COLS-1))

def column_full(board, c):
    return board[0][c] != " "

def place_checker(board, c, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r, c

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

board = create_board()
players = CHECKERS[:PLAYERS]
current = random.randint(0, PLAYERS-1)

print_board(board)
while True:
    player = players[current]
    col_input = input(f"Player {player}, please enter a column: ").upper()
    while not valid_column(col_input):
        col_input = input(f"Player {player}, please enter a valid column: ").upper()
    c = ord(col_input) - 65
    if column_full(board, c):
        print("Column full. You lose your turn.")
    else:
        r, c = place_checker(board, c, player)
        print_board(board)
        if check_win(board, r, c, player):
            print(f"Player {player} won!")
            break
        if board_full(board):
            print("Draw!")
            break
    current = (current + 1) % PLAYERS
