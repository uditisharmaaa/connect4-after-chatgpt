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
    for r in range(ROWS):
        print("| " + " | ".join(b[r]) + " |")
        print("+---"*COLS + "+")

def valid_input(inp, b):
    if len(inp)!=1 or not ('A' <= inp <= chr(64+COLS)):
        return False
    c = ord(inp)-65
    return any(b[r][c]==" " for r in range(ROWS))

def place_checker(b, c, checker):
    for r in reversed(range(ROWS)):
        if b[r][c] == " ":
            b[r][c] = checker
            return r, c
    return -1, -1  # column full

def check_win(b, r, c, checker):
    def count_dir(dr, dc):
        nr, nc, cnt = r+dr, c+dc, 0
        while 0 <= nr < ROWS and 0 <= nc < COLS and b[nr][nc]==checker:
            cnt += 1
            nr += dr
            nc += dc
        return cnt
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        if count_dir(dr, dc) + count_dir(-dr, -dc) + 1 >= 4:
            return True
    return False

def full_board(b):
    return all(b[0][col]!=" " for col in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    while True:
        print_board(board)
        print(f"Player {players[current]}, please enter a column:")
        move = input().strip().upper()
        if not valid_input(move, board):
            continue
        col = ord(move)-65
        r, c = place_checker(board, col, players[current])
        if r == -1:
            current = (current + 1) % PLAYERS  # lose turn if full
            continue
        if check_win(board, r, c, players[current]):
            print_board(board)
            print(f"Player {players[current]} won!")
            break
        if full_board(board):
            print_board(board)
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
