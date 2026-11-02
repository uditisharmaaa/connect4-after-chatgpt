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
    for r in range(ROWS):
        print("+---"*COLS + "+")
        line = ""
        for c in range(COLS):
            line += "| " + board[r][c] + " "
        line += "|"
        print(line)
    print("+---"*COLS + "+")

def valid_input(s):
    if len(s) != 1:
        return False
    if not ('A' <= s <= chr(ord('A')+COLS-1)):
        return False
    return True

def place_checker(board, col, ch):
    # col is index of column
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = ch
            return True
    return False

def check_win(board, ch):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == ch and board[r][c+1] == ch and board[r][c+2] == ch and board[r][c+3] == ch:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == ch and board[r+1][c] == ch and board[r+2][c] == ch and board[r+3][c] == ch:
                return True
    # diagonal down right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == ch and board[r+1][c+1] == ch and board[r+2][c+2] == ch and board[r+3][c+3] == ch:
                return True
    # diagonal up right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == ch and board[r-1][c+1] == ch and board[r-2][c+2] == ch and board[r-3][c+3] == ch:
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
    current = random.randint(0, PLAYERS-1)
    game_over = False

    print_board(board)

    while not game_over:
        player = players[current]
        print("Player " + player + ", please enter a column:")
        inp = input()
        while not valid_input(inp):
            print("Invalid input. Please enter a column letter between A and " + chr(ord('A')+COLS-1) + ":")
            inp = input()
        col = ord(inp) - ord('A')
        placed = place_checker(board, col, player)
        if not placed:
            # if column full, player loses the turn
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, player):
            print("Player " + player + " won!")
            game_over = True
            continue
        if board_full(board):
            print("It's a draw!")
            game_over = True
            continue
        current = (current + 1) % PLAYERS

main()
