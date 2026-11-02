import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+" + "---+"*COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+"*COLS)

def valid_input(inp):
    return (len(inp)==1 and 'A' <= inp <= chr(ord('A')+COLS-1))

def drop_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, r, c, ch):
    def count_dir(dr, dc):
        cnt = 0
        rr, cc = r+dr, c+dc
        while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == ch:
            cnt += 1
            rr += dr
            cc += dc
        return cnt
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        if count_dir(dr, dc) + count_dir(-dr, -dc) + 1 >= 4:
            return True
    return False

def full_board(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        ch = players[current]
        inp = input(f"Player {ch}, please enter a column: ").upper()
        if not valid_input(inp):
            continue
        col = ord(inp) - ord('A')
        r, c = drop_checker(board, col, ch)
        if r == -1:
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, r, c, ch):
            print(f"Player {ch} won!")
            break
        if full_board(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
