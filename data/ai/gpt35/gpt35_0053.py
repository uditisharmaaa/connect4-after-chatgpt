import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN = 4

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
    return len(c) == 1 and 'A' <= c <= chr(ord('A')+COLS-1)

def place_checker(board, col, checker):
    c = ord(col) - ord('A')
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r, c
    return -1, -1

def check_line(board, r, c, dr, dc, checker):
    count = 0
    for i in range(WIN):
        rr, cc = r + dr*i, c + dc*i
        if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count += 1
        else:
            break
    return count == WIN

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        # Check backward direction for overlapping sequences
        for start in range(-WIN+1,1):
            sr, sc = r + dr*start, c + dc*start
            if 0 <= sr < ROWS and 0 <= sc < COLS:
                if check_line(board, sr, sc, dr, dc, checker):
                    return True
    return False

def full_board(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current]
        col = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not valid_col(col):
            continue
        r, c = place_checker(board, col, checker)
        if r == -1:
            current = (current +1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if full_board(board):
            print("Game is a draw!")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
