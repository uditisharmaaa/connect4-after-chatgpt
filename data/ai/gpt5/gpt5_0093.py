import os, random, string

# Config (change if needed; submission: 6x7 and 2 players)
ROWS, COLS = 6, 7
PLAYERS = ["X", "O", "V", "H", "M"][:2]  # set number of players (2..5) by slicing

EMPTY = " "

def clear():
    os.system('clear')

def make_board(r, c):
    return [[EMPTY for _ in range(c)] for _ in range(r)]

def print_board(board):
    clear()
    cols = len(board[0])
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row)
    print(sep)

def drop_piece(board, col, checker):
    # returns True if placed, else False (column full)
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = checker
            return True
    return False

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(board, checker):
    R, C = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if board[r][c] != checker: 
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r+dr, c+dc
                while cnt < 4 and in_bounds(rr, cc, R, C) and board[rr][cc] == checker:
                    cnt += 1
                    rr += dr; cc += dc
                if cnt == 4:
                    return True
    return False

def board_full(board):
    return all(cell != EMPTY for row in board for cell in row)

def get_valid_column_input(cols):
    while True:
        s = input("Please enter a column: ").strip()
        if len(s) != 1 or not s.isalpha():
            print("Invalid input. Enter a single letter.")
            continue
        ch = s.upper()
        idx = ord(ch) - ord('A')
        if 0 <= idx < cols:
            return idx
        print("Out of range. Try again.")

def main():
    assert 2 <= len(PLAYERS) <= 5 and COLS <= 26
    board = make_board(ROWS, COLS)
    current = random.randrange(len(PLAYERS))
    print_board(board)
    while True:
        checker = PLAYERS[current]
        print(f"Player {checker}, ", end="")
        col = get_valid_column_input(COLS)
        placed = drop_piece(board, col, checker)
        print_board(board)
        if not placed:
            print("Column is full. Turn lost.")
            if board_full(board):
                print("It's a draw!")
                break
        else:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
        current = (current + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
