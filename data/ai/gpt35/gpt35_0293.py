import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_column(ch):
    return ch.isalpha() and 'A' <= ch <= chr(ord('A')+COLS-1)

def get_column_index(ch):
    return ord(ch) - ord('A')

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def won(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in (1,-1):
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def full_board(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    while True:
        print_board(board)
        print(f"Player {players[current]}, please enter a column:")
        move = input().strip().upper()
        if not valid_column(move):
            continue
        col = get_column_index(move)
        row = place_checker(board, col, players[current])
        if row == -1:
            current = (current + 1) % PLAYERS
            continue
        if won(board, row, col, players[current]):
            print_board(board)
            print(f"Player {players[current]} won!")
            break
        if full_board(board):
            print_board(board)
            print("The game is a draw.")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
