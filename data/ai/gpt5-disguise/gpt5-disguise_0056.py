import os
import random

ROWS = 6
COLS = 7
N_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(board[0]))
    for r in range(len(board)):
        row = "|"
        for c in range(len(board[0])):
            row += " " + board[r][c] + " |"
        print(row)
        print("+" + "---+" * len(board[0]))

def drop_piece(board, col, sym):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return True
    return False

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, sym):
    rows = len(board)
    cols = len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != sym:
                continue
            for dr, dc in dirs:
                ok = True
                for k in range(1,4):
                    nr = r + dr*k
                    nc = c + dc*k
                    if not in_bounds(nr, nc, rows, cols) or board[nr][nc] != sym:
                        ok = False
                        break
                if ok:
                    return True
    return False

def check_draw(board):
    for r in board:
        for v in r:
            if v == " ":
                return False
    return True

def get_valid_column(cols):
    while True:
        s = input().strip().upper()
        if len(s) != 1:
            print("Invalid input. Try again:")
            continue
        if not ('A' <= s <= 'Z'):
            print("Invalid input. Try again:")
            continue
        idx = ord(s) - ord('A')
        if idx < 0 or idx >= cols:
            print("Invalid input. Try again:")
            continue
        return idx

def main():
    players = CHECKERS[:N_PLAYERS]
    board = create_board(ROWS, COLS)
    turn = random.randint(0, len(players)-1)
    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {players[turn]}, please enter a column:")
        col = get_valid_column(COLS)

        placed = drop_piece(board, col, players[turn])
        if not placed:
            print_board(board)
            print("Column is full. You lose your turn.")
        else:
            if check_win(board, players[turn]):
                print_board(board)
                print(f"Player {players[turn]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
