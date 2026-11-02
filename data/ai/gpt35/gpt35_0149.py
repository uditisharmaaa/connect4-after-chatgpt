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
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def col_to_index(ch):
    if len(ch)==1 and 'A' <= ch <= chr(ord('A')+COLS-1):
        return ord(ch)-ord('A')
    return -1

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def is_winning(board, r, c):
    def count_dir(dr, dc):
        cnt = 0
        nr, nc = r+dr, c+dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == board[r][c]:
            cnt += 1
            nr += dr; nc += dc
        return cnt
    if board[r][c] == " ": return False
    # check horizontal, vertical, diagonal /
    for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
        if count_dir(dr,dc)+count_dir(-dr,-dc)+1 >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current]
        col = input(f"Player {checker}, please enter a column: ").strip().upper()
        c = col_to_index(col)
        if c == -1:
            continue
        if not place_checker(board, c, checker):
            # column full -> lose turn
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        # find where we placed checker to check win
        for r in range(ROWS):
            if board[r][c] == checker:
                break
        print_board(board)
        if is_winning(board, r, c):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
