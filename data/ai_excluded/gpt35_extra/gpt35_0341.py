import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear(): os.system('clear')
def create_board(): return [[" "]*COLS for _ in range(ROWS)]
def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    sep = "+---"*COLS + "+"
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)
def valid_col(c): return 'A' <= c <= chr(ord('A') + COLS - 1)
def place_checker(board, col, checker):
    c = ord(col) - ord('A')
    for r in reversed(range(ROWS)):
        if board[r][c] == " ":
            board[r][c] = checker
            return True
    return False
def is_winner(board, ch):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != ch: continue
            if c + 3 < COLS and all(board[r][c+i] == ch for i in range(4)): return True
            if r + 3 < ROWS and all(board[r+i][c] == ch for i in range(4)): return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == ch for i in range(4)): return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r+i][c-i] == ch for i in range(4)): return True
    return False
def is_draw(board): return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        ch = CHECKERS[current]
        inp = input(f"Player {ch}, please enter a column: ").strip().upper()
        if not (len(inp) == 1 and valid_col(inp)):
            continue
        if not place_checker(board, inp, ch):
            current = (current + 1) % PLAYERS  # lose turn if full
            print_board(board)
            continue
        print_board(board)
        if is_winner(board, ch):
            print(f"Player {ch} won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__": main()
