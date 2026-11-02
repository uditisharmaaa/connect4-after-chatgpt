import os, random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS+"+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS+"+")

def col_to_index(c):
    if len(c)==1 and 'A' <= c <= chr(ord('A')+COLS-1):
        return ord(c) - ord('A')
    return -1

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in (1,-1):
            rr, cc = r, c
            while True:
                rr += dr*d
                cc += dc*d
                if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
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
        c = players[current]
        inp = input(f"Player {c}, please enter a column: ").strip().upper()
        col = col_to_index(inp)
        if col == -1:
            continue
        row = place_checker(board, col, c)
        if row == -1:
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, row, col, c):
            print(f"Player {c} won!")
            break
        if board_full(board):
            print("Game is a draw.")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
