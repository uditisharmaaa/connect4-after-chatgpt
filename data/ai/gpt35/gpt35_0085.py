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
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    print("+---"*COLS+"+")
    for r in range(ROWS):
        print("| " + " | ".join(board[r]) + " |")
        print("+---"*COLS+"+")

def valid_input(s):
    return len(s)==1 and 'A'<=s<chr(65+COLS)

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d; nc += dc*d
                if 0<=nr<ROWS and 0<=nc<COLS and board[nr][nc]==checker:
                    count += 1
                else:
                    break
        if count >= 4: return True
    return False

def full_board(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    while True:
        print_board(board)
        player = players[current]
        inp = input(f"Player {player}, please enter a column: ").upper()
        if not valid_input(inp):
            continue
        col = ord(inp)-65
        r = place_checker(board, col, player)
        if r == -1:
            current = (current + 1) % PLAYERS
            continue
        if check_win(board, r, col, player):
            print_board(board)
            print(f"Player {player} won!")
            break
        if full_board(board):
            print_board(board)
            print("Draw!")
            break
        current = (current + 1) % PLAYERS

if __name__=="__main__":
    main()
