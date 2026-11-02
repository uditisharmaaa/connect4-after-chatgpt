import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(" ", end=" ")
    for c in range(COLS):
        print(" "+letters[c]+" ", end="")
    print()
    print("+" + "---+"*COLS)
    for r in range(ROWS):
        print("|", end="")
        for c in range(COLS):
            print(" "+board[r][c]+" |", end="")
        print()
        print("+" + "---+"*COLS)

def input_to_col(inp):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(inp) == 1 and inp in letters[:COLS]:
        return letters.index(inp)
    return -1

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # diagonal down-right
    for r in range(ROWS -3):
        for c in range(COLS -3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and 
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS -3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and 
                board[r-2][c+2] == checker and board[r-3][c+3] == checker):
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        checker = players[current]
        inp = input(f"Player {checker}, please enter a column: ").upper()
        col = input_to_col(inp)
        if col == -1:
            continue
        placed = place_checker(board, col, checker)
        if not placed:
            # loses turn if column full
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
