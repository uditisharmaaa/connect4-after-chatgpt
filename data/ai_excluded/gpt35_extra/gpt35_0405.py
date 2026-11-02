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

def valid_col(c):
    return c.isalpha() and 'A' <= c <= chr(ord('A')+COLS-1)

def col_index(c):
    return ord(c)-ord('A')

def drop_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_dir(board, r, c, dr, dc, checker):
    count = 0
    for _ in range(4):
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr; c += dc
        else:
            break
    return count == 4

def check_win(board, r, c, checker):
    # horizontal, vertical, two diagonals
    return (check_dir(board, r, c, 0, 1, checker) and check_dir(board, r, c-3, 0, 1, checker)) or \
           (check_dir(board, r, c, 1, 0, checker) and check_dir(board, r-3, c, 1, 0, checker)) or \
           (check_dir(board, r, c, 1, 1, checker) and check_dir(board, r-3, c-3, 1, 1, checker)) or \
           (check_dir(board, r, c, 1, -1, checker) and check_dir(board, r-3, c+3, 1, -1, checker))

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randrange(PLAYERS)
    print_board(board)

    while True:
        checker = players[current]
        inp = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not valid_col(inp):
            continue
        c = col_index(inp)
        r = drop_checker(board, c, checker)
        if r == -1:
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
