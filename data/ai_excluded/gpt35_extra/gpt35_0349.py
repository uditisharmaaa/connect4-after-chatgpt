import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(b):
    clear()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in b:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_input(c):
    return len(c) == 1 and 'A' <= c <= chr(ord('A')+COLS-1)

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for dir in [1, -1]:
            nr, nc = r, c
            while True:
                nr += dr*dir
                nc += dc*dir
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                    count += 1
                else:
                    break
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = CHECKERS[current_player]
        while True:
            move = input(f"Player {checker}, please enter a column: ").upper()
            if not valid_input(move):
                continue
            col = ord(move) - ord('A')
            pos = place_checker(board, col, checker)
            break
        if pos == -1:
            current_player = (current_player + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, pos, col, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
