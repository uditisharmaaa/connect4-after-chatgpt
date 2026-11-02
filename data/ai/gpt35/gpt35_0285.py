import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_col_input(inp):
    return len(inp)==1 and 'A' <= inp <= chr(64+COLS)

def find_row(board, col):
    for r in range(ROWS-1,-1,-1):
        if board[r][col] == " ":
            return r
    return -1

def check_win(board, r, c, ch):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
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
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

board = create_board()
current = random.randint(0, PLAYERS-1)
print_board(board)

while True:
    player = CHECKERS[current]
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if not valid_col_input(col_input):
            continue
        col = ord(col_input) - 65
        row = find_row(board, col)
        if row == -1:
            current = (current +1)%PLAYERS  # lose turn if column full
            break
        board[row][col] = player
        print_board(board)
        if check_win(board, row, col, player):
            print(f"Player {player} won!")
            exit()
        if board_full(board):
            print("Game is a draw!")
            exit()
        current = (current +1)%PLAYERS
        break
