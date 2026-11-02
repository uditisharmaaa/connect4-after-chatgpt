import os
import random

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

def col_to_index(c):
    return ord(c)-ord('A')

def valid_input(inp, board):
    if len(inp)!=1 or not ('A' <= inp <= chr(ord('A')+COLS-1)): return False
    col = col_to_index(inp)
    return board[0][col] == " "

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None

def check_win(board, r, c, checker):
    def count_dir(dr, dc):
        count = 0
        nr, nc = r+dr, c+dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
            count +=1
            nr += dr
            nc += dc
        return count
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        if 1 + count_dir(dr, dc) + count_dir(-dr, -dc) >=4:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current]
        inp = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_input(inp, board):
            print("Invalid input. Try again.")
            continue
        col = col_to_index(inp)
        pos = place_checker(board, col, checker)
        if not pos:
            print("Column full, you lose your turn.")
            current = (current+1) % PLAYERS
            print_board(board)
            continue
        r,c = pos
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current+1) % PLAYERS

if __name__ == "__main__":
    main()
