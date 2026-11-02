import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

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

def col_to_index(c):
    return ord(c) - 65

def valid_input(s):
    return len(s)==1 and 'A' <= s <= chr(65+COLS-1)

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def win_check(board, r, c, checker):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
    for dr, dc in directions:
        count=1
        for dir in [1,-1]:
            rr, cc = r, c
            while True:
                rr += dr*dir
                cc += dc*dir
                if 0<=rr<ROWS and 0<=cc<COLS and board[rr][cc]==checker:
                    count+=1
                else:
                    break
        if count>=4:
            return True
    return False

def full_board(board):
    return all(board[0][c] != " " for c in range(COLS))

def game():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[turn]
        inp = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not valid_input(inp):
            continue
        col = col_to_index(inp)
        row = place_checker(board, col, checker)
        if row == -1:
            turn = (turn + 1) % PLAYERS
            continue
        print_board(board)
        if win_check(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if full_board(board):
            print("It's a draw!")
            break
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    game()
