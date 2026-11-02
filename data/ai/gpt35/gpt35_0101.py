import os
import random

ROWS = 6
COLS = 7
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

def valid_column(col):
    return col.isalpha() and col.upper() >= 'A' and col.upper() < chr(ord('A')+COLS)

def get_col_index(col):
    return ord(col.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    for r in reversed(range(ROWS)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r
    return -1  # column full

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
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
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_index = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current_index]
        col = input(f"Player {checker}, please enter a column: ").strip()
        if not valid_column(col):
            continue
        col_idx = get_col_index(col)
        row_idx = place_checker(board, col_idx, checker)
        if row_idx == -1:
            current_index = (current_index + 1) % PLAYERS  # lose turn if column full
            continue
        print_board(board)
        if check_win(board, row_idx, col_idx, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current_index = (current_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
