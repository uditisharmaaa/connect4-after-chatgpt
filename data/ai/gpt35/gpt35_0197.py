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
    print(" ", end=" ")
    for c in range(COLS):
        print(chr(ord('A')+c), end="   ")
    print()
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        print("|", end="")
        for c in range(COLS):
            print(f" {board[r][c]} |", end="")
        print()
    print("+" + "---+"*COLS)

def valid_column(ch):
    return len(ch) == 1 and 'A' <= ch <= chr(ord('A')+COLS-1)

def is_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None

def check_line(board, r, c, dr, dc, checker):
    count = 0
    for _ in range(4):
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        else:
            break
    return count == 4

def check_win(board, r, c, checker):
    return (check_line(board, r, c, 0, 1, checker) or     # Horizontal
            check_line(board, r, c, 1, 0, checker) or     # Vertical
            check_line(board, r, c, 1, 1, checker) or     # Diagonal down-right
            check_line(board, r, c, 1, -1, checker))      # Diagonal down-left

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randrange(PLAYERS)
    print_board(board)
    while True:
        checker = players[current]
        col_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not valid_column(col_input):
            continue
        col = ord(col_input) - ord('A')
        pos = place_checker(board, col, checker)
        if pos is None:
            current = (current + 1) % PLAYERS  # lose turn if column full
            print_board(board)
            continue
        r, c = pos
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if is_full(board):
            print("The game is a draw.")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
