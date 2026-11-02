import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = ""
    for i in range(COLS):
        letters += "  " + chr(ord('A')+i) + " "
    print(letters)
    print("+---"*COLS + "+")
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
        print("+---"*COLS + "+")

def get_column_index(inp):
    if len(inp) != 1:
        return -1
    ch = inp[0]
    if ch < 'A' or ch >= chr(ord('A')+COLS):
        return -1
    return ord(ch) - ord('A')

def place_checker(board, col, checker):
    if board[0][col] != " ":
        return False
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def check_winner(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal descending \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal ascending /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        p = players[current]
        again = True
        while again:
            inp = input("Player {}, please enter a column: ".format(p))
            col = get_column_index(inp.upper())
            if col == -1:
                continue
            if not place_checker(board, col, p):
                # fully filled column - lose turn
                again = False
            else:
                again = False
        print_board(board)
        if check_winner(board, p):
            print("Player {} won!".format(p))
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
