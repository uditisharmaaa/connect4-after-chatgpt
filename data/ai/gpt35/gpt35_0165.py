import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A')+i) for i in range(COLS)))
    print("+---"*COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---"*COLS + "+")

def valid_column(col):
    return ord('A') <= col <= chr(ord('A') + COLS -1)

def col_index(col):
    return ord(col) - ord('A')

def place_checker(board, col, checker):
    c = col_index(col)
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1, -1]:
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

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current]
        move = input(f"Player {checker}, please enter a column: ").upper()
        if len(move) != 1 or not valid_column(move):
            continue
        r = place_checker(board, move, checker)
        if r == -1:
            current = (current + 1) % PLAYERS
            continue
        print_board(board)
        if check_win(board, r, col_index(move), checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
