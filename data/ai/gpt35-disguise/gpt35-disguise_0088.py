import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"] 

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(" ", end=" ")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        print("|", end="")
        for c in range(COLS):
            print(" "+board[r][c]+" |", end="")
        print()
    print("+" + "---+"*COLS)

def valid_input(s):
    if len(s) != 1:
        return False
    s = s.upper()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if s not in letters[:COLS]:
        return False
    return True

def drop_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def is_winner(board, checker):
    #horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    #vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    #diag down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    #diag up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS-1)
    print_board(board)
    while True:
        print("Player "+players[current]+", please enter a column:")
        choice = input().strip().upper()
        if not valid_input(choice):
            print("Invalid input, try again.")
            continue
        col = ord(choice) - ord('A')
        if not drop_checker(board, col, players[current]):
            # column full, lose turn
            current = (current + 1) % NUM_PLAYERS
            print_board(board)
            continue
        print_board(board)
        if is_winner(board, players[current]):
            print("Player "+players[current]+" won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
