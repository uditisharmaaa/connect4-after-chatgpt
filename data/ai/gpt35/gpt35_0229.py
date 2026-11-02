import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

def create_board(): return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_col(c):
    return c.isalpha() and len(c)==1 and 'A' <= c <= chr(ord('A')+COLS-1)

def get_col_index():
    while True:
        col = input().upper()
        if valid_col(col):
            idx = ord(col) - ord('A')
            return idx
        print("Invalid column. Try again:")

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

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
print(f"Player {players[current]}, please enter a column:")

while True:
    col = get_col_index()
    r = place_checker(board, col, players[current])
    if r == -1:
        print_board(board)
        print(f"Column {chr(ord('A')+col)} is full! Player {players[current]} loses the turn.")
    else:
        print_board(board)
        if check_win(board, r, col, players[current]):
            print(f"Player {players[current]} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % PLAYERS
    print(f"Player {players[current]}, please enter a column:")
