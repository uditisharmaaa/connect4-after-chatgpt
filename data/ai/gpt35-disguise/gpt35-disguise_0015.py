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
    # Print column headers
    header = "  "
    for i in range(COLS):
        header += chr(ord('A') + i) + "   "
    print(header)
    # Print rows
    for r in range(ROWS):
        line = "+"
        for _ in range(COLS):
            line += "---+"
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " "+board[r][c]+" |"
        print(row_str)
    print("+---"*COLS + "+")

def valid_input(s):
    if len(s) != 1:
        return False
    c = s[0]
    if c < 'A' or c >= chr(ord('A') + COLS):
        return False
    return True

def place_checker(board, col, checker):
    # col is a number 0-based
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # column full

def is_winner(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS -3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS -3):
        for c in range(COLS -3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS -3):
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
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        player = players[current]
        print("Player "+player+", please enter a column:")
        inp = input().strip().upper()
        if not valid_input(inp):
            continue
        col = ord(inp) - ord('A')
        if not place_checker(board, col, player):
            # column full, player loses turn
            current = (current +1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if is_winner(board, player):
            print("Player "+player +" won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
