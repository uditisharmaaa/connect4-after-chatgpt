import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(b):
    clear()
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in b:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_input(ch):
    return len(ch) == 1 and 'A' <= ch <= chr(65+COLS-1)

def column_full(b, c):
    return b[0][c] != " "

def place_checker(b, c, checker):
    for r in range(ROWS-1, -1, -1):
        if b[r][c] == " ":
            b[r][c] = checker
            return r, c

def check_win(b, r, c, ch):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d; nc += dc*d
                if 0<=nr<ROWS and 0<=nc<COLS and b[nr][nc]==ch:
                    count += 1
                else:
                    break
            if count>=4:
                return True
    return False

def board_full(b):
    return all(b[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        ch = players[current]
        print(f"Player {ch}, please enter a column:")
        col = input().strip().upper()
        if not valid_input(col):
            continue
        c = ord(col) - 65
        if column_full(board, c):
            current = (current+1)%PLAYERS
            continue
        r, _ = place_checker(board, c, ch)
        print_board(board)
        if check_win(board, r, c, ch):
            print(f"Player {ch} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current+1)%PLAYERS

if __name__ == "__main__":
    main()
