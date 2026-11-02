import os
import random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    line = "+---"*COLS + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def valid_column(col):
    return col.isalpha() and 'A' <= col <= chr(ord('A')+COLS-1)

def place_checker(board, col_idx, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    return None

def check_win(board, r, c, ch):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in (1,-1):
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
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = CHECKERS[current]
        col = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_column(col):
            continue
        col_idx = ord(col) - ord('A')
        pos = place_checker(board, col_idx, checker)
        if not pos:
            current = (current + 1) % PLAYERS  # lose turn
            continue
        print_board(board)
        r, c = pos
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
