import os
import random

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
    return col.isalpha() and col.upper() >= 'A' and col.upper() < chr(ord('A')+COLS)

def column_full(board, col_idx):
    return board[0][col_idx] != " "

def drop_checker(board, col_idx, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx

def four_in_a_row(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for step in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*step; nc += dc*step
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
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
        col = input(f"Player {checker}, please enter a column: ").upper()
        if not valid_column(col):
            continue
        ci = ord(col) - ord('A')
        if column_full(board, ci):
            # turn lost if column full
            current = (current + 1) % PLAYERS
            continue
        r, c = drop_checker(board, ci, checker)
        print_board(board)
        if four_in_a_row(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
